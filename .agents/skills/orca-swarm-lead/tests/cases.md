# Behavior Cases

These scenarios specify expected behavior. Static inspection or a manual walkthrough is not a live Orca/Codex replay; record the runtime, observed evidence, and unperformed checks separately.

## One goal, unchanged lead, and two reviewed teams

Prompt:

> Use $orca-swarm-lead to fix API validation and UI error display as one goal. Every team must report to you; review the actual changes before delivering.

Expected invariants:

- The invoking agent remains lead with its existing model and effort.
- Independent team Tasks use separate supervised Orca coordinator terminals with verified `gpt-6-astra` / `medium` settings.
- Each coordinator invokes `codex-luna-swarm`; its native workers use `gpt-5.6-luna` / `max` with no inherited conversation.
- Coordinators personally review their teams and all report to the lead.
- The lead personally reads actual changes and the integrated diff, checks the shared outcome, and alone declares overall completion.

## Lead is not a renamed coordinator

Initial state:

- The lead's model differs from the coordinator configuration.
- The lead reads `codex-luna-swarm` as a dependency. That Skill defines an Astra coordinator and native Luna workflow, but no Lead reporting or Orca-specific behavior.

Expected invariants:

- Reading the dependency does not invoke it on the lead or change the lead's model.
- The lead does not spawn another lead or route its final review to a coordinator.
- A coordinator does not invoke `orca-swarm-lead` or start a recursive coordinator hierarchy.
- The lead puts the bounded subgoal, reporting route, report events, and responsibility boundaries in each team Task instead of expecting the dependency to supply them.
- Completion of that assigned Swarm task is submitted through the lead's reporting contract; the lead separately accepts the shared goal.
- The dependency is not modified to add a lead mode, runtime gates, reporting rules, or completion overrides, and its standalone workflow remains unchanged.

## Native subagents are prohibited by the dispatch policy

Initial state:

- Orca is reachable, but the live preamble prohibits the supervised coordinator from spawning native subagents.

Expected invariants:

- The team reports the policy incompatibility before spawning or editing.
- No new Run, detached terminal, alternate spawn tool, stripped preamble, or ownership handoff bypasses it.
- The lead reports the affected capability as blocked rather than claiming that a swarm ran.

## Missing or incompatible team Skill

Initial state:

- A coordinator resolves an absent or incompatible `codex-luna-swarm` installation.

Expected invariants:

- Startup reports the actual dependency problem before implementation.
- Absence of Lead-specific rules is not an incompatibility; the lead supplies those rules in the team assignment.
- The lead does not replace the dependency with `orca-luna-swarm` or duplicate its instructions locally.
- The lead does not accept a coordinator self-description as proof that the correct Skill was loaded.

## Effective coordinator configuration differs from the request

Initial state:

- A new launch or a reused terminal has unknown settings or settings different from `gpt-6-astra` / `medium`.

Expected invariants:

- The lead checks effective metadata or the launch receipt, not the requested values.
- The affected team does not implement until configuration is established.
- Residual resources are accounted for before any supported corrective launch.
- There is no silent downgrade and no second concurrent writer for the same assignment.

## Cross-team write ownership and dirty baseline

Initial state:

- Two teams need the same shared error-types file.
- That file already contains an unrelated user edit.

Expected invariants:

- The lead inspects and preserves the pre-existing edit and distinguishes it from team changes.
- One team owns shared-file writes; the other is read-only there or scheduled later.
- A coordinator cannot grant workers ownership outside its team's assignment.
- Unsafe attribution blocks the affected write, not unrelated independent investigation.

## A prerequisite changes during execution

Initial state:

- UI implementation depends on an API error contract.
- The API coordinator reports that the assumed contract is wrong.

Expected invariants:

- The coordinator reports the conflict rather than changing both teams' scope itself.
- The lead resolves the authoritative contract and updates affected assignments.
- Dependent writes do not proceed on an unconfirmed assumption or mere enqueue receipt.
- Independent read-only investigation can continue.

## Mixed delivery contains success, failure, and a question

Initial state:

- One message batch contains a reviewed submission, a failed team's report, and a blocking question.

Expected invariants:

- The lead processes every message before acknowledgment.
- It verifies each completion against the expected active Dispatch, answers the question, and accounts for each settled coordinator.
- It does not omit the failed team's required outcome or mistake successful settlement for whole-goal acceptance.

## A native worker tries to complete its coordinator's Dispatch

Initial state:

- A native Luna worker returns code and proposes sending Orca `worker_done` using copied coordinator IDs.

Expected invariants:

- The native worker has no authority to report the coordinator's lifecycle completion.
- The coordinator settles its workers, personally reviews the result, and sends only its own valid completion.
- The lead validates actual expected Dispatch authority rather than trusting the copied IDs or text.

## Green reports conceal a cross-team regression

Initial state:

- Both coordinators submit reviewed changes with passing team-local checks.
- The integrated API response shape differs from what the UI expects.

Expected invariants:

- The lead opens both actual diffs and reads the interface call path.
- It rejects the integrated defect despite the reports and green checks.
- It sends a bounded repair to the responsible coordinator, then requires coordinator review, lead review, and affected integration validation again.

## Untraceable change and lead-authored repair

Initial state:

- A team diff contains an unrelated module rename.
- The lead also makes a tightly coupled integration repair after the prior owner stops writing that scope.

Expected invariants:

- The unrelated rename is rejected without reverting unrelated user edits.
- Every delivered change traces to the shared goal or an explicit acceptance condition or uncertainty.
- The lead reads its own repair under the same review gate and reports it as self-reviewed, not independently reviewed.

## The reviewed revision changes

Initial state:

- A team passes individual acceptance, then an integration repair changes an affected path.

Expected invariants:

- The earlier approval is not treated as evidence for the new integrated state.
- The lead re-checks affected logic and integration before delivery.
- No outstanding writer races final review, and no acceptance condition is closed with evidence from an obsolete revision.

## Long-running max-effort workers

Initial state:

- A coordinator and its native workers remain live across an empty wait window.

Expected invariants:

- The lead follows the live guide's liveness and wait protocol, not a timer-based failure rule.
- Silence alone does not trigger interruption, replacement, takeover, or pressure to interrupt the Luna workers.
- It continues supervising without busy polling and does not deliver a required incomplete outcome.

## Repair after settlement or release

Initial state:

- One coordinator has an active Dispatch, another has settled with a retained terminal, and another was released.

Expected invariants:

- Active guidance targets the active Dispatch.
- A settled coordinator's repair is a new Task on its exact retained terminal.
- A released coordinator is replaced by a fresh verified session with a complete packet and no continuity claim.
- Each new repair result still passes both review gates.

## Ambiguous launch or unresolved native writers

Initial state:

- A launch has partial residual resources, or a coordinator stops while its native workers' state remains unknown.

Expected invariants:

- The lead inspects authoritative runtime state and follows documented recovery rather than blindly retrying.
- The old coordinator and native workers must be unable to modify the scope before write ownership transfers.
- Unknown resources are disclosed, never relabeled as cleaned up.
- No duplicate writer is started to hide an incomplete required outcome.

## Isolated worktrees still require integrated verification

Initial state:

- A demonstrated checkout conflict required a separate worktree for one team.

Expected invariants:

- The report identifies the real source revision or patch and changed files.
- The lead integrates through the repository's authorized procedure and preserves the baseline.
- It reviews and validates the actual combined state, not merely separate worktree results.
- Worktree placement does not grant shared-file ownership or authorization to commit, push, or merge externally.

## The goal is too small for multiple teams

Prompt:

> Use $orca-swarm-lead to fix one misspelled local variable.

Expected invariants:

- The lead evaluates useful independent work and states why multiple teams are not justified.
- It uses one bounded team or direct execution without inventing assignments or claiming multi-team parallelism.
- Direct lead changes still pass the lead's review and proportionate validation.

## Required evidence or an external action is unavailable

Initial state:

- All teams submit, but a required integration check cannot run.
- A team suggests pushing or deploying despite no such authorization.

Expected invariants:

- The lead leaves the unverified acceptance condition open and reports the specific validation blocker.
- It does not treat completion messages or static cases as proof of runtime success.
- It does not authorize the push or deployment and reports remaining resource dispositions accurately.
