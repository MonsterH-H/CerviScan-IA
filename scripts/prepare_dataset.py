"""Découverte des images et préparation des splits (train/val/test).

Génère :
- ml/data/interim/splits.csv (colonnes: path, label, split)
- ml/reports/metrics/class_counts.csv (statistiques par classe)
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

# On remonte au dossier racine AU-DESSUS du dossier /ml/ pour permettre l'import 'ml.src'
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Dossier spécifique au module ML
ML_ROOT = PROJECT_ROOT / "ml"

from ml.src.data.datasets import discover_images
from ml.src.data.splits import stratified_split


def main() -> None:
    data_dir = ML_ROOT / "data"

    # Répertoires contenant les images brutes
    train_dirs = [
        data_dir / "train" / "train",
        data_dir / "additional_Type_1_v2",
        data_dir / "additional_Type_2_v2",
        data_dir / "additional_Type_3_v2",
    ]
    class_names = ["Type_1", "Type_2", "Type_3"]

    print(f"[INFO] Recherche d'images dans : {data_dir}")
    items = discover_images(train_dirs, class_names)
    
    if not items:
        print("[ERREUR] Aucune image trouvée. Vérifiez vos dossiers de données.")
        return

    print(f"[OK] {len(items)} images trouvees.")

    # Paramètres du split (Reproductibilité : Règle 4)
    seed = 42
    val_ratio = 0.15
    test_ratio = 0.15

    # Calcul des indices via split stratifié (Règle 13)
    train_idx, val_idx, test_idx = stratified_split(
        items, 
        val_ratio=val_ratio, 
        test_ratio=test_ratio, 
        seed=seed
    )

    # Attribution du split à chaque image
    assigned_splits = [""] * len(items)
    for i in train_idx: assigned_splits[i] = "train"
    for i in val_idx: assigned_splits[i] = "val"
    for i in test_idx: assigned_splits[i] = "test"

    # Création des dossiers de sortie
    interim_dir = data_dir / "interim"
    reports_dir = ML_ROOT / "reports" / "metrics"
    interim_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Sauvegarde des splits
    split_path = interim_dir / "splits.csv"
    with split_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["path", "label", "split"])
        for i, (path, label) in enumerate(items):
            try:
                rel_path = Path(path).relative_to(ML_ROOT).as_posix()
            except ValueError:
                rel_path = Path(path).as_posix()
            writer.writerow([rel_path, label, assigned_splits[i]])

    # Export des statistiques de classes (Règle 2)
    counts = Counter([label for _, label in items])
    counts_path = reports_dir / "class_counts.csv"
    with counts_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "count"])
        for label, count in sorted(counts.items()):
            writer.writerow([label, count])

    print(f"[INFO] Splits enregistres dans : {split_path}")
    print(f"[INFO] Statistiques enregistrees dans : {counts_path}")


if __name__ == "__main__":
    main()
