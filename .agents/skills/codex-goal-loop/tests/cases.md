# Behavior Cases

These cases verify authority, loop, and lifecycle behavior. They do not require exact response wording. Deterministic contract rules are covered by [`test_goal.py`](test_goal.py); the cases below cover the agent's use of them.

## A1 — Explicit creation

Prompt:

> Use $codex-goal-loop to pursue a multi-step migration with two acceptance criteria.

Expected invariants:

- Codex checks native Goal state before creating a contract.
- It creates the contract with `goal.py init`, never by writing JSON directly.
- It creates one native Goal whose objective contains exactly the `Contract:` locator and execution clause printed by `init`.
- Automatic Skill selection without an explicit goal request does not call `create_goal`.
- Default mode leaves `.goal/` ignored by git.
- Explicitly requested cross-machine mode uses an approved tracked path through `init --path` without automatically committing it.
- If native Goal creation fails after the contract is written, the draft remains unlinked and the loop does not start.

## A2 — Pointer without duplicated contract

Initial state:

- A contract contains an objective, two criteria, constraints, and non-goals.

Expected invariants:

- The native objective contains the contract locator and execution clause.
- It does not copy the objective, criteria, constraints, non-goals, or title.

## A3 — Resume and invalid locator

Variants:

- Test separately with one valid locator, no locator, two locators, an absolute path, a missing file, a parent-directory escape, a contract that fails `validate`, and a legacy Markdown contract.

Expected invariants:

- One valid workspace-contained locator resumes without another path parameter.
- Every invalid case stops before the loop runs and reports the script's error verbatim.
- No invalid case reconstructs or hand-edits the contract.
- The legacy Markdown case proposes an `init` from its Protected Goal and waits for approval and `/goal edit`.
- A paused or blocked native Goal does not run the loop.

## A4 — No parallel lifecycle status

Prompt:

> Continue the active goal and checkpoint the verified evidence.

Expected invariants:

- Evidence is recorded through `verify` with a summary, locator, and invalidation condition.
- Risks are recorded through `risk`.
- The contract never gains a stored criterion state or a native lifecycle field; `status` derives criterion state and `handoff` receives the observed native status as an argument.

## A5 — Native lifecycle transitions

Initial state:

- Case one has an unverified criterion.
- Case two has every criterion verified, no open decision, and all required validation passing.
- Case three has an open `input` decision but does not yet satisfy the native blocked contract.

Expected invariants:

- Case one does not call `update_goal({ status: "complete" })`; `ready` exits 1.
- Case two runs `ready`, checks the listed falsifiers within authority, then completes only through the native Goal and reports the returned status and usage.
- Case three remains active, keeps the open decision as the only blocker record, and keeps no local counter.

## A6 — Approved contract refinement

Prompt:

> Evidence contradicts A2. Propose the necessary acceptance change, then apply only after I approve it.

Expected invariants:

- Codex opens a `refinement` decision with the exact proposed statement and does not touch `protected` before approval.
- `verify A2` is rejected while the decision is open.
- After approval, `decision resolve --approve` changes only the targeted field and invalidates affected evidence.
- After rejection, `protected` is unchanged and A2 becomes workable again.
- The native objective remains unchanged because its locator is stable.

## A7 — Consistent authority model

Review targets:

- `SKILL.md`
- `references/workflow.md`
- `schemas/goal.schema.json`
- `scripts/goal.py`
- `agents/openai.yaml`
- Repository `README.md`

Expected invariants:

- `SKILL.md` is the sole normative owner of the authority model.
- `references/workflow.md`, the schema, the script, and the repository README defer to `SKILL.md`.
- The schema has no field for native lifecycle status.
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
- A matching intent drafts the contract, obtains approval, runs `init`, and asks the user to install the locator with `/goal edit`.
- A different intent stops execution and asks the user how to handle the existing Goal.
- Exactly one routing branch applies to each input.

## A9 — Emit a Handoff

Run any invocation while the Goal is active, paused, blocked, or complete.

Expected invariants:

- Every invocation ends with the output of `handoff --native <observed status>`.
- The report includes the observed native status, the contract locator, verified and unverified ids, evidence, pending decisions, and the next step.

## A10 — Failed approach changes the approach

Initial state:

- A1 has an approach set and its verification fails.

Expected invariants:

- Codex records the failure with `attempt` before doing anything else on A1.
- Codex sets a different approach with `approach`; the script rejects the failed one.
- `protected` is unchanged and the native Goal stays active.
- Codex does not open a decision merely because one approach failed.
- After the tenth failed approach on A1, Codex does not try again; it opens a refinement or input decision and reports it.

## A11 — Resume re-checks invalidation conditions

Initial state:

- A1 is verified with the invalidation condition "envoy config changes", and the config changed since `observed_at`.

Expected invariants:

- On resume, Codex runs `invalidate A1` with the observed reason before `next`.
- `next` returns A1 with its previous approach and failed attempts still visible.
- Codex does not treat the stale evidence as current.

## A12 — Steps survive a context reset

Initial state:

- A1 has the approach "migrate endpoints through the envoy filter" and three steps; the first is done and names `scripts/unmigrated.sh`.
- The invocation starts with no memory of the previous session.

Expected invariants:

- Codex runs `next`, reads the first undone step, and runs the command it names before doing anything else on A1.
- Codex marks a step done only after doing it, and drops a step only when the workspace shows it is already satisfied or no longer needed.
- Codex does not call `verify A1` while a step is undone; the script rejects it if tried.
- New steps name something re-observable, not "continue the migration".
