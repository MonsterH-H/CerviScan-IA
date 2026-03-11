"""Inference entry points for ONNX and Torch models.
Ce module est le cœur de la mise en production du modèle.
Il charge le fichier converti (.onnx) généré par cli/export.py et permet de faire
tourner l'intelligence artificielle pour obtenir un résultat final, à partir d'une image.
Pas besoin de PyTorch ici, juste la bibliothèque allégée 'onnxruntime'.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import numpy as np
import onnxruntime as ort


class OnnxPredictor:
    """Classe chargeant un modèle ONNX pour exécuter une prédiction."""
    
    def __init__(self, model_path: str | Path):
        # 1. Création de la Session d'Inférence ONNX.
        # onnxruntime est la librairie officielle de l'ONNX. Elle va lire le fichier .onnx et le préparer.
        # "CPUExecutionProvider" force le calcul sur le processeur (CPU) au lieu du GPU
        # car onnxruntime-cpu est beaucoup plus léger à intégrer dans un backend (la PWA).
        self.session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
        
        # 2. Récupération dynamique du nom d'entrée. 
        # (Dans cli/export.py on l'avait configuré à "input").
        self.input_name = self.session.get_inputs()[0].name

    def predict(self, batch: np.ndarray) -> np.ndarray:
        # 3. La Phase Magique de l'IA (Inférence).
        # On passe le tableau de pixels (l'image traitée) au modèle et l'équation retourne le résultat.
        # On envoie un batch (plusieurs images ou une seule avec [1, 3, 384, 384]).
        return self.session.run(None, {self.input_name: batch})[0]


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Fonction Softmax en version NumPy pure.
    Raison : L'ONNX retourne des logits (des nombres mathématiques de -infini à +infini).
    La fonction Softmax les transforme en probabilités de 0% à 100% dont la somme fait exactement 1.
    """
    
    # 4. Stabilisation numérique : on soustrait la plus grande valeur.
    # Empêche un bug très courant de dépassement de limite lors du calcul (Overflow).
    x = x - np.max(x, axis=axis, keepdims=True)
    
    # 5. Calcul des exponentielles puis division par le total, pour créer des poucentages.
    exp = np.exp(x)
    return exp / np.sum(exp, axis=axis, keepdims=True)
