"""Planner service — pick a grammar, run the LLM, compile to DiagramIR."""

from __future__ import annotations

import logging

from ai_chart_diagram_generator.config.settings import Settings
from ai_chart_diagram_generator.grammar.flowchart_grammar import parse_flowchart
from ai_chart_diagram_generator.grammar.sequence_grammar import parse_sequence
from ai_chart_diagram_generator.models.diagram_ir import DiagramIR, DiagramKind
from ai_chart_diagram_generator.services.llm_client import LLMClient

_log = logging.getLogger(__name__)

GRAMMAR_REGISTRY: dict[str, object] = {
    "flowchart": parse_flowchart,
    "sequence": parse_sequence,
}

_TYPE_KEYWORDS: dict[DiagramKind, tuple[str, ...]] = {
    DiagramKind.FLOWCHART: ("flow", "process", "steps", "decision", "workflow"),
    DiagramKind.SEQUENCE: ("sequence", "interaction", "actor", "message", "call"),
    DiagramKind.ERD: ("schema", "table", "entity", "foreign key", "erd", "database"),
    DiagramKind.GANTT: ("gantt", "timeline", "milestone", "deadline", "sprint"),
    DiagramKind.MINDMAP: ("mind map", "brainstorm", "topic", "ideas"),
    DiagramKind.NETWORK: ("network", "topology", "subnet", "router", "host"),
}


class PlannerService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._llm = LLMClient(settings)

    def classify(self, prompt: str) -> DiagramKind:
        low = prompt.lower()
        best, best_score = DiagramKind.UNKNOWN, 0
        for kind, words in _TYPE_KEYWORDS.items():
            score = sum(1 for w in words if w in low)
            if score > best_score:
                best, best_score = kind, score
        return best

    def plan(self, *, prompt: str, requested_type: str = "auto") -> DiagramIR:
        kind = DiagramKind(requested_type) if requested_type != "auto" else self.classify(prompt)
        _log.debug("classified prompt as %s", kind)

        grammar = GRAMMAR_REGISTRY.get(kind.value)
        raw = self._llm.complete(prompt=prompt, kind=kind)
        if grammar is None:
            _log.warning("no grammar for %s; falling back to flowchart", kind)
            return parse_flowchart(raw)
        return grammar(raw)  # type: ignore[operator]