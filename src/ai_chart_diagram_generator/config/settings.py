"""Settings loader — TOML defaults layered with env overrides."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

_DEFAULT_CONFIG = Path(__file__).with_name("defaults.toml")


@dataclass(slots=True)
class Settings:
    version: str = "0.6.3"
    log_level: str = "INFO"
    export_root: Path = field(default_factory=lambda: Path.home() / "Documents" / "acdg")
    model_backend: str = "local-gguf"
    model_path: str | None = None
    llm_timeout_s: float = 30.0
    render_timeout_s: float = 2.0
    max_nodes: int = 512
    preferred_renderer: str = "cpp-shim"


def _env_override(key: str, default: str) -> str:
    return os.environ.get(f"ACDG_{key.upper()}", default)


def load_settings(config_path: Path | None = None) -> Settings:
    path = config_path or _DEFAULT_CONFIG
    raw: dict[str, object] = {}
    if path.exists():
        with path.open("rb") as fh:
            raw = tomllib.load(fh)

    s = Settings()
    if (v := raw.get("log_level")) is not None:
        s.log_level = str(v)
    if (v := raw.get("export_root")) is not None:
        s.export_root = Path(str(v)).expanduser()
    if (v := raw.get("model_backend")) is not None:
        s.model_backend = str(v)
    if (v := raw.get("model_path")) is not None:
        s.model_path = str(v)
    if (v := raw.get("llm_timeout_s")) is not None:
        s.llm_timeout_s = float(v)
    if (v := raw.get("render_timeout_s")) is not None:
        s.render_timeout_s = float(v)
    if (v := raw.get("max_nodes")) is not None:
        s.max_nodes = int(v)
    if (v := raw.get("preferred_renderer")) is not None:
        s.preferred_renderer = str(v)

    # env wins
    s.log_level = _env_override("log_level", s.log_level)
    if mp := os.environ.get("ACDG_MODEL_PATH"):
        s.model_path = mp
    s.export_root = Path(_env_override("export_root", str(s.export_root))).expanduser()
    return s