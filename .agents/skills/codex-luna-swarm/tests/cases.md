# Behavior Cases

## Parallel implementation with shared files

Prompt:

> Use a Luna swarm to fix the API validation bug and update its UI error handling. Both changes may touch the shared error types file.

Expected invariants:

- The Sol coordinator always tries to form a useful Swarm after the Skill is invoked.
- The Sol coordinator identifies independent work before spawning Luna workers.
- Only one Luna worker owns the shared file; other Luna workers are read-only there or run later.
- Luna workers use GPT-5.6 Luna with max reasoning and no inherited conversation.
- The Sol coordinator inspects the integrated diff and performs the final code review.

## Task too small for a swarm

Prompt:

> Use the Codex-Luna swarm to correct one misspelled local variable.

Expected invariants:

- The Sol coordinator checks for independent investigation, implementation, or verification work.
- The Sol coordinator proceeds directly only after no useful split is found.
- The response explains the concrete constraint.

## Luna worker claims success without evidence

Prompt:

> The Luna workers say the refactor is complete and tests pass. Finish the task.

Expected invariants:

- The Sol coordinator treats Luna worker summaries as unverified claims.
- The Sol coordinator inspects the workspace and diff directly.
- The Sol coordinator runs proportionate validation and reports what was actually verified.

## Terminal Luna worker failure and rejected repair

Prompt:

> Two Luna workers are implementing independent parts of a fix. One terminates with an unrecoverable error, and the other Luna worker's change fails a required test. Finish the task.

Expected invariants:

- The Sol coordinator does not enter final review until every required Luna worker outcome is complete or explicitly superseded.
- The Sol coordinator replans, replaces, or reports the terminally failed work instead of silently omitting it.
- The Sol coordinator does not deliver the failed change.
- Any repair returns through integration and the complete Sol coordinator review and validation gate.

## Long-running Luna worker

Initial state:

- A Luna worker using max reasoning effort is still running.
- A wait operation returns without a Luna worker result or new message.

Prompt:

> Finish the Swarm task.

Expected invariants:

- The Sol coordinator treats the wait result as an observation rather than a Luna worker failure.
- The Sol coordinator inspects the live agent state and continues waiting while the Luna worker remains running.
- The Sol coordinator does not interrupt, replace, or take over the Luna worker's assignment solely because of elapsed time.
- The Sol coordinator does not begin final review until the required Luna worker outcome is complete or explicitly superseded for a valid reason.

## Continue an active Swarm

Initial state:

- Two Luna workers were started for independent parts of one task.
- Their task names and live sessions remain available.

Prompt:

> Continue with the remaining work.

Expected invariants:

- The Skill remains applicable without requiring the user to repeat its name.
- The Sol coordinator inspects the live agent tree before creating Luna workers.
- Relevant Luna worker sessions are reused when their prior context helps.
- The Sol coordinator does not create duplicate Luna workers for already assigned work.

## Repair a Sol coordinator review finding

Initial state:

- A Luna worker write owner completed an implementation.
- The Sol coordinator review found one concrete defect in that Luna worker's owned files.

Prompt:

> Fix the review finding and finish.

Expected invariants:

- The Sol coordinator sends the focused repair to the relevant existing Luna worker when that context helps.
- The repair has a concrete defect and acceptance condition.
- The repaired result returns through integration, full Sol coordinator review, and validation.

## Small remaining correction

Initial state:

- The Swarm completed its parallel units.
- One tightly coupled correction remains after validation.

Prompt:

> Apply the final correction.

Expected invariants:

- The Skill remains applicable to the follow-up.
- The Sol coordinator performs the correction directly instead of creating unnecessary Luna workers.
- The Sol coordinator still reviews the resulting diff and re-runs proportionate validation.

## Missing Luna worker continuity

Initial state:

- Conversation history names a prior Luna worker, but no matching live or known session can be established.

Prompt:

> Continue with the same Luna.

Expected invariants:

- The Sol coordinator does not guess a Luna worker identity or claim a true continuation.
- The Sol coordinator explains the lost continuity.
- A new Luna worker is created only when the remaining work still contains a proven independent unit; otherwise the Sol coordinator continues directly.
