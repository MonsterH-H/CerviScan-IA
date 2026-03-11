"""CLI (Command Line Interface) entry for export to ONNX.
Ce script a pour but de prendre le modèle PyTorch entraîné (.pth) et de le convertir
vers un format universel, léger et très rapide à charger en Production : l'ONNX.
C'est indispensable pour l'intégration future avec la PWA (Progressive Web App).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from ml.src.models.efficientnet import build_model
from ml.src.utils.config import load_and_merge


def main() -> None:
    # 1. Gestion des arguments CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", action="append", default=[], help="Chemins optionnels vers YAMLs")
    parser.add_argument("--checkpoint", required=True, help="Chemin vers le fichier de poids du modèle (.pth) à exporter")
    parser.add_argument("--output", default=None, help="Chemin final du fichier .onnx produit")
    args = parser.parse_args()

    # 2. Configuration du dossier racine 'ml'
    base_dir = Path(__file__).resolve().parents[2]

    if args.config:
        cfg_paths = args.config
    else:
        cfg_paths = [
            str(base_dir / "configs" / "base.yaml"),
            str(base_dir / "configs" / "data.yaml"),
            str(base_dir / "configs" / "train.yaml"),
        ]

    # 3. Chargement de l'architecture du modèle
    cfg = load_and_merge(cfg_paths)
    
    # Construction d'un modèle "vide" de même architecture (EfficientNet-B4)
    model = build_model(cfg)
    
    # 4. Chargement des Poids (les connaissances apprises)
    state = torch.load(args.checkpoint, map_location="cpu")
    model.load_state_dict(state)
    
    # 5. Mode "Évaluation" : Désactive les mécanismes dynamiques (ex: Dropout) inadaptés pour l'inférence
    model.eval()

    # 6. Création d'une image "fantôme" (Dummy)
    # ONNX a besoin de voir un exemple d'entrée pour tracer le chemin du réseau ("tracing")
    input_size = cfg.get("model", {}).get("input_size", [3, 384, 384])
    dummy = torch.randn(1, input_size[0], input_size[1], input_size[2])

    # 7. Préparation du chemin de sortie
    if args.output is None:
        output_path = base_dir / "models" / "exported" / "model.onnx"
    else:
        out = Path(args.output)
        output_path = out if out.is_absolute() else (base_dir / out)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 8. EXPORTATION VERS ONNX !
    torch.onnx.export(
        model,                                           # Le modèle avec ses poids chargés
        dummy,                                           # L'image fantôme de test
        str(output_path),                                # Nom du fichier final (ex: cerviscan.onnx)
        input_names=["input"],                           # Nom donné au nœud d'entrée (pratique pour l'API web)
        output_names=["logits"],                         # Nom donné au nœud de sortie
        opset_version=int(cfg.get("export", {}).get("opset", 17)), # Version de l'export (v17 est le standard actuel)
    )


if __name__ == "__main__":
    main()
