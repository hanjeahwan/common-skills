# Goal Template

Use this starting point for one persistent Goal document. Merge or omit sections as needed,
but keep the result, boundaries, completion basis, current judgment, and next step understandable
without the conversation. State unknowns honestly and delete unused prompts. The date-only
filename supplies the creation date; do not add a creation-time field.

```markdown
# <Goal title>

Status: In progress
Completion: Not met

## Objective and Boundaries

<The user result that should hold.>
<Scope, non-goals, applicable constraints, and the work actually authorized.>
<Relevant version, inputs, environment, or comparison baseline, only when needed for judgment.>

## Completion Basis

<Observable results sufficient to establish the objective, and how to verify them.>
<Required checks and constraints, including what their results must establish.>

## Current Judgment and Action

<Established facts, material unknowns, and missing conditions that affect the next decision.>
<The next authorized action and expected feedback, or the blocker/stop reason and resume condition.>

## Results and Evidence

<Actual results, distinguishing observations from inferences; mark unverified claims explicitly.>
<Key evidence: source, relevant baseline, method, result, and coverage.>
<Actual artifact paths; failed, blocked, or unrun checks and their effect on acceptance.>
```

## Use Only What the Task Needs

A prerequisite stays in this document: identify the missing condition, the action it enables,
and how readiness will be checked. For actual parallel work, add owners, write scopes, outputs,
and the coordinator of the shared record. Do not create child Goal documents.

Summarize the findings and limitations supporting the verdict. Link durable detailed reports
and source artifacts where useful; they may be consulted to verify the evidence. A bare link
is not a result, and copying the full report is unnecessary. Label project-root-relative paths;
use document-relative paths for Markdown links and recheck them if a project convention moves the file.

For a document-only request, record the scope of that request and stop after drafting or updating.
Do not infer permission to execute the underlying work or mark it complete because the draft exists.
When a next action is awaiting authorization, label it as proposed, not scheduled or performed.

On completion, replace pending-action prompts with the actual result, set `Status: Closed` and
`Completion: Met`, and add `Completed on: YYYY-MM-DD` using the project's timezone or UTC.
Keep the file in place unless applicable project conventions require archiving or relocation.
When the completion basis is unmet, retain `Status: In progress` and `Completion: Not met` and
explain the remaining gap or stop reason. Session end, file location, and a negative experimental
finding are not verdicts by themselves; judge them against the actual objective.
