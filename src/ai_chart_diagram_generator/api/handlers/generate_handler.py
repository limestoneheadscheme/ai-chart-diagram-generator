"""Handler: prompt -> IR -> rendered file. Delegates everything."""

from __future__ import annotations

import time
from pathlib import Path

from ai_chart_diagram_generator.bootstrap.app import AppContext
from ai_chart_diagram_generator.models.requests import GenerateResponse
from ai_chart_diagram_generator.utils.logging import get_logger

_log = get_logger(__name__)


def handle_generate(
    ctx: AppContext,
    *,
    prompt: str,
    diagram_type: str = "auto",
    out_path: Path | None = None,
    dump_ir: bool = False,
) -> GenerateResponse:
    t0 = time.perf_counter()
    try:
        ir = ctx.planner.plan(prompt=prompt, requested_type=diagram_type)
        if (bad := ir.validate_references()) and not ctx.settings.model_backend == "none":
            _log.warning("IR has dangling edges: %s", bad)
        rendered = ctx.renderer.render(ir, out_path or ctx.settings.export_root / "out.svg")
        if dump_ir:
            _log.info("IR dump: %s", ir.model_dump_json(indent=2))
        return GenerateResponse(
            ok=True,
            ir=ir,
            rendered_path=rendered,
            elapsed_ms=(time.perf_counter() - t0) * 1000,
        )
    except Exception as exc:  # noqa: BLE001 — handler boundary
        _log.exception("generate failed")
        return GenerateResponse(ok=False, error=str(exc), elapsed_ms=(time.perf_counter() - t0) * 1000)