# Goal File Template

Use this template only when creating a goal file, restoring required sections, or applying an externally approved Goal Refinement. Keep the file at `.goal/<title-datetime>.md`.

```md
# Goal

## Protected Goal

### L0 Objective

### L1 Acceptance Criteria

- A1: ...

### Constraints

### Non-goals

---

## Working State

### Status

CONTINUE

### Acceptance Status

- A1: UNVERIFIED

### Current Iteration Target

### Established Facts

### Current Hypothesis

### Important Evidence

### Unknowns / Risks

### Next Best Action
```

## Section Ownership

- `Protected Goal` is the sole authority for L0 Objective and L1 Acceptance Criteria. Change it only after explicit external approval.
- `Working State` is a compressed, replaceable checkpoint. Patch this section after meaningful verification and before an invocation handoff.
- Refer to Acceptance Criteria by ID in `Working State`; do not duplicate or reinterpret their wording.
- Record evidence summaries and locations, not full transcripts or raw private data.
