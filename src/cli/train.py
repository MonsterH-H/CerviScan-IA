"""CLI entry for training."""

from __future__ import annotations

import argparse
from pathlib import Path

from ml.src.training.trainer import train
from ml.src.utils.config import load_and_merge


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", action="append", default=[], help="Path to a config yaml")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parents[2]

    if args.config:
        cfg_paths = args.config
    else:
        cfg_paths = [
            str(base_dir / "configs" / "base.yaml"),
            str(base_dir / "configs" / "data.yaml"),
            str(base_dir / "configs" / "train.yaml"),
            str(base_dir / "configs" / "eval.yaml"),
        ]

    cfg = load_and_merge(cfg_paths)
    train(cfg)


if __name__ == "__main__":
    main()
