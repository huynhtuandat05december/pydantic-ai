---
phase: 3
title: "Add the docs page + navigation entry"
status: pending
priority: P2
dependencies: [1]
---

# Phase 3: Add the docs page + navigation entry

## Overview
Add `docs/examples/trip-planner.md` (mirroring `docs/examples/pydantic-model.md`) and
register it in `docs/navigation.yml`, so the example follows the universal
"every example has a docs page" convention.

> Scope note: this touches only a new docs file + the docs navigation config, never
> library code under `pydantic_ai_slim/`. If the maintainer prefers the spec's narrowest
> reading (no docs page), this phase can be dropped without affecting acceptance
> criteria 1-4. See the ASSUMPTION in `plan.md`.

## Requirements
- Functional: a rendered docs page with description frontmatter, a `Demonstrates:` list
  linking `[structured output_type](../output.md#structured-output)`, a Running section,
  and a `snippet` fence pointing at the example file.
- Non-functional: follow `docs/CLAUDE.md` — use a model **alias** (`{{ openai:medium }}`),
  `python/uv-run -m` run form, reference-style API links.

## Architecture
- `tests/test_examples.py` discovers docs snippets and runs them with `infer_model`
  monkeypatched to `TestModel`, so the page needs no cassette and no network.
- The page body is a near-copy of `docs/examples/pydantic-model.md` with trip-planner
  wording and the correct `path="/examples/pydantic_ai_examples/trip_planner.py"`.

## Related Code Files
- Create: `docs/examples/trip-planner.md`
- Modify: `docs/navigation.yml` (add `path`/`slug` + redirect slug, mirroring the
  `pydantic-model.md` block near lines 976-979)
- Reference: `docs/examples/pydantic-model.md`

## Implementation Steps
1. Copy the structure of `docs/examples/pydantic-model.md`:
   - `---` frontmatter with a one-line `description:` of the trip planner.
   - `# Trip Planner` heading + one-sentence intro.
   - `Demonstrates:` bullet linking `[structured `output_type`](../output.md#structured-output)`.
   - `## Running the Example` with `python/uv-run -m pydantic_ai_examples.trip_planner`.
   - `## Example Code` with ```` ```snippet {path="/examples/pydantic_ai_examples/trip_planner.py"}``` ````.
2. In `docs/navigation.yml`, add a new entry under the examples/getting-started group
   mirroring the `pydantic-model.md` block: a `path: "examples/trip-planner.md"` +
   `slug:` and the redirect `- "examples/trip-planner"` sub-entry.
3. If the page references a model, use the `{{ openai:medium }}` alias form, not a raw ID
   (unlike the `.py`, which may keep a concrete default).

## Success Criteria
- [ ] `docs/examples/trip-planner.md` exists and mirrors the `pydantic-model.md` shape.
- [ ] `docs/navigation.yml` has a matching entry + redirect slug.
- [ ] The example runs under the docs test harness (mocked `TestModel`) without a cassette.
- [ ] No raw model IDs in the docs page (`tests/test_docs_model_aliases.py` convention).

## Risk Assessment
- Risk: navigation entry malformed → nav validation failure. Mitigation: copy the exact
  indentation/shape of the existing `pydantic-model.md` block.
- Risk: raw model ID trips `tests/test_docs_model_aliases.py`. Mitigation: use an alias in prose/snippet references.
- Risk: scope creep beyond spec. Mitigation: phase is explicitly droppable (see scope note); acceptance criteria 1-4 do not depend on it.
