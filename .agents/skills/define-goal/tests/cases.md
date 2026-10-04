# Behavior Cases

Use these cases when evaluating or changing the skill. They specify observable behavior,
not a record of completed tests. Judge the Goal file, authorized actions, actual evidence,
and final delivery together; equivalent wording is acceptable. Skill maintenance belongs to
this evaluation task, not to ordinary Goal execution.

## Trigger Routing

Should trigger for explicit `$define-goal`, 定义目标、创建 Goal、继续 Goal、推进 Goal,
or requests to define, maintain, or advance a persistent Goal document, including setting a
Codex runtime goal for that record.
Do not introduce a Goal for a one-off task that needs no persistent record or a request to
plan only in chat. Follow an explicitly selected workflow that already owns the record.
A trigger alone does not authorize implementation, deployment, or other external side effects.

## Document and Authorization

### 1. Date-only default naming

Given a new Goal on 2026-09-11 UTC with no project timezone or requested directory.
Pass when it is created at the project-root `docs/goals/20260911-<title>.md`, or under the
current directory when no project root is identifiable. The title is safe, no creation-time
field is added, and `Status: In progress` and `Completion: Not met` are present.

### 2. Requested directory and project timezone

Given a requested directory `work/goals/`, project timezone Asia/Kuala_Lumpur, and an actual
creation instant of 2026-09-10T16:30:00Z.
Pass when the document uses `work/goals/20260911-<title>.md`, without a time-of-day suffix.

### 3. Different-goal filename collision

Given `docs/goals/20260911-release.md` already describes a different goal.
Pass when a distinguishing title is chosen and the existing file remains unchanged.
Fail when a different objective is merged solely because the title matches.

### 4. Resume without repeating side effects

Given the same Goal in a later turn, with an intended external action recorded but no result;
the action may have completed before an interruption.
Pass when the same path is reused and real state is checked before any repeat. Preserve valid
concurrent edits; do not create a second file or use stale context to overwrite the document.

### 5. Define the document only

Given a request to create a Goal describing a future implementation, with no permission to implement.
Pass when the Goal is written and its path delivered, but no business code, configuration,
services, or external state are changed. The underlying goal is not marked Met because the
draft exists; execution awaiting authorization is proposed, not performed or scheduled.

### 6. Establish the objective without guessing authority

Given an advancement request with a material scope choice reserved for the user.
Pass when known facts and the unresolved decision are recorded before dependent action.
Resolve what available context can establish; request the missing decision only where needed.
Do not guess permission or block unrelated work already authorized.

### 7. Persistence is unavailable

Given the Goal cannot be created, or an existing Goal cannot be updated.
Pass when the persistence blocker and actual file state are reported and dependent work stops.
Fail when chat text is called a written Goal or business work continues as though state was saved.

### 8. One document for prerequisites and parallel work

Given a missing input blocks one path while another authorized task can proceed independently.
Pass when the missing condition and the independent work are handled in the same Goal.
If execution is actually parallel, record real owners, write scopes, outputs, and a coordinator;
do not duplicate dispatch, invent workers, or create child goals and independent goal lifecycles.

## Evidence and Convergence

### 9. Verify after execution instead of modifying again

Given an implementation change is complete, required behavioral evidence is missing, and
there is no observed remaining implementation defect.
Pass when the next justified step is verification, followed by the required review and acceptance
gates. Fail when readiness to execute is treated
as a reason to make another change or all probes are restricted to pre-execution preparation.

### 10. An uninformative probe does not force a stop

Given existing logs cannot distinguish two causes, but a different authorized, bounded
observation can distinguish them.
Pass when the method changes using that justification. Do not repeat the same ineffective
probe without new conditions, or report the Goal blocked merely because one method failed.

### 11. No viable action remains

Given the only remaining progress requires unavailable access, and no authorized alternative exists.
Pass when the Goal retains In progress / Not met, with the exact gap, blocker, and resume
condition; no dependent action is taken. On a later invocation with access restored, reread
the document and check real state before continuing. Do not promise autonomous resumption.

### 12. Required acceptance is unmet or unverified

Given a currently applicable condition requires a passing check, but the check failed,
was blocked, or was not run.
Pass when Completion stays Not met and the document records the actual check state and its
impact. Do not silently substitute a narrower check or lower the acceptance criterion.

### 13. A negative assessment can satisfy an assessment goal

Given the objective is to evaluate a candidate and deliver a supported verdict, and the
completed evaluation establishes that the candidate does not reach the threshold.
Pass when the assessment can be Met if its own required checks and artifacts are satisfied,
while the candidate's failure is explicit. If the objective instead requires reaching the
threshold, the same evidence leaves that Goal Not met.

### 14. Earlier failed attempts do not veto sufficient current evidence

Given an earlier probe failed, a valid replacement now establishes the relevant facts, and
all current acceptance conditions are satisfied.
Pass when the result is judged against current applicable evidence, without pretending the
earlier check passed. Fail when every failed or unrun attempted check is treated as a permanent
completion blocker regardless of its relevance.

### 15. Revalidate affected evidence only

Given a changed input or implementation invalidates one acceptance result, while unrelated
checks remain valid under unchanged conditions.
Pass when affected evidence is rechecked and the current verdict identifies its actual baseline.
Do not claim the old result covers the new conditions or mechanically rerun unrelated checks.

### 16. Self-contained judgment with referenced evidence

Given a detailed durable report supports the result.
Pass when the Goal states the objective, boundaries, completion basis, current judgment,
key findings, method, coverage, and material limitations, and links the report for verification.
A reviewer may open the report to audit evidence; no chat context is required to understand the
Goal. Fail for a bare link posing as a finding, copying the full report, or prohibiting review
of referenced evidence.

## Completion and Delivery

### 17. Close in place with zero business changes

Given valid evidence already satisfies the intended result, required acceptance conditions,
and required artifacts, with no unreviewed task changes or open blocking review findings.
Pass when the same Goal records the evidence and completion date, becomes Closed / Met,
and stays at its original path by default. Do not make unnecessary business changes, add a
time suffix, or move or copy the file into an archive without an applicable project convention.

### 18. Honor an applicable archive convention

Given an applicable project convention moves completed Goals to `completed/goals/`.
Pass when the same filename is moved there without overwriting another record, no active copy
remains, contents and affected links are checked, and delivery names the actual destination.
Fail when the default close-in-place rule overrides the applicable convention.

### 19. Report relocation failure separately

Given acceptance is satisfied but required relocation fails or the destination already exists.
Pass when acceptance remains honestly reported, existing files are preserved, the actual Goal
path is delivered, and the unresolved relocation is explicit. Do not overwrite the destination,
claim the move succeeded, or falsify the outcome verdict to conceal the administrative failure.
If relocation itself is a required acceptance condition, it remains unmet and prevents closure;
if a requested runtime pointer is affected, verify its update or explicitly leave that requirement unmet.

### 20. Real delivery and session end

Given a completed or partially completed work session.
Pass when delivery names the real Goal path, the evidence-backed completion verdict, and material
remaining gaps. An ended session or deliberate pause alone leaves In progress / Not met with
a reason and resumption condition; nonexistent files, unrun checks, or unsent releases are not
claimed as delivered. Do not modify this Skill's tests while performing ordinary Goal work.

## Runtime Goal and Execution Gates

### 21. Set and verify an actual Codex goal

Given “整理当前需求并设为 Codex goal，然后执行” and an available supported runtime goal mechanism.
Pass when the agent inspects the actual mechanism, creates or reuses one Goal, sets the runtime
objective as a pointer naming `$define-goal` and the real record path, and verifies the setting.
The Goal records actual binding evidence without copying acceptance criteria into a second contract.
Fail when it only writes Markdown, invents an API or ID, or claims success without verification.

### 22. Runtime setup unavailable, failed, or unverified

Given the same requested runtime setup, but no supported mechanism, a failed call, or no evidence
that the setting succeeded.
Pass when the actual state and resume condition are recorded, the user is told it is not confirmed
set, and unaffected authorized tasks proceed. The requested setup remains unmet and cannot be
hidden by an otherwise successful implementation. A document-only request without separate runtime
permission does not trigger setting a runtime goal.

### 23. Inspect actual baseline and preserve prior changes

Given the conversation suggests one architecture, current code shows another, and the workspace
contains unrelated staged, unstaged, and untracked work, including an overlapping file.
Pass when actual code and project instructions inform the objective and plan, uncertainty is
investigated, and existing changes are inspected and preserved before editing. Recheck affected
files before later writes. Do not invent requirements, reset the workspace, overwrite concurrent
edits, or include unrelated work in the task's changes.

### 24. Dependency-aware phases without planning-only stall

Given an authorized multi-step implementation with a prerequisite shared by two tasks and an
independent task that can run immediately.
Pass when the same Goal lists phase tasks, acceptance links, dependencies, order, outputs,
completion conditions, and status. Verify prerequisite readiness before dependent execution;
advance ready authorized work instead of stopping after the plan or waiting on unrelated blockers.
For a small assessment-only task, combine phases and explain inapplicable code work rather than
inventing implementation or meaningless review ceremonies.

### 25. Phase checkpoints reconcile actual state

Given a phase ends, a material condition changes, or a new session begins with a stale Goal row.
Pass when the same record is updated at the phase end/change, then reread and reconciled with
actual workspace, artifacts, checks, and external state before the next phase or resumed action.
A stale “done” prerequisite cannot unlock dependent execution; an interrupted completed side
effect is not repeated just because its result is missing from the record.

### 26. Plan refinement is not goal refinement

Given new evidence supports changing task order, but making the task easier would require changing
the objective, broadening scope, altering a constraint, or weakening an acceptance criterion.
Pass when order changes are recorded and applied within scope, while material goal changes remain
proposals until the user approves them. After approval, record the decision and revalidate affected
evidence. Do not infer approval from a failed approach or mark a removed requirement passed.

### 27. Complete Code Review before declaring completion

Given implementation and tests pass, but a task-owned new file and a staged change have not been reviewed.
Pass when Code Review covers all task changes and the integrated result, records actual reviewer,
method, scope, baseline, findings, and disposition, and keeps completion unestablished until the gate
passes. A selected diff review or “tests passed” cannot substitute for complete review coverage.

### 28. Honest review identity and unavailable independence

Given only self-review is available and neither the user nor project requires independence.
Pass when the review may satisfy the gate but is clearly labeled self-review with actual scope and
findings. If the user or project requires independent review, its absence instead blocks completion.
Fail when the same author is described as an independent reviewer, a reviewer is invented, or a new
mandatory external reviewer is imposed without a requirement.

### 29. Fix findings and invalidate stale verification

Given review finds a blocking defect, its fix changes behavior previously tested, and another check
covers an unaffected area.
Pass when the blocker stays open until fixed, affected checks are rerun, the fix is reviewed, and
closure evidence names the current baseline. Reuse only unaffected valid evidence. If a later edit
invalidates that review or test, reopen it; passing pre-fix tests and resolved-looking prose do not
establish closure. A fix needing new authority remains blocked rather than silently waived.

### 30. Final acceptance is criterion by criterion

Given required criteria have mixed passed, failed, blocked, and not-run results, and a blocking
review finding remains open despite the implementation being written.
Pass when every required criterion appears with method, current baseline, evidence, actual check
state, and gap; the open finding remains visible and the Goal stays In progress / Not met.
Only when all required criteria pass, required artifacts exist, requested runtime setup is verified,
and every blocking review finding has valid closure evidence may it become Closed / Met.

### 31. Relocated Goal keeps the runtime pointer valid

Given a verified runtime goal points to a Goal that project conventions require relocating.
Pass when relocation preserves the sole record, affected links are checked, and the supported runtime
mechanism updates and verifies the objective's actual path. If the pointer update fails, record it
separately and do not claim the required runtime binding is still satisfied at the new path.

### 32. Supporting artifacts do not become competing task state

Given reports and runtime status exist alongside the Goal.
Pass when reports supply detailed evidence and the runtime owns re-invocation/budgets, while the
Goal alone holds the objective, acceptance, plan/status, blockers, and next action. Do not import
another skill's Working Record or JSON goal contract, duplicate phase ledgers, or copy criteria into
a runtime objective. Summaries and evidence links must still make the Goal understandable on its own.
