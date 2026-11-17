"""Example of getting structured output from an agent using `output_type`.

The agent returns a validated `TripPlan` Pydantic model rather than free-form text.

Run with:

    uv run -m pydantic_ai_examples.trip_planner
"""

import os

import logfire
from pydantic import BaseModel, Field

from pydantic_ai import Agent
from pydantic_ai.capabilities import Caching

# 'if-token-present' means nothing will be sent (and the example will work) if you don't have logfire configured
logfire.configure(send_to_logfire='if-token-present')
logfire.instrument_pydantic_ai()


class TripPlan(BaseModel):
    """A structured plan for a trip."""

    destination: str
    days: int = Field(description='Number of days for the trip')
    activities: list[str] = Field(description='Suggested activities, in order')


model = os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-5.2')
print(f'Using model: {model}')
agent = Agent(model, output_type=TripPlan, capabilities=[Caching()])


def main() -> None:
    result = agent.run_sync('Plan a 3 day trip to Kyoto, Japan.')
    print(result.output)
    print(result.usage)


if __name__ == '__main__':
    main()
