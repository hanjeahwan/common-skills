# Behavior Cases

## Parallel implementation with shared files

Prompt:

> Use a Luna swarm to fix the API validation bug and update its UI error handling. Both changes may touch the shared error types file.

Expected invariants:

- Sol identifies independent work before spawning agents.
- Only one worker owns the shared file; other workers are read-only there or run later.
- Workers use GPT-5.6 Luna with max reasoning and no inherited conversation.
- Sol inspects the integrated diff and performs the final code review.

## Task too small for a swarm

Prompt:

> Use the Codex-Luna swarm to correct one misspelled local variable.

Expected invariants:

- Sol declines unnecessary fan-out and handles the bounded task directly.
- The response explains that no independent work units exist.

## Worker claims success without evidence

Prompt:

> The Luna workers say the refactor is complete and tests pass. Finish the task.

Expected invariants:

- Sol treats worker summaries as unverified claims.
- Sol inspects the workspace and diff directly.
- Sol runs proportionate validation and reports what was actually verified.

## Worker failure and rejected repair

Prompt:

> Two Luna workers are implementing independent parts of a fix. One times out, and the other worker's change fails a required test. Finish the task.

Expected invariants:

- Sol does not enter final review until every required worker outcome is complete or explicitly superseded.
- Sol replans, replaces, or reports the timed-out work instead of silently omitting it.
- Sol does not deliver the failed change.
- Any repair returns through integration and the complete Sol code review and validation gate.

## Continue the same Swarm on a later turn

Initial state:

- The previous turn started two Luna workers for independent parts of one task.
- Their task names and live sessions remain available.

Prompt:

> Continue with the remaining work.

Expected invariants:

- The Skill remains applicable without requiring the user to repeat its name.
- Sol inspects the live agent tree before creating workers.
- Relevant Luna sessions are reused when their prior context helps.
- Sol does not create duplicate workers for already assigned work.

## Repair a Sol review finding

Initial state:

- A Luna write owner completed an implementation.
- Sol review found one concrete defect in that worker's owned files.

Prompt:

> Fix the review finding and finish.

Expected invariants:

- Sol sends the focused repair to the relevant existing Luna when that context helps.
- The repair has a concrete defect and acceptance condition.
- The repaired result returns through integration, full Sol review, and validation.

## Small follow-up within the same task

Initial state:

- The Swarm completed its parallel units.
- One tightly coupled correction remains after validation.

Prompt:

> Apply the final correction.

Expected invariants:

- The Skill remains applicable to the follow-up.
- Sol performs the correction directly instead of creating unnecessary workers.
- Sol still reviews the resulting diff and re-runs proportionate validation.

## Missing worker continuity

Initial state:

- Conversation history names a prior Luna worker, but no matching live or known session can be established.

Prompt:

> Continue with the same Luna.

Expected invariants:

- Sol does not guess a worker identity or claim a true continuation.
- Sol explains the lost continuity.
- A new Luna is created only when the remaining work still contains a proven independent unit; otherwise Sol continues directly.
