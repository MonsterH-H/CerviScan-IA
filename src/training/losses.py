"""Définition des fonctions de perte (Loss).
La 'Loss' (La Perte), c'est la jauge mathématique qui mesure à quel point
l'IA s'est trompée à chaque fois qu'elle regarde une image.
L'objectif unique de l'IA (et de l'Optimiseur AdamW) est de faire baisser ce chiffre (Loss) vers 0.
Plus la Perte est basse, plus l'IA est intelligente et a compris les cancers du col de l'utérus.
"""

from __future__ import annotations

from typing import Optional
import torch
import torch.nn as nn


def get_loss(name: str = "cross_entropy", class_weights: Optional[list[float]] = None) -> nn.Module:
    """
    Crée et renvoie la "Boussole de l'Erreur" (Fonction de Perte/Loss Function).
    
    Args:
        name: Typiquement la "Cross Entropy" (Entropie Croisée), qui sert 
              exclusivement à juger des IA de Multi-Classification (Où il faut choisir LA bonne case parmi 3).
        class_weights: Des bonus et malus de correction injectés par 'train.yaml'.
                       C'est LA Règle 13 (Gérer le déséquilibre). S'il y a très peu de maladies graves
                       (Type 3), le "poids" de l'erreur sur le Type 3 sera décuplé. C'est pénalisé X fois
                       plus que de se tromper sur une image Saine (Type 1 ou 2).
    """
    
    # On met le nom en minuscules pour comparer (par sécurité au cas où l'utilisateur ait écrit 'Cross_Entropy')
    name = name.lower()
    if name == "cross_entropy":
        # 1. On "pèse" la faute de l'IA selon son déséquilibre de classe au préalable ("balanced" !)
        if class_weights is not None:
            # PyTorch a besoin de manipuler une liste de nombres (ex: [2.5, 0.5, 1.2]) en format Tenseur 32-bits
            weights = torch.tensor(class_weights, dtype=torch.float32)
        else:
            weights = None
            
        # 2. On retourne l'Exécuteur de Sanction : Le fameux Module "CrossEntropyLoss()".
        # Qui s'occupe à la fois de regrouper un peu les Softmax calculés, et de distribuer l'injustice via ses "weights".
        return nn.CrossEntropyLoss(weight=weights)
    
    # 3. Arrêt de sécurité au cas où l'utilisateur se trompe de fonction dans la configuration yaml ("focal_loss")
    raise ValueError(f"❌ Fonction de perte non supportée (ou mal orthographiée) : {name}")
