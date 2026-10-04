# Goal Template

Use this structure for one persistent Goal. `SKILL.md` owns workflow, reconciliation, and completion
rules; this file supplies fields, not a second policy. Compact or combine sections without dropping
applicable information. Preserve valid content and concurrent edits, reconcile superseded current
claims in place, state unknowns honestly, and remove unused prompts. Keep existing filenames/headings
when usable; the date-only filename supplies the creation date.

```markdown
# <Goal title>

Status: In progress
Completion: Not met

## Problem, Goal, and Boundaries

<Problem/current gap and successful end state in user terms: this goal succeeds when ...>
<Scope, non-goals, constraints, and effective authorization with its decision/source.>
<Material unknowns or missing targets, their effect, and how to resolve them; do not invent metrics.>
<Selected approach and only the rationale/conditions needed for current decisions, not progress history.>

## Success Criteria and Acceptance

<One acceptance set for the outcome criteria and required delivery gates. Check that these cover the
in-scope user problem, not just completed steps; keep essential scenarios and supported thresholds explicit.>

| Criterion / kind | Observable required result | Verification method | Current result | Evidence |
| --- | --- | --- | --- | --- |
| <Criterion; outcome or delivery gate> | <What must hold> | <Check or observation> | <passed / failed / blocked / not run> | <Evidence reference or explicit gap> |

## Execution Plan and Current State

<Current phase and verified facts affecting the next decision; distinguish observations from inferences.>

| Phase / tasks | Task dependencies and order | Expected artifacts | Completion conditions | Task status |
| --- | --- | --- | --- | --- |
| <Phase and tasks> | <Prerequisites of each action> | <Outputs> | <Criteria/checks permitting exit> | <pending / in progress / completed / blocked / cancelled; reason> |

<Include necessary investigation, prerequisites, execution, verification, review/repair, and final
acceptance; explain combined or unnecessary phases. Task progress is not the criterion's check result.>
<Next authorized action and expected feedback; blocker cause, affected tasks, resume condition, and
independent work. Point to task/criterion entries rather than maintain a second status list.>
<For document-only work: future execution is proposed or unplanned, not scheduled.>
<For actual parallel work only: owners, write scopes, outputs, shared-record coordinator.>

## Review and Evidence

### Verification evidence

<For each result: executor, source, checked baseline (commit/working-tree state for code, relevant
inputs/resource state otherwise), method/command, actual result, coverage, and limitations.
Distinguish inspected worker evidence from personally run checks.>
<Actual artifact paths and durable report references with key findings; no raw logs or secrets.>
<Necessary historical observations, decisions, or failed checks: baseline, what superseded them, and
replacement evidence or unresolved gap. Keep obsolete next steps out of the current plan.>

### Review

<Actual reviewer or method: self-review / independent review; scope and reviewed baseline.>
<Required review not yet performed or blocked, and its effect on acceptance.>
<For no-change work, what artifacts/findings were assessed and why there is no code diff to review.>

| Finding | Evidence / affected path | Blocking? | Resolution and recheck evidence | State |
| --- | --- | --- | --- | --- |
| <Finding, or explicit none if reviewed> | <Trigger and baseline> | <Yes/no and reason> | <Fix, verification, renewed review> | <Open/closed> |

### Final acceptance

<Does current evidence establish the successful end state and all required gates? Refer to the one
criterion set above, without copying statuses or implementation progress. Expose remaining gaps and
material limitations; reconcile this verdict with current authorization, facts, and next action.>
<When completion is established under SKILL.md, update the header and add Completed on: YYYY-MM-DD.>
```
