# Goal Workflow

Apply the authority and invariants in [`SKILL.md`](../SKILL.md) throughout this workflow. Every contract read or write goes through `python3 <skill-root>/scripts/goal.py`; `<contract>` below is the workspace-relative contract path.

## Contract Discovery

The contract is the only state this Skill reads. `current` resolves it:

```bash
python3 <skill-root>/scripts/goal.py current
```

- Definition: a contract is unfinished while `ready` would fail, that is while any criterion is unverified or any decision is open.
- One-contract condition: exactly one unfinished contract exists under `.goal/`.
- One-contract action: use it.
- No-contract condition: no unfinished contract exists.
- No-contract action: report that, naming any finished contract the error lists so a just-completed goal is not reported as missing. Start a new one only on an explicit request.
- Many-contract condition: more than one unfinished contract exists.
- Many-contract action: stop and ask which one to use. Do not guess.
- Tracked-contract rule: `--path` writes outside `.goal/` and is not discovered, because `.goal/` is ignored by git and `init` refuses a `--path` inside it. Pass a tracked contract's path explicitly, and ask the user for it after a context reset rather than concluding no goal exists.
- Invalid-contract condition: `current` names a contract under `invalid:`, or `validate <contract>` reports errors.
- Invalid-contract action: stop, report the errors verbatim, and ask the user to restore the file. Do not treat an unreadable contract as a missing one.
- Legacy-contract condition: `current` names a Markdown contract under `legacy:`.
- Legacy-contract action: stop, propose an `init` built from its Protected Goal, and create it after approval. Legacy Working State evidence is not migrated; re-verify every criterion.
- Prohibition: never reconstruct or hand-edit a contract, and never resolve it from anything but `.goal/` or an explicit path.

## Start A Goal

- Start condition: the user explicitly asked to set a goal, for example `$codex-goal-loop <intent>`.
- Non-start condition: automatic Skill selection, or `$codex-goal-loop` with no objective, does not authorize creating anything.
- Contract investigation: distinguish verified facts, assumptions, acceptance conditions, constraints, and non-goals.
- Ambiguity condition: a missing decision changes goal scope or success.
- Ambiguity action: present the proposed objective and criteria and request the missing decision before `init`.
- Local-contract condition: the user did not request cross-machine, fresh-clone, or cloud use.
- Local-contract action: run `init` without `--path`. The script writes `.goal/<title>-<datetime>.json`, appends `/.goal/` to the workspace-root `.gitignore` when absent, and refuses to write while git does not ignore the path.
- Tracked-contract condition: the user explicitly requires cross-machine, fresh-clone, or cloud use.
- Tracked-contract approval gate: obtain approval for a workspace-root-relative tracked project-document path, then run `init --path <path>`.
- Tracked-contract prohibitions: do not ignore, commit, or publish the tracked contract automatically.
- Existing-contract condition: an unfinished contract already exists and the request names a different goal.
- Existing-contract action: stop and ask whether to finish or abandon the existing one first. Abandoning means the user deletes or moves that `.goal/` file; that is not a hand-edit of contract content. Two unfinished contracts make `current` ambiguous, so do not start a second one without that decision.
- Verification action: run `status <contract>` before the first loop pass.
- Runtime-goal condition: the user asks for a runtime goal over this work, either alongside `init` or in a later message.
- Runtime-goal action: use the pointer objective `init` printed. It names `$codex-goal-loop` and the contract path so unattended turns route back here, and it copies no acceptance criteria.
- Runtime-goal prohibition: do not restate the objective, criteria, or constraints in it, and do not manage its status afterwards.

## Finish

- Condition: `ready <contract>` exits 0.
- Falsifier check: for each criterion, check the falsifier `ready` prints when its source or tool is reachable within current authority.
- Validation check: every validation command required by `protected` has succeeded.
- Action: report completion and the evidence behind it. The contract stays on disk as a record; `current` stops returning it.
- Prohibition: do not mark anything complete while `ready` exits 1.

The script requires Python 3.10+ and the `jsonschema` package.

```bash
python3 <skill-root>/scripts/goal.py init \
  --title "<short title>" \
  --objective "<objective>" \
  --accept "<first criterion>" --accept "<second criterion>" \
  --constraint "<constraint>" --non-goal "<non-goal>" \
  --risk "<known risk>" \
  --max-attempts 10
```

## Resume

1. Run `current` to resolve the contract.
2. Run `status <contract>` and read the whole checkpoint.
3. Re-observe relevant repository, tool, and external state.
4. For each verified criterion, check its invalidation conditions against current evidence. Run `invalidate <contract> <id> --reason` for each condition that occurred.
5. Run `next <contract>`. Re-observe what its first undone step points to, drop steps that are already satisfied, then act.

Default `.goal/` contracts resume only while the same workspace data exists.

## Commands

| Command | Loop phase | Effect |
| --- | --- | --- |
| `current` | Observe | Print the single unfinished contract under `.goal/`, or fail when there is none or several. |
| `status <contract> [--json]` | Observe | Print the whole checkpoint with derived criterion states (open, blocked, exhausted, verified) and the next step. |
| `risk <contract> --add ... --drop N` | Observe | Add an open risk or drop a resolved one. Risks inform the agent; they do not block criteria. |
| `invalidate <contract> A1 --reason ...` | Observe | Return a verified criterion to unverified when an invalidation condition occurred. |
| `next <contract> [--json]` | Decide | Name the single criterion to pursue, or report pending decisions or readiness. |
| `approach <contract> A1 --approach ...` | Decide | Set the current approach. Rejects an approach already recorded as failed, or any approach once `max_attempts` is reached. |
| `step <contract> A1 --add ... --done N --drop N` | Decide, Act | Break the criterion into re-observable steps, mark one done after doing it, or drop one the workspace shows is unnecessary. |
| `verify <contract> A1 --summary ... --locator ... --invalidated-by ...` | Verify | Mark the criterion verified with evidence, replacing any previous evidence. Rejected while a decision blocks it or a step is undone. |
| `attempt <contract> A1 --outcome ... [--approach ...]` | Verify | Record that the current approach failed and clear it. Recording an approach that was never set passes the same gates as `approach`. |
| `decision open <contract> --kind refinement\|input --request ... [--blocks ...] [--target objective\|max_attempts\|constraints\|non_goals\|A1 --operation set\|add\|remove --proposed ...]` | Verify | Record a request only the user can answer. An open objective refinement blocks every criterion. |
| `decision resolve <contract> D1 --approve\|--reject [--note ...]` | Resume | Record the user's answer. An approved refinement rewrites `protected` and invalidates affected evidence. |
| `ready <contract>` | Complete | Exit 0 only when every criterion is verified and no decision is open; list each falsifier. |
| `handoff <contract>` | Handoff | Print the end-of-invocation report. |
| `validate <contract>` | Any | Check the contract against the schema and invariants. |

- Use one criterion at a time: the one `next` returns. Within it, do one step at a time and mark it done before starting the next.
- Write each step so a later invocation can check it from the workspace: a command to run, a file to inspect, an explicit list of ids. Steps are working state; add and drop them without approval.
- Record every failed verification with `attempt` before changing the approach.
- Use `decision open --kind refinement` to propose a change to `protected`. Present the request verbatim and wait; never apply it yourself. A proposal that no longer fits `protected` is refused when opened, and an approval of one that went stale reports what changed so the user can reject it.
- Use `--blocks` on a decision only for criteria that truly cannot advance until it is resolved. A refinement blocks its target criterion implicitly.
- When `next` reports a criterion as exhausted, open one of: a refinement whose target is that criterion, a refinement raising `max_attempts`, or an input decision that blocks it. Approving the first two makes it workable again, and approving the third clears its attempts. Approving a refinement of the objective, constraints, or non-goals does not, so pair it with one of the three when the criterion must continue.

## Handoff

At the end of every invocation, run `handoff <contract>` and report its output:

```md
Contract: <workspace-relative-path>
Acceptance: verified [...]; unverified [...]
Evidence: most important current observations
Pending decision: exact external input required, if any
Next: next criterion and step, required decision, or completion statement
```
