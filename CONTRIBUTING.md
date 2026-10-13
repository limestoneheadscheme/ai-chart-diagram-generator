# Contributing to ai-chart-diagram-generator

Thanks for wanting to peel a layer off. This repo is a Windows desktop
tool that turns natural-language prompts into structured charts and
diagrams (flowcharts, sequence diagrams, entity-relationship graphs,
Gantt timelines, network topologies, mind maps). Contributions are
welcome across the Python service layer, the C++ renderer shim, and
the plugin adapters.

## Ground rules

- Target Python 3.12+. Windows 10/11 is the primary supported platform.
  Linux/macOS work for headless rendering only.
- One concern per PR. If you're adding a new diagram type, add the
  grammar module, the service, the handler, and a test in the same PR.
- Every new diagram type needs a fixture under `tests/fixtures/`.
- Run the full check before opening a PR:

```
python -m pip install -e .[dev]
python -m pytest -q
python -m ruff check src tests
python -m mypy src
```

## Repo layout

```
src/ai_chart_diagram_generator/
  bootstrap/      entry, app wiring, CLI/desktop launcher
  api/            thin handlers (request -> service -> response)
  services/       business logic (parse, plan, render, export)
  models/         dataclasses, pydantic schemas, IR types
  adapters/       platform + renderer backends (C++, C#, Java bridges)
  grammar/        per-diagram-type parsers and validators
  utils/          logging, fs, timing, id helpers
  config/         settings loader, defaults, schema
tests/
  unit/
  integration/
  fixtures/
docs/
  architecture/
  prompts/
```

## Adding a new diagram type

1. Create `src/ai_chart_diagram_generator/grammar/<type>_grammar.py`
   exposing `parse(prompt: str) -> DiagramIR`.
2. Register it in `services/planner.py` under `GRAMMAR_REGISTRY`.
3. Add a handler in `api/handlers/<type>_handler.py`.
4. Add the backend hint in `adapters/render_backend.py`.
5. Ship a fixture + unit test + one integration test.

## Style

- Ruff with the repo's `pyproject.toml` config. Line length 100.
- Type hints everywhere. `mypy --strict` on `src/`.
- No `print()` in `src/`. Use `utils/logging.py`.
- Services are pure where possible. Side effects live in adapters.

## Commit messages

Conventional commits: `feat:`, `fix:`, `refactor:`, `docs:`, `test:`,
`chore:`. Scope uses the subpackage name, e.g.
`feat(grammar): add sequence-diagram parser`.

## Reporting bugs

Open an issue with: OS build, Python version, the prompt you fed in,
the diagram type you expected, and the raw IR dump (`--dump-ir`).