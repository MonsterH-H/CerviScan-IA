"""Inference entry points for ONNX and Torch models."""

from __future__ import annotations

from pathlib import Path
from typing import List

import numpy as np
import onnxruntime as ort


class OnnxPredictor:
    def __init__(self, model_path: str | Path):
        self.session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name

    def predict(self, batch: np.ndarray) -> np.ndarray:
        return self.session.run(None, {self.input_name: batch})[0]


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - np.max(x, axis=axis, keepdims=True)
    exp = np.exp(x)
    return exp / np.sum(exp, axis=axis, keepdims=True)
