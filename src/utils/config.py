"""Utilitaires pour le chargement et la fusion de fichiers de configuration YAML."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict
import yaml


def load_yaml(path: str | Path) -> Dict[str, Any]:
    """Charge un fichier YAML et retourne un dictionnaire."""
    p = Path(path)
    if not p.exists():
        return {}
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def _merge_dicts(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    """Fusionne récursivement deux dictionnaires de configuration."""
    out = dict(a)
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _merge_dicts(out[k], v)
        else:
            out[k] = v
    return out


def load_and_merge(paths: list[str | Path]) -> Dict[str, Any]:
    """Charge plusieurs fichiers YAML et les fusionne (le dernier l'emporte)."""
    cfg: Dict[str, Any] = {}
    for p in paths:
        cfg = _merge_dicts(cfg, load_yaml(p))
    return cfg
