"""CLI (Command Line Interface) entry for evaluation.
Ce script est conçu pour exécuter l'évaluation du modèle après ou pendant l'entraînement.
Il charge un modèle sauvegardé (checkpoint) et le teste sur un ensemble de données (Validation ou Test).
Il est très important pour la Règle n°11 : Valider la performance sur des données jamais vues.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Fix: Ajout de la racine au PYTHONPATH pour eviter le ModuleNotFoundError
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from ml.src.training.trainer import evaluate
from ml.src.utils.config import load_and_merge


def main() -> None:
    # 1. Définition des paramètres CLI (Ligne de commande)
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", action="append", default=[], help="Chemin vers un (ou plusieurs) fichier(s) YAML de config")
    parser.add_argument("--checkpoint", required=True, help="Chemin absolu ou relatif vers le fichier de poids du modèle (.pth ou .pt)")
    parser.add_argument("--split", choices=["val", "test"], default="val", help="Choix de l'ensemble de données (Validation = 'val', Évaluation Finale = 'test')")
    args = parser.parse_args()

    # 2. Résolution dynamique du chemin principal (racine 'ml')
    base_dir = Path(__file__).resolve().parents[2]

    # 3. Chargement de toutes les configurations requises pour l'évaluation
    if args.config:
        cfg_paths = args.config
    else:
        cfg_paths = [
            str(base_dir / "configs" / "base.yaml"),
            str(base_dir / "configs" / "data.yaml"),
            str(base_dir / "configs" / "train.yaml"),
            str(base_dir / "configs" / "eval.yaml"),
        ]

    # 4. Fusion des configurations (Merge)
    cfg = load_and_merge(cfg_paths)
    
    # 5. DÉMARRAGE : Lancement de l'évaluation sur l'ensemble demandé
    evaluate(cfg, args.checkpoint, split=args.split)


if __name__ == "__main__":
    main()
