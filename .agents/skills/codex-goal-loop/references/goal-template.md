# Goal Contract Template

Use this template when creating a contract, restoring required sections, migrating a legacy file, or applying an externally approved refinement.

The default local path is `.goal/<title-datetime>.md`. When cross-machine, fresh-clone, or cloud resume is explicitly required, use the user-approved tracked project-document path instead.

```md
# Goal: <title>

## Protected Goal

### L0 Objective

### L1 Acceptance Criteria

- A1: ...

### Constraints

### Non-goals

---

## Working State

### Acceptance Status

- A1: UNVERIFIED | VERIFIED
  - Evidence: <observable result and locator>
  - Observed: <timestamp or invocation>
  - Invalidated by: <changes that require re-verification>

### Current Iteration Target

### Established Facts

### Current Hypothesis

### Important Evidence

### Unknowns / Risks

### Pending External Decision

### Next Best Action
```

## Section Ownership

- `Protected Goal` is the sole authority for the display title, L0 Objective, L1 Acceptance Criteria, constraints, and non-goals. Change it only after explicit user approval.
- Native Codex Goal is the sole authority for lifecycle, budget, and usage state. Never add `CONTINUE`, `BLOCKED`, or `DONE` to this file as lifecycle status.
- `Working State` is a compressed, replaceable evidence checkpoint. Patch it after meaningful verification and before an invocation handoff.
- Refer to Acceptance Criteria by ID in Working State; do not duplicate or reinterpret their wording.
- Preserve still-valid evidence across invocations. Re-verify evidence affected by its invalidation conditions or time-sensitive external facts.
- Record evidence summaries and locators, not full transcripts or raw private data.
