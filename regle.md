# Les Regles d'Or du ML/DL Professionnel

## Concret, Direct, Applicable

---

# PHASE 1 : AVANT DE TOUCHER AU MODELE

---

### REGLE 1 : Comprends le probleme AVANT de coder

```
FAIS :
  -> Parle au metier : "c'est quoi le vrai probleme ?"
  -> Definition de la metrique de SUCCES business
  -> Verifie que le ML est la BONNE solution
  -> Demande : "qui va UTILISER la prediction ?"

EVITE :
  -> Ouvrir Jupyter et coder direct
  -> Choisir l'algorithme avant de voir les donnees
  -> Resoudre un probleme que personne n'a
```

---

### REGLE 2 : Connais tes donnees comme ta poche

```
FAIS :
  -> Regarde les donnees MANUELLEMENT (pas juste .describe())
  -> Comprends chaque colonne avec le metier
  -> Verifie les distributions
  -> Cherche les valeurs ABERRANTES
  -> Verifie les correlations
  -> Regarde les valeurs manquantes
  -> Cherche les DOUBLONS

EVITE :
  -> Faire confiance aux donnees sans verifier
  -> Ignorer les colonnes que tu ne comprends pas
  -> Sauter l'EDA parce que "c'est long"

CONCRETEMENT :
  df.shape
  df.head(20)          # pas juste 5
  df.info()
  df.describe()
  df.isnull().sum()
  df.duplicated().sum()
  df['target'].value_counts()
  df.corr()
```

---

### REGLE 3 : Verifie la qualite avant la quantite

```
FAIS :
  -> 1000 lignes PROPRES > 100 000 lignes SALES
  -> Verifie la coherence des donnees
  -> Cherche les erreurs de saisie
  -> Verifie que les dates sont logiques
  -> Verifie que les montants sont positifs quand ils doivent l'etre

EVITE :
  -> "Plus de donnees = mieux" sans verifier la qualite
  -> Garder des lignes avec des valeurs impossibles
     (age = 250, salaire = -5000)
```

---

# PHASE 2 : PREPARATION DES DONNEES

---

### REGLE 4 : Separe AVANT de transformer

```
L'ORDRE CORRECT :
  1. Separer train / test
  2. PUIS normaliser, encoder, imputer
  3. fit sur le TRAIN
  4. transform sur le TEST

L'ERREUR CLASSIQUE :
  1. Normaliser tout
  2. PUIS separer
  -> Data leakage garanti

CODE :
  X_train, X_test, y_train, y_test = train_test_split(X, y)
  
  scaler.fit(X_train)                 # apprend sur TRAIN
  X_train = scaler.transform(X_train) # transforme TRAIN
  X_test = scaler.transform(X_test)   # transforme TEST (memes params)
```

---

### REGLE 5 : Gere les valeurs manquantes intelligemment

```
FAIS :
  -> Comprends POURQUOI c'est manquant
  -> Numerique : mediane (robuste) ou moyenne
  -> Categoriel : mode ou categorie "Inconnu"
  -> Beaucoup de NaN (>40%) : supprime la colonne
  -> Parfois NaN = une INFORMATION ("pas renseigne" = un signal)

EVITE :
  -> Remplir par 0 sans reflechir
  -> Supprimer toutes les lignes avec NaN (perte de donnees)
  -> Utiliser la moyenne quand il y a des outliers
  -> Ignorer les NaN et esperer que ca marche
```

---

### REGLE 6 : Encode correctement les categories

```
FAIS :
  -> PAS d'ordre -> One-Hot Encoding
     (Paris, Lyon, Marseille -> 3 colonnes de 0/1)
  -> Ordre -> Label Encoding ou Ordinal Encoding
     (Petit < Moyen < Grand -> 0, 1, 2)
  -> Trop de categories (>20) -> Target Encoding ou Frequency Encoding
  -> drop_first=True pour eviter la multicolinearite

EVITE :
  -> Label Encoding sur des villes
     (Paris=0, Lyon=1 -> le modele croit Lyon > Paris)
  -> One-Hot sur une colonne avec 500 categories
```

---

### REGLE 7 : Normalise quand il faut

```
NECESSAIRE pour :
  -> KNN, SVM, Regression, Reseaux de neurones, PCA

PAS NECESSAIRE pour :
  -> Arbres de decision, Random Forest, XGBoost

FAIS :
  -> StandardScaler par defaut (moyenne=0, std=1)
  -> RobustScaler si outliers
  -> MinMaxScaler si vous voulez [0,1]

EVITE :
  -> Normaliser la target en classification
  -> Oublier de normaliser pour KNN ou SVM
  -> fit_transform sur le test set
```

---

### REGLE 8 : Feature Engineering intelligent

```
FAIS :
  -> Cree des features qui ont du SENS METIER
  -> Dates -> jour de semaine, mois, est_weekend, saison
  -> Interactions -> prix x quantite = montant_total
  -> Ratios -> dette / revenu = taux_endettement

EVITE :
  -> Creer 200 features au hasard
  -> Features qui contiennent la reponse (leakage)
  -> Features non disponibles en production
```

---

# PHASE 3 : MODELISATION

---

### REGLE 9 : Commence TOUJOURS par une baseline

```
FAIS :
  -> Baseline simple : predire la moyenne / la classe majoritaire
  -> Modele simple : Regression Logistique / Decision Tree
  -> Votre modele complexe doit BATTRE le simple
  -> Si le simple suffit -> gardez-le

EVITE :
  -> Commencer par un reseau de neurones
  -> Ignorer la baseline
```

---

### REGLE 10 : Choisis la bonne metrique

```
FAIS :

  REGRESSION :
    -> RMSE si les grosses erreurs sont graves
    -> MAE si toutes les erreurs comptent pareil
    -> R2 pour comparer les modeles

  CLASSIFICATION :
    -> Classes equilibrees -> Accuracy OK
    -> Classes desequilibrees -> F1-Score ou AUC-ROC
    -> Faux Negatifs graves (medical) -> Recall
    -> Faux Positifs graves (spam) -> Precision

EVITE :
  -> Utiliser accuracy sur des donnees desequilibrees
```

---

### REGLE 11 : Valide CORRECTEMENT

```
FAIS :
  -> TOUJOURS cross-validation (5 ou 10 folds)
  -> Regarder la VARIANCE entre les folds
  -> StratifiedKFold si classification
  -> Le test set = touche UNE SEULE FOIS a la fin

EVITE :
  -> Un seul split train/test
  -> Tuner les hyperparametres sur le test set
```

---

### REGLE 12 : Detecte l'overfitting

```
FAIS :
  -> Compare TOUJOURS train score et test score
  -> Ecart > 10% -> suspect
  -> Plot la learning curve
  -> Simplifie le modele si overfitting

EVITE :
  -> Ne regarder que le train score
  -> Ignorer les signes d'overfitting

SIGNAUX D'ALARME :
  Train: 99%  Test: 72%  -> OVERFITTING
  Train: 88%  Test: 85%  -> OK
  Train: 60%  Test: 58%  -> UNDERFITTING
```

---

### REGLE 13 : Classes desequilibrees

```
FAIS :
  -> Verifie TOUJOURS la distribution de la target
  -> class_weight='balanced' dans le modele
  -> SMOTE pour creer des exemples synthetiques (si besoin)
  -> Utiliser F1 ou AUC, pas l'accuracy
  -> Stratifier le split (stratify=y)

EVITE :
  -> Ignorer le desequilibre
  -> Se rejouir de 95% d'accuracy quand 95% des donnees sont de la meme classe
```

---

# PHASE 4 : DEEP LEARNING

---

### REGLE 14 : Deep Learning seulement quand c'est justifie

```
UTILISE LE DL POUR :
  -> Images (CNN)
  -> Texte (Transformers)
  -> Audio
  -> Donnees NON structurees

EVITE LE DL POUR :
  -> Donnees tabulaires classiques (XGBoost est souvent meilleur)
  -> Peu de donnees (< 5000 lignes)
```

---

### REGLE 15 : Architecture Deep Learning

```
FAIS :
  -> Commence PETIT puis agrandis
  -> BatchNorm entre les couches
  -> Dropout (0.2-0.5) pour regulariser
  -> Activation ReLU (cachee) + Sigmoid/Softmax (sortie)
  -> Adam comme optimizer par defaut

EVITE :
  -> Reseau trop profond pour peu de donnees
  -> Pas de regularisation
```

---

# PHASE 5 : PRODUCTION

---

### REGLE 17 : Le modele doit marcher en VRAI

```
FAIS :
  -> Teste avec des donnees REALISTES
  -> Teste les cas EXTREMES (edge cases)
  -> Teste les valeurs MANQUANTES en entree
  -> Mesure le temps d'INFERENCE

EVITE :
  -> "Ca marchait dans le notebook"
```

---

### REGLE 18 : Surveille ton modele en production

```
FAIS :
  -> Log chaque prediction (input + output)
  -> Surveille les distributions (data drift)
  -> Planifie le re-entrainement (mensuel, hebdomadaire...)

EVITE :
  -> Deployer et oublier
```

---

### REGLE 19 : Rends le modele explicable

```
FAIS :
  -> Feature Importance
  -> SHAP values
  -> Savoir dire "le modele predit X PARCE QUE..."

EVITE :
  -> Boite noire sans explication
```

---

### REGLE 20 : Documente TOUT

```
FAIS :
  -> README qui explique le projet
  -> POURQUOI ce modele et pas un autre
  -> COMMENT reproduire les resultats
  -> QUELLES sont les limites connues

EVITE :
  -> Notebook de 300 cellules sans commentaire
```

---

# CHECKLIST FINALE

```
AVANT DE DIRE "MON MODELE EST PRET" :

DONNEES
  - J'ai compris chaque feature
  - J'ai verifie les NaN et les outliers
  - Pas de data leakage

PREPROCESSING
  - Split AVANT preprocessing
  - Encoding correct
  - Classes gerees

MODELE
  - Baseline simple faite
  - Cross-validation effectuee
  - Pas d'overfitting
  - Bonne metrique choisie

PRODUCTION
  - Edge cases testes
  - Temps d'inference mesure
  - Documentation complete
```

---

Note finale : Un modele professionnel est un modele fiable, explicable et qui cree de la valeur.