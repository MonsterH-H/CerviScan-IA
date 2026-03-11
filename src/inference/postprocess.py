"""Postprocessing: softmax, thresholds, quality gates.
Ce fichier gère la "traduction" des résultats bruts de l'Intelligence Artificielle.
C'est ici que l'on passe des "nombres mathématiques flous" (Logits)
à un Diagnostic final que les humains (Agents et Médecins) vont lire : La Classe 0, 1 ou 2.
"""

from __future__ import annotations

from typing import Dict

import numpy as np


def postprocess_logits(logits: np.ndarray) -> Dict[str, np.ndarray]:
    """Transforme les logits de l'IA en prédictions cliniques (Sain, Bas Grade, Haut Grade)."""
    
    # 1. Étape Mathématique (Stabilisation des "logits")
    # On évite que des calculs avec des nombres virtuels géants ne fassent crasher la PWA/Serveur.
    logits = logits - np.max(logits, axis=1, keepdims=True)
    
    # 2. Exponentielle
    probs = np.exp(logits)
    
    # 3. Softmax
    # Chaque prédiction (Type_1, Type_2, Type_3) devient un "Taux de Confiance" (Probabilité de 0 à 100%).
    # La somme totale de ces confiance fait exactement 100.
    probs = probs / np.sum(probs, axis=1, keepdims=True)
    
    # 4. LE DIAGNOSTIC FINAL (Prédiction - argmax).
    # L'algorithme regarde les colonnes [Type_1, Type_2, Type_3] et choisit l'indice qui a le % le plus haut. 
    # S'il y a: 11% Type_1, 5% Type_2, 84% Type_3...  la fonction retourne "2" (Index pour Type_3).
    preds = np.argmax(probs, axis=1)
    
    # 5. Retourne un dictionnaire contenant les pourcentages détaillés ET le mot final de l'IA.
    return {"probs": probs, "preds": preds}
