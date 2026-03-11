"""CLI entry for export to ONNX."""

from __future__ import annotations

import argparse
from pathlib import Path

import torch

from ml.src.models.efficientnet import build_model
from ml.src.utils.config import load_and_merge


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", action="append", default=[], help="Path to a config yaml")
    parser.add_argument("--checkpoint", required=True, help="Path to model checkpoint")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parents[2]

    if args.config:
        cfg_paths = args.config
    else:
        cfg_paths = [
            str(base_dir / "configs" / "base.yaml"),
            str(base_dir / "configs" / "data.yaml"),
            str(base_dir / "configs" / "train.yaml"),
        ]

    cfg = load_and_merge(cfg_paths)
    model = build_model(cfg)
    state = torch.load(args.checkpoint, map_location="cpu")
    model.load_state_dict(state)
    model.eval()

    input_size = cfg.get("model", {}).get("input_size", [3, 384, 384])
    dummy = torch.randn(1, input_size[0], input_size[1], input_size[2])

    if args.output is None:
        output_path = base_dir / "models" / "exported" / "model.onnx"
    else:
        out = Path(args.output)
        output_path = out if out.is_absolute() else (base_dir / out)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    torch.onnx.export(
        model,
        dummy,
        str(output_path),
        input_names=["input"],
        output_names=["logits"],
        opset_version=int(cfg.get("export", {}).get("opset", 17)),
    )


if __name__ == "__main__":
    main()
