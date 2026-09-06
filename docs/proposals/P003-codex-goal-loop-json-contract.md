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
the cap is released only by a user decision. The Skill owns the contract and
nothing else: it neither calls nor reasons about the runtime's own goal
mechanism, which has its own instructions. This supersedes both the contract
format and the authority split of P002.

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
- P002 made the Skill route on native `active`, `paused`, and `blocked`. The host
  already instructs the model about that state machine, so the Skill was a second
  set of rules over the same facts. In live runs the two disagreed: one session
  refused to act on a user's answer until `/goal resume`, another acted on it
  immediately, and both believed they were following the Skill.

## Scope

- Contract format, location, schema, and the script that owns its transitions.
- The loop and lifecycle definitions in `SKILL.md` and `references/workflow.md`.
- Removing the runtime lifecycle coupling that P002 introduced.
- Behavior cases and deterministic unit tests for the script.
- One link in P002 that pointed at the removed Markdown template.

## Non-goals

- Changing, wrapping, or documenting the runtime's own goal mechanism. It keeps its own instructions.
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

### The contract is the whole scope

The Skill defines one lifecycle, over the contract: open while `current` returns
it, awaiting the user while every remaining criterion is blocked or exhausted,
and done once `ready` exits 0. `current` finds the single unfinished contract
under `.goal/`, so no pointer has to live anywhere else.

The runtime's own goal mechanism is not modeled here at all. P002 had the Skill
route on it, which meant two sets of rules over the same facts and no added
control. Progress now depends only on the contract and the observable
workspace.

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
- Storing any external lifecycle status in the contract: still forbidden, and
  `handoff` no longer takes one as an argument either.
- Mirroring the runtime's blocked threshold or gating progress on a runtime
  command: removed after two live runs disagreed under identical conditions.

## Migration

Existing `.goal/*.md` contracts are not converted. On resume the workflow stops,
proposes an `init` built from the legacy `Protected Goal`,. Legacy Working State evidence is
discarded and re-verified.

## Verification

- `python3 -m unittest discover -s .agents/skills/codex-goal-loop/tests`: 26
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
- Three live runs on 2026-09-06 in Orca terminals (`codex` 0.153.x,
  `gpt-5.6-luna`, reasoning effort low) against a two-criterion fixture. Each
  drove `init`, steps, evidence, an `input` decision, and completion. They also
  produced the evidence for removing the lifecycle coupling: with identical
  contract state, one run refused to act on the user's answer and one acted
  immediately, each citing the Skill. Contract-level behavior was consistent in
  all three.
- Live runs after the decoupling. Prompted with `$codex-goal-loop`, the agent
  ran `init`, resolved the contract with `current`, drove criteria through steps
  to verified evidence, and passed `ready`, calling no goal tool. One deviation:
  it asked for an approval in prose instead of recording it with `decision open`,
  so `handoff` reported no pending decision while one was outstanding.
- An ablation established that the Skill occupies the goal-setting intent: the
  same request without the Skill loaded made the runtime start its own goal,
  with the Skill loaded it did not. A vague non-suppression clause was tried and
  measurably failed, so it was removed. The working shape is two requests: one
  invoking the Skill to build the contract, then one asking for a runtime goal.
  Verified twice end to end on a three-criterion fixture: the second request
  started a runtime goal that drove all three criteria to verified across
  unattended turns, and `ready` then exited 0.
- The first of those runs exposed a second-copy defect: the runtime objective
  restated the acceptance criteria instead of pointing at the contract, which
  goes stale on the next approved refinement and does not route an unattended
  turn back through the Skill. `init` now prints a pointer objective naming the
  contract path and `$codex-goal-loop`, and `SKILL.md` documents the split. The
  re-run stored exactly that pointer:
  `Pursue the contract at .goal/<file>.json with $codex-goal-loop until ready passes.`

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
