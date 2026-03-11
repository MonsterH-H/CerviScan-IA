# 🛠️ Guide Complet : Exécution du Projet & Gestion avec Git

Ce document vous explique comment exécuter votre projet de A à Z et comment versionner votre travail avec Git de manière professionnelle.

---

## 🚀 PARTIE 1 : Exécution du Projet (De A à Z)

Assurez-vous d'être dans le dossier `ml/` de votre projet et que votre environnement virtuel est activé.

```powershell
# 1. Activation de l'environnement virtuel (depuis le dossier ml/)
.\.venv\Scripts\Activate.ps1

# 2. Vérification des dépendances
pip install -r requirements.txt
```

### Étape 1 : Préparation des données
Cette étape permet d'analyser vos dossiers d'images et de scinder équitablement les données (Train / Val / Test).
```powershell
python scripts/prepare_dataset.py
```
> **Résultat :** Un fichier [data/interim/splits.csv](file:///c:/AI/Machine%20Learning/SentAI/ml/data/interim/splits.csv) sera créé. Il est indispensable pour la suite.

### Étape 2 : Entraînement du modèle
Lancez le processus d'apprentissage de l'intelligence artificielle (architecture EfficientNet-B4).
```powershell
python -m src.cli.train --config configs/train.yaml
```
> **Astuce :** L'entraînement peut prendre du temps selon votre carte graphique (GPU). Les meilleurs poids seront sauvegardés dans `weights/best_model.pth`.

### Étape 3 : Évaluation
Vérifiez les performances (F1-Score, Recall) sur les données de test (non vues par le modèle).
```powershell
python -m src.cli.eval --model weights/best_model.pth --config configs/eval.yaml
```

### Étape 4 : Exportation (Production)
Convertissez votre modèle entraîné au format ONNX pour l'intégrer facilement dans la PWA de CerviScan.
```powershell
python -m src.cli.export --model weights/best_model.pth --output outputs/cerviscan_v1.onnx
```

---

## 🐙 PARTIE 2 : Gestion avec Git (Étape par Étape)

Git vous permet de sauvegarder l'historique de votre code, de revenir en arrière en cas d'erreur et de collaborer.

### 1. Initialiser Git et lier le projet
```powershell
# Initialise le dépôt Git (si ce n'est pas déjà fait)
git init

# (Optionnel) Ajout du dépôt distant si vous utilisez GitHub/GitLab
# Remplacez l'URL par la vôtre
# git remote add origin https://github.com/votre-nom/SentAI.git
```

### 2. Le fichier [.gitignore](file:///c:/AI/Machine%20Learning/SentAI/ml/.gitignore) (MANDATOIRE)
Il est essentiel de ne **PAS** commiter les données lourdes, les modèles générés, ni l'environnement virtuel.
Vérifiez que le fichier [.gitignore](file:///c:/AI/Machine%20Learning/SentAI/ml/.gitignore) dans votre dossier `ml/` contient les lignes suivantes :
```text
# Ne pas tracker l'environnement virtuel
.venv/
venv/
env/

# Ne pas tracker les fichiers de cache Python
__pycache__/
*.pyc
*.pyo

# Ne pas tracker les données massives et modèles générés
data/
weights/
outputs/
reports/

# Fichiers configs locaux et logs
*.log
.vscode/
.DS_Store
```

### 3. Sauvegarder votre travail (Commit)
Lorsque vous avez fini une fonctionnalité ou corrigé un bug, suivez ce flux de travail :

**A. Voir ce qui a été modifié :**
```powershell
git status
```

**B. Ajouter les fichiers modifiés (Staging) :**
```powershell
# Ajouter un fichier précis
git add USER_GUIDE.md

# Ou ajouter tous les fichiers modifiés d'un coup
git add .
```

**C. Créer une sauvegarde avec un message descriptif (Commit) :**
```powershell
git commit -m "feat: correction des chemins absolus ml/ et mise à jour des guides"
```
> *Utilisez des préfixes comme `feat:` (nouvelle fonctionnalité), `fix:` (correction), `docs:` (documentation).*

### 4. Pousser vers GitHub / GitLab (Push)
Une fois votre travail commité, vous l'envoyez sur le serveur distant.

```powershell
# La première fois, on définit la branche par défaut
git branch -M main

# Puis on pousse le code (seulement la première fois avec -u)
git push -u origin main

# Les fois suivantes, un simple push suffit :
git push
```

### 5. Revenir en arrière en cas de problème (Rollback)

**Vous avez modifié un fichier et voulez annuler (avant un `git add`) :**
```powershell
git checkout -- src/mon_fichier.py
```

**Vous avez déjà fait un `git add`, mais voulez l'annuler (Unstage) :**
```powershell
git restore --staged src/mon_fichier.py
```

**Vous voulez annuler le tout dernier commit :**
```powershell
git reset --soft HEAD~1
```

---
Avec ces étapes, vous avez un environnement de Machine Learning reproductible et parfaitement versionné !
