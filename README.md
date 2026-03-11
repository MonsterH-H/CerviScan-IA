# CAHIER DES CHARGES — CERVI-SCAN IA
## Application d'Aide au Diagnostic du Cancer du Col de l'Utérus par Intelligence Artificielle

---

> **Version :** 2.0  
> **Statut :** Document de référence  
> **Date :** Mars 2024  
> **Confidentialité :** Strictement confidentiel — Usage interne  

---

## TABLE DES MATIÈRES

1. [Présentation du Projet](#1-présentation-du-projet)
2. [Périmètre Fonctionnel & Rôles](#2-périmètre-fonctionnel--rôles)
3. [Modules Fonctionnels Détaillés](#3-modules-fonctionnels-détaillés)
   - 3.1 Authentification & Gestion des Sessions
   - 3.2 Gestion des Patientes
   - 3.3 Dépistage Assisté par IA
   - 3.4 Historique & Comparaison d'Images
   - 3.5 Validation Médecin
   - 3.6 Tableau de Bord
   - 3.7 Système de Rapports Intelligents (Groq)
   - 3.8 Système de Notifications & Emails
4. [Workflows Métier Complets](#4-workflows-métier-complets)
5. [Intégration Groq — Rapports & IA Générative](#5-intégration-groq--rapports--ia-générative)
6. [Système d'Emails — Cas d'Usage Complets](#6-système-demails--cas-dusage-complets)
7. [Modèle de Données](#7-modèle-de-données)
8. [Architecture Technique](#8-architecture-technique)
9. [Spécifications IA (Modèle Vision)](#9-spécifications-ia-modèle-vision)
10. [Sécurité & Conformité](#10-sécurité--conformité)
11. [Interfaces Utilisateur](#11-interfaces-utilisateur)
12. [Plan de Tests & Qualité](#12-plan-de-tests--qualité)
13. [Déploiement & Infrastructure](#13-déploiement--infrastructure)

---

## 1. PRÉSENTATION DU PROJET

### 1.1 Contexte & Problématique

Le cancer du col de l'utérus est le quatrième cancer le plus fréquent chez la femme dans le monde. En Afrique subsaharienne, il représente la première cause de mortalité féminine par cancer, notamment en raison d'un accès limité aux structures spécialisées et d'un manque de personnel médical qualifié pour l'interprétation des résultats de dépistage.

La méthode IVA (Inspection Visuelle à l'Acide acétique) est une approche reconnue par l'OMS comme alternative efficace dans les contextes à ressources limitées. Son principal frein reste la subjectivité de l'interprétation visuelle et le manque de formation continue des agents de santé.

**CerviScan IA** répond à ce défi en combinant une application mobile/web accessible aux agents de terrain avec un moteur d'intelligence artificielle capable d'analyser les images cervicales et de produire un diagnostic assisté en moins de 10 secondes.

### 1.2 Description du Produit

CerviScan IA est une **Progressive Web Application (PWA)** multiplateforme permettant :

- La gestion complète du parcours patient de dépistage
- L'analyse automatique des images cervicales par IA (modèle de vision)
- La génération de rapports quotidiens, hebdomadaires et mensuels par Groq (IA générative)
- L'envoi automatique de notifications email pour le suivi des patientes et des rappels de dépistage
- La supervision centralisée par les médecins et superviseurs de district

### 1.3 Objectifs Mesurables

| Objectif | Indicateur | Cible |
|----------|-----------|-------|
| Réduire le délai de diagnostic | Temps entre capture et résultat IA | < 10 secondes |
| Améliorer la concordance agent/IA | Taux de validation sans désaccord | ≥ 88% |
| Assurer la traçabilité | % de dépistages avec dossier complet | 100% |
| Réduire les perdues de vue | % de patientes revenues au contrôle | +25% vs. baseline |
| Automatiser les rapports | Temps agent pour rapport mensuel | < 5 min (auto-généré) |

### 1.4 Portée Géographique & Contraintes Terrain

- Déploiement en zones à connectivité instable (mode offline obligatoire)
- Support multilingue : Français, Bambara, Wolof (phase 2)
- Compatibilité appareils Android 8+ et navigateurs modernes
- Capture d'image via smartphone ou tablette + accessoire optionnel (colposcope connecté)

---

## 2. PÉRIMÈTRE FONCTIONNEL & RÔLES

### 2.1 Matrice des Rôles et Permissions

| Fonctionnalité | Infirmier / Sage-femme | Médecin | Superviseur | Admin Système |
|---|:---:|:---:|:---:|:---:|
| Créer fiche patiente | ✅ | ✅ | ❌ | ✅ |
| Réaliser un dépistage | ✅ | ✅ | ❌ | ❌ |
| Voir résultats IA | ✅ | ✅ | ❌ | ❌ |
| Valider/corriger diagnostic | ❌ | ✅ | ❌ | ❌ |
| Voir tableau de bord personnel | ✅ | ✅ | ✅ | ✅ |
| Voir statistiques district | ❌ | ✅ | ✅ | ✅ |
| Générer rapports | ❌ | ✅ | ✅ | ✅ |
| Configurer notifications email | ❌ | ❌ | ✅ | ✅ |
| Gérer utilisateurs | ❌ | ❌ | ❌ | ✅ |
| Accéder à l'API Groq | ❌ | ❌ | ❌ | ✅ (auto) |

### 2.2 Description des Rôles

**Infirmier / Sage-femme (Agent de terrain)**
Utilisateur principal de l'application. Réalise les dépistages au sein des CSCOM (Centres de Santé Communautaire). Accède uniquement à ses propres patientes et dépistages. Reçoit les rappels par email pour les contrôles périodiques à programmer.

**Médecin (Superviseur clinique)**
Valide les cas complexes signalés par l'IA ou l'agent. Supervise les agents de plusieurs centres. Reçoit des rapports hebdomadaires automatiques générés par Groq. Peut corriger les diagnostics IA.

**Superviseur (Superviseur de district)**
Accès en lecture uniquement aux statistiques agrégées de son district. Reçoit des rapports mensuels OMS-compatibles générés par Groq. Ne peut pas modifier les dossiers patients.

**Admin Système**
Configure les utilisateurs, les centres de santé, les paramètres de notification et les seuils d'alerte IA. Gère l'infrastructure technique.

---

## 3. MODULES FONCTIONNELS DÉTAILLÉS

### 3.1 Module 1 — Authentification & Gestion des Sessions

#### Fonctionnalités

**Connexion sécurisée**
- Formulaire email + mot de passe avec validation côté client
- JWT (Access Token 15min + Refresh Token 7 jours)
- Détection de session expirée avec redirection automatique
- Déconnexion automatique après 30 minutes d'inactivité
- Option "Se souvenir de moi" (refresh token persistant 30 jours)

**Récupération de mot de passe**
1. L'agent saisit son email professionnel
2. Envoi automatique d'un email avec lien de réinitialisation (valide 1h)
3. Page de réinitialisation avec contraintes de sécurité :
   - Minimum 8 caractères
   - Au moins 1 majuscule, 1 chiffre, 1 caractère spécial
4. Confirmation par email après changement réussi

**Gestion des sessions multi-appareils**
- Un agent peut être connecté sur smartphone ET tablette simultanément
- Déconnexion forcée possible depuis l'interface admin
- Historique des 5 dernières connexions visible par l'utilisateur

**Emails liés à l'authentification**

| Événement | Destinataire | Email envoyé |
|-----------|------------|-------------|
| Création de compte | Nouvel utilisateur | Email de bienvenue + instructions |
| Mot de passe oublié | Utilisateur | Lien de réinitialisation (expire 1h) |
| Changement de mot de passe | Utilisateur | Confirmation de changement |
| Connexion depuis nouveau lieu | Utilisateur | Alerte de sécurité |
| Compte bloqué (5 tentatives) | Utilisateur + Admin | Notification de blocage |

---

### 3.2 Module 2 — Gestion des Patientes

#### Données du Dossier Patient

```
SECTION IDENTITÉ
─────────────────
• Nom complet *
• Date de naissance * (calcul automatique de l'âge)
• Numéro de téléphone
• Email (optionnel, pour notifications directes)
• Village / Quartier *
• Numéro d'identifiant national (si disponible)

SECTION ANTÉCÉDENTS MÉDICAUX
──────────────────────────────
• Antécédents médicaux pertinents (texte libre)
• Statut VIH : Positif / Négatif / Inconnu
• Sous traitement ARV : Oui / Non
• Nombre de grossesses (gesté)
• Nombre d'accouchements (parité)
• Date des dernières règles
• Contraception actuelle : type
• Antécédents de dépistage col utérin : Oui / Non
• Si oui : résultat et date du dernier dépistage (saisie manuelle si externe)

SECTION CONTACT & SUIVI
────────────────────────
• Contact d'urgence (nom + téléphone)
• Préférence de notification : SMS / Email / Appel
• Consentement numérique enregistré : Oui / Non (requis avant tout dépistage)
```

#### Fonctionnalités de Recherche et Navigation

- **Recherche rapide** : Nom, prénom, numéro de téléphone, ID patient
- **Filtres avancés** : Tranche d'âge, statut dernier dépistage, date prochain contrôle, résultat IA
- **Liste avec indicateurs visuels** :
  - 🟢 Dernier dépistage Normal, prochain contrôle > 3 mois
  - 🟡 Contrôle à planifier dans les 30 jours
  - 🔴 En attente de validation médecin / traitement recommandé
  - ⚫ Perdue de vue (>3 mois après date prévue de contrôle)

#### Consentement Éclairé Numérique

Avant la création de tout dossier, l'agent fait lire ou lit à la patiente le formulaire de consentement. La validation se fait par :
1. Case à cocher par l'agent certifiant avoir expliqué la procédure
2. Signature numérique de la patiente (si tablette disponible)
3. Ou code PIN à 4 chiffres communiqué oralement par la patiente
4. Timestamp et ID agent enregistrés dans l'audit trail

---

### 3.3 Module 3 — Dépistage Assisté par IA

#### 3.3.1 Processus de Capture (Step-by-Step)

```
ÉTAPE 1 — SÉLECTION PATIENTE
══════════════════════════════
→ Rechercher ou créer dossier patient
→ Vérifier consentement (badge vert requis)
→ Vérifier date dernières règles (< J1 ou > J5 du cycle)
→ Confirmer absence de grossesse en cours

ÉTAPE 2 — CHECKLIST PRÉ-EXAMEN
═══════════════════════════════
□ Col de l'utérus visible et accessible
□ Pas de saignement actif
□ Éclairage suffisant (indicateur luminosité app)
□ Application d'acide acétique à 3-5% confirmée
□ Chronomètre 60 secondes lancé

ÉTAPE 3 — CAPTURE PHOTOGRAPHIQUE
══════════════════════════════════
→ Guidage cadrage en temps réel (overlay cercle cervical)
→ Indicateur de qualité image :
   - Netteté : [████████░░] 80%
   - Luminosité : [█████████░] 90%
   - Centrage : ✅
→ Minimum 3 photos obligatoires (max 6)
→ Possibilité de relancer le chronomètre si nécessaire
→ Aperçu avant envoi avec possibilité de suppression

ÉTAPE 4 — ENVOI & ANALYSE
═══════════════════════════
→ Upload sécurisé (chiffré TLS 1.3)
→ Barre de progression avec statut :
   "Analyse en cours... (8s estimé)"
→ Résultat affiché sur écran principal
```

#### 3.3.2 Affichage des Résultats IA

```
╔══════════════════════════════════════════════════╗
║          RÉSULTAT DE L'ANALYSE IA                ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  🔴 LÉSION HAUT GRADE SUSPECTÉE                  ║
║  Niveau de confiance : 92%                       ║
║                                                  ║
╠══════════════════════════════════════════════════╣
║  📊 CLASSIFICATION DÉTAILLÉE                     ║
║  ─────────────────────────────────               ║
║  Type 3 — Lésion sévère (HSIL/CIN3) : 92%       ║
║  Type 2 — Lésion modérée (LSIL/CIN2) :  7%      ║
║  Type 1 — Normal / Inflammation       :  1%      ║
║                                                  ║
╠══════════════════════════════════════════════════╣
║  📍 LOCALISATION DE LA ZONE SUSPECTE             ║
║  ─────────────────────────────────               ║
║  Quadrant : Supérieur (10h — 14h)                ║
║  Surface concernée : ~25% de la ZT               ║
║  Proximité OE : Orifice externe impliqué : OUI   ║
║                                                  ║
╠══════════════════════════════════════════════════╣
║  🏥 RECOMMANDATION CLINIQUE                      ║
║  ─────────────────────────────────               ║
║  ➤ Traitement immédiat recommandé                ║
║  ➤ Cryothérapie ou LEEP selon disponibilité      ║
║  ➤ Consultation spécialisée dans les 2 semaines  ║
║  ➤ ENVOI EN VALIDATION MÉDECIN AUTOMATIQUE       ║
║                                                  ║
╠══════════════════════════════════════════════════╣
║  [Image avec heatmap de chaleur superposée]      ║
║  Zone rouge = zone suspecte détectée             ║
╚══════════════════════════════════════════════════╝
```

**Codes couleurs des résultats :**

| Niveau | Couleur | Confiance IA | Action automatique |
|--------|---------|-------------|-------------------|
| Normal | 🟢 Vert | ≥ 90% | Planifier prochain contrôle (3 ans) |
| Lésion bas grade | 🟡 Orange | ≥ 85% | Contrôle à 1 an, alerte médecin optionnelle |
| Lésion haut grade | 🔴 Rouge | Toute confiance | Envoi validation médecin OBLIGATOIRE |
| Indéterminé | ⚪ Gris | < 70% | Redemander captures + envoi médecin |

#### 3.3.3 Validation par l'Agent

```
SECTION VALIDATION AGENT
══════════════════════════

Le résultat IA est-il cohérent avec votre observation clinique ?

○ OUI — Je confirme le résultat IA
○ NON — Je ne suis pas d'accord avec l'IA

[Si désaccord sélectionné]
────────────────────────
Votre évaluation clinique :
○ Normal
○ Lésion bas grade
○ Lésion haut grade
○ Inflammation / Cervicite
○ Autre : [Champ texte libre]

Motif du désaccord (obligatoire) :
┌─────────────────────────────────┐
│ [Saisie texte libre min. 20 car]│
└─────────────────────────────────┘

[ENREGISTRER ET ENVOYER EN VALIDATION]
```

**Règles de déclenchement de validation médecin obligatoire :**
1. Résultat IA = Haut Grade (quelle que soit la confiance)
2. Confiance IA < 75% (tous types)
3. Désaccord explicite agent/IA
4. Première grossesse en cours détectée lors de la saisie

---

### 3.4 Module 4 — Historique Patient & Comparaison

#### Vue Chronologique du Dossier

```
PATIENTE : AISSATA DIALLO — 45 ans
ID Patient : PAT-2022-0847
Statut VIH : Négatif  |  Parité : 4  |  Dernier dépistage : il y a 12 mois
─────────────────────────────────────────────────────────────────────────

📅 15 MARS 2024 — DÉPISTAGE #3
────────────────────────────────
   Réalisé par   : Infirmière Marie KONE
   Centre        : CSCOM Bamako Sud
   IA            : Normal (98% confiance) 🟢
   Agent         : Normal — Concordance IA ✅
   Médecin       : Non requis
   Prochain ctrl : Mars 2027
   [📷 Voir images] [📄 Télécharger rapport]

📅 15 MARS 2023 — DÉPISTAGE #2
────────────────────────────────
   Réalisé par   : Infirmière Marie KONE
   Centre        : CSCOM Bamako Sud
   IA            : Normal (95% confiance) 🟢
   Agent         : Normal — Concordance IA ✅
   Médecin       : Non requis
   [📷 Voir images] [📄 Télécharger rapport]

📅 15 MARS 2022 — DÉPISTAGE #1
────────────────────────────────
   Réalisé par   : Infirmière Fatou TRAORE
   Centre        : CSCOM Bamako Sud
   IA            : Lésion bas grade (87% confiance) 🟡
   Agent         : Bas grade — Concordance IA ✅
   Médecin       : Dr. TOURE — Validé le 16/03/2022
   Commentaire   : "Surveillance renforcée à 1 an recommandée"
   [📷 Voir images] [📄 Télécharger rapport]
```

#### Fonctionnalité de Comparaison d'Images

- **Vue côte à côte** : Deux dépistages sélectionnables via dropdown
- **Zoom synchronisé** : Le zoom sur une image s'applique à l'autre
- **Overlay heatmap** : Superposition des zones IA activables/désactivables
- **Annotations médecin** : Affichage des annotations laissées par le médecin validateur
- **Export PDF** : Rapport de comparaison exportable en un clic

---

### 3.5 Module 5 — Validation Médecin

#### File d'Attente & Priorisation

```
╔══════════════════════════════════════════════════════════╗
║  BONJOUR DR. TOURE — CAS EN ATTENTE DE VALIDATION        ║
║  7 cas total  |  3 prioritaires  |  4 standard           ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  🔴 PRIORITAIRES (en attente > 6h ou haut grade)         ║
║  ───────────────────────────────────────────────         ║
║                                                          ║
║  ┌────────────────────────────────────────────────┐      ║
║  │ AISSATA DIALLO — 45 ans   │ ⏱ En attente 14h  │      ║
║  │ Centre : CSCOM Bamako Sud │ Agent : M. KONE     │      ║
║  │ Date : 15/03/2024 14:32   │                    │      ║
║  │                                                │      ║
║  │ IA : 🔴 Haut Grade — Confiance 72%             │      ║
║  │ Agent : "Aspect douteux, lésion possible"      │      ║
║  │ Désaccord : NON  |  3 images disponibles       │      ║
║  │                                                │      ║
║  │  [📷 VOIR IMAGES]  [✅ VALIDER]  [✏️ CORRIGER] │      ║
║  └────────────────────────────────────────────────┘      ║
║                                                          ║
║  🟡 STANDARD                                             ║
║  ───────────                                             ║
║  FATOU SOW — 52 ans                                      ║
║  IA : Bas Grade (88%) | Agent : Bas Grade ✅             ║
║  [Voir] [Valider] [Corriger]                             ║
╚══════════════════════════════════════════════════════════╝
```

#### Actions du Médecin Validateur

**Option A — Validation du diagnostic IA**
- Confirme le résultat IA sans modification
- Peut ajouter un commentaire clinique (optionnel)
- La patiente reçoit un email/SMS de résultat (si email renseigné)

**Option B — Correction du diagnostic**
- Sélection du nouveau diagnostic corrigé
- Commentaire clinique obligatoire (min. 30 caractères)
- Nouvelle recommandation clinique générée
- Notification à l'agent de terrain avec le motif de correction

**Option C — Demande de nouvel examen**
- Raison sélectionnée : Qualité image insuffisante / Aspect atypique / Période incorrecte du cycle
- L'agent reçoit un email de relance avec instructions
- Délai maximum pour le nouvel examen : 7 jours (alerte si dépassé)

**Option D — Orientation spécialisée**
- Génère automatiquement une lettre de référence PDF
- Incluant : résultats IA, images annotées, historique, commentaire médecin
- Envoyée par email à l'agent pour remise à la patiente

---

### 3.6 Module 6 — Tableau de Bord

#### Vue Infirmier / Sage-femme

```
╔═══════════════════════════════════════════════════════╗
║  BONJOUR MARIE KONE — CSCOM BAMAKO SUD                ║
║  Mercredi 15 Mars 2024 — 09:45                        ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  📊 MON ACTIVITÉ DU JOUR                              ║
║  ──────────────────────                               ║
║  Dépistages réalisés  : 4 / 8 (objectif journalier)  ║
║  En attente validation: 2 cas                         ║
║  Rendez-vous prévus   : 3 cet après-midi             ║
║                                                       ║
╠═══════════════════════════════════════════════════════╣
║  📋 DERNIERS DÉPISTAGES                               ║
║  ──────────────────────                               ║
║  09:30  Fatou SOW        — Normal ✅                   ║
║  10:15  Awa KEITA        — Bas grade 🟡 En validation ║
║  11:00  Mariam DIALLO    — Normal ✅                   ║
║  11:45  Kadiatou BALDE   — Haut grade 🔴 Urgent       ║
║                                                       ║
╠═══════════════════════════════════════════════════════╣
║  📅 RAPPELS PATIENTES (Contrôles à planifier)         ║
║  ────────────────────────────────────────────         ║
║  🔴 URGENT — 3 patientes : contrôle dépassé > 1 mois ║
║  🟡 CETTE SEMAINE — 5 patientes à contacter           ║
║  🟢 CE MOIS — 12 patientes à planifier                ║
║                                                       ║
║  [📤 Envoyer rappels email] [📋 Voir liste complète]  ║
╚═══════════════════════════════════════════════════════╝
```

#### Vue Médecin

```
╔═══════════════════════════════════════════════════════╗
║  BONJOUR DR. TOURE — DISTRICT BAMAKO                  ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  📊 INDICATEURS SEMAINE (9—15 Mars 2024)              ║
║  ──────────────────────────────────────               ║
║  Total dépistages        : 124                        ║
║  Taux anormaux           : 8.3%  ▲ +1.2% vs mois préc║
║  En attente validation   : 7 cas                      ║
║  Temps moyen validation  : 4.2h                       ║
║  Concordance IA / agents : 89%                        ║
║                                                       ║
╠═══════════════════════════════════════════════════════╣
║  📈 RÉPARTITION DIAGNOSTICS (semaine)                 ║
║  ─────────────────────────────────                    ║
║  Normal            : 82% ████████████████░░░░         ║
║  Lésion bas grade  : 12% ████░░░░░░░░░░░░░░░░         ║
║  Lésion haut grade :  6% ██░░░░░░░░░░░░░░░░░░         ║
║                                                       ║
╠═══════════════════════════════════════════════════════╣
║  ⚠️  ALERTES                                          ║
║  ──────────                                           ║
║  🔴 3 cas en attente validation depuis > 24h          ║
║  🟡 CSCOM Nord : taux anomalie 14% (seuil : 10%)      ║
║  🟡 Agent Diallo : 3 désaccords avec IA cette semaine ║
╚═══════════════════════════════════════════════════════╝
```

#### Vue Superviseur de District

```
╔═══════════════════════════════════════════════════════╗
║  TABLEAU DE BORD DISTRICT — SUPERVISEUR M. COULIBALY  ║
║  Mars 2024 — 12 centres actifs sur 15                 ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  PERFORMANCES DISTRICT                                ║
║  ─────────────────────                               ║
║  Objectif mensuel dépistages : 450 / 500 (90%)        ║
║  Taux couverture population cible : 23%               ║
║  Patientes perdues de vue       : 47 (10.4%)          ║
║                                                       ║
║  TOP CENTRES ACTIFS                                   ║
║  ────────────────────                                 ║
║  1. CSCOM Bamako Sud   : 89 dépistages ✅              ║
║  2. CSCOM Kati         : 74 dépistages ✅              ║
║  3. CSCOM Koulikoro    : 61 dépistages 🟡              ║
║                                                       ║
║  CENTRES INACTIFS (> 7 jours)                         ║
║  ─────────────────────────                            ║
║  ⚠️  CSCOM Dioïla  — Dernier dépistage : 01/03/2024   ║
║  ⚠️  CSCOM Nara    — Jamais utilisé                   ║
║                                                       ║
║  [📊 Rapport Groq complet] [📤 Export OMS] [📧 Email] ║
╚═══════════════════════════════════════════════════════╝
```

---

### 3.7 Module 7 — Système de Rapports Intelligents (Groq)

#### 3.7.1 Architecture Groq dans l'Application

CerviScan IA utilise l'API Groq avec le modèle **LLaMA 3.1 70B** pour générer des rapports de santé publique en langage naturel, personnalisés selon le profil et le rôle de l'utilisateur. Groq est utilisé pour trois fonctions principales :

1. **Génération des rapports journaliers / hebdomadaires / mensuels** en prose lisible
2. **Rédaction automatique des emails de notification** personnalisés pour les patientes
3. **Analyse des tendances** et génération d'alertes intelligentes

#### 3.7.2 Rapport Journalier Automatique (Agent de terrain)

**Déclenchement :** Chaque jour à 18h00 (heure locale), envoyé par email à l'agent

**Données transmises à Groq (prompt) :**
```json
{
  "role": "system",
  "content": "Tu es un assistant de santé publique. Tu génères un rapport journalier synthétique pour une infirmière travaillant dans un centre de santé en Afrique subsaharienne. Le rapport doit être concis, professionnel, encourageant et en français. Tu dois mentionner les chiffres clés, les cas nécessitant un suivi, et terminer par un message de motivation."
}
{
  "role": "user",
  "content": {
    "agent_name": "Marie KONE",
    "centre": "CSCOM Bamako Sud",
    "date": "2024-03-15",
    "stats": {
      "depistages_realises": 8,
      "objectif": 8,
      "normaux": 6,
      "bas_grade": 1,
      "haut_grade": 1,
      "en_attente_validation": 1,
      "concordance_ia": 0.88
    },
    "cas_urgents": ["AISSATA DIALLO - haut grade - envoyé en validation"],
    "rendez_vous_demain": 5,
    "patientes_a_rappeler": 3
  }
}
```

**Exemple d'output Groq généré (corps du rapport email) :**
```
RAPPORT JOURNALIER — CSCOM BAMAKO SUD
15 Mars 2024 — Infirmière Marie KONE

Bonsoir Marie,

Voici le résumé de votre journée du 15 mars 2024.

ACTIVITÉ DU JOUR
Vous avez atteint votre objectif journalier avec 8 dépistages réalisés.
Répartition des résultats : 6 cas normaux, 1 lésion de bas grade et
1 cas suspect de haut grade ayant été transmis en validation urgente
au Dr. TOURE.

CAS NÉCESSITANT UN SUIVI
→ Aissata DIALLO (45 ans) : Haut grade suspecté — En attente validation
  médicale. Assurez-vous que la patiente est joignable pour la suite.

POUR DEMAIN
Vous avez 5 rendez-vous planifiés et 3 patientes à relancer pour leur
contrôle périodique.

PERFORMANCE QUALITÉ
Votre taux de concordance avec l'IA ce jour est de 88%, ce qui est
conforme aux standards attendus. Continuez ce bon travail.

Bonne soirée et à demain,
L'équipe CerviScan IA
```

#### 3.7.3 Rapport Hebdomadaire (Médecin)

**Déclenchement :** Chaque lundi matin à 07h00, envoyé par email au médecin

**Contenu généré par Groq :**
- Synthèse de l'activité des 7 derniers jours dans son périmètre
- Analyse des tendances (hausse/baisse des anomalies)
- Identification des agents nécessitant une formation complémentaire (faible concordance IA)
- Recommandations cliniques personnalisées
- Récapitulatif des cas validés et de leurs délais

#### 3.7.4 Rapport Mensuel OMS (Superviseur)

**Déclenchement :** Le 1er de chaque mois à 06h00

**Structure du rapport généré :**

```
RAPPORT MENSUEL — FORMAT OMS/IARC
District de Bamako — Février 2024
Généré automatiquement par CerviScan IA (Groq LLaMA 3.1)

1. COUVERTURE DU DÉPISTAGE
   ─────────────────────────
   Population cible (femmes 25-65 ans)   : ~12,400
   Dépistages réalisés ce mois           : 450
   Taux de couverture mensuel            : 3.6%
   Cumul annuel (Jan–Fév 2024)           : 7.1%

2. RÉSULTATS CLINIQUES
   ────────────────────
   Normaux                               : 387 (86.0%)
   Lésions bas grade (LSIL/CIN1)         : 45 (10.0%)
   Lésions haut grade (HSIL/CIN2-3)      : 18 (4.0%)
   Indéterminés / Qualité insuffisante   : 0 (0.0%)

3. PERFORMANCE IA & CONCORDANCE
   ────────────────────────────
   Taux validation IA sans correction    : 94.2%
   Concordance IA / Agents terrain       : 89.1%
   Cas corrigés par médecin              : 6 (1.3%)

4. ANALYSE DES TENDANCES
   ──────────────────────
   Groq identifie une hausse de 1.8 point du taux de lésions
   haut grade vs. le mois précédent, principalement concentrée
   dans les tranches d'âge 40-50 ans au CSCOM Kati. Une investigation
   épidémiologique locale est recommandée.

5. PERDUES DE VUE & SUIVI
   ─────────────────────
   Patientes attendues pour contrôle     : 67
   Revenues au contrôle                  : 44 (65.7%)
   Perdues de vue (> 2 semaines retard)  : 23 (34.3%)
   → 23 emails/SMS de rappel envoyés automatiquement

6. RECOMMANDATIONS (générées par Groq)
   ─────────────────────────────────────
   → Renforcer la sensibilisation dans les villages de Kati
   → Former à nouveau les 2 agents avec concordance IA < 80%
   → Résoudre la connectivité du CSCOM Dioïla (inactif 14 jours)
```

#### 3.7.5 Rapport d'Alerte en Temps Réel

Groq est interrogé **immédiatement** dans les situations suivantes pour générer un message d'alerte personnalisé :

| Déclencheur | Destinataire | Contenu généré |
|-------------|-------------|----------------|
| Haut grade détecté par IA | Médecin | Résumé clinique urgent + données patiente |
| 3 désaccords IA/agent consécutifs | Superviseur | Analyse du pattern + recommandation formation |
| Centre inactif > 5 jours | Superviseur + Admin | Rapport d'inactivité avec suggestions |
| Taux anomalie centre > 10% | Médecin district | Alerte épidémiologique avec contexte |
| Patiente perdue de vue > 3 mois | Agent référent | Email de relance personnalisé pour la patiente |

---

### 3.8 Module 8 — Système de Notifications & Emails

#### 3.8.1 Architecture Email

**Stack technique :**
- **Fournisseur SMTP** : SendGrid (ou Mailgun en fallback)
- **Templating** : MJML (templates email responsive)
- **File d'attente** : Celery + Redis (envoi asynchrone)
- **Contenu** : Généré par Groq pour les emails complexes / template statique pour les emails transactionnels

**Langues supportées :** Français (v1), Bambara (v2), Wolof (v2)

#### 3.8.2 Catalogue Complet des Emails Envoyés

---

**EMAIL 1 — BIENVENUE NOUVEL AGENT**
- **À :** Nouveau compte créé
- **Quand :** Immédiatement après création du compte par l'admin
- **Objet :** `Bienvenue sur CerviScan IA — Vos accès sont prêts`
- **Contenu :**
  - Message de bienvenue personnalisé
  - Identifiants de connexion (lien de définition du mot de passe)
  - Lien vers tutoriel vidéo de prise en main
  - Contact support technique
  - Charte de confidentialité à signer numériquement

---

**EMAIL 2 — RÉINITIALISATION MOT DE PASSE**
- **À :** Agent ayant demandé la réinitialisation
- **Quand :** Dès la demande soumise
- **Objet :** `CerviScan IA — Réinitialisez votre mot de passe`
- **Contenu :**
  - Lien de réinitialisation sécurisé (valide 1h)
  - Avertissement : si non demandé, contacter l'admin
  - Bouton CTA unique et visible

---

**EMAIL 3 — RAPPORT JOURNALIER AGENT**
- **À :** Infirmier/Sage-femme actif ce jour
- **Quand :** Chaque soir à 18h00 (automatique)
- **Objet :** `📊 Votre rapport du [DATE] — [X] dépistages réalisés`
- **Contenu généré par Groq :**
  - Bilan de la journée en prose
  - Cas urgents à surveiller
  - Rappel des rendez-vous du lendemain
  - Message de motivation personnalisé

---

**EMAIL 4 — ALERTE CAS URGENT (MÉDECIN)**
- **À :** Médecin référent du centre
- **Quand :** Immédiatement après détection haut grade ou désaccord critique
- **Objet :** `🔴 [URGENT] Cas à valider — [NOM PATIENTE] — [CENTRE]`
- **Contenu :**
  - Identité de la patiente (anonymisée selon config)
  - Résultat IA avec score de confiance
  - Évaluation de l'agent
  - Lien direct vers l'interface de validation
  - Images en pièce jointe (si taille < 5Mo)
  - Délai maximum de réponse : 24h (rappel automatique si non traité)

---

**EMAIL 5 — RAPPEL DE VALIDATION NON TRAITÉE**
- **À :** Médecin
- **Quand :** 12h après l'envoi initial non traité, puis à 24h
- **Objet :** `⏰ Rappel : Cas en attente depuis [X]h — [NOM PATIENTE]`
- **Contenu :**
  - Récapitulatif du cas
  - Escalade automatique au superviseur si > 48h sans réponse

---

**EMAIL 6 — NOTIFICATION RÉSULTAT À L'AGENT (APRÈS VALIDATION MÉDECIN)**
- **À :** Agent qui a réalisé le dépistage
- **Quand :** Dès que le médecin a validé le cas
- **Objet :** `✅ Validation reçue — [NOM PATIENTE] — [RÉSULTAT FINAL]`
- **Contenu :**
  - Résultat final validé par le médecin
  - Commentaire clinique du médecin
  - Si correction : explication du motif de correction
  - Recommandations pour la patiente
  - Actions à effectuer (orienter, planifier contrôle, etc.)

---

**EMAIL 7 — RAPPEL DE DÉPISTAGE À LA PATIENTE**
- **À :** Patiente (si email renseigné dans le dossier)
- **Quand :** J-30, J-7, J-1 avant la date prévue de contrôle
- **Objet :** `💊 Votre contrôle de santé approche — [NOM CENTRE]`
- **Contenu généré par Groq :**
  - Message personnalisé, chaleureux, encourageant
  - Date et lieu du prochain contrôle
  - Nom de l'infirmière référente
  - Informations pratiques (ne pas venir pendant les règles, etc.)
  - Numéro de contact du centre

**Exemple d'email généré par Groq pour une patiente :**
```
Chère Aissata,

Nous vous écrivons depuis le CSCOM Bamako Sud pour vous rappeler
que votre contrôle de suivi est prévu dans 7 jours, le mercredi
22 mars 2024.

Ce dépistage est important pour votre santé. Il ne dure que
quelques minutes et permet de s'assurer que tout va bien.

📍 Lieu    : CSCOM Bamako Sud
📅 Date    : 22 mars 2024
⏰ Horaire : Venez de préférence le matin (8h–12h)
👩‍⚕️ Agent  : Infirmière Marie KONE vous accueillera

IMPORTANT : Venez de préférence en dehors de vos règles.
Pas besoin de rendez-vous, vous êtes attendue.

Pour toute question : 76 XX XX XX

À très bientôt,
L'équipe de santé du CSCOM Bamako Sud
```

---

**EMAIL 8 — ALERTE PATIENTE PERDUE DE VUE (À L'AGENT)**
- **À :** Agent référent de la patiente
- **Quand :** 30 jours après la date prévue de contrôle non honorée
- **Objet :** `⚠️ [X] patientes perdues de vue — Relance requise`
- **Contenu généré par Groq :**
  - Liste des patientes à relancer
  - Pour chaque patiente : dernier résultat, date prévue, contacts disponibles
  - Modèle de message SMS à envoyer manuellement si pas d'email patiente
  - Protocole de recherche active (visite à domicile recommandée si haut grade)

---

**EMAIL 9 — RAPPORT HEBDOMADAIRE MÉDECIN**
- **À :** Médecin
- **Quand :** Chaque lundi à 07h00
- **Objet :** `📋 Rapport hebdomadaire — Semaine [X] — District [NOM]`
- **Contenu généré par Groq :**
  - Synthèse de l'activité des 7 derniers jours
  - Analyse des tendances et anomalies
  - Top 3 cas cliniques remarquables
  - Performance des agents
  - Recommandations pour la semaine

---

**EMAIL 10 — RAPPORT MENSUEL SUPERVISEUR**
- **À :** Superviseur de district
- **Quand :** 1er de chaque mois à 06h00
- **Objet :** `📊 Rapport mensuel [MOIS/ANNÉE] — District [NOM] — Format OMS`
- **Contenu :** Rapport complet OMS format PDF en pièce jointe (généré par Groq + moteur PDF)

---

**EMAIL 11 — LETTRE DE RÉFÉRENCE MÉDICALE**
- **À :** Agent référent de la patiente
- **Quand :** À la demande du médecin validateur
- **Objet :** `📄 Lettre de référence — [NOM PATIENTE] — À remettre à la patiente`
- **Contenu :**
  - PDF en pièce jointe : lettre de référence officielle avec en-tête
  - Images annotées par le médecin
  - Résumé du dossier (anonymisé selon destinataire)
  - Coordonnées du centre de référence

---

**EMAIL 12 — ALERTE SYSTÈME ADMIN**
- **À :** Administrateur système
- **Quand :** Erreurs critiques, quota API dépassé, panne détectée
- **Objet :** `🔧 [ALERTE SYSTÈME] [TYPE D'ERREUR] — CerviScan IA`
- **Contenu :**
  - Nature de l'erreur
  - Centre(s) affecté(s)
  - Données non synchronisées potentielles
  - Lien vers logs système

---

## 4. WORKFLOWS MÉTIER COMPLETS

### 4.1 Workflow 1 — Premier Dépistage d'une Nouvelle Patiente

```
[AGENT CONNECTÉ À L'APPLICATION]
           │
           ▼
┌─────────────────────────────────┐
│  CRÉATION DU DOSSIER PATIENT    │
│  • Saisie informations patient  │
│  • Recueil consentement         │
│  • Validation et enregistrement │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  CHECKLIST PRÉ-EXAMEN           │
│  □ Cycle menstruel favorable    │
│  □ Pas de grossesse en cours    │
│  □ Matériel disponible          │
│  □ Éclairage suffisant          │
└─────────────────────────────────┘
           │
      ┌────┴────┐
      │ VALIDE ?│
      └────┬────┘
           │ OUI
           ▼
┌─────────────────────────────────┐
│  APPLICATION ACIDE ACÉTIQUE     │
│  Chronomètre 60s lancé          │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  CAPTURE PHOTOGRAPHIQUE         │
│  • Guidage cadrage en temps réel│
│  • 3 à 6 photos prises          │
│  • Vérification qualité image   │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  ENVOI AU SERVEUR D'ANALYSE IA  │
│  • Upload chiffré TLS           │
│  • Pré-traitement OpenCV        │
│  • Inférence modèle ONNX        │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  AFFICHAGE RÉSULTATS IA         │
│  • Classification + confiance   │
│  • Heatmap de localisation      │
│  • Recommandation clinique      │
└─────────────────────────────────┘
           │
      ┌────┴──────────────┐
      │  RÉSULTAT HAUT    │  RÉSULTAT NORMAL
      │  GRADE OU         │  OU BAS GRADE
      │  CONFIANCE <75%   │  ≥ 85% CONFIANCE
      └────────┬──────────┘
               │                    │
               ▼                    ▼
 ┌──────────────────────┐  ┌──────────────────────────┐
 │  VALIDATION AGENT    │  │  VALIDATION AGENT         │
 │  Accord/Désaccord    │  │  Confirmation résultat IA │
 │  Commentaire requis  │  │  Commentaire optionnel    │
 └──────────┬───────────┘  └────────────┬─────────────┘
            │                           │
            ▼                           ▼
 ┌──────────────────────┐  ┌──────────────────────────┐
 │  ENVOI EN VALIDATION │  │  PLANIFICATION CONTRÔLE  │
 │  MÉDECIN OBLIGATOIRE │  │  • Normal: +3 ans         │
 │  + Email Dr. TOURE   │  │  • Bas grade: +1 an       │
 └──────────┬───────────┘  │  • Email rappel planifié  │
            │              └────────────┬─────────────┘
            ▼                           │
 ┌──────────────────────┐               ▼
 │  MÉDECIN VALIDE      │    ┌──────────────────────┐
 │  ou corrige          │    │  DÉPISTAGE ARCHIVÉ   │
 │  dans les 24h        │    │  Dossier mis à jour   │
 └──────────┬───────────┘    │  Rapport journalier  │
            │                │  Groq déclenché 18h  │
            ▼                └──────────────────────┘
 ┌──────────────────────┐
 │  NOTIFICATION AGENT  │
 │  Email résultat final│
 └──────────────────────┘
```

---

### 4.2 Workflow 2 — Contrôle Périodique (Patiente Existante)

```
[AGENT RECHERCHE LA PATIENTE]
           │
           ▼
┌─────────────────────────────────┐
│  CONSULTATION HISTORIQUE        │
│  • Dernier résultat IA          │
│  • Date et résultat précédents  │
│  • Évolution dans le temps      │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  MISE À JOUR DOSSIER            │
│  • Vérification données actuelles│
│  • Nouvelles grossesses ? VIH ? │
│  • Renouvellement consentement  │
└─────────────────────────────────┘
           │
           ▼
      [PROTOCOLE IDENTIQUE AU PREMIER DÉPISTAGE]
      [ÉTAPES CAPTURE → ANALYSE → VALIDATION]
           │
           ▼
┌─────────────────────────────────┐
│  COMPARAISON AUTOMATIQUE        │
│  Images N vs. N-1 côte à côte   │
│  Évolution zone d'intérêt       │
│  Signalement IA si dégradation  │
└─────────────────────────────────┘
           │
      ┌────┴───────────┐
      │  DÉGRADATION   │  STABLE / AMÉLIORÉ
      │  DÉTECTÉE ?    │
      └────────┬───────┘
               │ OUI             │ NON
               ▼                 ▼
  ┌────────────────────┐  ┌──────────────────┐
  │  ALERTE ESCALADE   │  │  CLÔTURE         │
  │  Envoi médecin     │  │  Nouveau contrôle│
  │  Rapport comparatif│  │  planifié        │
  └────────────────────┘  └──────────────────┘
```

---

### 4.3 Workflow 3 — Validation Médicale Complète

```
[NOTIFICATION EMAIL MÉDECIN REÇUE]
           │
           ▼
┌─────────────────────────────────────────┐
│  MÉDECIN OUVRE L'INTERFACE              │
│  File d'attente triée par priorité      │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  EXAMEN DU CAS                          │
│  • Images (zoom, heatmap overlay)       │
│  • Résultat IA + score confiance        │
│  • Commentaire agent terrain            │
│  • Historique de la patiente            │
│  • Antécédents pertinents               │
└─────────────────────────────────────────┘
           │
      ┌────┴────────────────────────────────┐
      │           DÉCISION MÉDECIN          │
      └──┬─────────────┬──────────────┬─────┘
         │             │              │
         ▼             ▼              ▼
  ┌──────────┐  ┌──────────────┐  ┌──────────────┐
  │ VALIDE   │  │  CORRIGE     │  │  REDEMANDE   │
  │ IA ✅    │  │  LE DIAG. ✏️│  │  EXAMEN 🔄   │
  └────┬─────┘  └──────┬───────┘  └──────┬───────┘
       │               │                  │
       ▼               ▼                  ▼
 Dossier      Nouveau diag.       Email agent
 archivé      enregistré          + instructions
 avec         + commentaire       + délai 7j
 validation   obligatoire         max
       │               │
       └───────┬────────┘
               │
               ▼
    ┌──────────────────────┐
    │  EMAIL NOTIFICATION  │
    │  AGENT DE TERRAIN    │
    │  Résultat + consignes│
    └──────────────────────┘
               │
               │ Si haut grade validé
               ▼
    ┌──────────────────────┐
    │  GÉNÉRATION LETTRE   │
    │  DE RÉFÉRENCE (PDF)  │
    │  + Email à l'agent   │
    └──────────────────────┘
```

---

### 4.4 Workflow 4 — Rappel & Suivi des Patientes Perdues de Vue

```
[TÂCHE AUTOMATIQUE — 06h00 chaque matin]
           │
           ▼
┌─────────────────────────────────────────┐
│  SCAN BDD : Patientes avec contrôle     │
│  prévu dans les 30 jours               │
│  OU dépassé de > 0 jours               │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  SEGMENTATION PAR URGENCE               │
│  • J-30 : Rappel préventif              │
│  • J-7  : Rappel rapproché              │
│  • J+1  : Première relance              │
│  • J+30 : Perdue de vue officielle      │
│  • J+90 : Alerte superviseur            │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  GÉNÉRATION DES MESSAGES PAR GROQ       │
│  • Personnalisation nom, centre, date   │
│  • Ton adapté à l'urgence du délai      │
│  • Langue selon préférence patiente     │
└─────────────────────────────────────────┘
           │
      ┌────┴──────────────────┐
      │  EMAIL disponible ?   │
      └──┬──────────────┬─────┘
         │ OUI          │ NON
         ▼              ▼
  Email envoyé    Notification
  à la patiente   push à l'agent
                  + modèle SMS
                  fourni
           │
           ▼
┌─────────────────────────────────────────┐
│  ENREGISTREMENT DANS L'AUDIT TRAIL      │
│  Date, canal, statut envoi, contenu     │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  RAPPORT PERDUE DE VUE (mensuel)        │
│  Groq analyse et génère recommandations │
│  Envoyé au superviseur district         │
└─────────────────────────────────────────┘
```

---

### 4.5 Workflow 5 — Génération & Envoi du Rapport Groq

```
[DÉCLENCHEUR : Heure programmée ou événement]
           │
           ▼
┌─────────────────────────────────────────┐
│  COLLECTE DES DONNÉES BDD               │
│  Requête SQL agrégée par période/scope  │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  CONSTRUCTION DU PROMPT GROQ            │
│  • System prompt (rôle + contexte)      │
│  • Data JSON injectée                   │
│  • Instructions de format               │
│  • Langue cible                         │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  APPEL API GROQ                         │
│  Modèle : llama-3.1-70b-versatile       │
│  Temperature : 0.4 (factuel)            │
│  Max tokens : 2048                      │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  POST-TRAITEMENT DU TEXTE               │
│  • Vérification cohérence des chiffres  │
│  • Remplacement variables dynamiques    │
│  • Formatage email HTML (MJML)          │
└─────────────────────────────────────────┘
           │
      ┌────┴──────────────────┐
      │  FORMAT REQUIS ?      │
      └──┬────────────────┬───┘
         │ Email seul      │ PDF requis
         ▼                 ▼
  Envoi SendGrid    Génération PDF
  direct            (pièce jointe)
                    + Envoi SendGrid
           │
           ▼
┌─────────────────────────────────────────┐
│  LOG ENVOI + ARCHIVAGE RAPPORT          │
│  Statut : envoyé / erreur / en attente  │
└─────────────────────────────────────────┘
```

---

## 5. INTÉGRATION GROQ — RAPPORTS & IA GÉNÉRATIVE

### 5.1 Configuration Groq

```python
# Configuration API Groq (backend Python FastAPI)

GROQ_CONFIG = {
    "api_key": os.getenv("GROQ_API_KEY"),
    "base_url": "https://api.groq.com/openai/v1",
    "model": "llama-3.1-70b-versatile",
    "fallback_model": "llama-3.1-8b-instant",  # Si quota dépassé
    "temperature": 0.4,                          # Factuel, peu créatif
    "max_tokens": 2048,
    "timeout": 30                                # Secondes
}
```

### 5.2 Catégories d'Utilisation de Groq

| Catégorie | Fréquence | Modèle | Tokens max | Langue |
|-----------|-----------|--------|-----------|--------|
| Rapport journalier agent | 1x/jour/agent | LLaMA 3.1 70B | 600 | FR |
| Rapport hebdomadaire médecin | 1x/semaine/médecin | LLaMA 3.1 70B | 1200 | FR |
| Rapport mensuel superviseur | 1x/mois/district | LLaMA 3.1 70B | 2048 | FR |
| Email rappel patiente | Selon calendrier | LLaMA 3.1 8B | 400 | FR/Local |
| Alerte urgente médecin | Selon événements | LLaMA 3.1 8B | 300 | FR |
| Analyse tendances perdue de vue | 1x/mois | LLaMA 3.1 70B | 1000 | FR |

### 5.3 Contrôle Qualité des Outputs Groq

Avant tout envoi d'un contenu généré par Groq, le système effectue les vérifications suivantes :

1. **Cohérence numérique** : Les chiffres cités par Groq sont comparés aux données source. Si écart > 5%, le rapport est régénéré.
2. **Présence des champs obligatoires** : Validation par schéma JSON avant templating email.
3. **Détection hallucinations** : Si Groq mentionne un nom de patiente non présent dans les données, l'email est bloqué et loggé.
4. **Fallback** : Si Groq échoue (timeout, quota), un email template statique est envoyé avec les données brutes.
5. **Archivage** : Chaque output Groq est stocké en base avec l'ID du rapport associé pour audit.

---

## 6. SYSTÈME D'EMAILS — CAS D'USAGE COMPLETS

### 6.1 Synthèse des 12 Emails de l'Application

| # | Nom Email | Déclencheur | Destinataire | Groq ? |
|---|-----------|------------|-------------|--------|
| 1 | Bienvenue Agent | Création compte | Nouvel agent | Non |
| 2 | Reset Mot de passe | Demande utilisateur | Agent | Non |
| 3 | Rapport Journalier | 18h00 chaque jour | Agent actif | ✅ OUI |
| 4 | Alerte Cas Urgent | Haut grade ou désaccord | Médecin | ✅ OUI |
| 5 | Rappel Validation Non Traitée | +12h et +24h | Médecin | Non |
| 6 | Résultat Validation | Validation médecin | Agent référent | Non |
| 7 | Rappel Dépistage Patiente | J-30, J-7, J-1 | Patiente | ✅ OUI |
| 8 | Perdue de Vue | J+30 après contrôle prévu | Agent + Patiente | ✅ OUI |
| 9 | Rapport Hebdomadaire | Chaque lundi 07h00 | Médecin | ✅ OUI |
| 10 | Rapport Mensuel OMS | 1er du mois 06h00 | Superviseur | ✅ OUI |
| 11 | Lettre de Référence | Décision médecin | Agent (pour patiente) | Non |
| 12 | Alerte Système | Erreur critique | Admin | Non |

### 6.2 Paramétrage des Notifications

Chaque utilisateur peut configurer dans ses préférences :

- **Heure de réception** du rapport journalier (défaut : 18h00)
- **Canal de rappel** : Email / Notification push / Les deux
- **Seuils d'alerte** personnalisés (ex : alerter si taux anomalie > 8%)
- **Langues** des emails générés
- **Fréquence des digests** (immédiat / quotidien / hebdomadaire)

---

## 7. MODÈLE DE DONNÉES

### 7.1 Schéma Entité-Relation Principal

```
USERS
──────
id (UUID)
email (unique)
password_hash
full_name
role (enum: nurse, doctor, supervisor, admin)
centre_id (FK → HEALTH_CENTRES)
is_active (bool)
last_login (timestamp)
created_at

HEALTH_CENTRES
───────────────
id (UUID)
name
district
region
country
coordinates (lat, lng)
is_active (bool)

PATIENTS
─────────
id (UUID)
full_name
date_of_birth
phone
email (nullable)
village
medical_history (text)
hiv_status (enum: positive, negative, unknown)
gravida (int)
parity (int)
last_menstrual_period (date)
consent_given (bool)
consent_date (timestamp)
consent_agent_id (FK → USERS)
created_by (FK → USERS)
centre_id (FK → HEALTH_CENTRES)
next_screening_date (date)
created_at

SCREENINGS
───────────
id (UUID)
patient_id (FK → PATIENTS)
agent_id (FK → USERS)
centre_id (FK → HEALTH_CENTRES)
screening_date (timestamp)
checklist_passed (bool)
images_count (int)

AI_RESULTS
───────────
id (UUID)
screening_id (FK → SCREENINGS)
result_type (enum: normal, low_grade, high_grade, indeterminate)
confidence_score (float 0-1)
type1_probability (float)
type2_probability (float)
type3_probability (float)
lesion_location (json: quadrant, surface_pct, oe_involved)
heatmap_url (string)
recommendation (text)
processing_time_ms (int)
model_version (string)
created_at

AGENT_VALIDATIONS
──────────────────
id (UUID)
screening_id (FK → SCREENINGS)
agent_id (FK → USERS)
agrees_with_ai (bool)
agent_diagnosis (enum)
agent_comment (text)
requires_doctor_validation (bool)
created_at

DOCTOR_VALIDATIONS
───────────────────
id (UUID)
screening_id (FK → SCREENINGS)
doctor_id (FK → USERS)
final_diagnosis (enum)
validated_ai (bool)
correction_reason (text nullable)
action (enum: validated, corrected, re_exam, refer)
referral_letter_url (string nullable)
created_at
response_time_hours (float)

IMAGES
───────
id (UUID)
screening_id (FK → SCREENINGS)
image_url (string)
image_order (int 1-6)
quality_score (float)
brightness_score (float)
sharpness_score (float)
is_deleted (bool)
created_at

NOTIFICATIONS
──────────────
id (UUID)
type (enum: email_1, email_2, ..., email_12)
recipient_id (FK → USERS nullable)
patient_id (FK → PATIENTS nullable)
status (enum: pending, sent, failed, bounced)
groq_generated (bool)
groq_prompt_hash (string nullable)
content_preview (text)
sent_at (timestamp nullable)
error_message (text nullable)
created_at

GROQ_REPORTS
─────────────
id (UUID)
report_type (enum: daily, weekly, monthly, alert, perdue_de_vue)
recipient_id (FK → USERS)
period_start (date)
period_end (date)
input_data (json)
output_text (text)
notification_id (FK → NOTIFICATIONS)
groq_model (string)
tokens_used (int)
generation_time_ms (int)
status (enum: success, fallback, failed)
created_at

AUDIT_LOGS
───────────
id (UUID)
user_id (FK → USERS)
action (string)
entity_type (string)
entity_id (UUID)
ip_address (string)
changes (json)
created_at
```

---

## 8. ARCHITECTURE TECHNIQUE

### 8.1 Stack Technologique Complète

#### Frontend

| Technologie | Version | Rôle |
|-------------|---------|------|
| React + TypeScript | 18.2+ | Framework UI principal |
| Vite | 5.0+ | Build tool + HMR |
| TailwindCSS | 3.4+ | Styling utility-first |
| React Query (TanStack) | 5.0+ | Cache serveur + synchronisation |
| Zustand | 4.4+ | State management global |
| React Router | 6.8+ | Routage SPA |
| Axios | 1.6+ | Client HTTP avec intercepteurs JWT |
| React Hook Form + Zod | 7.0+ / 3.22+ | Formulaires + validation schéma |
| Workbox | 7.0+ | Service Worker PWA + cache offline |

#### Backend

| Technologie | Version | Rôle |
|-------------|---------|------|
| Python FastAPI | 0.110+ | API REST asynchrone |
| SQLAlchemy 2.0 | 2.0+ | ORM PostgreSQL |
| Pydantic | 2.0+ | Validation données + schémas API |
| Alembic | 1.13+ | Migrations base de données |
| python-jose | 3.3+ | JWT authentification |
| passlib[bcrypt] | 1.7+ | Hashage mots de passe |
| Celery | 5.3+ | File de tâches asynchrones |
| Redis | 7.0+ | Broker Celery + cache sessions |
| python-groq | 0.5+ | SDK officiel API Groq |
| SendGrid Python | 6.11+ | Envoi emails transactionnels |
| MJML (via API) | - | Templates emails responsive |

#### IA & Vision

| Technologie | Version | Rôle |
|-------------|---------|------|
| ONNX Runtime | 1.17+ | Inférence modèle vision CPU/GPU |
| OpenCV-Python | 4.9+ | Prétraitement images, qualité |
| Pillow | 10.3+ | Manipulation images |
| NumPy | 1.26+ | Calculs matriciels |
| Groq Python SDK | 0.5+ | Génération texte rapports |

#### Infrastructure

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| Base de données | PostgreSQL 16 | Stockage principal |
| Cache | Redis 7 | Sessions, Celery broker |
| Stockage images | MinIO (S3-compatible) | Images cervicales chiffrées |
| Proxy | Nginx 1.25 | Reverse proxy, SSL, static |
| Conteneurisation | Docker + Compose | Déploiement unifié |
| Monitoring | Prometheus + Grafana | Métriques applicatives |
| Logs | Loki + Grafana | Agrégation logs centralisée |

### 8.2 Architecture en Couches

```
┌──────────────────────────────────────────────┐
│           CLIENT (PWA React)                  │
│  • Offline-first avec Service Worker         │
│  • IndexedDB pour cache local patientes      │
│  • Sync automatique dès reconnexion          │
└───────────────────┬──────────────────────────┘
                    │ HTTPS / TLS 1.3
                    ▼
┌──────────────────────────────────────────────┐
│              NGINX (Reverse Proxy)            │
│  • Terminaison SSL                           │
│  • Rate limiting                             │
│  • Fichiers statiques                        │
└───────────────────┬──────────────────────────┘
                    │
          ┌─────────┴──────────┐
          ▼                    ▼
┌──────────────────┐  ┌────────────────────────┐
│  FastAPI API     │  │  Celery Workers         │
│  • Auth JWT      │  │  • Envoi emails         │
│  • Patients CRUD │  │  • Rapports Groq         │
│  • Screenings    │  │  • Rappels automatiques │
│  • Validation    │  │  • Sync offline         │
└─────────┬────────┘  └────────────────────────┘
          │
    ┌─────┴─────────────────┐
    │                       │
    ▼                       ▼
┌──────────┐     ┌──────────────────────┐
│PostgreSQL│     │  Services Externes    │
│  (BDD)   │     │  • Groq API           │
└──────────┘     │  • SendGrid SMTP      │
                 │  • MinIO (images)     │
                 └──────────────────────┘
```

### 8.3 Mode Offline (PWA)

La gestion du mode hors-ligne est critique pour les zones à connectivité instable.

**Données cachées localement (IndexedDB) :**
- Liste des patientes de l'agent connecté (sync toutes les 4h si réseau)
- Formulaires vierges et listes de valeurs
- Derniers dépistages de chaque patiente (30 jours)

**Fonctionnalités disponibles sans réseau :**
- Consultation des dossiers patients synchronisés
- Saisie du dossier d'une nouvelle patiente (en attente de sync)
- Capture et stockage local des images (max 50 Mo en attente)
- Checklist et chronomètre pré-examen

**Fonctionnalités nécessitant le réseau :**
- Analyse IA des images (traitement serveur)
- Validation médecin
- Envoi des emails
- Génération des rapports Groq

**Comportement de resynchronisation :**
- Détection automatique du retour de connectivité
- Tentative d'upload des données en attente
- Notification à l'agent : "3 dépistages synchronisés avec succès"
- Résolution automatique des conflits de données

---

## 9. SPÉCIFICATIONS IA (MODÈLE VISION)

### 9.1 Modèle de Détection Cervicale

**Type de modèle :** CNN (Convolutional Neural Network) — Architecture EfficientNet-B4 fine-tunée

**Format de déploiement :** ONNX (Open Neural Network Exchange) pour compatibilité cross-plateforme

**Classes de sortie :**
```
Classe 0 : Normal / Inflammation bénigne
Classe 1 : Lésion bas grade (LSIL / CIN 1)
Classe 2 : Lésion haut grade (HSIL / CIN 2-3)
Classe 3 : Suspect carcinome invasif
Classe 4 : Indéterminé / Qualité image insuffisante
```

### 9.2 Pipeline de Traitement des Images

```
IMAGE BRUTE (JPEG/PNG, 12–48 MP)
           │
           ▼
┌─────────────────────────────────┐
│  CONTRÔLE QUALITÉ (OpenCV)      │
│  • Calcul netteté (Laplacien)   │
│  • Analyse luminosité (HSV)     │
│  • Détection flou de mouvement  │
│  • Score qualité 0–100          │
│  → Rejet si score < 60          │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  PRÉ-TRAITEMENT                 │
│  • Redimensionnement 384x384    │
│  • Normalisation [0, 1]         │
│  • Augmentation : flip H+V      │
│  • Correction balance blancs    │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  INFÉRENCE ONNX RUNTIME         │
│  • Input : tensor [1, 3, 384, 384]│
│  • Output : probabilités [5]    │
│  • Activation GradCAM           │
│    → Heatmap de localisation    │
└─────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  POST-TRAITEMENT                │
│  • Softmax sur les probabilités │
│  • Fusion heatmaps (3 images)   │
│  • Détermination quadrant/ZT    │
│  • Calcul surface concernée     │
│  • Génération résultat final    │
└─────────────────────────────────┘
```

### 9.3 Métriques de Performance du Modèle IA

| Métrique | Valeur cible | Valeur baseline |
|----------|-------------|-----------------|
| Sensibilité (haut grade) | ≥ 92% | 85% |
| Spécificité (haut grade) | ≥ 88% | 82% |
| AUC-ROC globale | ≥ 0.95 | 0.90 |
| Faux négatifs haut grade | ≤ 5% | 10% |
| Temps d'inférence (CPU) | ≤ 8 secondes | 12s |
| Temps d'inférence (GPU T4) | ≤ 2 secondes | 4s |

---

## 10. SÉCURITÉ & CONFORMITÉ

### 10.1 Sécurité des Données

**Chiffrement :**
- Transit : TLS 1.3 obligatoire
- Repos : AES-256 pour images et données personnelles sensibles
- Base de données : Chiffrement au niveau colonne pour données VIH et résultats
- Tokens JWT : Algorithme RS256 (asymétrique)

**Contrôle d'accès :**
- RBAC (Role-Based Access Control) granulaire
- Principe du moindre privilège : chaque rôle n'accède qu'à ses données
- Isolation des données par centre de santé
- Audit trail immuable de toutes les actions

**Sécurité des images médicales :**
- Stockage MinIO avec bucket policy privé
- URL présignées (expire après 15 minutes)
- Watermarking invisible des images téléchargées
- Interdiction d'indexation par les moteurs de recherche

### 10.2 Conformité Réglementaire

**RGPD / Loi Malienne sur la protection des données :**
- Consentement explicite recueilli avant toute saisie
- Droit à l'effacement implémenté (anonymisation irréversible, pas suppression physique)
- Droit d'accès : les patientes peuvent demander leurs données via l'agent
- Registre des traitements maintenu

**Normes médicales :**
- ISO 13485 (dispositifs médicaux — recommandé phase 2)
- Guidelines OMS pour le dépistage du cancer du col
- Le modèle IA est présenté comme outil d'aide, jamais de diagnostic final

**Sécurité applicative :**
- OWASP Top 10 adressé
- Tests de pénétration trimestriels
- Scan de vulnérabilités automatique (CI/CD pipeline)
- Rate limiting sur tous les endpoints d'authentification

### 10.3 Audit Trail

Chaque action sensible est journalisée avec :
- ID utilisateur + rôle
- Timestamp précis (UTC)
- Adresse IP
- Données avant/après modification
- ID session

Actions tracées : connexion/déconnexion, création/modification dossier patient, chaque dépistage réalisé, chaque validation médecin, chaque envoi email, chaque accès aux images médicales, export de données.

---

## 11. INTERFACES UTILISATEUR

### 11.1 Principes de Design

**Design System :**
- Couleurs primaires : Bleu médical `#1B6CA8`, Vert santé `#2ECC71`, Rouge urgent `#E74C3C`
- Typographie : Inter (lisibilité maximale sur petits écrans)
- Taille minimale des éléments interactifs : 44x44px (WCAG 2.1 AA)
- Contraste couleurs : ratio ≥ 4.5:1 pour tous les textes

**Responsive Design :**
- Mobile first (320px min)
- Breakpoints : 375px, 768px, 1024px, 1440px
- Interface optimisée pour utilisation en extérieur (luminosité élevée)

### 11.2 Pages & Écrans Principaux

| Écran | Rôle(s) | Description |
|-------|---------|-------------|
| Login | Tous | Authentification + récupération mdp |
| Dashboard | Tous | Vue personnalisée selon rôle |
| Liste Patientes | Agent, Médecin | Recherche + filtres |
| Dossier Patiente | Agent, Médecin | Fiche complète + historique |
| Nouveau Dépistage | Agent | Wizard en 4 étapes guidées |
| Résultats IA | Agent | Affichage résultat + validation |
| File Validation | Médecin | Cas en attente, triés par priorité |
| Comparaison Images | Agent, Médecin | Viewer côte à côte |
| Rapports | Médecin, Superviseur | Interface consultation + export |
| Administration | Admin | Gestion utilisateurs et centres |
| Profil | Tous | Paramètres personnels + notifications |

### 11.3 Mode Offline — Indicateurs UX

Quand le réseau est indisponible :
- **Bandeau orange** en haut de l'écran : "Mode hors ligne — Les analyses IA seront disponibles dès reconnexion"
- **Badge compteur** sur l'icône de sync : "3 dépistages en attente de synchronisation"
- Les champs qui nécessitent le réseau sont grisés avec info-bulle
- Le chronomètre et la capture fonctionnent normalement

---

## 12. PLAN DE TESTS & QUALITÉ

### 12.1 Niveaux de Tests

**Tests Unitaires (Backend)**
- Coverage cible : ≥ 80% des fonctions critiques
- Frameworks : pytest + pytest-asyncio
- Couverture obligatoire : logique IA, calculs de scores, règles de validation, génération prompts Groq

**Tests d'Intégration**
- Tests API endpoints (pytest + httpx)
- Tests d'intégration Groq (mocking API en CI, appels réels en staging)
- Tests pipeline email (SendGrid sandbox)

**Tests End-to-End (E2E)**
- Framework : Playwright
- Scénarios couverts : Workflow 1 complet, Workflow 3 (validation médecin), envoi email
- Exécution : à chaque déploiement en staging

**Tests de Performance**
- Temps de réponse API < 200ms (hors analyse IA)
- Temps d'analyse IA < 10s (CPU), < 3s (GPU)
- Charge simultanée : 50 agents actifs sans dégradation

**Tests Terrain (UAT)**
- Phase pilote : 3 CSCOM volontaires, 2 mois
- Métriques collectées : taux d'adoption, erreurs terrain, concordance IA
- Retour utilisateurs formalisé (questionnaire post-session)

### 12.2 Critères d'Acceptation

| Fonctionnalité | Critère | Mesure |
|---------------|---------|--------|
| Analyse IA | Résultat en < 10s | 95ème percentile |
| Authentification | Login en < 2s | Temps de réponse |
| Rapport Groq | Généré en < 45s | Temps total |
| Email envoyé | Délivré en < 5 min | Timestamp SendGrid |
| PWA offline | Données accessibles sans réseau | Test déconnexion |
| Concordance IA | ≥ 88% sans correction | Dataset de test |

---

## 13. DÉPLOIEMENT & INFRASTRUCTURE

### 13.1 Environnements

| Environnement | Usage | URL |
|--------------|-------|-----|
| Development | Dev local | localhost |
| Staging | Tests + UAT | staging.cerviscan.health |
| Production | Utilisateurs réels | app.cerviscan.health |

### 13.2 Docker Compose — Services

```yaml
services:
  frontend:      # React PWA (Nginx serve build)
  api:           # FastAPI (3 replicas en prod)
  worker:        # Celery workers (emails + Groq)
  beat:          # Celery beat (tâches planifiées)
  db:            # PostgreSQL 16
  redis:         # Redis 7 (Celery + cache)
  minio:         # Stockage images S3-compatible
  nginx:         # Reverse proxy + SSL
  prometheus:    # Métriques
  grafana:       # Dashboards monitoring
```

### 13.3 Variables d'Environnement Critiques

```bash
# Authentification
SECRET_KEY=<clé RS256 privée>
JWT_ACCESS_EXPIRE_MINUTES=15
JWT_REFRESH_EXPIRE_DAYS=7

# Base de données
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/cerviscan

# Groq
GROQ_API_KEY=<clé API Groq>
GROQ_MODEL_PRIMARY=llama-3.1-70b-versatile
GROQ_MODEL_FALLBACK=llama-3.1-8b-instant

# Email
SENDGRID_API_KEY=<clé SendGrid>
FROM_EMAIL=noreply@cerviscan.health
FROM_NAME=CerviScan IA

# Stockage
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=<access key>
MINIO_SECRET_KEY=<secret key>
MINIO_BUCKET_IMAGES=cerviscan-images

# IA
AI_MODEL_PATH=/models/cerviscan_v2.onnx
AI_CONFIDENCE_THRESHOLD=0.75
AI_HIGH_GRADE_ALWAYS_REFER=true

# Tâches planifiées (horaires UTC)
DAILY_REPORT_HOUR=17          # 18h heure locale Mali
WEEKLY_REPORT_DAY=0           # Lundi
MONTHLY_REPORT_DAY=1
REMINDER_J30_ENABLED=true
REMINDER_J7_ENABLED=true
REMINDER_J1_ENABLED=true
```

### 13.4 Plan de Sauvegarde & Reprise

- **Backup BDD** : Snapshot PostgreSQL toutes les 6h, rétention 30 jours
- **Backup images** : Réplication MinIO cross-région (si infrastructure disponible), rétention 5 ans
- **RTO (Recovery Time Objective)** : < 4 heures
- **RPO (Recovery Point Objective)** : < 6 heures (dernier backup)
- **Plan de reprise** : Documentation de procédure de restauration testée trimestriellement

---

## ANNEXE A — GLOSSAIRE

| Terme | Définition |
|-------|-----------|
| IVA | Inspection Visuelle à l'Acide acétique — méthode de dépistage cervical adaptée aux ressources limitées |
| CIN 1/2/3 | Néoplasie Cervicale Intraépithéliale de grade 1, 2 ou 3 — classification histologique des lésions |
| LSIL | Low-Grade Squamous Intraepithelial Lesion — lésion de bas grade |
| HSIL | High-Grade Squamous Intraepithelial Lesion — lésion de haut grade |
| ZT | Zone de Transformation — zone anatomique du col à haut risque de lésions |
| OE | Orifice Externe — ouverture du canal cervical |
| CSCOM | Centre de Santé Communautaire — structure de soins de premier niveau |
| Perdue de vue | Patiente n'ayant pas honoré son rendez-vous de contrôle |
| Concordance IA | Taux d'accord entre le diagnostic IA et la validation finale de l'agent ou du médecin |
| GradCAM | Gradient-weighted Class Activation Mapping — technique de visualisation de l'attention du modèle IA |
| ONNX | Open Neural Network Exchange — format standard pour modèles de machine learning |
| Groq | Plateforme d'inférence IA ultra-rapide basée sur LPU (Language Processing Unit) |
| LLaMA 3.1 | Modèle de langage de Meta AI, hébergé et optimisé sur Groq |
| MJML | Framework de templating pour emails HTML responsive |
| PWA | Progressive Web App — application web installable avec fonctionnalités natives |

---

## ANNEXE B — MATRICE RISQUES

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|-----------|
| Faux négatifs IA (lésion non détectée) | Faible | Critique | Double validation agent + médecin obligatoire haut grade |
| Panne Groq API | Moyenne | Moyen | Fallback template statique, alertes admin |
| Perte de connectivité terrain | Élevée | Moyen | Mode offline complet, sync différé |
| Fuite données médicales | Faible | Critique | Chiffrement bout-en-bout, audit trail, accès role-based |
| Images de mauvaise qualité | Élevée | Moyen | Contrôle qualité automatique + guidage UX temps réel |
| Non-adoption des agents | Moyenne | Élevé | Formation in-situ, UI simplifiée, support réactif |
| Épuisement quota email SendGrid | Faible | Moyen | Monitoring quotas, alertes à 80%, fournisseur backup |

---

*Document rédigé par l'équipe projet CerviScan IA — Version 2.0 — Mars 2024*  
*Ce document est confidentiel et ne peut être partagé sans autorisation explicite.*
