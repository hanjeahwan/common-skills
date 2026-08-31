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

> Use the Sol-Luna swarm to correct one misspelled local variable.

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
