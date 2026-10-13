"""Intermediate representation — every diagram type compiles to this."""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class DiagramKind(str, Enum):
    FLOWCHART = "flowchart"
    SEQUENCE = "sequence"
    ERD = "erd"
    GANTT = "gantt"
    MINDMAP = "mindmap"
    NETWORK = "network"
    UNKNOWN = "unknown"


class Node(BaseModel):
    id: str = Field(min_length=1, max_length=64)
    label: str = Field(min_length=1, max_length=256)
    kind: Literal["process", "decision", "actor", "entity", "milestone", "host", "concept"] = "process"
    attrs: dict[str, str] = Field(default_factory=dict)

    @field_validator("id")
    @classmethod
    def _id_safe(cls, v: str) -> str:
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError(f"node id must be alnum/dash/underscore: {v!r}")
        return v


class Edge(BaseModel):
    src: str
    dst: str
    label: str | None = Field(default=None, max_length=128)
    style: Literal["solid", "dashed", "dotted"] = "solid"


class DiagramIR(BaseModel):
    kind: DiagramKind
    title: str = Field(default="Untitled", max_length=200)
    nodes: list[Node] = Field(default_factory=list)
    edges: list[Edge] = Field(default_factory=list)
    meta: dict[str, str] = Field(default_factory=dict)

    @property
    def node_ids(self) -> set[str]:
        return {n.id for n in self.nodes}

    def validate_references(self) -> list[str]:
        """Return edges whose src/dst don't exist. Empty list == clean."""
        ids = self.node_ids
        return [f"{e.src}->{e.dst}" for e in self.edges if e.src not in ids or e.dst not in ids]