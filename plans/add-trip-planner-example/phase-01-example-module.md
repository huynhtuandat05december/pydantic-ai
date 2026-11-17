---
phase: 1
title: "Add the example module"
status: pending
priority: P1
dependencies: []
---

# Phase 1: Add the example module

## Overview
Create `examples/pydantic_ai_examples/trip_planner.py`, a <60-line, self-contained
structured-output example mirroring `pydantic_model.py`.

## Requirements
- Functional: define `TripPlan` (BaseModel) with `destination: str`, `days: int`,
  `activities: list[str]`; a module-level `agent = Agent(model, output_type=TripPlan)`;
  a `main()`; and an `if __name__ == '__main__':` guard that runs the agent and prints
  the structured output.
- Non-functional: idiomatic, fully typed, no `Any`/`cast`; importable with a fake API
  key (model inferred lazily at run time); under ~60 lines.

## Architecture
- Module-level `agent` is required so Phase 2's test can call
  `agent.override(model=TestModel())`.
- Select the model like `pydantic_model.py`:
  `model = os.getenv('PYDANTIC_AI_MODEL', 'openai:<tier>')` then
  `agent = Agent(model, output_type=TripPlan)`. Do NOT use `Agent.override` to pick the
  app model (per CLAUDE.md model-selection guidance) — the env-var default is the
  application model, override is reserved for the test.
- Keep `main()` synchronous using `agent.run_sync(...)` for simplicity (the structured
  output feature does not need streaming/async).

## Related Code Files
- Create: `examples/pydantic_ai_examples/trip_planner.py`
- Reference (do not modify): `examples/pydantic_ai_examples/pydantic_model.py`

## Implementation Steps
1. Add a module docstring with a `Run with:` section (`uv run -m pydantic_ai_examples.trip_planner`), matching sibling examples.
2. Import `os`, `BaseModel` from `pydantic`, `Agent` from `pydantic_ai`.
3. Define `class TripPlan(BaseModel)` with the three fields (add short field semantics only if it keeps under the line budget; docstrings optional).
4. `model = os.getenv('PYDANTIC_AI_MODEL', 'openai:<tier>')`; `agent = Agent(model, output_type=TripPlan, instructions=...)` with a one-line instruction describing the trip-planning task.
5. Define `def main() -> None:` that calls `agent.run_sync('<a concrete prompt, e.g. "Plan a 3-day trip to Kyoto.">')`, then prints `result.output` (and optionally `result.usage()`).
6. Add `if __name__ == '__main__': main()`.

## Success Criteria
- [ ] File exists with `TripPlan` + `Agent(output_type=TripPlan)` + `main()` + `__main__` guard.
- [ ] `uv run python -c "import pydantic_ai_examples.trip_planner"` imports cleanly with a fake key.
- [ ] `PYRIGHT_PYTHON_IGNORE_WARNINGS=1 uv run pyright examples/pydantic_ai_examples/trip_planner.py` is clean.
- [ ] Under ~60 lines; no `Any`/`cast`.

## Risk Assessment
- Risk: raw model ID leaking into docs later. Mitigation: the `.py` keeps a concrete default (fine for runnable example code), but the docs page (Phase 3) must use an alias per `docs/CLAUDE.md`.
- Risk: making `main()` async adds asyncio noise. Mitigation: use `run_sync` — structured output needs nothing more.
