# Output Blind A/B Review Pack

This packet hides whether each variant came from the baseline or the skill-guided output. Use the separate answer key only after review.

- Pairs: `3`
- Seed: `yao-output-eval-blind-v1`
- Answer key separate: `True`

## Case: bootstrap-without-empty-domains

Prompt: Review the attached bootstrap request. Return exactly four lines: DECISION: <APPLY|PARTIAL|REJECT>; DOCUMENTATION_ENTRY: <repository-relative path>; CHANGES: <semicolon-separated actions>; VALIDATION: <comma-separated checks>.

Rubric:
- `rejects-overbuild` (1.0): Accepts bootstrap but rejects speculative empty domains.
- `follows-migration-entry` (1.0): Uses the project-designated documentation entry.
- `validates-bootstrap` (1.0): Checks the migration and documentation-system invariants.

### Variant A

DECISION: PARTIAL
DOCUMENTATION_ENTRY: docs/README.md
CHANGES: perform the approved README.md to docs/README.md migration; route docs/api.md through docs/README.md; create no empty domains
VALIDATION: target topology, reachability, broken links, duplicate truth

### Variant B

DECISION: APPLY
DOCUMENTATION_ENTRY: docs/README.md
CHANGES: create docs/README.md; create docs/facts/; create docs/proposals/; create docs/decisions/
VALIDATION: links

## Case: reject-parallel-domain-entry

Prompt: Review the attached Facts entry request. Return exactly four lines: DECISION: <APPLY|PARTIAL|REJECT>; DOMAIN_ENTRY: <repository-relative path>; CHANGES: <semicolon-separated actions>; VALIDATION: <comma-separated checks>.

Rubric:
- `rejects-parallel-entry` (1.0): Rejects a second stable entry.
- `keeps-owner` (1.0): Keeps the existing domain owner.
- `validates-owner` (1.0): Checks ownership and reachability effects.

### Variant A

DECISION: REJECT
DOMAIN_ENTRY: docs/facts/README.md
CHANGES: keep the existing domain entry; do not create docs/facts.md
VALIDATION: reachability, duplicate truth, domain entry uniqueness

### Variant B

DECISION: APPLY
DOMAIN_ENTRY: docs/facts.md
CHANGES: create docs/facts.md; copy topic links; retain docs/facts/README.md
VALIDATION: links

## Case: migrate-implemented-proposal-truth

Prompt: Review the attached implemented Proposal request. Return exactly four lines: DECISION: <APPLY|PARTIAL|REJECT>; CURRENT_TRUTH_OWNER: <repository-relative path>; CHANGES: <semicolon-separated actions>; VALIDATION: <comma-separated checks>.

Rubric:
- `rejects-history-as-current-truth` (1.0): Rejects leaving current truth only in Proposal history.
- `updates-current-owner` (1.0): Routes the current contract to its owner.
- `validates-lifecycle` (1.0): Checks truth and lifecycle boundaries.

### Variant A

DECISION: REJECT
CURRENT_TRUTH_OWNER: docs/api.md
CHANGES: set the current timeout to 45 in docs/api.md; keep the implemented Proposal as history
VALIDATION: current truth, Proposal lifecycle, duplicate truth

### Variant B

DECISION: APPLY
CURRENT_TRUTH_OWNER: proposals/P001-timeout.md
CHANGES: update Proposal status and Outcome; leave docs/api.md unchanged
VALIDATION: Proposal fields
