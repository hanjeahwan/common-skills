# Goal Template

Use this structure for one persistent Goal. `SKILL.md` owns the workflow and completion rules;
this file supplies recording fields, not a second policy. Compact or combine sections without
omitting applicable information. Preserve existing records when adding missing fields, state
unknowns honestly, and remove unused prompts. The date-only filename supplies the creation date.

```markdown
# <Goal title>

Status: In progress
Completion: Not met

## Problem, Goal, and Boundaries

<Problem/current gap and the desired user outcome, in your own words.>
<Scope, non-goals, constraints, and work actually authorized.>
<Material assumptions or unknowns, their effect, and how to resolve them.>
<Relevant versions, inputs, environment, or comparison baseline when needed.>

## Acceptance Criteria

| Criterion | Observable required result | Verification method | Current result | Evidence |
| --- | --- | --- | --- | --- |
| <Criterion> | <What must hold> | <Check or observation> | <passed / failed / blocked / not run> | <Reference below> |

## Phase Plan

| Phase / tasks | Dependencies and order | Expected artifacts | Completion conditions | Status |
| --- | --- | --- | --- | --- |
| <Phase and tasks> | <Prerequisites and sequence> | <Outputs> | <Criteria/checks permitting exit> | <pending / in progress / completed / blocked / cancelled; reason> |

<Include investigation, prerequisites, execution, verification, review/repair, and final acceptance
at the detail needed for this task; explain combined or unnecessary phases. For document-only work,
label any future plan as proposed, or state that execution has not been planned.>
<For actual parallel work only: owners, write scopes, outputs, shared-record coordinator.>

## Current State and Next Action

<Current phase and established facts, distinguishing observations from inferences.>
<Next authorized action and expected feedback; work awaiting permission is only proposed.>
<Blockers: cause, affected tasks, and resume condition; identify independent work that can continue.>
<Material changes to the plan and why; references to affected criteria/evidence, not duplicate results.>

## Review and Evidence

### Verification evidence

<For each result: source, relevant baseline, method, actual result, coverage, and limitations.>
<Actual artifact paths and durable report references; summarize findings rather than paste raw logs.>
<Historical evidence invalidated by later changes, with replacement evidence or an explicit gap.>

### Review

<Actual reviewer or method: self-review / independent review; scope and reviewed baseline.>
<Required review not yet performed or blocked, and its effect on acceptance.>
<For no-change work, what artifacts/findings were assessed and why there is no code diff to review.>

| Finding | Evidence / affected path | Blocking? | Resolution and recheck evidence | State |
| --- | --- | --- | --- | --- |
| <Finding, or explicit none if reviewed> | <Trigger and baseline> | <Yes/no and reason> | <Fix, verification, renewed review> | <Open/closed> |

### Final acceptance

<Overall verdict supported by the criterion results above and the review gate; do not copy a second
independent set of criterion statuses here. Include remaining gaps and material limitations.>
<When completion is established under SKILL.md, update the header and add Completed on: YYYY-MM-DD.>
```
