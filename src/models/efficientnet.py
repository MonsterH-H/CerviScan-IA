"""Définition du modèle EfficientNet-B4 pour CerviScan.
C'est le "Coeur de l'Intelligence Artificielle".
EfficientNet est une famille de modèles de vision par ordinateur (Computer Vision)
réputée dans le monde de la santé pour équilibrer parfaitement la Vitesse et la Précision.
La version 'B4' est excellente pour traiter nos images à la taille précise de 384x384.
"""

from __future__ import annotations

from typing import Any, Dict

import timm
import torch.nn as nn


def build_model(cfg: Dict[str, Any]) -> nn.Module:
    """
    Construit le modèle de classification basé sur l'architecture EfficientNet (B4).
    
    Args:
        cfg: Configuration YAML contenant l'architecture, le nb de classes, etc.
        
    Returns:
        Un objet "model" PyTorch tout neuf, prêt pour l'entraînement ou l'inférence.
    """
    
    # 1. Récupération des paramètres de l'IA depuis la 'Configuration Base/Data'.
    # Si le fichier config est absent, on force les bonnes valeurs par "défaut" (EfficientNet-B4, 3 Classes, Transfer Learning)
    # (Règle d'Or 15: utiliser une Architecture éprouvée dans le monde médical)
    arch = cfg.get("model", {}).get("architecture", "efficientnet_b4")
    num_classes = int(cfg.get("model", {}).get("num_classes", 3))
    pretrained = bool(cfg.get("model", {}).get("pretrained", True))

    # 2. Le Chargement Magique via "Timm" (PyTorch Image Models)
    # C'est LA librairie de l'état de l'art pour les réseaux de neurones complexes aujourd'hui.
    # NB: 'timm' gère automatiquement le remplacement de la toute dernière couche du cerveau
    # car l'IA de base est conçue pour 1000 classes (chiens, voitures...), et on la "bride" à 3 !
    model = timm.create_model(
        arch, 
        pretrained=pretrained, 
        num_classes=num_classes
    )
    
    return model
