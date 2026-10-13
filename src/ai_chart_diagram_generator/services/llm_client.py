"""LLM client — local GGUF (llama-cpp) or a stub when no model is set."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ai_chart_diagram_generator.config.settings import Settings
from ai_chart_diagram_generator.models.diagram_ir import DiagramKind
from ai_chart_diagram_generator.utils.prompts import build_prompt

if TYPE_CHECKING:
    from llama_cpp import Llama

_log = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._llm: Llama | None = None

    def _ensure(self) -> "Llama":
        if self._llm is not None:
            return self._llm
        if not self._settings.model_path:
            raise RuntimeError("ACDG_MODEL_PATH is unset and model_backend != 'none'")
        from llama_cpp import Llama  # heavy import, deferred

        _log.info("loading GGUF model from %s", self._settings.model_path)
        self._llm = Llama(
            model_path=self._settings.model_path,
            n_ctx=4096,
            n_threads=4,
            verbose=False,
        )
        return self._llm

    def complete(self, *, prompt: str, kind: DiagramKind) -> str:
        if self._settings.model_backend == "none":
            return _stub_response(kind)
        llm = self._ensure()
        out = llm(
            build_prompt(prompt, kind),
            max_tokens=1024,
            temperature=0.2,
            stop=["```", "\n\n\n"],
        )
        return out["choices"][0]["text"]


def _stub_response(kind: DiagramKind) -> str:
    return f"title: stub {kind.value}\nA -> B\nB -> C\n"
</｜｜DSML｜｜ parameter>
</｜｜DSML｜｜ invoke>
</｜｜DSML｜｜ calls>