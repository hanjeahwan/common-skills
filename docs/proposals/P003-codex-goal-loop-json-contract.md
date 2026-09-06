---
id: P003
status: implemented
---

# Codex Goal Loop JSON Contract

## Summary

Replace the Markdown goal contract and the iteration unit defined in
[P002](P002-codex-goal-loop-refactor.md) with one schema-validated JSON contract
whose every transition runs through `scripts/goal.py`. The contract stores facts
only; criterion state is derived. Failed approaches per criterion are capped, and
the cap is released only by a user decision. This supersedes the contract format
and loop unit of P002; P002's authority split between the native Codex Goal and
the contract is unchanged.

## Problem

P002 left three weaknesses in place:

- The contract was Markdown that the agent edited by hand. Nothing could reject
  a criterion marked verified without evidence, a `Protected Goal` edit without
  approval, or a duplicated lifecycle status.
- The loop unit was an "iteration" with its own `Current Iteration Target`. The
  unit added bookkeeping without adding control: the criterion being pursued was
  already the only thing that mattered.
- The agent could retry a failed approach indefinitely. Repeated failure had no
  mechanical consequence and no forced hand-back to the user.

## Scope

- Contract format, location, schema, and the script that owns its transitions.
- The loop definition in `SKILL.md` and `references/workflow.md`.
- Behavior cases and deterministic unit tests for the script.
- One link in P002 that pointed at the removed Markdown template.

## Non-goals

- Changing native Codex Goal ownership of lifecycle, budget, and usage.
- Adding a scheduler, event ledger, subgoal tree, lock, or automatic commit.
- Migrating existing Markdown contracts automatically.
- Refactoring other skills.

## Proposal

### Contract is JSON, validated before every write

`.goal/<title>-<YYYYMMDD-HHmmss>.json` conforms to
[`schemas/goal.schema.json`](../../.agents/skills/codex-goal-loop/schemas/goal.schema.json)
plus cross-field invariants in the script. Every mutating command validates the
result and refuses to persist an invalid contract. The agent never edits the file
directly. `jsonschema` is a hard dependency; a stdlib subset validator was rejected
because it would be a second implementation of the same rules.

### The loop unit is the acceptance criterion, not an iteration

Observe, Decide, Act, and Verify remain, but `next` deterministically returns the
single criterion to pursue: open criteria in `protected` order, an in-progress
approach first. There is no iteration counter, target, or hypothesis field.

### The contract stores facts; state is derived

`working` holds, per criterion, the current approach, failed attempts, and
evidence, plus goal-level risks and decisions. Criterion state is computed:
`verified` when evidence exists, `blocked` when an open decision blocks it,
`exhausted` when attempts reach the cap, otherwise `open`. A stored `state` field
was removed after review because it duplicated `evidence` and required an
invariant to keep the two in sync. `facts`, `checkpointed_at`, `last_invalidation`
and `risks[].blocks` were removed for the same reason: the script never read them,
or their names promised behavior the script did not implement.

### Failed approaches are capped and released only by the user

`protected.max_attempts` defaults to 10. `attempt` always records a failure, but
once the cap is reached `approach` and `attempt` refuse new approaches and `next`
skips the criterion. The only exits are an approved refinement of that criterion
or an approved `input` decision that blocks it; either restores the attempt
budget. Rejection leaves the criterion exhausted. The cap is contract data, not a
hidden script constant, so it is visible in the handoff and changeable only
through a refinement decision.

### `protected` changes only through approved refinement decisions

Decisions have two kinds. `refinement` carries a target (`objective`,
`max_attempts`, `constraints`, `non_goals`, or a criterion id) and is applied by
the script on approval. `input` is anything only the user can supply. An open
objective refinement blocks every criterion; an approved one drops all evidence.
The former `authority` kind was merged into `input` because the script treated
them identically.

### Rejected alternatives

- Append-only event ledger with derived snapshot: more auditable, but P002's
  no-ledger boundary stands, and a readable current-state file matters more for
  an agent that resumes after context reset.
- Keeping `state` alongside `evidence` for readability: `status --json` exposes
  the derived state instead.
- Storing native lifecycle status in the contract: still forbidden; `handoff`
  takes the observed native status as an argument.

## Migration

Existing `.goal/*.md` contracts are not converted. On resume the workflow stops,
proposes an `init` built from the legacy `Protected Goal`, and after approval
asks the user to install the new locator with `/goal edit`. Legacy Working State
evidence is discarded and re-verified.

## Verification

- `python3 -m unittest discover -s .agents/skills/codex-goal-loop/tests`: 21
  tests covering derived state, the attempt cap and its release, refinement
  blocking and application, readiness, path containment, and corruption
  detection.
- `python3 ~/.agents/skills/dao-skill/scripts/quality_check.py .agents/skills/codex-goal-loop` passed.
- `python3 .agents/skills/docs-system/scripts/validate.py .` passed.
- An independent review agent found no P0 and five P1 issues (attempt bypassing
  the cap, exhausted criteria with no exit after an `input` decision, no script
  path for `constraints`/`non_goals`/`max_attempts`, non-ASCII titles rejected,
  open objective refinement not blocking). All five were fixed and regression
  tests added. A second pass then removed four guards that had no failure model
  behind them.
- Not verified: a live Codex session exercising `create_goal` and `update_goal`
  against a generated contract. Evidence remains structural.

## Outcome

Implemented in the
[`codex-goal-loop` instructions](../../.agents/skills/codex-goal-loop/SKILL.md),
the [workflow](../../.agents/skills/codex-goal-loop/references/workflow.md),
the [schema](../../.agents/skills/codex-goal-loop/schemas/goal.schema.json),
the [script](../../.agents/skills/codex-goal-loop/scripts/goal.py), the
[behavior cases](../../.agents/skills/codex-goal-loop/tests/cases.md), and the
[unit tests](../../.agents/skills/codex-goal-loop/tests/test_goal.py).
`references/goal-template.md` was deleted. P002 remains the record of the
authority split this proposal builds on.
