# SentAI - Machine Learning Stack

Ce dossier contient l'infrastructure d'intelligence artificielle pour le diagnostic du cancer du col de l'utérus.

## Objectifs du Modele
- Architecture : EfficientNet-B4 (pre-entraine).
- Entree : Images RGB redimensionnees en 384x384 (normalisees).
- Sortie : Classification en 3 types cliniques (Type 1, Type 2, Type 3).
- Format final : Export ONNX pour integration PWA.

## Correspondance des Labels
- 0 : Type 1 (Sain / Normal)
- 1 : Type 2 (Lesion de bas grade)
- 2 : Type 3 (Lesion de haut grade / Suspect)

## Structure du Projet
- configs/ : Fichiers YAML gerant les hyperparametres (base, data, train, eval).
- data/ : Images d'origine, fichiers intermediaires (splits.csv) et rapports.
- notebooks/ : Pipelines d'analyse (01_Exploration) et d'entrainement (Master_Pipeline).
- scripts/ : Utilitaires de preparation des donnees.
- src/ : Code source modulaire (data, models, training, utils).

## Comment l'utiliser (depuis la racine)

### 1. Preparation de l'environnement
Installez les dependances via le fichier ml/requirements.txt.

### 2. Etape 1 : Preparation des donnees
Organise les images et cree le fichier de repartition equilibree.
```bash
.\ml\.venv\Scripts\python.exe ml/scripts/prepare_dataset.py
```

### 3. Etape 2 : Exploration et Analyse
Ouvrez le notebook ml/notebooks/01_Exploration_Et_Analyse_SentAI.ipynb pour valider la qualite des donnees.

### 4. Etape 3 : Entrainement
Utilisez le notebook ml/notebooks/SentAI_Master_Pipeline.ipynb ou la CLI :
```bash
.\ml\.venv\Scripts\python.exe -m ml.src.cli.train
```

## Regles d'Or
Le projet suit les regles definies dans ml/regle.md (Reproductibilite, Baseline, Metriques F1-Macro).
