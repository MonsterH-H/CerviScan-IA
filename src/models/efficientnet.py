"""Définition du modèle EfficientNet-B4 pour CerviScan."""

from __future__ import annotations

from typing import Any, Dict

import timm
import torch.nn as nn


def build_model(cfg: Dict[str, Any]) -> nn.Module:
    """
    Construit le modèle de classification basé sur EfficientNet.
    
    Args:
        cfg: Configuration contenant l'architecture, le nombre de classes, etc.
        
    Returns:
        Un modèle PyTorch prêt pour l'entraînement ou l'inférence.
    """
    # Récupération des paramètres depuis la configuration (Règle 15: Architecture éprouvée)
    arch = cfg.get("model", {}).get("architecture", "efficientnet_b4")
    num_classes = int(cfg.get("model", {}).get("num_classes", 3))
    pretrained = bool(cfg.get("model", {}).get("pretrained", True))

    # Chargement via timm
    # NB: timm gère automatiquement le remplacement de la dernière couche linéaire
    model = timm.create_model(
        arch, 
        pretrained=pretrained, 
        num_classes=num_classes
    )
    
    return model
