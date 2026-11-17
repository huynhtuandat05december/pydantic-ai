"""Test the trip planner example runs with `TestModel` (no API key, no network)."""

import pytest

from pydantic_ai.models.test import TestModel


def test_trip_planner_produces_valid_trip_plan(monkeypatch: pytest.MonkeyPatch):
    # The example builds an OpenAI agent at import time, which needs a key to construct
    # (but never makes a request, since the run below overrides the model with `TestModel`).
    monkeypatch.setenv('OPENAI_API_KEY', 'mock-api-key')

    from pydantic_ai_examples.trip_planner import TripPlan, agent

    with agent.override(model=TestModel()):
        result = agent.run_sync('Plan a 3 day trip to Kyoto, Japan.')

    assert isinstance(result.output, TripPlan)
