# Goal Template

Use this starting point for one authoritative Goal. Combine sections and keep entries brief for
small tasks, but retain the objective, boundaries, acceptance, phase plan/status, evidence, review,
blockers, and next step. Mark genuinely inapplicable items with a reason. State unknowns honestly
and remove unused prompts. The date-only filename supplies creation date; add no creation-time field.

```markdown
# <Goal title>

Status: In progress
Completion: Not met

## Objective and Boundaries

<The user result that should hold, derived from conversation, project rules, and actual artifacts.>
<Scope, non-goals, constraints, and work actually authorized; cite relevant sources.>
<Baseline: relevant version, inputs, environment, existing changes and preservation constraints.>

## Runtime Goal

<If requested: actual runtime mechanism, goal identifier if supplied, pointer to this document,
verified setting/readback evidence, or exact failure/unavailability and resume condition.>
<Otherwise: Not requested. Do not claim that writing this file sets a native runtime goal.>

## Acceptance Criteria and Evidence

| ID | Required result / constraint | Verification method | Current baseline and evidence | Check state | Gap / next action |
| --- | --- | --- | --- | --- | --- |
| A1 | <observable outcome> | <how to establish it> | <source, result, coverage; initially none> | not run | <next check> |

<Use passed, failed, blocked, or not run. No required criterion may be omitted at final acceptance.>

## Phase Plan and Status

| Phase / task | Acceptance IDs | Dependencies and order | Output | Completion condition | Status |
| --- | --- | --- | --- | --- | --- |
| <phase and concrete task> | A1 | <prerequisite IDs or none; sequence/parallelism> | <artifact/result> | <observable readiness> | pending |

<Cover current-state verification, planning, prerequisites, execution, verification, review,
repair/reverification, and final acceptance; combine phases or explain inapplicability as needed.>
<For real parallel work: owners, write scopes, outputs, and the shared-record coordinator.>

## Current Judgment and Action

<Established facts, inferences, unknowns, and missing conditions affecting the next decision.>
<Current phase and next authorized action with expected feedback; or proposed action awaiting approval.>
<Blockers: affected tasks/criteria, what can still proceed, exact resume condition and who can resolve it.>
<Latest checkpoint: completed phase or material change, actual state reconciled, evidence invalidated.>
<Approved material objective/scope/constraint/criteria changes: user decision and affected evidence.>

## Review and Repair

<Reviewer identity and method: self-review or genuinely independent review; reviewed scope/baseline.>
<For code: review all task changes and the integrated result. For non-code: artifact review and
why Code Review is inapplicable. If required independent review is unavailable, record a blocker.>

| Finding | Blocking? | Disposition / fix | Reverification and review evidence | State |
| --- | --- | --- | --- | --- |
| <finding or explicitly no findings> | <yes/no> | <actual action> | <current result and baseline> | <open/closed> |

## Result and Final Acceptance

<Actual result and artifacts; key findings and limitations, with durable evidence links.>
<Check every required acceptance row against current evidence and every blocking review finding
against closure evidence. Invalidate and rerun affected checks/reviews after later changes.>
<Completion verdict and remaining gaps. Set Closed / Met only after the entire gate passes.>
```

## Checkpoints and Evidence

Update this record after each phase and material change. Before resuming or entering a phase,
reread it and check actual workspace, dependencies, artifacts, and any previously attempted side
effects. Preserve existing changes. A prerequisite stays here, including what it enables and how
readiness is verified. No child Goals or second task-state record are needed.

Keep key findings and limitations here; a bare link is not a result. Link durable reports and source
artifacts for detailed verification instead of copying them. Label project-root-relative paths;
use document-relative Markdown links and recheck them after relocation. Keep the runtime objective
as a pointer to this document and `$define-goal`, not a second copy of criteria or a status ledger.

For a document-only request, stop after the requested definition or update. Execution awaiting
authorization is proposed, not scheduled or performed; the underlying objective remains Not met.

On completion, replace pending-action prompts with results, set `Status: Closed` and `Completion: Met`,
and add `Completed on: YYYY-MM-DD` using the project's timezone or UTC. Keep the file in place unless
project conventions require relocation. Verify any required runtime pointer update too. If acceptance
is unmet, retain `Status: In progress` and `Completion: Not met` with the gap and resume condition.
Report relocation failures separately from the outcome; do not claim a required delivery condition
passed when it did not. A session end or negative experimental finding is not a verdict by itself.
