---
description: "A Pydantic AI example that returns a validated trip plan from an agent using structured output with any supported model."
---

# Trip Planner

Example of getting structured output from an agent using `output_type`, returning a validated `TripPlan` model rather than free-form text.

Demonstrates:

- [structured `output_type`](../output.md#structured-output)

## Running the Example

With [dependencies installed and environment variables set](./setup.md#usage), run:

```bash
python/uv-run -m pydantic_ai_examples.trip_planner
```

This example uses an OpenAI model by default. To run it with Gemini, set `PYDANTIC_AI_MODEL` to a model ID with the `google:` prefix.

```bash
PYDANTIC_AI_MODEL="{{ google:medium }}" python/uv-run -m pydantic_ai_examples.trip_planner
```

## Example Code

```snippet {path="/examples/pydantic_ai_examples/trip_planner.py"}```
