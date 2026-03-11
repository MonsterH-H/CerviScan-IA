"""Boucle d'entraînement et orchestration du pipeline CerviScan IA."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from ml.src.data.datasets import CervixImageDataset, ImageSample
from ml.src.data.transforms import build_eval_transforms, build_train_transforms
from ml.src.models.efficientnet import build_model
from ml.src.training.losses import get_loss
from ml.src.training.metrics import classification_metrics
from ml.src.utils.io import ensure_dir
from ml.src.utils.logging import get_logger
from ml.src.utils.seed import set_seed


@dataclass
class TrainResult:
    """Résultats d'une session d'entraînement."""
    best_epoch: int
    best_metric: float
    history: List[Dict[str, float]]


def _make_loaders_from_csv(cfg: Dict[str, Any]):
    """Charge les données à partir du fichier splits.csv (Règle 4)."""
    base_dir = Path(__file__).resolve().parents[2]
    csv_path = base_dir / "data" / "interim" / "splits.csv"
    
    if not csv_path.exists():
        raise FileNotFoundError(f"❌ Le fichier {csv_path} est introuvable. Exécutez prepare_dataset.py.")

    df = pd.read_csv(csv_path)
    
    def df_to_samples(subset_df):
        return [ImageSample(path=str(base_dir / row['path']), label=row['label']) for _, row in subset_df.iterrows()]

    train_samples = df_to_samples(df[df['split'] == 'train'])
    val_samples = df_to_samples(df[df['split'] == 'val'])
    test_samples = df_to_samples(df[df['split'] == 'test'])

    train_tfms = build_train_transforms(cfg)
    val_tfms = build_eval_transforms(cfg)

    train_ds = CervixImageDataset(train_samples, transform=train_tfms)
    val_ds = CervixImageDataset(val_samples, transform=val_tfms)
    test_ds = CervixImageDataset(test_samples, transform=val_tfms)

    train_bs = int(cfg.get("training", {}).get("batch_size", 16))
    num_workers = int(cfg.get("training", {}).get("num_workers", 0)) # Mis à 0 pour Windows par sécurité

    train_loader = DataLoader(train_ds, batch_size=train_bs, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_ds, batch_size=train_bs, shuffle=False, num_workers=num_workers)
    test_loader = DataLoader(test_ds, batch_size=train_bs, shuffle=False, num_workers=num_workers)

    return train_loader, val_loader, test_loader


def _get_class_weights(cfg: Dict[str, Any], base_dir: Path) -> List[float] | None:
    """Calcule les poids des classes pour gerer le desequilibre (Regle 13)."""
    if cfg.get("training", {}).get("class_weight") != "balanced":
        return None

    counts_path = base_dir / "reports" / "metrics" / "class_counts.csv"
    if not counts_path.exists():
        return None

    df = pd.read_csv(counts_path)
    counts = df['count'].values
    total = counts.sum()
    n_classes = len(counts)
    
    # Formule standard: total / (n_classes * count)
    weights = total / (n_classes * counts)
    return weights.tolist()



def _run_epoch(model, loader, loss_fn, device, optimizer=None, scaler=None):
    """Exécute une seule époque (Train ou Eval)."""
    is_train = optimizer is not None
    model.train() if is_train else model.eval()

    total_loss = 0.0
    all_preds = []
    all_targets = []

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        if is_train:
            optimizer.zero_grad()

        with torch.set_grad_enabled(is_train):
            # Support du Mixed Precision (Règle 18)
            if scaler is not None:
                with torch.cuda.amp.autocast():
                    logits = model(images)
                    loss = loss_fn(logits, labels)
                if is_train:
                    scaler.scale(loss).backward()
                    scaler.step(optimizer)
                    scaler.update()
            else:
                logits = model(images)
                loss = loss_fn(logits, labels)
                if is_train:
                    loss.backward()
                    optimizer.step()

        total_loss += loss.item() * images.size(0)
        preds = torch.argmax(logits, dim=1)
        all_preds.extend(preds.cpu().numpy())
        all_targets.extend(labels.cpu().numpy())

    metrics = classification_metrics(np.array(all_targets), np.array(all_preds))
    metrics["loss"] = total_loss / len(loader.dataset)
    return metrics


def train(cfg: Dict[str, Any]) -> TrainResult:
    """Lance l'entraînement complet."""
    logger = get_logger("train")
    set_seed(int(cfg.get("project", {}).get("seed", 42)))
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_loader, val_loader, _ = _make_loaders_from_csv(cfg)
    model = build_model(cfg).to(device)

    # Gestion du desequilibre de classes (Regle 13)
    base_dir = Path(__file__).resolve().parents[2]
    class_weights = _get_class_weights(cfg, base_dir)
    
    loss_name = cfg.get("training", {}).get("loss", "cross_entropy")
    loss_fn = get_loss(loss_name, class_weights=class_weights)
    optimizer = torch.optim.AdamW(
        model.parameters(), 
        lr=float(cfg.get("training", {}).get("learning_rate", 3e-4)),
        weight_decay=float(cfg.get("training", {}).get("weight_decay", 1e-4))
    )

    epochs = int(cfg.get("training", {}).get("epochs", 10))
    scaler = torch.cuda.amp.GradScaler() if device.type == "cuda" else None

    ckpt_dir = Path(__file__).resolve().parents[2] / "models" / "checkpoints"
    ensure_dir(ckpt_dir)

    best_metric, best_epoch, history = -1.0, -1, []

    for epoch in range(1, epochs + 1):
        train_m = _run_epoch(model, train_loader, loss_fn, device, optimizer, scaler)
        val_m = _run_epoch(model, val_loader, loss_fn, device)

        combined = {f"train_{k}": v for k, v in train_m.items()}
        combined.update({f"val_{k}": v for k, v in val_m.items()})
        history.append(combined)

        score = val_m.get("f1_macro", 0.0)
        if score > best_metric:
            best_metric, best_epoch = score, epoch
            torch.save(model.state_dict(), ckpt_dir / "best.pt")

        logger.info(f"Époque {epoch}/{epochs} | Loss Val: {val_m['loss']:.4f} | F1 Val: {score:.4f}")

    return TrainResult(best_epoch, best_metric, history)


def evaluate(cfg: Dict[str, Any], checkpoint_path: str | Path, split: str = "val") -> Dict[str, float]:
    """Évalue un modèle sur un split donné."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    loaders = _make_loaders_from_csv(cfg)
    loader = loaders[1] if split == "val" else loaders[2]

    model = build_model(cfg).to(device)
    model.load_state_dict(torch.load(str(checkpoint_path), map_location=device))

    loss_fn = get_loss(cfg.get("training", {}).get("loss", "cross_entropy"))
    return _run_epoch(model, loader, loss_fn, device)
