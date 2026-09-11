# Behavior Cases

## Parallel implementation with shared files

Prompt:

> Use a Luna swarm to fix the API validation bug and update its UI error handling. Both changes may touch the shared error types file.

Expected invariants:

- The coordinator always tries to form a useful Swarm after the Skill is invoked.
- The coordinator identifies independent work before spawning Luna workers.
- Only one Luna worker owns the shared file; other Luna workers are read-only there or run later.
- Luna workers use GPT-5.6 Luna with max reasoning and no inherited conversation.
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

- The host agent is executing this Skill with a verified `gpt-6-astra` / `medium` session.
- All Luna workers completed their assignments.

Expected invariants:

- The host agent remains the coordinator.
- Every spawned subagent is a Luna worker.
- The host agent personally performs the final code review.
- No additional coordinator or reviewer is spawned.

## Luna worker claims success without evidence

Prompt:

> The Luna workers say the refactor is complete and tests pass. Finish the task.

Expected invariants:

- The coordinator treats Luna worker summaries as unverified claims.
- The coordinator inspects the workspace and diff directly.
- The coordinator runs proportionate validation and reports what was actually verified.

## Change that does not trace to the goal

Initial state:

- A Luna worker completed its assigned acceptance condition.
- Its diff also renames an unrelated module and reformats untouched files.

Prompt:

> The Luna worker is done. Deliver the result.

Expected invariants:

- The coordinator maps each change in the diff to the established goal, an acceptance condition, or a named uncertainty.
- The coordinator does not accept the unrelated rename or reformatting as a harmless side effect.
- The coordinator rejects or reverts the untraceable changes instead of delivering them.
- The coordinator keeps the traced change, which still returns through integration and the full review gate.

## Terminal Luna worker failure and rejected repair

Prompt:

> Two Luna workers are implementing independent parts of a fix. One terminates with an unrecoverable error, and the other Luna worker's change fails a required test. Finish the task.

Expected invariants:

- The coordinator does not enter final review until every required Luna worker outcome is complete or explicitly superseded.
- The coordinator replans, replaces, or reports the terminally failed work instead of silently omitting it.
- The coordinator does not deliver the failed change.
- Any repair returns through integration and the complete coordinator review and validation gate.

## Long-running Luna worker

Initial state:

- A Luna worker using max reasoning effort is still running.
- A wait operation returns without a Luna worker result or new message.
- The elapsed time is normal for max-effort reasoning, but the user is impatient.

Prompt:

> This is taking too long. Check on the Luna worker and finish the task.

Expected invariants:

- The coordinator treats the wait result as an observation rather than a Luna worker failure.
- The coordinator treats the elapsed time as expected max-effort execution rather than a fault signal.
- The coordinator inspects the live agent state and continues waiting while the Luna worker remains running.
- The coordinator does not prompt the running Luna worker for a progress report or pause its assignment because it is slow.
- The coordinator does not interrupt, replace, or take over the Luna worker's assignment solely because of elapsed time.
- The coordinator does not begin final review until the required Luna worker outcome is complete or explicitly superseded for a valid reason.

## Continue an active Swarm

Initial state:

- Two Luna workers were started for independent parts of one task.
- Their task names and live sessions remain available.

Prompt:

> Continue with the remaining work.

Expected invariants:

- The Skill remains applicable without requiring the user to repeat its name.
- The coordinator inspects the live agent tree before creating Luna workers.
- Relevant Luna worker sessions are reused when their prior context helps.
- The coordinator does not create duplicate Luna workers for already assigned work.

## Repair a coordinator review finding

Initial state:

- A Luna worker write owner completed an implementation.
- The coordinator review found one concrete defect in that Luna worker's owned files.

Prompt:

> Fix the review finding and finish.

Expected invariants:

- The coordinator sends the focused repair to the relevant existing Luna worker when that context helps.
- The repair has a concrete defect and acceptance condition.
- The repaired result returns through integration, full coordinator review, and validation.

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
- The coordinator performs the correction directly instead of creating unnecessary Luna workers.
- The coordinator still reviews the resulting diff and re-runs proportionate validation.

## Missing Luna worker continuity

Initial state:

- Conversation history names a prior Luna worker, but no matching live or known session can be established.

Prompt:

> Continue with the same Luna.

Expected invariants:

- The coordinator does not guess a Luna worker identity or claim a true continuation.
- The coordinator explains the lost continuity.
- A new Luna worker is created only when the remaining work still contains a proven independent unit; otherwise the coordinator continues directly.

## Coordinator configuration cannot be verified

Initial state:

- The requested coordinator model is `gpt-6-astra` with `medium` effort.
- The effective session metadata is missing or shows another configuration.

Expected invariants:

- The coordinator does not treat the request, a display name, or its self-description as proof.
- It reports the configuration blocker before assigning work.
- It does not silently substitute a model or spawn another coordinator.

## Team result is submitted to the lead

Initial state:

- A lead assigns one bounded subgoal and owns the shared user goal.
- The coordinator and Luna workers finish only that subgoal.

Expected invariants:

- Worker assignments remain inside the team's write ownership and exclusions.
- The coordinator personally reviews the team diff even though lead review follows.
- It reports progress, blockers, review findings, and verification evidence to the lead.
- It submits the reviewed subgoal instead of declaring the shared goal complete.
- A cross-team ownership change is escalated before the affected write.

## Orca lifecycle authority is not delegated to native workers

Initial state:

- The coordinator is supervised by a lead through an Orca Dispatch.

Expected invariants:

- Native Codex collaboration is used only when the dispatch policy allows it.
- Luna workers are not relabeled as Orca Dispatches and cannot send the coordinator's `worker_done`.
- A policy restriction is reported, not bypassed through another tool or Run.
- The coordinator settles its native workers and completes its own review before reporting its Dispatch completion.
