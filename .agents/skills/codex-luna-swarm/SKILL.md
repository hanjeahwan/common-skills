---
name: codex-luna-swarm
description: Start or continue parallel coding work as the host coordinator that performs mandatory code review while `gpt-5.6-luna` workers run at max reasoning effort. Use when a coding task has multiple independent investigation or implementation units; when the user asks for a Luna swarm, Codex-Luna swarm, parallel workers, or coordinator-reviewed workers; or when related work continues, repairs, validates, or reviews an active Swarm. When invoked, require the coordinator to evaluate a useful Swarm split before proceeding without fan-out.
---

# Codex–Luna Swarm

Use one execution pattern: workers investigate or implement in parallel, then the coordinator personally reviews the combined code before delivery. Parallelism provides speed; the coordinator review gate provides safety. Do not split these into separate modes.

```mermaid
flowchart TD
    S[Coordinator Splits Tasks] --> L1[Worker 1]
    S --> L2[Worker 2]
    S --> LN[Worker N]
    L1 --> G[Collect Changes And Evidence]
    L2 --> G
    LN --> G
    G --> R[Coordinator Performs Code Review]
    R -->|Rejected| F[Return Targeted Fix]
    F --> G
    R -->|Approved| V[Verify And Deliver]
```

## Responsibility Boundary

Use `coordinator` as the canonical name for the coordinating and reviewing actor. Use `worker` as the canonical name for each delegated actor. Keep `agent tree` and `subagent` only for their runtime and tool meanings.

| Work | Coordinator | Workers |
|---|---|---|
| Initial investigation | Perform the minimum investigation needed to define the problem and scope | Deepen independent lines of investigation |
| Code call paths | Define the boundary and verify critical paths | Investigate separate modules in parallel |
| External research needed by the coding task | Verify conclusions that affect decisions against authoritative sources | Investigate separate official sources or approaches |
| Root-cause decision | Make the final determination | Provide candidate causes and evidence |
| Code implementation | Implement directly or delegate | Act as the primary implementer |
| Tests and checks | Re-run and verify critical results | Run relevant checks first and report them |
| Code review | Perform it personally | Never substitute for the coordinator's review |
| Conflict resolution and delivery | Retain final decision authority | Do not make the final decision |

## Invariants

- Host-role binding: The host agent executing this Skill is the coordinator for the entire Swarm, keeping its current model and reasoning settings unchanged.
- Spawned-role restriction: Every subagent spawned while this Skill is active is a worker.
- Review ownership: The host agent personally performs Step 5.
- Every worker is spawned with `model: "gpt-5.6-luna"`, `reasoning_effort: "max"`, and `fork_turns: "none"`.
- Workers must not spawn subagents.
- Workers must not accept another worker's code as reviewed.
- Every code change must pass the coordinator's direct review, including code the coordinator wrote or repaired itself. A worker's summary, test result, or self-assessment cannot replace this gate.
- Every change in the integrated result must trace to the established goal, an acceptance condition, or a named uncertainty. A change that cannot be traced is rejected or reverted, not carried into delivery.
- When this Skill is invoked, the coordinator must evaluate the task against the Swarm condition in Step 1 before proceeding alone.
- Never invent work merely to increase the worker count.
- The coordinator retains every approval decision.
- The coordinator applies the current authorization and safety boundaries to delegated work.
- Delegation must remain within the authorized scope.
- Keep this Skill active while work serves the same user-visible outcome, including repairs, validation, and review.
- The user does not need to repeat the Skill name while it remains active.
- Reuse an existing worker when its assignment continues the same objective, owned files, or evidence path.
- Create a new worker only for independent work or deliberate context isolation.
- Inspect the known and live agent tree before assigning work.
- Assign each work unit to one worker.
- Never infer a missing worker identity.
- Claim worker continuity only when the known and live agent tree establishes the identity.
- A wait operation that returns no update does not change a running worker's state.
- Continue waiting while a worker remains running.
- Workers run at max reasoning effort and therefore take longer than ordinary delegated work: slowness or silence is expected execution, not a fault signal.
- Elapsed time alone must not justify prompting a running worker for progress, pausing it, interrupting it, replacing it, or taking over its assignment.

## Workflow

### 1. Establish The Work

Before assigning workers:

- State the user-visible goal, current behavior, constraints, acceptance conditions, and out-of-scope work from inspected evidence.
- Separate independent investigation, implementation, and verification units from work that depends on earlier findings.
- Swarm condition: At least two independent units can run concurrently without conflicting write ownership, and each unit advances an acceptance condition or resolves a named uncertainty.
- Swarm action: Assign each qualifying unit to a worker.
- Direct-execution condition: No split satisfies the Swarm condition.
- Direct-execution action: The coordinator proceeds alone and states the concrete constraint.

### 2. Assign Independent Ownership

Give each worker a bounded task packet:

```yaml
objective: one concrete outcome
facts: only the verified context needed for this task
scope: allowed files, components, or questions
write_owner: files this worker alone may modify; empty means read-only
acceptance: observable conditions for success
exclusions: actions and areas outside authority
return: findings, sources when research was performed, changed files, validation, and unresolved risks
```

- Start with two to four workers.
- Increase the worker count only when more proven independent units remain unassigned.

- Shared-file condition: Two or more workers may touch the same file.
- Shared-file action: Assign one worker as the write owner and make the other workers read-only for that file.
- Scheduling alternative: Run dependent write assignments sequentially.

- Assignment preparation: Inspect the known and live agent tree.
- Worker reuse condition: An existing worker retains context needed by the assignment.
- Worker reuse action: Update that worker's bounded task instead of creating a duplicate assignment.

### 3. Run Workers

Use the collaboration subagent tool directly with:

```json
{
  "model": "gpt-5.6-luna",
  "reasoning_effort": "max",
  "fork_turns": "none"
}
```

- Spawn action: Send each worker the complete bounded task packet because it receives no inherited conversation.
- Execution action: Run independent worker assignments concurrently.
- Wait action: Wait for worker results without busy polling.
- No-update action: Inspect the live agent state.
- Running-state action: Continue waiting. Max-effort execution is expected to take longer, so do not prompt a running worker for a progress report or pause its assignment to check on it.
- Interrupt condition: The user requests interruption, the assignment leaves task scope, or continued execution would cross an authorization or safety boundary.
- Interrupt action: Interrupt the running worker.
- Replacement condition: The prior worker is no longer running and its assignment remains incomplete because it failed, reported that it cannot continue, or returned a partial result.
- Replacement action: Spawn a replacement worker with a complete bounded task packet.
- Additional-worker condition: A proven independent unit remains unassigned.
- Additional-worker action: Spawn another worker for that unit.
- Direct-execution condition: The remaining work does not satisfy the Swarm condition.
- Direct-execution action: The coordinator completes the remaining work and applies the integration, review, and validation gates.

### 4. Integrate Evidence And Changes

- Integration entry gate: Every required worker outcome is complete or validly superseded.
- Supersede a required worker outcome only when its assigned work is no longer part of the user-visible task.
- Recovery condition: A worker is no longer running and its required outcome remains incomplete.
- Recovery action: Return the incomplete assignment to Step 3.
- Omission prohibition: Never omit an incomplete required outcome.
- Evidence collection: The coordinator reads every worker result.
- Workspace inspection: The coordinator inspects the actual workspace.
- Evidence gate: Treat worker summaries as claims until files, diffs, logs, or test output support them.

- Reconcile contradictory worker results.
- Reject out-of-scope edits and unexplained files.
- Resolve integration at the authoritative source.
- Never preserve duplicate implementations as an integration shortcut.
- Request rework only when review produces concrete new evidence.
- Never repeat an unchanged failed instruction.

### 5. Coordinator Code Review Gate

The coordinator personally reviews the combined result before declaring success:

1. Inspect the complete diff and map each change to the confirmed goal or root cause.
2. Read the changed logic in its caller, callee, state, and error-propagation context.
3. Look adversarially for incorrect assumptions, write conflicts, duplicate rules, hidden fallbacks, scope expansion, and regressions.
4. Run the available tests, type checks, builds, and lint that cover the changed behavior and affected paths.
5. Confirm the original problem is resolved and important normal paths still work.

- Self-authored condition: The coordinator implemented or repaired part of the change itself.
- Self-authored action: Put that code through this same gate. Knowing the intent behind a change is not evidence that it is correct, so read it as adversarially as delegated code and state that it was self-reviewed.
- Review-failure action: The coordinator identifies a concrete defect and acceptance condition.
- Untraceable-change action: The coordinator rejects or reverts the change instead of carrying it into delivery.
- Worker repair condition: The prior worker's context is needed for the repair.
- Worker repair action: Send the focused repair to that worker.
- Coordinator repair condition: The repair does not need worker context and remains within the coordinator's existing authority.
- Coordinator repair action: The coordinator fixes the defect directly.
- Stop condition: Further progress requires guessing or new authorization.
- Stop action: Stop and report the required evidence or authorization.
- Re-entry gate: Every repair returns to Step 4 and passes the complete coordinator review and validation gate before delivery.

### 6. Deliver

The final response must identify:

- how work was divided and which workers changed files;
- what the coordinator found during its own code review;
- evidence that the original problem and normal paths were verified;
- tests and checks run, including failures or omissions;
- unresolved assumptions, risks, and unrelated findings.

Only the coordinator can mark the overall task complete.

## Boundaries

- Do not build a DAG engine, voting system, consensus layer, persistent memory, role registry, or recursive hierarchy unless a demonstrated failure requires it.
- Do not create a persistent session registry or duplicate lifecycle state to preserve worker continuity.
- Do not let worker count substitute for task decomposition or evidence quality.
- Do not ask multiple workers to make competing edits in the shared workspace.
- Do not treat passing tests as sufficient code review.
- Do not commit, push, deploy, publish, delete, or perform irreversible actions unless the user has separately authorized them.

## Quality Standard

A successful run meets all of these conditions:

- Independent worker assignments provide real parallel execution.
- No concurrent write ownership conflict remains.
- The coordinator independently inspects the integrated code and verification evidence before delivery.
