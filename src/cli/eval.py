"""CLI entry for evaluation."""

from __future__ import annotations

import argparse
from pathlib import Path

from ml.src.training.trainer import evaluate
from ml.src.utils.config import load_and_merge


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", action="append", default=[], help="Path to a config yaml")
    parser.add_argument("--checkpoint", required=True, help="Path to model checkpoint")
    parser.add_argument("--split", choices=["val", "test"], default="val")
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
    evaluate(cfg, args.checkpoint, split=args.split)


if __name__ == "__main__":
    main()
