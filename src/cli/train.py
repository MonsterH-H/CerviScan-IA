"""CLI (Command Line Interface) entry for training.
Ce script est le point d'entrée principal pour démarrer l'entraînement de l'IA (CerviScan IA).
Il gère la fusion des multiples fichiers de configuration YAML et lance la fonction d'apprentissage.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Fix: Ajout de la racine au PYTHONPATH pour eviter le ModuleNotFoundError
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Important : importe la fonction de création du modèle et d'entraînement
from ml.src.training.trainer import train
from ml.src.utils.config import load_and_merge


def main() -> None:
    # 1. Gestion des arguments en ligne de commande (permet de personnaliser l'appel)
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", action="append", default=[], help="Chemin vers un (ou plusieurs) fichier(s) YAML de configuration")
    args = parser.parse_args()

    # 2. Résolution du chemin racine (permet d'exécuter le script de n'importe où dans le terminal)
    # resolve().parents[2] remonte depuis ml/src/cli/ jusqu'au dossier racine 'ml'
    base_dir = Path(__file__).resolve().parents[2]

    # 3. Récupération des fichiers de configuration
    # Si l'utilisateur n'a spécifié aucune config, on force le chargement de toutes les configs par défaut.
    # L'ordre est important : du moins spécifique (base) au plus spécifique (eval/train).
    if args.config:
        cfg_paths = args.config
    else:
        cfg_paths = [
            str(base_dir / "configs" / "base.yaml"),   # (Modèle, Architecture)
            str(base_dir / "configs" / "data.yaml"),   # (Dossiers de données, Labels)
            str(base_dir / "configs" / "train.yaml"),  # (Vitesse, Epochs, Optimiseur)
            str(base_dir / "configs" / "eval.yaml"),   # (Métriques à observer)
        ]

    # 4. Fusion des Configurations (Merge) en un seul dictionnaire Python
    cfg = load_and_merge(cfg_paths)
    
    # 5. DÉMARRAGE : Appel de la fonction "train" présente dans trainer.py
    train(cfg)


if __name__ == "__main__":
    main()
