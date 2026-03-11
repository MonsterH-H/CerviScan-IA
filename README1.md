# SentAI - Machine Learning Stack

Ce dossier contient l'infrastructure d'intelligence artificielle pour le diagnostic du cancer du col de l'utérus.

## Objectifs du Modele
- Architecture : EfficientNet-B4 (pre-entraine).
- Entree : Images RGB redimensionnees en 384x384 (normalisees).
- Sortie : Classification en 3 types cliniques (Type 1, Type 2, Type 3).
- Format final : Export ONNX pour integration PWA.

## Correspondance des Labels (Classes 0, 1, 2)

Afin de permettre une compréhension totale par les équipes médicales (profanes en informatique) et les ingénieurs (Data Scientists), voici l'explication des 3 classes utilisées par l'IA :

### 1. Pour les Médecins et Patients (Langage Clinique / Profane)
Ces chiffres sont des catégories pour classer l'état de santé du col de l'utérus détecté sur l'image :
- **Classe 0 = Type 1 (Sain / Normal) :** Le col de l'utérus est en bonne santé. Il n'y a pas de lésion inquiétante ou précancéreuse visible.
- **Classe 1 = Type 2 (Lésion de bas grade) :** L'intelligence artificielle a détecté de petites anomalies bénignes ou des lésions très précoces (comme une infection bénigne au HPV). Cela demande généralement une simple surveillance.
- **Classe 2 = Type 3 (Lésion de haut grade / Suspect) :** C'est le cas sérieux. L'IA a détecté des lésions graves ou fortement suspectes d'être cancéreuses ou précancéreuses. Cela nécessite une biopsie ou une intervention médicale rapide.

### 2. Pour les Data Scientists (Langage Technique / Machine Learning)
Un algorithme (EfficientNet-B4) ne comprend pas le texte en entrée/sortie, mais des nombres entiers (indices) convertis ensuite en probabilités.
- **Label Encoding (0-Indexé) :** Les noms de dossiers textuels ("Type_1", "Type_2", "Type_3") sont convertis en indices de tableau (0, 1, 2) compatibles avec la fonction de perte (CrossEntropyLoss).
- **Inférence / Output :** En sortie, le modèle ONNX/PyTorch génère un tenseur de 3 probabilités Softmax (ex: `[0.10, 0.05, 0.85]`). La classe finale est obtenue via un `argmax(dim=1)` sur ce tenseur (ici l'index `2` car 0.85 est la plus grande probabilité).

## Structure du Projet
- configs/ : Fichiers YAML gerant les hyperparametres (base, data, train, eval).
- data/ : Images d'origine, fichiers intermediaires (splits.csv) et rapports.
- notebooks/ : Pipelines d'analyse (01_Exploration) et d'entrainement (Master_Pipeline).
- scripts/ : Utilitaires de preparation des donnees.
- src/ : Code source modulaire (data, models, training, utils).

## Comment l'utiliser

### 1. Preparation de l'environnement
Installez les dependances via le fichier requirements.txt.

### 2. Etape 1 : Preparation des donnees
Organise les images et cree le fichier de repartition equilibree.
```bash
.\.venv\Scripts\python.exe scripts/prepare_dataset.py
```

### 3. Etape 2 : Exploration et Analyse
Ouvrez le notebook notebooks/01_Exploration_Et_Analyse_SentAI.ipynb pour valider la qualite des donnees.

### 4. Etape 3 : Entrainement
Utilisez le notebook notebooks/SentAI_Master_Pipeline.ipynb ou la CLI :
```bash
.\.venv\Scripts\python.exe -m src.cli.train
```

## Regles d'Or
Le projet suit les regles definies dans regle.md (Reproductibilite, Baseline, Metriques F1-Macro).
