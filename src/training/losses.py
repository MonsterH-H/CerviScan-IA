"""Définition des fonctions de perte (Loss)."""

from __future__ import annotations

from typing import Optional
import torch
import torch.nn as nn


def get_loss(name: str = "cross_entropy", class_weights: Optional[list[float]] = None) -> nn.Module:
    """
    Retourne la fonction de perte spécifiée.
    
    Args:
        name: Nom de la loss (par défaut: cross_entropy).
        class_weights: Poids pour gérer le déséquilibre de classes (Règle 13).
    """
    name = name.lower()
    if name == "cross_entropy":
        if class_weights is not None:
            weights = torch.tensor(class_weights, dtype=torch.float32)
        else:
            weights = None
        return nn.CrossEntropyLoss(weight=weights)
    
    raise ValueError(f"❌ Fonction de perte non supportée : {name}")
