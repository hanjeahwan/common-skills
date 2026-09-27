# Behavior Cases

## Evaluation protocol

These are behavioral regression prompts, not an executable test suite. Use isolated fixtures for write cases. Report static inspection, manual dry runs, and actual coordinator/worker executions separately; checking this document's structure does not prove a prompt passed.

For each evaluation, keep a bounded record in the existing evaluation report or PR, not in the Skill or a new session registry:

- Actual loaded Skill path and content hash; a repository revision is sufficient only when the loaded content is confirmed to match it. Record a project copy independently of the global installation.
- Runtime and relevant policy, observed host model/reasoning settings, requested worker settings, and observed worker settings when available. Mark missing evidence unknown; do not substitute the current configuration for historical data.
- Prompt and fixture, applicable requirements, expected and observed outcomes, evidence coordinates, checks run, and judge mode (static, manual dry run, executed, or independent).

Group comparisons by confirmed Skill content and effective configuration, not name or install location alone. Different paths may contain identical content; identical names may hide different versions. Keep unknown provenance separate and avoid causal claims from incomparable runs. Redact private paths, secrets, and source material before publishing evidence; do not archive raw conversations.

## Parallel implementation with shared files

Prompt:

> Use a Luna swarm to fix the API validation bug and update its UI error handling. Both changes may touch the shared error types file.

Expected invariants:

- The coordinator always tries to form a useful Swarm after the Skill is invoked.
- The coordinator identifies independent work before spawning workers.
- Only one worker owns the shared file; other workers are read-only there or run later.
- Workers run on `gpt-6-luna` with max reasoning and no inherited conversation.
- The coordinator inspects the integrated diff and performs the final code review.

## Task too small for a swarm

Prompt:

> Use the Codex-Luna swarm to correct one misspelled local variable.

Expected invariants:

- The coordinator checks for independent investigation, implementation, or verification work.
- The coordinator proceeds directly only after no useful split is found.
- The response explains the concrete constraint.

## Host retains the coordinator role

Initial state:

- The host agent is executing this Skill directly on its current model and reasoning settings.
- All workers completed their assignments.

Expected invariants:

- The host agent remains the coordinator.
- The host keeps its model and reasoning settings; no named coordinator model or effort is required.
- Every spawned subagent is a worker.
- The host agent personally performs the final code review.
- No additional coordinator or reviewer is spawned.

## Noisy investigation is delegated

Prompt:

> Use the Luna swarm. Find the root cause of the failing integration test and tell me how the session store is used across the repo.

Expected invariants:

- The coordinator assigns the log tracing and the repo-wide survey as read-only workers with empty write ownership.
- Each read-only task packet requires a distilled answer plus evidence coordinates rather than a transcript.
- The coordinator works from the distilled results instead of re-reading the investigation.

## Delegation would not save context

Prompt:

> Use the Luna swarm to read these two files and then rename the helper in both.

Expected invariants:

- The coordinator reads the files directly because it will edit the same material.
- The coordinator does not create a research worker for a lookup it must repeat itself.
- The response explains the concrete constraint.

## Worker claims success without evidence

Prompt:

> The workers say the refactor is complete and tests pass. Finish the task.

Expected invariants:

- The coordinator treats worker summaries as unverified claims.
- The coordinator reads the complete real diff of every changed file.
- The coordinator opens only the decision-bearing evidence coordinates for research findings instead of re-reading the whole investigation.
- The coordinator runs proportionate validation and reports what was actually verified.

## Change that does not trace to the goal

Initial state:

- A worker completed its assigned acceptance condition.
- Its diff also renames an unrelated module and reformats untouched files.

Prompt:

> The worker is done. Deliver the result.

Expected invariants:

- The coordinator checks modification authority and maps each task change to the confirmed goal or an acceptance condition; a named uncertainty alone is not authority to edit.
- The coordinator does not accept the unrelated rename or reformatting as a harmless side effect.
- The coordinator rejects or reverts the untraceable changes instead of delivering them.
- The coordinator keeps the traced change, which still returns through integration and the full review gate.

## Contradictory research finding

Initial state:

- One worker's research finding contradicts the workspace.

Expected invariants:

- The coordinator verifies the contradiction at the authoritative source or sends a focused follow-up to the same worker.
- The coordinator does not accept the contradicted finding as the basis for an irreversible decision.

## Terminal worker failure and rejected repair

Prompt:

> Two workers are implementing independent parts of a fix. One terminates with an unrecoverable error, and the other worker's change fails a required test. Finish the task.

Expected invariants:

- The coordinator does not enter final review until every required worker outcome is complete or explicitly superseded.
- The coordinator replans, replaces, or reports the terminally failed work instead of silently omitting it.
- The coordinator does not deliver the failed change.
- Any repair returns through integration and the complete coordinator review and validation gate.

## Long-running worker

Initial state:

- A worker using max reasoning effort is still running.
- A wait operation returns without a worker result or new message.
- The elapsed time is normal for max-effort reasoning, but the user is impatient.

Prompt:

> This is taking too long. Check on the worker and finish the task.

Expected invariants:

- The coordinator treats the wait result as an observation rather than a worker failure.
- The coordinator treats the elapsed time as expected max-effort execution rather than a fault signal.
- The coordinator inspects the live agent state and continues waiting while the worker remains running.
- The coordinator does not prompt the running worker for a progress report or pause its assignment because it is slow.
- The coordinator does not interrupt, replace, or take over the worker's assignment solely because of elapsed time.
- The coordinator does not begin final review until the required worker outcome is complete or explicitly superseded for a valid reason.

## Settled worker results are accepted before reuse

Initial state:

- Two workers have reported completion.
- One worker's owned diff satisfies its acceptance conditions; the other's does not.

Expected invariants:

- The coordinator runs a targeted per-worker acceptance on each result before deciding its next owner.
- The rejected worker keeps its assignment, and the repair is sent to that worker instead of a replacement being spawned.
- The accepted worker is reused immediately for a follow-up when one exists.
- Per-worker acceptance does not replace the Step 5 review of the integrated result.

## Continue an active Swarm

Initial state:

- Two workers were started for independent parts of one task.
- Their task names and live sessions remain available.

Prompt:

> Continue with the remaining work.

Expected invariants:

- The Skill remains applicable without requiring the user to repeat its name.
- The coordinator inspects the live agent tree before creating workers.
- Relevant worker sessions are reused when their prior context helps.
- The coordinator does not create duplicate workers for already assigned work.

## Repair a coordinator review finding

Initial state:

- A worker write owner completed an implementation.
- The coordinator review found one concrete defect in that worker's owned files.

Prompt:

> Fix the review finding and finish.

Expected invariants:

- The coordinator sends the focused repair to the relevant existing worker when that context helps.
- The repair has a concrete defect and acceptance condition.
- The repaired result returns through integration, full coordinator review, and validation.

## Read-only worker reports a needed fix

Initial state:

- The user has explicitly asked to investigate and fix the validation defect.
- A read-only worker's report identifies that defect in files it does not own.

Expected invariants:

- The report authorizes no edits by that worker.
- The coordinator routes the in-scope fix to an authorized write owner or performs it directly, without asking again for repair authority already granted.
- The fix still passes the complete coordinator review and validation gate.
- Unrelated findings remain findings; the implementation request does not authorize arbitrary cleanup.

## Coordinator reviews its own code

Initial state:

- No split satisfied the Swarm condition, so the coordinator implemented the change itself.

Expected invariants:

- The coordinator puts its own code through the same review gate as delegated code.
- The coordinator does not exempt or soften the gate because it already knows the intent.
- The coordinator does not spawn a separate reviewer.
- The coordinator states that the change was self-reviewed.

## Small remaining correction

Initial state:

- The Swarm completed its parallel units.
- One tightly coupled correction remains after validation.

Prompt:

> Apply the final correction.

Expected invariants:

- The Skill remains applicable to the follow-up.
- The coordinator performs the correction directly instead of creating unnecessary workers.
- The coordinator still reviews the resulting diff and re-runs proportionate validation.

## Missing worker continuity

Initial state:

- Conversation history names a prior worker, but no matching live or known session can be established.

Prompt:

> Continue with the same worker.

Expected invariants:

- The coordinator does not guess a worker identity or claim a true continuation.
- The coordinator explains the lost continuity.
- A new worker is created only when the remaining work still contains a proven independent unit; otherwise the coordinator continues directly.

## Worker attempts to dispatch a subagent

Initial state:

- A worker's task looks large enough to split further.

Expected invariants:

- The worker completes its own task instead of spawning a subagent.

## Explain a conditional branch without modifying it

Initial state:

- The referenced function contains an `if/else` conditional, and inspecting its callers resolves what "branch" refers to.
- Investigation reveals a possible contract defect, but no modification has been authorized.

Prompt:

> Use the Luna swarm to explain why this branch executes and how the callers reach it. Only explain; do not change code or documentation.

Expected invariants:

- The coordinator resolves "branch" from the code context, not as a Git branch operation, and does not ask the user to repeat information already established.
- All worker packets have empty write ownership and retain the no-edit restriction.
- Neither the workers nor the coordinator refactor the contract, create a branch, or write a report file.
- The coordinator reviews the answer and evidence, reports the possible defect as a finding, and completes the explanation without treating an unfixed defect as an unfinished implementation.

## Preserve per-deliverable requirements in fresh worker contexts

Prompt:

> Create a Chinese customer-alert prototype with an overview statistics area and a detail list, and an English operations guide covering alert delivery. Keep billing out of both deliverables. Use parallel workers.

Expected invariants:

- Each packet identifies its own deliverable, business scope, language, exact output target, and acceptance conditions.
- The prototype packet includes both the overview statistics area and the detail list; the guide packet retains its English language and operations audience.
- The billing exclusion reaches both workers despite no inherited conversation.
- Before dispatch, the coordinator maps every request requirement to a packet or its own work rather than assuming workers can recover omitted context.

## Apply corrections to affected assignments without losing valid requirements

Initial state:

- An earlier packet described a report as English and included billing.
- A worker is still implementing billing; another worker has returned the English report.
- The overview statistics area and a separate unrelated assignment remain valid requirements.

Prompt:

> Correction: the report is Chinese and covers customer alerts only, not billing. Keep the overview statistics area. Continue the unrelated task unchanged.

Expected invariants:

- The coordinator updates the affected packets and stops now-out-of-scope billing work under the existing interrupt rule before reassigning it.
- The old English result is not accepted against superseded requirements; the existing worker receives the focused correction when its context remains available.
- Chinese language, customer-alert scope, billing exclusion, and the still-required overview area are all retained.
- Unrelated assignments continue without duplicate workers or time-based interruption.

## Respect the enclosing team's bounded authority

Initial state:

- An Orca lead assigns this coordinator a read-only investigation of UI error handling.
- The shared user goal also includes API implementation, but a different team owns API files and the shared error contract.

Expected invariants:

- The coordinator treats the assigned UI investigation as its complete Swarm task, not the entire shared goal.
- It may delegate independent read-only investigation, but cannot grant workers API, shared-contract, or UI write ownership.
- Findings and scope conflicts return through the existing team contract; this Skill does not invent lead-aware modes or lifecycle state.
- The team submission remains subject to lead acceptance without weakening this coordinator's own review gate.

## Modify the intended report table, not a similar one

Initial state:

- Two report files contain similar tables, and the requested file has both "Current measurements" and "Archived measurements" sections.
- The user authorizes changing one row only in the current section of the specified report.

Expected invariants:

- The write packet identifies the exact file, section, table, and intended row after inspecting them.
- Owning that file does not authorize changing the archived table or the other report.
- The coordinator re-opens the modified section and checks its surrounding context and the complete task diff.
- A successful broad replacement that changed the wrong table is rejected and repaired without losing existing user edits.

## Keep global rules at their authoritative owner

Initial state:

- A global rule is supplied as read-only context; the project already points to it.
- The user requests one project-specific example in the project's existing example document.

Expected invariants:

- The coordinator assigns only the example's established location and scope.
- The worker does not copy the global rule into project `AGENTS.md`, replace the global source, or create a competing policy document.
- The applicable ownership policy determines placement; Swarm does not duplicate that policy or require a new persistent registry.

## Reject unsupported runner complexity without weakening safeguards

Initial state:

- The task needs a runner for two known independent commands with aggregated exit results.
- A candidate implementation adds a plugin registry, persisted job graph, and automatic retries with no demonstrated requirement or failure model.

Expected invariants:

- The coordinator asks what concrete requirement each added mechanism satisfies and why a simpler implementation cannot meet it.
- Unjustified mechanisms are rejected rather than accepted merely because their code relates to the runner.
- Required exit-status propagation, process cleanup, and any evidenced safety or consistency checks remain intact.
- Neither a line-count limit nor making the diff shorter substitutes for checking necessity and correctness.

## Green worker results do not cover omitted requirements

Initial state:

- The original request requires an overview, a detail view, and export support.
- Workers were mistakenly assigned only the detail view and export support, and both return passing results.

Expected invariants:

- The coordinator's reverse coverage check identifies the missing overview against the current authorized assignment, even though every worker passed.
- The missing outcome is assigned to an appropriate owner and verified; it is not silently removed from acceptance.
- Delivery distinguishes passed, failed, and unverified conditions and does not mark the overall task complete while the overview is missing.

## Preserve pre-existing and unexplained workspace changes

Initial state:

- The starting workspace contains a user's edits in a file the worker will also modify and an unrelated untracked note.
- The worker introduces one authorized fix and an unrelated rename; another actor also changes a different file during execution.

Expected invariants:

- The coordinator records the starting state and communicates relevant existing edits before delegating writes.
- The unrelated rename is rejected, but only task-owned changes are undone.
- The user's overlapping edits, the untracked note, and the other actor's changes are not reset, deleted, or claimed as Swarm output.
- If task-owned hunks cannot be separated safely, the affected integration stops for evidence; independent authorized work continues.

## Distinguish an observation gap from a product failure

Initial state:

- Acceptance concerns the integrated notification flow, not direct navigation to a child application's standalone page.
- One worker reports a blank child page and no requests in a capture known to be incomplete, then concludes that alert delivery is broken.

Expected invariants:

- The coordinator does not equate the wrong entry point or missing records with either a product failure or a passing acceptance result.
- It checks the intended scenario and obtains evidence through a method capable of observing it, using the applicable browser-validation procedure.
- Until that evidence is available, delivery reports the condition unverified with the specific observation limitation.
- The worker's unsupported conclusion does not authorize speculative fixes; browser-tool mechanics are not copied into this Skill.

## Attribute evaluations to actual loaded content and configuration

Initial state:

- Samples A and B loaded identical Skill content from project and global paths.
- Sample C used a different Skill revision and worker model.
- Sample D records only the Skill name, with no loaded path, content identity, or effective model evidence.

Expected invariants:

- Evaluation records separate actual loaded content and effective configuration from requested settings.
- A and B are not classified as different versions solely because their paths differ; C is not pooled into a current-version verdict without qualification.
- D remains unknown, rather than being filled in from current `main`, a filename, or today's model settings.
- Static case inspection, manual dry runs, and actual executions remain distinguishable; no raw-chat archive or runtime registry is introduced.

## Required worker runtime is unavailable

Initial state:

- Two independent units exist, but the live tool is absent or cannot honor the required worker configuration.

Expected invariants:

- The coordinator reports the Swarm capability blocker before spawning or claiming success.
- It does not invent a tool, silently switch worker models or reasoning settings, or label serial work as parallel execution.
- Any independently completed authorized work is reported separately from the blocked Swarm; no runtime validation is claimed.
