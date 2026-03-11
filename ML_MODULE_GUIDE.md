# 🏥 Guide d'Utilisation : CerviScan IA (SentAI)
> **Stack Machine Learning Premium** — Diagnostic du Cancer du Col de l'Utérus.

Ce guide centralise toutes les commandes nécessaires pour manipuler, entraîner et déployer le modèle de vision de la solution **CerviScan IA**.

---

## 🚀 1. Préparation de l'Environnement

Avant de commencer, assurez-vous que votre environnement virtuel est configuré et que les dépendances sont installées.

```powershell
# Création de l'environnement (si non fait)
python -m venv ml/.venv

# Activation (Windows)
.\ml\.venv\Scripts\Activate.ps1

# Installation des dépendances "State-of-the-Art"
pip install -r ml/requirements.txt
```

---

## 📁 2. Pipeline de Données

Le modèle utilise une architecture **EfficientNet-B4**. Les données doivent être structurées et équilibrées avant l'entraînement.

### Commande de préparation
Cette commande scanne les dossiers sources, gère les doublons, et crée un fichier `splits.csv` équilibré (stratifié).

```powershell
python ml/scripts/prepare_dataset.py
```

| Fichier Généré | Description |
| :--- | :--- |
| `ml/data/splits.csv` | Registre de répartition Train/Val/Test (Indispensable pour la reproductibilité). |
| `ml/reports/eda.pdf` | (Optionnel) Rapport d'analyse exploratoire des données. |

---

## 🧠 3. Entraînement du Modèle (Training)

L'entraînement est piloté par CLI (Command Line Interface) et configuré via les fichiers YAML dans `ml/configs/`.

### Lancer un entraînement standard
```powershell
python -m ml.src.cli.train --config ml/configs/train.yaml
```

### Paramètres Clés (à ajuster dans `train.yaml`)
*   **Epochs (50)** : Nombre de cycles complets sur les données.
*   **Batch Size (16)** : Compromis idéal entre vitesse et stabilité mémoire GPU.
*   **Learning Rate (0.0003)** : Pas d'apprentissage optimisé pour le transfert learning.
*   **Mixed Precision (True)** : Accélère l'entraînement sur les GPU modernes (Float16).

---

## 📊 4. Évaluation & Performance

Une fois le modèle entraîné, il est impératif de valider sa robustesse sur le "Test Set" (données jamais vues).

### Commande d'évaluation
```powershell
python -m ml.src.cli.eval --model weights/best_model.pth --config ml/configs/eval.yaml
```

> [!IMPORTANT]
> **Métriques Cibles (KPIs) :**
> *   **F1-Score Macro :** Doit être > 0.85 pour garantir que les types 2 et 3 ne sont pas négligés.
> *   **Recall (Type 3) :** Critique pour ne pas manquer de cas suspects.

---

## 🚢 5. Export & Déploiement (Production)

Pour l'intégration dans la **PWA (Progressive Web App)**, le modèle doit être converti au format **ONNX**.

### Commande d'exportation
```powershell
python -m ml.src.cli.export --model weights/best_model.pth --output outputs/cerviscan_v1.onnx
```

*   **Format :** ONNX (Open Neural Network Exchange).
*   **Avantages :** Inférence ultra-rapide côté navigateur (JS/WebAssembly).
*   **Opset :** 17 (pour une compatibilité maximale avec les moteurs récents).

---

## 🛠️ 6. Antisèche (Cheat Sheet) des Commandes

| Action | Commande |
| :--- | :--- |
| **Setup** | `pip install -r ml/requirements.txt` |
| **Data Prep** | `python ml/scripts/prepare_dataset.py` |
| **Train** | `python -m ml.src.cli.train` |
| **Eval** | `python -m ml.src.cli.eval --model ...` |
| **Export** | `python -m ml.src.cli.export --model ...` |
| **Test Env** | `python ml/test_env.py` |

---

## 🛡️ 7. Règles d'Or de Développement
*Extract du fichier `ml/regle.md`*

1.  **Split AVANT Transfo :** On ne normalise jamais avant d'avoir séparé le Train et le Test.
2.  **Baseline Simple :** Toujours comparer les résultats avec un modèle simple.
3.  **Data Leakage :** Vérifiez qu'aucune image de test n'est présente dans le train via les IDs patientes.
4.  **Inférence Réelle :** Un modèle qui tourne en 30 secondes est inutile sur le terrain. Visez **< 10s**.

---

*Document généré pour l'équipe **CerviScan IA** — 2024.*
