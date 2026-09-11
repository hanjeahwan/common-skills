# Behavior Cases

Use these cases when evaluating or changing the skill. They specify observable behavior,
not a record of completed tests. Judge the Goal file, authorized actions, actual evidence,
and final delivery together; equivalent wording is acceptable. Skill maintenance belongs to
this evaluation task, not to ordinary Goal execution.

## Trigger Routing

Should trigger for explicit `$define-goal`, 定义目标、创建 Goal、继续 Goal、推进 Goal,
or requests to define, maintain, or advance a persistent Goal document.
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
Pass when the next justified step is verification. Fail when readiness to execute is treated
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
and required artifacts.
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

### 20. Real delivery and session end

Given a completed or partially completed work session.
Pass when delivery names the real Goal path, the evidence-backed completion verdict, and material
remaining gaps. An ended session or deliberate pause alone leaves In progress / Not met with
a reason and resumption condition; nonexistent files, unrun checks, or unsent releases are not
claimed as delivered. Do not modify this Skill's tests while performing ordinary Goal work.
