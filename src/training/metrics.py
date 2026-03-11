"""Calcul des métriques de performance pour la classification.
Ici se trouve "Le Tableau des Scores".
C'est le Juge impartial qui nous dit : "Oui l'IA a bien travaillé !"
Ou "Non, l'IA s'est contentée de prédire au hasard "Sain" pour gonfler ses statistiques".
"""

from __future__ import annotations

from typing import Dict
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix


def classification_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calcule l'Exactitude et le fameux "F1-score macro".
    
    Args:
        y_true: La Vérité absolue (ce que les médecins experts ont dit que la patiente avait).
        y_pred: Ce que l'IA a deviné.
    """
    return {
        # 1. ACCURACY (Taux de Réussite Global)
        # Piège de Data Scientist : Donne le pourcentage brut de "Coup dans le mille".
        # Le problème, c'est que si 95% des gens sont sains (Type_1), l'IA peut juste toujours crier "Sain!" 
        # et avoir un super score de 95%... en ignorant totalement les Type_3 (Cancers). C'est pour ça qu'on s'en méfie.
        "accuracy": float(accuracy_score(y_true, y_pred)),
        
        # 2. F1 MACRO (L'Arbitre Ultime - Règle n°13)
        # F1 Score = Mixte entre "La précision" (j'ai raison quand j'annonce un cancer) 
        # et "Le Rappel" (j'ai pu trouvé 100% des cancers qui existaient dans l'hôpital).
        # "Macro" = Il calcule un F1 Score par Type, puis il fait la moyenne finale. Si le cancer (Type_3) est raté, la moyenne chute dramatiquement. 
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
    }


def confusion(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Crée une Matrice de Confusion (Règle 11).
    C'est un tableau croisé :
    "Parmi les 10 Cancers (Type_3) de l'hôpital, combien l'IA a pris pour un Type_1 ? Combien pour un Type_2 ?"
    C'est l'outil le plus puissant pour voir où l'IA hesite.
    """
    return confusion_matrix(y_true, y_pred)
