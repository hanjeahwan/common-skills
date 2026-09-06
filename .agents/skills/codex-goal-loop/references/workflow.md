# Goal Workflow

Apply the authority and invariants in [`SKILL.md`](../SKILL.md) throughout this workflow. Every contract read or write goes through `python3 <skill-root>/scripts/goal.py`; `<contract>` below is the workspace-relative locator.

## Native Objective And Locator

`init` prints the exact text to store in the native objective:

```text
Contract: .goal/<title>-<YYYYMMDD-HHmmss>.json

Pursue the referenced contract's protected objective, acceptance criteria,
constraints, and non-goals as the sole authority for what this Goal means.
Drive every acceptance criterion to verified with current observable evidence
through scripts/goal.py, then complete this Codex Goal. Do not change the
protected section without an approved refinement decision.
```

- Locator format: one normalized workspace-root-relative path without globs, environment variables, or parent-directory escapes.
- Locator boundary: the resolved path stays below the active workspace. The script refuses every other path.
- Execution precondition: `validate <contract>` exits 0.
- Authority-failure condition: the native objective contains at least one locator but does not resolve exactly one normalized, workspace-contained, existing contract.
- Authority-failure action: stop Goal execution and request contract restoration or `/goal edit`.
- Invalid-contract condition: `validate` reports schema or invariant errors.
- Invalid-contract action: stop Goal execution, report the errors verbatim, and request restoration or `/goal edit`.
- Legacy-contract condition: the locator resolves to a Markdown contract from an earlier version of this Skill.
- Legacy-contract action: stop, propose an `init` built from its Protected Goal, and after approval ask the user to install the new locator with `/goal edit`. Legacy Working State evidence is not migrated; re-verify every criterion.
- Prohibition: never reconstruct or hand-edit a contract.

## Route Native Goal State

Read native Goal state once at the start of the invocation.

- No-Goal condition: no unfinished native Goal exists.
- No-Goal action: start a Goal only when the user explicitly requested creation.
- Active-Goal condition: the native Goal is active.
- Active-Goal action: resolve the contract through the locator branches in this workflow.
- Paused-or-blocked condition: the native Goal is paused or blocked.
- Paused-or-blocked action: stop Goal execution, report the last observed status and the native user action required to resume, and do not run the loop.
- Complete-Goal condition: the native Goal is complete.
- Complete-Goal action: treat the native Goal as finished.
- New-Goal condition: the user makes a new explicit creation request.
- New-Goal action: start another Goal.

## Start An Explicit Goal

- Start condition: no unfinished native Goal exists and the user explicitly requested Goal creation.
- Contract investigation: distinguish verified facts, assumptions, acceptance conditions, constraints, and non-goals.
- Ambiguity condition: a missing decision changes Goal scope or success.
- Ambiguity action: present the proposed objective and criteria and request the missing decision before `init`.
- Local-contract condition: the user did not request cross-machine, fresh-clone, or cloud use.
- Local-contract action: run `init` without `--path`. The script writes `.goal/<title>-<datetime>.json`, appends `/.goal/` to the workspace-root `.gitignore` when absent, and refuses to write while git does not ignore the path.
- Tracked-contract condition: the user explicitly requires cross-machine, fresh-clone, or cloud use.
- Tracked-contract approval gate: obtain approval for a workspace-root-relative tracked project-document path, then run `init --path <path>`.
- Tracked-contract prohibitions: do not ignore, commit, or publish the tracked contract automatically.
- Native creation action: call `create_goal` with the exact `Contract:` locator and execution clause printed by `init`.
- Verification action: re-read the native Goal and run `status <contract>` before the first loop pass.
- Creation-failure condition: native Goal creation fails after the contract is written.
- Creation-failure action: retain the contract as an unlinked draft, report the exact failure, and do not run the loop.
- Retry condition: a later explicit creation request matches an unlinked draft.
- Retry action: reuse the matching draft.
- Supersede condition: the requested Goal cannot use the matching draft.
- Supersede action: obtain explicit user approval before superseding the draft.

The script requires Python 3.10+ and the `jsonschema` package.

```bash
python3 <skill-root>/scripts/goal.py init \
  --title "<short title>" \
  --objective "<objective>" \
  --accept "<A1 statement>" --accept "<A2 statement>" \
  --constraint "<constraint>" --non-goal "<non-goal>" \
  --risk "<known risk>" \
  --max-attempts 10
```

## Resolve An Active Goal

- Resume condition: the native objective contains exactly one valid locator to an existing valid contract, and the invocation does not request a different Goal.
- Resume action: resume with that contract.
- Invalid-contract condition: the Authority-failure or Invalid-contract condition above applies.
- Invalid-contract action: stop Goal execution and request restoration or `/goal edit`.
- Matching-intent condition: the native objective has no locator and matches the requested intent.
- Matching-intent action: draft the objective and criteria, obtain user approval, run `init`, and ask the user to install the printed locator with `/goal edit` before resuming.
- Conflicting-intent condition: the native objective has no locator and a different intent, or the resolved contract belongs to a Goal other than the one requested by the invocation.
- Conflicting-intent action: stop Goal execution and ask the user to continue, complete, pause, or clear the existing Goal.

## Resume

1. Resolve exactly one valid `Contract:` locator.
2. Run `status <contract>` and read the whole checkpoint.
3. Re-observe relevant repository, tool, and external state.
4. For each verified criterion, check its invalidation conditions against current evidence. Run `invalidate <contract> <id> --reason` for each condition that occurred.
5. Run `next <contract>` and act on its result.

Default `.goal/` contracts resume only while the same workspace data exists. A native lifecycle handle does not make a missing local contract portable.

## Commands

| Command | Loop phase | Effect |
| --- | --- | --- |
| `status <contract> [--json]` | Observe | Print the whole checkpoint with derived criterion states (open, blocked, exhausted, verified) and the next step. |
| `risk <contract> --add ... --drop N` | Observe | Add an open risk or drop a resolved one. Risks inform the agent; they do not block criteria. |
| `invalidate <contract> A1 --reason ...` | Observe | Return a verified criterion to unverified when an invalidation condition occurred. |
| `next <contract> [--json]` | Decide | Name the single criterion to pursue, or report pending decisions or readiness. |
| `approach <contract> A1 --approach ... [--next-action ...]` | Decide | Set the current approach. Rejects an approach already recorded as failed, or any approach once `max_attempts` is reached. |
| `verify <contract> A1 --summary ... --locator ... --invalidated-by ...` | Verify | Mark the criterion verified with evidence, replacing any previous evidence. Rejected while a decision blocks it. |
| `attempt <contract> A1 --outcome ... [--approach ...]` | Verify | Record that the current approach failed and clear it. Recording an approach that was never set passes the same gates as `approach`. |
| `decision open <contract> --kind refinement\|input --request ... [--blocks ...] [--target objective\|max_attempts\|constraints\|non_goals\|A1 --operation set\|add\|remove --proposed ...]` | Verify | Record a request only the user can answer. An open objective refinement blocks every criterion. |
| `decision resolve <contract> D1 --approve\|--reject [--note ...]` | Resume | Record the user's answer. An approved refinement rewrites `protected` and invalidates affected evidence. |
| `ready <contract>` | Complete | Exit 0 only when every criterion is verified and no decision is open; list each falsifier. |
| `handoff <contract> --native active\|paused\|blocked\|complete` | Handoff | Print the end-of-invocation report. |
| `validate <contract>` | Any | Check the contract against the schema and invariants. |

- Use one criterion at a time: the one `next` returns.
- Record every failed verification with `attempt` before changing the approach.
- Use `decision open --kind refinement` to propose an objective or criterion change. Present the request verbatim and wait; never apply it yourself.
- Use `--blocks` on a decision only for criteria that truly cannot advance until it is resolved. A refinement blocks its target criterion implicitly.
- When `next` reports a criterion as exhausted, open a refinement decision (the criterion or objective is wrong) or an input decision that blocks it (something only the user can supply). Approval of either resets that criterion's attempts; rejection leaves it exhausted.

## Native Lifecycle

### Continue

- Transition condition: `next` returns a criterion to pursue.
- Native action: leave the native Goal active.
- Report action: name the criterion and next action.

### Blocked

- Report condition: `next` reports that only open decisions remain, that every remaining criterion is exhausted, or an authority boundary or unavailable required input prevents progress.
- Immediate action: open the decision with `decision open --kind input`, then report the exact request.
- Native transition condition: the current native Goal tool contract permits `blocked`.
- Native transition action: call `update_goal({ status: "blocked" })`.
- Active-state condition: the native blocked transition is not yet permitted.
- Active-state action: leave the native Goal active. The unchanged open decision is the evidence that the same blocker persists across Goal turns.
- Counter prohibition: do not store a separate blocker counter.

### Complete

Call `update_goal({ status: "complete" })` only when every completion condition passes:

- `ready <contract>` exits 0.
- Every normal path affected by the Goal has current verification evidence.
- Every falsifier listed by `ready` whose source or tool is available within current authority has been checked and did not occur.
- Every validation command explicitly required by `protected` has succeeded.

After native completion succeeds, report the final status and usage returned by the tool. The contract stores no completion flag.

## Handoff

At the end of every invocation, run `handoff <contract> --native <observed status>` and report its output:

```md
Native Goal as last observed: active | paused | blocked | complete
Contract: <workspace-relative-path>
Acceptance: verified [...]; unverified [...]
Evidence: most important current observations
Pending decision: exact external input required, if any
Next: next criterion and action, required decision, or completion statement
```
