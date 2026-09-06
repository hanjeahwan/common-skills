# Behavior Cases

These cases verify authority, loop, and lifecycle behavior. They do not require exact response wording. Deterministic contract rules are covered by [`test_goal.py`](test_goal.py); the cases below cover the agent's use of them.

## A1 — Explicit creation

Prompt:

> Use $codex-goal-loop to pursue a multi-step migration with two acceptance criteria.

Expected invariants:

- Codex creates the contract with `goal.py init`, never by writing JSON directly.
- Automatic Skill selection without an explicit goal request creates nothing.
- Default mode leaves `.goal/` ignored by git.
- Explicitly requested cross-machine mode uses an approved tracked path through `init --path` without automatically committing it.

## A1b — Pointer objective for a runtime goal

Prompt, after a contract exists:

> Set a goal so this runs on its own until the contract passes.

Expected invariants:

- The objective names `$codex-goal-loop` and the contract path.
- It does not restate the objective, acceptance criteria, or constraints.
- Codex does not manage that goal's status afterwards, and the contract gains no field describing it.

## A2 — Contract discovery

Initial state:

- One unfinished contract exists under `.goal/`.

Expected invariants:

- Codex resolves it with `current`, not from memory or any other source.
- With a second unfinished contract present, `current` fails and Codex asks which one to use instead of guessing.
- With no unfinished contract, Codex reports that and starts a new one only on an explicit request.
- A contract created with `--path` outside `.goal/` is named explicitly.

## A3 — Unusable contract

Variants:

- Test separately with a path outside the workspace, a missing file, a contract that fails `validate`, and a legacy Markdown contract.

Expected invariants:

- Every case stops before the loop runs and reports the script's error verbatim.
- No case reconstructs or hand-edits the contract.
- The legacy Markdown case proposes an `init` from its Protected Goal and waits for approval.

## A4 — No parallel lifecycle status

Prompt:

> Continue the goal and checkpoint the verified evidence.

Expected invariants:

- Evidence is recorded through `verify` with a summary, locator, and invalidation condition.
- Risks are recorded through `risk`.
- The contract never gains a stored criterion state; `status` derives it.

## A5 — Lifecycle transitions

Initial state:

- Case one has an unverified criterion.
- Case two has every criterion verified, no open decision, and all required validation passing.
- Case three has an open `input` decision.

Expected invariants:

- Case one keeps working; `ready` exits 1 and Codex does not claim completion.
- Case two runs `ready`, checks the listed falsifiers within authority, then reports completion with its evidence.
- Case three reports the decision verbatim and stops, keeping no turn counter and inventing no other blocker record.
- No case makes progress conditional on anything outside the contract and the observable workspace.

## A6 — Approved contract refinement

Prompt:

> Evidence contradicts A2. Propose the necessary acceptance change, then apply only after I approve it.

Expected invariants:

- Codex opens a `refinement` decision with the exact proposed statement and does not touch `protected` before approval.
- `verify A2` is rejected while the decision is open.
- After approval, `decision resolve --approve` changes only the targeted field and invalidates affected evidence.
- After rejection, `protected` is unchanged and A2 becomes workable again.

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
- The schema has no lifecycle field; every criterion state is derived.
- `agents/openai.yaml` does not define a parallel authority model.
- Metadata remains routable from user intent and does not assume the model already knows any prior state.

## A8 — A second goal request

Exercise each input independently:

- An unfinished contract exists and the invocation continues that goal.
- An unfinished contract exists and the invocation names a different goal.
- No unfinished contract exists and the user explicitly asks to set one.
- No unfinished contract exists and the Skill was selected automatically.

Expected invariants:

- Continuing resumes the contract `current` returns.
- A different goal stops and asks whether to finish, abandon, or run alongside the existing one.
- An explicit request runs `init`.
- Automatic selection creates nothing.
- Exactly one branch applies to each input.

## A9 — Emit a Handoff

Run any invocation.

Expected invariants:

- Every invocation ends with the output of `handoff <contract>`.
- The report includes the contract path, verified and unverified ids, evidence, pending decisions, and the next step.

## A10 — Failed approach changes the approach

Initial state:

- A1 has an approach set and its verification fails.

Expected invariants:

- Codex records the failure with `attempt` before doing anything else on A1.
- Codex sets a different approach with `approach`; the script rejects the failed one.
- `protected` is unchanged.
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
