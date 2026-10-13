"""Application wiring — build the service graph once, hand it to handlers."""

from __future__ import annotations

import logging
from dataclasses import dataclass

from ai_chart_diagram_generator.adapters.render_backend import RenderBackendRegistry
from ai_chart_diagram_generator.config.settings import Settings, load_settings
from ai_chart_diagram_generator.services.exporter import ExporterService
from ai_chart_diagram_generator.services.planner import PlannerService
from ai_chart_diagram_generator.services.renderer import RendererService
from ai_chart_diagram_generator.utils.logging import configure_logging

_log = logging.getLogger(__name__)


@dataclass(slots=True)
class AppContext:
    """Frozen-ish container the handlers pull from. Built once at boot."""

    settings: Settings
    planner: PlannerService
    renderer: RendererService
    exporter: ExporterService
    backends: RenderBackendRegistry


def build_app(settings: Settings | None = None) -> AppContext:
    settings = settings or load_settings()
    configure_logging(settings.log_level)
    _log.info("booting ai-chart-diagram-generator %s", settings.version)

    backends = RenderBackendRegistry.discover(settings)
    planner = PlannerService(settings)
    renderer = RendererService(settings, backends)
    exporter = ExporterService(settings)

    return AppContext(
        settings=settings,
        planner=planner,
        renderer=renderer,
        exporter=exporter,
        backends=backends,
    )