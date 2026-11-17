---
id: add-trip-planner-example
type: ticket
flow: feature
status: done
title: Add a structured-output trip planner example
acceptance:
  - New file examples/pydantic_ai_examples/trip_planner.py defines a Pydantic model TripPlan (destination, days, activities list) and an Agent with output_type=TripPlan
  - The example has a `main()` and runs with `python -m pydantic_ai_examples.trip_planner`
  - A test runs the agent with pydantic_ai.models.test.TestModel (no API key, no network) and asserts the result is a valid TripPlan
  - "`uv run pytest <the new test file>` passes"
  - Follows the repo's conventions in AGENTS.md / CLAUDE.md (formatting, typing, docs for examples if required)
---

Add a small, self-contained example that shows how to get structured output
from an agent using `output_type`.

Scope:
- Only add new files (the example, its test, and an example doc page if the
  repo requires one for every example). Do not modify library code under
  `pydantic_ai_slim/`.
- Keep the example under ~60 lines.
- Run only the targeted test, not the full suite.
