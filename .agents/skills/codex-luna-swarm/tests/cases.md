# Behavior Cases

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

- The coordinator maps each change in the diff to the established goal, an acceptance condition, or a named uncertainty.
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

- A read-only worker's report identifies a concrete defect in files it does not own.

Expected invariants:

- The report authorizes no edits by that worker.
- The coordinator routes the fix to the write owner or performs it directly.
- The fix still passes the complete coordinator review and validation gate.

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
