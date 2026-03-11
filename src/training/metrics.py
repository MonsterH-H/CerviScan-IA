"""Calcul des métriques de performance pour la classification."""

from __future__ import annotations

from typing import Dict
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix


def classification_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """Calcule l'exactitude et le F1-score macro."""
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "f1_macro": float(f1_score(y_true, y_pred, average="macro")),
    }


def confusion(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """Calcule la matrice de confusion (Règle 11)."""
    return confusion_matrix(y_true, y_pred)
