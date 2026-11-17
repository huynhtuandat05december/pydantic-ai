---
phase: 2
title: "Add the dedicated TestModel test"
status: pending
priority: P1
dependencies: [1]
---

# Phase 2: Add the dedicated TestModel test

## Overview
Add `tests/test_trip_planner_example.py` that runs the example's `agent` with
`TestModel` (no API key, no network) and asserts a valid `TripPlan` result.

## Requirements
- Functional: run the agent under `TestModel` and assert the output is a `TripPlan`
  with the expected field types (`destination: str`, `days: int`, `activities: list[str]`).
- Non-functional: in-process (no subprocess), deterministic, no network, fast.

## Architecture
- Import the module's `agent` and `TripPlan` from `pydantic_ai_examples.trip_planner`.
- Use `with agent.override(model=TestModel()):` then `result = agent.run_sync('...')`.
  `TestModel` auto-generates a value that satisfies the `output_type` schema, so
  `result.output` is a valid `TripPlan` instance.
- Assert `isinstance(result.output, TripPlan)` and that
  `result.output.activities` is a `list` and `result.output.days` is an `int`.

## Related Code Files
- Create: `tests/test_trip_planner_example.py`
- Reference: `tests/conftest.py` (already imports `TestModel`), existing tests that use
  `agent.override(model=TestModel())`.

## Implementation Steps
1. `from pydantic_ai.models.test import TestModel`.
2. `from pydantic_ai_examples.trip_planner import TripPlan, agent`.
3. Write `def test_trip_planner_returns_valid_trip_plan() -> None:` that overrides the
   model with `TestModel()`, calls `agent.run_sync('Plan a trip.')`, and asserts the
   output type/fields.
4. Ensure the test needs no `OPENAI_API_KEY` — `TestModel` bypasses provider auth; the
   import must not construct a real provider at import time (verify in Phase 1 that the
   model string is only inferred at run time).

## Success Criteria
- [ ] `uv run pytest tests/test_trip_planner_example.py` passes with no network and no API key.
- [ ] Test asserts `isinstance(result.output, TripPlan)` plus field-type checks.
- [ ] `PYRIGHT_PYTHON_IGNORE_WARNINGS=1 uv run pyright tests/test_trip_planner_example.py` is clean.

## Risk Assessment
- Risk: importing the example triggers provider construction → auth error without a key.
  Mitigation: keep model inference lazy in Phase 1 (`Agent(model_string, ...)` defers
  inference to run time); the override replaces it before any run.
- Risk: `TestModel` output shape surprises (e.g. empty list). Mitigation: assert types,
  not specific values; `TestModel` fills required fields validly.
