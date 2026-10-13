"""Request/response envelopes used by the api layer."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from ai_chart_diagram_generator.models.diagram_ir import DiagramIR


class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=8000)
    diagram_type: str = "auto"
    out_path: Path | None = None
    dump_ir: bool = False


class GenerateResponse(BaseModel):
    ok: bool
    ir: DiagramIR | None = None
    rendered_path: Path | None = None
    error: str | None = None
    elapsed_ms: float = 0.0