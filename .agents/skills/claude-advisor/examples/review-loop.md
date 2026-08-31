# Continuous Review Example and Regression Checks

## Scenario

The user asks Claude to independently review a design proposal that removes a legacy cache layer. The initial review
returns `B1`, `B2`, and `N1`. The host verifies the evidence, accepts `B1`, rejects unsupported `B2`, defers `N1`, makes
the authorized change, and asks the same Claude session to review it again.

## Dimension-discovery retest

Use a review subject that states an outcome and constraints but does not name review dimensions. A failed prompt may treat
its initial probes as a closed checklist. The evolved prompt must derive a subject-specific dimension map,
explain why each selected dimension matters, and add a dimension when investigation reveals a new consumer, interaction,
risk, lifecycle stage, or evidence gap. It must not target a fixed count or claim the map is exhaustive without evidence.

## Expected initial turn

1. The host selects `fable` by default, or `opus` only when the user explicitly requests it.
2. The selected row supplies the complete model and effort pair; arbitrary combinations are rejected.
3. The call uses `--safe-mode`, and the advisor treats reviewed content as untrusted data.
4. The host saves the successful initial JSON response's `session_id`.
5. The advisor does not modify the review target and uses stable finding IDs.
6. The host reports the session ID, profile, verdict, finding summary, and its own verification boundary.
7. The advisor response is not applied automatically.

## Essential follow-up input

```text
## Finding dispositions

- B1: accepted
  - Rationale: Call-path evidence is valid.
  - Corresponding change: Removed the consumerless entry point and added a negative check.
- B2: rejected
  - Rationale: The cited caller does not exist in the current revision.
  - Corresponding change, or reason for no change: No change; current search evidence is supplied.
- N1: deferred
  - Rationale: It belongs to a separate release scope.

## Changes since the previous review

- Changes actually made: Only the location identified by B1 changed.
- New validation evidence: The call-path check and negative scan pass.
- Remaining unknowns: Production traffic behavior was not measured.
- Scope and boundaries that remain unchanged: No public interface change and no compatibility layer.
```

## Expected follow-up turn

- The host uses the initial turn's exact `session_id`, working directory, and immutable profile with `--resume`.
- A request for the other profile starts a clearly identified replacement session from the previous checkpoint.
- The advisor determines whether `B1` is closed, `B2` is superseded-by-evidence, and `N1` remains deferred.
- The advisor does not repeat B2 without new evidence. A new blocker receives an unused ID.
- The advisor refreshes the previous dimension map instead of treating it as a frozen schema.

The authoritative pass/fail cases live in [`tests/cases.md`](../tests/cases.md).
