# Behavior Cases

These cases verify authority and lifecycle behavior. They do not require exact response wording.

## A1 — Explicit creation

Prompt:

> Use $codex-goal-loop to pursue a multi-step migration with two acceptance criteria.

Expected invariants:

- Codex checks native Goal state before writing a contract.
- It creates one structured contract.
- It creates one native Goal.
- The native objective contains exactly one `Contract:` locator.
- Automatic Skill selection without an explicit goal request does not call `create_goal`.
- Default mode verifies that `.goal/` is ignored.
- Explicitly requested cross-machine mode uses an approved tracked path without automatically committing it.
- If native Goal creation fails after the contract is written, the draft remains unlinked.
- No iteration starts after native Goal creation fails.

## A2 — Pointer without duplicated contract

Initial state:

- A contract contains L0, two L1 criteria, constraints, and non-goals.

Expected invariants:

- The native objective contains the contract locator and execution clause.
- It does not copy L0, L1, constraints, non-goals, or the display title.

## A3 — Resume and invalid locator

Variants:

- Test separately with one valid locator, no locator, two locators, an absolute path, a missing file, and a parent-directory escape.

Expected invariants:

- One valid workspace-contained locator resumes without another path parameter.
- Every invalid case stops before an iteration.
- No invalid case reconstructs the contract from memory.
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
- Case two completes only through the native Goal.
- Case two reports the returned status and usage.
- Case three remains active.
- Case three records `Pending External Decision`.
- Case three keeps no local blocker counter.

## A6 — Approved contract refinement

Prompt:

> Evidence contradicts A2. Propose the necessary acceptance change, then apply only after I approve it.

Expected invariants:

- Codex does not edit Protected Goal before explicit approval.
- After approval, only the approved fields change.
- Evidence affected by the approved change becomes unverified.
- The native objective remains unchanged because its locator is stable.

## A7 — Consistent authority model

Review targets:

- `SKILL.md`
- `references/workflow.md`
- `references/goal-template.md`
- `agents/openai.yaml`
- Repository `README.md`

Expected invariants:

- `SKILL.md` is the sole normative owner of the authority model.
- `references/workflow.md`, `references/goal-template.md`, and the repository README defer to `SKILL.md`.
- `agents/openai.yaml` does not define a parallel authority model.
- Metadata remains routable from user intent and does not assume the model already knows native Goal state.
- No target instructs the host to preserve a separate goal-file handoff parameter.

## A8 — Route an active Goal by intent

Exercise each input independently:

- The native objective contains one valid contract locator, and the invocation continues the same Goal.
- The native objective contains one valid contract locator, and the invocation requests a different Goal.
- The native objective contains no locator, and it matches the requested intent.
- The native objective contains no locator, and it has a different intent.

Expected invariants:

- Continuing the same Goal resumes the resolved contract.
- Requesting a different Goal stops execution and asks the user how to handle the existing Goal.
- A matching intent drafts a contract, obtains approval, and asks the user to install the locator with `/goal edit`.
- A different intent stops execution and asks the user how to handle the existing Goal.
- Exactly one routing branch applies to each input.

## A9 — Emit a Handoff

Run any invocation while the Goal is active, paused, blocked, or complete.

Expected invariants:

- Every invocation ends with a Handoff report.
- The report includes the observed native status.
- The report includes the contract locator.
- The report summarizes acceptance status.
- The report identifies the evidence produced.
- The report identifies any pending decision.
- The report states the next action.
