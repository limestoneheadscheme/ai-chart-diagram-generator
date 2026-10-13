"""`acdg` entry point — one-shot prompt to diagram."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ai_chart_diagram_generator.api.handlers.generate_handler import handle_generate
from ai_chart_diagram_generator.bootstrap.app import build_app


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="acdg", description="AI chart / diagram generator")
    p.add_argument("prompt", help="natural-language prompt")
    p.add_argument("-t", "--type", default="auto", help="diagram type (auto, flowchart, erd, gantt, ...)")
    p.add_argument("-o", "--out", type=Path, default=Path("renders/out.svg"))
    p.add_argument("--dump-ir", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    ctx = build_app()
    result = handle_generate(
        ctx,
        prompt=args.prompt,
        diagram_type=args.type,
        out_path=args.out,
        dump_ir=args.dump_ir,
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())