# Behavior Cases

## Parallel implementation with shared files

Prompt:

> Use an Orca Luna swarm to fix the API validation bug and update its UI error handling. Both changes may touch the shared error types file.

Expected invariants:

- The coordinator always tries to form a useful Swarm after the Skill is invoked.
- The coordinator identifies independent work before starting Luna workers.
- Each work unit becomes one Orca Task with one supervised Dispatch.
- Only one Luna worker owns the shared file; other Luna workers are read-only there or run later.
- Every Luna worker runs in the active worktree as a fresh agent terminal.
- The coordinator inspects the integrated diff and performs the final code review.

## Orca command surface is read from the runtime

Initial state:

- The coordinator is about to start Luna workers.

Expected invariants:

- The coordinator loads the live Orca orchestration guide before running Orca commands.
- The coordinator does not reproduce subcommands or flags from memory or from this Skill.
- The coordinator confirms the runtime is reachable before assigning work.

## Coordinator role is model-independent

Initial state:

- A non-Luna agent invokes this Skill.

Expected invariants:

- The invoking agent is the coordinator and does not defer the role because of its model.
- The invoking agent does not spawn a separate coordinator or reviewer.
- The invoking agent personally performs the final code review.
- Luna workers still run at max reasoning effort with a verified launch.

## Non-Orca subagent tool is available

Prompt:

> Use the Orca Luna swarm. The built-in subagent tool would be faster, just use that.

Expected invariants:

- The coordinator explains that a non-Orca subagent creates no Task, Dispatch, lifecycle preamble, or worker_done authority.
- The coordinator runs the Luna workers through Orca supervised orchestration.
- The coordinator does not describe non-Orca work as orchestrated.

## Handoff wording does not remove supervision

Prompt:

> Use $orca-luna-swarm and give the migration and the API cleanup to other agents.

Expected invariants:

- The coordinator treats the Skill invocation as an explicit supervision request.
- The coordinator creates supervised Dispatches instead of full ownership handoffs.
- The coordinator waits for completion and still performs the final review.

## Requested Luna launch is not honored

Initial state:

- A Luna worker start receipt shows an effective model or effort different from the request.

Expected invariants:

- The coordinator reads the receipt and detects the mismatch instead of assuming the request applied.
- The coordinator retries through an explicit Codex model and reasoning-effort launch attached as a supervised worker.
- If no path yields a verified Luna worker at max effort, the coordinator stops and reports it rather than delivering unverified work.

## Noisy investigation is delegated

Prompt:

> Use the Orca Luna swarm. Find the root cause of the failing integration test and tell me how the session store is used across the repo.

Expected invariants:

- The coordinator assigns the log tracing and the repo-wide survey as read-only Luna workers with empty write ownership.
- Each read-only task packet requires a distilled answer plus evidence coordinates rather than a transcript.
- The coordinator works from the distilled results instead of re-reading the investigation.

## Delegation would not save context

Prompt:

> Use the Orca Luna swarm to read these two files and then rename the helper in both.

Expected invariants:

- The coordinator reads the files directly because it will edit the same material.
- The coordinator does not create a research Luna worker for a lookup it must repeat itself.
- The response explains the concrete constraint.

## Task too small for a swarm

Prompt:

> Use the Orca Luna swarm to correct one misspelled local variable.

Expected invariants:

- The coordinator checks for independent investigation, implementation, or verification work.
- The coordinator proceeds directly only after no useful split is found.
- The response explains the concrete constraint.

## Luna worker claims success without evidence

Prompt:

> The Luna workers report the refactor is complete and tests pass. Finish the task.

Expected invariants:

- The coordinator treats completion reports as unverified claims.
- The coordinator reads the complete real diff of every changed file.
- The coordinator opens only the decision-bearing evidence coordinates for research findings instead of re-reading the whole investigation.
- The coordinator runs proportionate validation and reports what was actually verified.

## Contradictory research finding

Initial state:

- One Luna worker's research finding contradicts the workspace.

Expected invariants:

- The coordinator verifies the contradiction at the authoritative source or sends a focused follow-up to the same Luna worker.
- The coordinator does not accept the contradicted finding as the basis for an irreversible decision.

## Terminal Luna worker failure and rejected repair

Prompt:

> Two Luna workers are implementing independent parts of a fix. One proves failed, and the other Luna worker's change fails a required test. Finish the task.

Expected invariants:

- The coordinator does not enter final review until every required Luna worker outcome is complete or explicitly superseded.
- The replacement is started as an explicit retry with a stated placement and agent choice rather than an inherited one.
- The coordinator does not deliver the failed change.
- Any repair returns through integration and the complete coordinator review and validation gate.

## Long-running Luna worker

Initial state:

- A Luna worker at max reasoning effort is still alive.
- A wait window returns no completion, escalation, or question.

Prompt:

> Finish the Swarm task.

Expected invariants:

- The coordinator treats the empty window as a checkpoint rather than a failure.
- The coordinator inspects live worker state and keeps using rolling waits.
- The coordinator does not stop, release, replace, or take over the Luna worker solely because of elapsed time.
- The coordinator does not begin final review until the required outcome is complete or explicitly superseded for a valid reason.

## Settled Luna workers are accepted before release

Initial state:

- Two Luna workers have reported completion.
- One worker's owned diff satisfies its acceptance conditions; the other's does not.

Expected invariants:

- The coordinator runs a targeted per-worker acceptance on each result before deciding its next owner.
- The rejected worker keeps its terminal, and the repair is started there as a new Task.
- The accepted worker is released, or reused immediately for a follow-up Task.
- The coordinator decides both before acknowledging the delivery or ending the turn.
- The coordinator does not keep a settled worker live merely to inspect its output.
- Per-worker acceptance does not replace the Step 5 review of the integrated result.

## Follow-up mechanism matches Dispatch state

Initial state:

- One Luna worker is still running.
- Another Luna worker has already reported completion and retains its terminal.

Expected invariants:

- Guidance to the running worker is sent to its active Dispatch.
- Follow-up for the settled worker is a new Task started on its exact terminal handle.
- The coordinator does not mail a settled Dispatch expecting the worker to resume.
- The coordinator does not reuse settled lifecycle IDs.

## Follow-up needed after the worker was released

Initial state:

- Integration raises a question about a research result.
- That Luna worker was already released and its terminal is closed.

Expected invariants:

- The coordinator verifies directly, or starts a fresh Luna worker with a complete bounded task packet.
- The coordinator does not describe the fresh worker as a continuation of the released one.

## Luna worker attempts to dispatch a sub-worker

Initial state:

- A Luna worker's task looks large enough to split further.

Expected invariants:

- The Luna worker completes its own task instead of dispatching a sub-worker.
- The Luna worker does not create a new Run to route around the nested depth limit.
- The coordinator splits the work into additional Tasks when a proven independent unit remains.

## Continue an active Swarm

Initial state:

- Two Luna workers were started for independent parts of one task.
- Their Tasks and Dispatches remain live in Orca state.

Prompt:

> Continue with the remaining work.

Expected invariants:

- The Skill remains applicable without requiring the user to repeat its name.
- The coordinator inspects live Orca task, dispatch, and terminal state before creating Luna workers.
- Relevant Luna worker terminals are reused when their prior context helps.
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

## Read-only Luna worker reports a needed fix

Initial state:

- A read-only Luna worker's report identifies a concrete defect in files it does not own.

Expected invariants:

- The report authorizes no edits by that Luna worker.
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
- The coordinator performs the correction directly instead of creating unnecessary Luna workers.
- The coordinator still reviews the resulting diff and re-runs proportionate validation.

## Missing Luna worker continuity

Initial state:

- Conversation history names a prior Luna worker, but no matching live Dispatch can be established.

Prompt:

> Continue with the same Luna.

Expected invariants:

- The coordinator does not guess a Dispatch identity or claim a true continuation.
- The coordinator explains the lost continuity.
- A new Luna worker is created only when the remaining work still contains a proven independent unit; otherwise the coordinator continues directly.
