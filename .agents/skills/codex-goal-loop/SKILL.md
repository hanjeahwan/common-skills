---
name: codex-goal-loop
description: Pursue an explicitly requested bounded goal, or continue a previously established goal contract, through repeated evidence-driven Observe, Decide, Act, and Verify iterations backed by the native Codex Goal lifecycle. Use for long-running or autonomous work; do not use for ordinary one-shot tasks.
---

# Codex Goal Loop

Use a structured contract for goal semantics and the native Codex Goal for lifecycle. Keep the objective and acceptance conditions stable while evidence, hypotheses, and implementation approach evolve.

## Authority

- `Protected Goal` in the referenced contract is the sole authority for its display title, L0 Objective, L1 Acceptance Criteria, constraints, and non-goals.
- The native Codex Goal is the sole authority for goal identity, lifecycle status, budget, and usage.
- `Working State` is a replaceable evidence checkpoint. It must not contain a parallel lifecycle status.
- Current observable repository and external state override stale checkpoint claims.

## Invariants

- Preserve the approved L0 Objective and L1 Acceptance Criteria.
- Propose an L1 refinement when current evidence contradicts an Acceptance Criterion or shows that no authorized action can satisfy it.
- To refine L0 or L1, propose the exact change and supporting evidence.
- Apply an L0 or L1 refinement only after explicit user approval.
- Change the L2 approach or current iteration target when new evidence invalidates the current approach.
- Every action must advance a named Acceptance Criterion or resolve a named uncertainty that blocks its verification.
- Mark an Acceptance Criterion verified only with observable evidence.
- Record the evidence locator, observation time, and invalidation conditions.
- Re-verify evidence after an invalidation condition occurs or a time-sensitive external fact changes.
- Treat a failed approach as evidence. Failure alone does not justify a blocked transition.
- Treat context reset and execution-budget exhaustion as handoffs rather than blockers.
- Do not revert or overwrite changes that cannot be attributed to the current goal.

## Native Goal Gates

Use native Goal operations according to their current tool contract:

- Read native Goal state with `get_goal` before starting or resuming work.
- Call `create_goal` only after an explicit user request.
- Treat an explicit `$codex-goal-loop <intent>` invocation as a creation request.
- Automatic Skill selection does not authorize `create_goal`.
- `$codex-goal-loop` without an objective does not authorize `create_goal`.
- Pass a token budget only when the user explicitly requests one.
- Use `update_goal` only for a justified `complete` or `blocked` transition.
- Leave `/goal edit`, `/goal pause`, `/goal resume`, and `/goal clear` to the user or host.
- Never emulate native Goal lifecycle operations inside the contract.
- Stop before reading or mutating a contract when native Goal state cannot be read.
- Store exactly one deterministic contract locator and one execution clause in the native objective.

## Reference Router

- Read [`references/workflow.md`](references/workflow.md) before starting, resuming, iterating, changing native lifecycle state, or handing off a Goal.
- Read [`references/goal-template.md`](references/goal-template.md) only when creating a contract, restoring required sections, or applying an approved refinement.
- Use the existing contract during an ordinary resume.

## Responsibility Boundary

- The agent owns Goal alignment, Observe, Decide, Act, Verify, approved contract content, and Working State checkpoints.
- Native Codex Goal owns lifecycle, budget, and usage state.
- The user or host owns objective edits, pause, resume, clear, invocation, and context reset.
- The host may preserve native Goal state.
- The host must not choose the L2 approach.
- The host must not declare Acceptance Criteria verified.

## Boundaries

- Do not turn the Skill into a scheduler, wake-up system, or lifecycle runner.
- Do not create separate goal revisions, event ledgers, subgoal trees, locks, automatic commits, or local lifecycle counters without evidence that the simple design fails.
- Do not treat plans, documentation, tests, prior claims, or Working State as unquestionable truth.

## Quality Standard

When evidence invalidates an approach:

1. Keep Protected Goal unchanged.
2. Record the failed approach and its evidence.
3. Choose a new L2 approach.
4. Leave the native Goal active unless the native blocked contract is satisfied.
