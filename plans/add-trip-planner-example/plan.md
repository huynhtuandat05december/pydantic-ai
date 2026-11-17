---
title: "Add a structured-output trip planner example"
slug: add-trip-planner-example
status: pending
mode: fast
source: skill
created: 2026-11-17
phases:
  - id: 1
    title: "Add the example module"
    status: pending
  - id: 2
    title: "Add the dedicated TestModel test"
    status: pending
  - id: 3
    title: "Add the docs page + navigation entry"
    status: pending
---

# Plan: Add a structured-output trip planner example

## Goal

Ship a small, self-contained example that demonstrates getting **structured output**
from an `Agent` via `output_type`, following the exact conventions of the existing
`pydantic_model.py` / `roulette_wheel.py` examples. New files only — no changes to
library code under `pydantic_ai_slim/`.

Spec: `docs/specs/add-trip-planner-example.md`.

## Acceptance criteria (from spec)

1. `examples/pydantic_ai_examples/trip_planner.py` defines a Pydantic model
   `TripPlan` (`destination`, `days`, `activities` list) and an `Agent` with
   `output_type=TripPlan`.
2. The example has a `main()` and runs with `python -m pydantic_ai_examples.trip_planner`.
3. A test runs the agent with `pydantic_ai.models.test.TestModel` (no API key, no
   network) and asserts the result is a valid `TripPlan`.
4. `uv run pytest <the new test file>` passes.
5. Follows repo conventions (formatting, typing, example docs if required).

## Assumptions (fast mode — defaults chosen, not confirmed with maintainer)

- ASSUMPTION: `TripPlan` fields are `destination: str`, `days: int`, `activities: list[str]`.
- ASSUMPTION: Default model is selected via `PYDANTIC_AI_MODEL` env var defaulting to an OpenAI model, mirroring `pydantic_model.py`; docs use a model alias, never a raw model ID.
- ASSUMPTION: The example exposes a module-level `agent` so the test can `agent.override(model=TestModel())`; `main()` is sync and the `__main__` block calls `agent.run_sync(...)`.
- ASSUMPTION: Dedicated test lives at `tests/test_trip_planner_example.py` and imports the example module in-process (no subprocess).
- ASSUMPTION: A docs page (`docs/examples/trip-planner.md`) plus a `docs/navigation.yml` entry are added, since every existing example has a matching docs page; this touches only new files + docs config (not library code), honoring the "docs page if the repo requires one for every example" scope note.
- ASSUMPTION: The example stays under ~60 lines and omits the optional `logfire.configure(...)` lines to keep it minimal (both are present in `pydantic_model.py` but are not required for the feature being shown).

## Key facts discovered during research

- `examples/pydantic_ai_examples/pydantic_model.py` is the canonical structured-output example: module-level `class MyModel(BaseModel)`, `model = os.getenv('PYDANTIC_AI_MODEL', ...)`, module-level `agent = Agent(model, output_type=MyModel)`, and an `if __name__ == '__main__':` block calling `agent.run_sync(...)`.
- `tests/test_examples.py` monkeypatches `infer_model` → `mock_infer_model`, which substitutes `TestModel` for any inferred model string. So the docs-rendered example runs **without** a cassette/network — no recording work needed.
- `tests/import_examples.py` only imports every `examples/pydantic_ai_examples/*.py` (used in CI); it must import cleanly with a fake API key, which it will since the model is only inferred lazily at run time.
- Every `.py` example under `examples/pydantic_ai_examples/` has a sibling `docs/examples/<slug>.md` whose body is `---`/description + `Demonstrates:` list + Running section + `​```snippet {path="/examples/pydantic_ai_examples/<name>.py"}​````. `pydantic-model.md` is the template to copy.
- `docs/navigation.yml` lists example pages under the "Getting started" / examples tree (see the `pydantic-model.md` entry around lines 976-979). New page needs both `path`/`slug` and a redirect slug entry, mirroring the existing block.
- Docs rules (`docs/CLAUDE.md`): name models with an alias (`{{ openai:medium }}`), never a raw ID; use `uv run -m` / `python/uv-run -m` form in docs; keep examples executable.

## Phases

1. **Add the example module** — `examples/pydantic_ai_examples/trip_planner.py`. See `phase-01-example-module.md`.
2. **Add the dedicated TestModel test** — `tests/test_trip_planner_example.py`. See `phase-02-testmodel-test.md`.
3. **Add the docs page + navigation entry** — `docs/examples/trip-planner.md` + `docs/navigation.yml`. See `phase-03-docs-page.md`.

## Out of scope

- No changes to any library code under `pydantic_ai_slim/`.
- No cassette recording / real network calls.
- No running of the full test suite — only the new test file is run.

## Validation

- `uv run pytest tests/test_trip_planner_example.py` passes.
- `uv run python -m pydantic_ai_examples.trip_planner` runs (with a real key) — or is exercised via the mocked docs test path.
- Targeted lint/typecheck on the new files only:
  `PYRIGHT_PYTHON_IGNORE_WARNINGS=1 uv run pyright examples/pydantic_ai_examples/trip_planner.py tests/test_trip_planner_example.py`.
- `pre-commit` (lint/format) runs on commit; do not run repo-wide `make test`/`make typecheck`.

## Handoff

Next step: `/ck:cook plans/add-trip-planner-example/plan.md` (small, low-risk, well-understood).
