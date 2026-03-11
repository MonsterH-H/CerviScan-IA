"""Postprocessing: softmax, thresholds, quality gates."""

from __future__ import annotations

from typing import Dict

import numpy as np


def postprocess_logits(logits: np.ndarray) -> Dict[str, np.ndarray]:
    logits = logits - np.max(logits, axis=1, keepdims=True)
    probs = np.exp(logits)
    probs = probs / np.sum(probs, axis=1, keepdims=True)
    preds = np.argmax(probs, axis=1)
    return {"probs": probs, "preds": preds}
