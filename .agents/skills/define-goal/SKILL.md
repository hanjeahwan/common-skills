---
name: define-goal
description: Define, update, or advance one persistent Goal record with dependency-aware execution, review, and evidence-based acceptance; bind a Codex runtime goal when requested. Use when the user asks to define a goal, set a Codex goal, create or continue a Goal document, or invokes "$define-goal", "定义目标", "创建 Goal", "继续 Goal", or "推进 Goal". Defining the document alone does not authorize its underlying work. Do not use for one-off tasks that need no persistent Goal document.
---

# Define Goal

One goal, one authoritative document. Keep the objective, boundaries, plan, status, evidence,
blockers, and next action together. Conversation is temporary working context. Do not create
child goals, duplicate records, or a second task-state system.

## Document Contract

- Path: `<dir>/YYYYMMDD-<title>.md`. Use the user-specified directory; otherwise use `docs/goals/`
  at the project root, identified by the nearest ancestor containing `.git` or the project's
  entry file. If no root can be identified, use `docs/goals/` in the current directory.
- Use the actual creation date in the project's timezone, or UTC when none is specified.
  Choose a short, filesystem-safe title and keep the filename. Reuse the same goal's existing
  document; for a different goal with a colliding name, choose a distinguishing title. Never overwrite.
- Read applicable project instructions and the user-specified or matching Goal before acting.
  If none exists, read [`references/goal-template.md`](references/goal-template.md) and create it
  before substantive action. Create directories as needed; scale the record to the task without
  dropping required information.
- Distinguish **define or refine the document** from **advance the underlying goal**. Do only
  the requested work; a Goal records authorization, never grants it. Document-only delivery
  stops after the requested definition or update, without claiming the underlying result.
- At every phase end and material change, update the same record. Before resuming or entering
  a new phase, reread it and reconcile with actual code, artifacts, checks, and external state.
  Check whether an intended side effect already ran before repeating it; preserve concurrent edits.
  If the record cannot be written, stop dependent work and report the persistence blocker.

## Codex Runtime Goal

A Markdown Goal is not a native runtime goal. When the user requests setting or continuing a
Codex runtime goal, inspect the current runtime's available tools and instructions. Use its
actual supported mechanism to set or update the goal, then verify the returned state or read it
back. Never invent an API, command, identifier, or successful setting.

Use an objective that points to this record and workflow, rather than copying criteria:

```text
Use $define-goal to pursue the Goal at <actual Goal path> until its final acceptance gate passes.
```

Record the verified binding and evidence in the Goal. The runtime controls re-invocation and
budgets; this document remains the authority for the objective, plan, and acceptance. Do not
create another contract or mirror a separate runtime task ledger. On resume, reconcile the
binding when relevant; after an authorized relocation, update and verify the pointer.
If the mechanism is unavailable, fails, or cannot be verified, record that exact state and the
resume condition, and say the runtime goal is not confirmed set. Continue unaffected authorized
work. A requested runtime setup remains unmet until verified; document creation alone cannot
satisfy it. Do not set a runtime goal for a document-only request unless separately requested.

## Workflow

Advance through **verify current state → plan phases → complete prerequisites → execute by
dependency → verify → Code Review → repair and reverify → final acceptance**. These are gates
within an adaptive loop, not a one-pass waterfall: discoveries can reopen earlier work, and
independent tasks can proceed together. For small tasks, combine phases; mark an inapplicable
step with a reason instead of inventing code changes, reviewers, or unnecessary work.

### 1. Establish the baseline and completion basis

Inspect the conversation, project rules, and relevant actual code or artifacts. Derive the
objective, scope, non-goals, constraints, and observable acceptance criteria from that evidence.
Distinguish facts, inferences, and unknowns; investigate resolvable uncertainty before dependent
work rather than inventing requirements. A user decision blocks only tasks that depend on it.
Do not investigate unrelated unknowns before an otherwise justified action.

Before editing, inspect the current workspace and existing changes, including staged, unstaged,
and untracked files when using Git. Identify task-owned changes and preserve unrelated or
concurrent edits. Recheck affected files before later writes; do not reset, overwrite, or fold
unrelated changes into the task. Record the relevant baseline and preservation constraints.

### 2. Plan phases and prerequisites in the same record

For every phase, record its tasks, dependencies, execution order, outputs, completion conditions,
and status. Link tasks to acceptance criteria. Keep the next executable action explicit.
A prerequisite supplies a condition needed by a particular path; record what it enables and
verify readiness before dependent execution. Do not treat a planned prerequisite as completed.
For actual parallel work, record real owners, write scopes, outputs, and the coordinator who
updates the shared Goal. Do not invent workers or independent goal lifecycles.

Adjust the plan when evidence justifies it. Material changes to the objective, scope, constraints,
or acceptance criteria require user approval before adoption; record the decision and revalidate
affected evidence. Reordering work does not authorize expanding scope or lowering acceptance.

### 3. Execute, observe, and verify

When an authorized action is ready and unblocked, take it; do not stop at planning. Record intent
and expected feedback before important side effects, then actual results and the next step.
Choose the smallest sufficient execution, repair, or probe. Verification is a probe, and an
unverified outcome is not automatically an implementation defect.

A failed method does not alone block the goal. Change methods when justified; repeat a strategy
only with new evidence, changed conditions, or bounded retries justified by a failure model.
When a path is blocked, record the affected tasks, exact blocker, next action, and resume condition;
continue independent authorized work. Stop dependent work when no viable authorized path remains
or an applicable limit is reached. Do not promise future re-invocation the runtime has not arranged.

Record each required check as **passed, failed, blocked, or not run**, with its source, baseline,
method, result, coverage, and effect on acceptance. Summarize key findings and limitations in the
Goal; link durable reports or artifacts for detail, without copying raw logs or secrets.

### 4. Review all changes, repair, and reverify

Before final acceptance, review the full task changes and integrated result against the objective,
project rules, scope, and acceptance criteria. For code changes, Code Review is mandatory; include
all task-owned staged, unstaged, and new files, not only a selected patch. For non-code work, review
the changed artifacts as appropriate and explain why Code Review is not applicable.

Record the actual reviewer, method, reviewed baseline and scope, findings, and disposition.
Label self-review as self-review; never present it as independent review. Use an independent
reviewer when available and appropriate. If independent review is required by the user or project
but unavailable, record a blocker; otherwise an honestly identified self-review can satisfy the gate.

Track blocking findings in the same Goal. Fix them within authorization, rerun affected checks,
and review the fixes before closing each finding with evidence. If a fix needs new authority,
record the blocker instead of waiving it. Later changes that invalidate a check or review reopen
that evidence: reverify and rereview the affected scope, retaining only unaffected valid evidence.

## Boundaries

- Follow an explicitly selected workflow that already owns the task record; do not add a competing Goal.
- Do not invent requirements, permissions, runtime capabilities, workers, performed actions, or evidence.
- Keep the requested objective and acceptance stable; proposing a change is not approval to adopt it.
- Document-only requests do not authorize execution, and runtime setup does not expand execution scope.

## Quality Gate and Delivery

Perform final acceptance criterion by criterion in the same Goal, recording the current baseline,
check outcome, evidence, and remaining gap. Close only when **every required acceptance criterion
passes, required artifacts exist, and every blocking review finding is closed with valid evidence**.
Required runtime setup, if requested, must also be verified. Code being written, a command succeeding,
a plan ending, or a file existing does not establish completion.

Judge failed earlier attempts and negative experimental findings against the actual objective;
they do not automatically prevent a supported assessment from completing. Never count a required
failed, blocked, or unrun check as passed or silently replace it with a narrower check.

- On completion, record the actual result, acceptance evidence, review disposition, material limitations,
  and completion date. Set `Status: Closed` and `Completion: Met`; keep the file in place by default.
- If project conventions require relocation, keep the filename and single record. Do not overwrite
  a destination; verify location, content, links, and any runtime pointer. Report relocation or
  pointer-update failure separately and keep any required delivery condition explicitly unmet.
- Otherwise retain `Status: In progress` and `Completion: Not met`, with the gap, next authorized
  action or blocker/stop reason, and resume condition. Session end is not goal completion.
- Deliver the actual document path, runtime-binding state when requested, completion verdict, key
  evidence, review method, and remaining gaps. Claim only operations and checks actually performed.
