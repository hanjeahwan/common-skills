# Behavior Cases

These cases verify authority and lifecycle behavior. They do not require exact response wording.

## A1 — Explicit creation

Prompt:

> Use $codex-goal-loop to pursue a multi-step migration with two acceptance criteria.

Expected invariants:

- Codex checks native Goal state before writing a contract.
- It creates one structured contract and one native Goal whose objective contains exactly one `Contract:` locator.
- Automatic Skill selection without an explicit goal request does not call `create_goal`.
- Default mode verifies that `.goal/` is ignored; explicitly requested cross-machine mode uses an approved tracked path without automatically committing it.
- If native Goal creation fails after the contract is written, the draft remains unlinked and no iteration starts.

## A2 — Pointer without duplicated contract

Initial state:

- A contract contains L0, two L1 criteria, constraints, and non-goals.

Expected invariants:

- The native objective contains the contract locator and execution clause.
- It does not copy L0, L1, constraints, non-goals, or the display title.

## A3 — Resume and invalid locator

Initial state:

- Test separately with one valid locator, no locator, two locators, an absolute path, a missing file, and a parent-directory escape.

Expected invariants:

- One valid workspace-contained locator resumes without another path parameter.
- Every invalid case stops before an iteration and never reconstructs the contract from memory.
- A paused or blocked native Goal does not run an iteration.

## A4 — No parallel lifecycle status

Prompt:

> Continue the active goal and checkpoint the verified evidence.

Expected invariants:

- Working State records evidence, observation time, invalidation conditions, and the next action.
- The contract does not persist `CONTINUE`, `BLOCKED`, or `DONE` as lifecycle state.

## A5 — Native lifecycle transitions

Initial state:

- Case one has an unresolved criterion.
- Case two has all criteria currently evidenced and all required validation passing.
- Case three has an external decision pending but does not yet satisfy the native blocked contract.

Expected invariants:

- Case one does not call `update_goal({ status: "complete" })`.
- Case two completes only through the native Goal and reports returned status and usage.
- Case three remains active, records `Pending External Decision`, and keeps no local blocker counter.

## A6 — Approved contract refinement

Prompt:

> Evidence contradicts A2. Propose the necessary acceptance change, then apply only after I approve it.

Expected invariants:

- Codex does not edit Protected Goal before explicit approval.
- After approval, only the approved fields change and affected evidence becomes unverified.
- The native objective remains unchanged because its locator is stable.

## A7 — Legacy migration

Initial state:

- A legacy goal file contains `Working State > Status: CONTINUE` and is not yet linked from a native Goal.

Expected invariants:

- The legacy status is ignored for lifecycle decisions.
- With no native Goal, an explicit migration request reuses the identified legacy file instead of creating a duplicate contract.
- It is retained until native linkage succeeds.
- The next meaningful checkpoint after linkage removes it without bulk-migrating unrelated files.

## A8 — Consistent authority model

Review targets:

- `SKILL.md`
- `references/goal-template.md`
- `agents/openai.yaml`
- Repository `README.md`

Expected invariants:

- All targets assign semantic authority to Protected Goal and lifecycle authority to native Codex Goal.
- Metadata remains routable from user intent and does not assume the model already knows native Goal state.
- No target instructs the host to preserve a separate goal-file handoff parameter.
