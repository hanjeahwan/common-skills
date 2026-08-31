# Reference Standard

This document is the normative reference for the docs-system conventions:
ownership, reachability, document types, lifecycle, entry/index conventions,
structure policy and the machine-checkable contracts.

Scope of the generic validator: only contracts that can be judged
deterministically from an artifact or its path. Repository-specific owners,
required document sets, entry roots, governed sets and monorepo topology are
never inferred by the generic validator; projects enforce those themselves.

## 1. Ownership

Every durable claim has exactly one authoritative owner. Ownership is decided
by responsibility, not location:

> Which document should change when this information changes?

- If the answer is ambiguous, the claim is either duplicated or mis-placed.
- Non-owner documents may summarize for navigation or onboarding, but a summary
  MUST link the canonical owner, MUST NOT add normative detail absent from the
  owner, and MUST NOT copy volatile status/counts/taxonomy that would need
  ongoing synchronization. On conflict the owner wins; eliminate the conflict.
- One fact, one term, one status, one routing rule: never maintain parallel
  copies that must be kept in sync.

## 2. Reachability

Hard constraints:

- Every governed documentation artifact MUST be reachable from the applicable
  project `AGENTS.md` through repository-internal documentation links.
- Every repository-internal link on that entry graph MUST resolve.
- A file that exists but cannot be reached from the entry chain is an
  orphan/unreachable document.
- A link whose target does not exist is a broken/dead link.
- Cross-links do not replace formal registration: child docs of a
  directory-organized domain MUST be navigated by that domain's entry.
- Leaf documents do not need to backlink every ancestor; reachability is
  required downward from the entry.
- Generated artifacts, validator fixtures and other explicitly
  non-project-document content may be excluded by project policy.

The generic validator checks link integrity within a scanned root but never
guesses a project's entry root, governed set or topology; those are project
validation or agent verification.

## 3. Directory-domain entry convention

When a documentation domain is organized as a directory, its single stable
entry is:

```text
<domain>/README.md
```

The README provides index/routing and brings domain-owned child docs and child
domains into the reachable graph. Do not maintain a sibling `<domain>.md` as a
second stable entry.

Whether a directory is a documentation domain is judged by project context;
the generic validator never scans directories and guesses domains.

When an index uses a table, choose exactly one canonical shape from
[`templates/index.md`](../templates/index.md):

```text
Documentation entry: Question | Owner
Proposal index:     Proposal | Topic
Decision index:     Decision | Lifecycle | Lifecycle detail
Research/Finding:   Question | Record
Postmortem index:   Postmortem | Lesson
```

These columns are exact machine contracts; do not add duplicate ID, title,
filename or status columns. Facts and other project-owned taxonomies keep their
project-specific index shape. The generic validator recognizes canonical index
tables by headers and links, never by directory name.

## 4. Document types and lifecycle

Types are information types, not a mandatory document set. A project MAY have
any subset; empty domains are never created just because a type is supported.

| Type | Answers | Notes |
| --- | --- | --- |
| Entry / Index | "Where do I start, where next" | Navigation and necessary summaries only; never a second source of facts/contracts/decisions. |
| Architecture | "How does the system work now" | Current flow, components, boundaries, invariants, relationships. No proposal detail, decision rationale, execution status, investigation history or operational procedure. |
| Reference / Contract | "What is the precise definition" | Schema, fields, request/response shape, API contract, enums, terminology. |
| Facts | "What is the currently verifiable fact" | Facts have explicit scope, evidence and boundaries where needed. The concrete fact taxonomy / fact-card representation is project-owned. |
| Decision | "Why was this design adopted" | Preserves historical choices. Implementations change through supersession or a new decision; history is not rewritten to match the current implementation. |
| Proposal | "What do we intend to change" | A Proposal is not current truth. After implementation, current behavior enters canonical docs, required rationale enters Decisions, and the Proposal stays as history. |
| Research / Finding | "What did we observe or establish within this evidence boundary" | Record date, scope, evidence and invalidation conditions where needed; do not use lifecycle status to imply current truth. |
| Postmortem | "What happened, why, and where was the reusable lesson deposited" | The incident is already closed. Current rules belong in their canonical owner, not in a Postmortem lifecycle. |
| Operations / Runbook | "How to execute, verify, recover, troubleshoot" | Operational procedure is separate from Architecture. |
| Execution State | Transient tasks, progress, follow-ups | Not canonical knowledge; the project chooses Issues/PRs or another execution surface. |

Lifecycle status has exactly one authoritative location per contract:

- Proposal status: the Proposal front matter (`status:`). A Proposal domain
  README lists only ID/title/navigation and never copies status.
- Decision lifecycle: the decisions domain README. Decision bodies never copy
  status. The only lifecycle values are `current`, `partially-superseded`,
  `superseded` and `void`.
- `partially-superseded` and `superseded` rows link the successor Decision.
- A not-yet-made choice is not a Decision lifecycle state; route it to a
  Proposal, Issue or the project's execution-state surface.
- Research, Finding and Postmortem artifacts do not carry lifecycle status.
  Research and Findings use evidence boundaries; Postmortems link any reusable
  current rule to its canonical owner.

## 5. Structure policy

- **Strong template** — for artifacts whose fields carry stable semantic
  meaning/lifecycle/operational contract. Reusable starters are provided for
  Proposal, Decision, Index and Runbook (see `templates/`).
- **Stable skeleton** — for documents needing a stable reader model while the
  concrete content varies per project (e.g. Entry, Architecture, Reference).
  Constrains responsibility; no exact heading requirement; no empty sections.
- **Free prose** — for explanation, examples, local rationale. Only
  ownership, reachability, lifecycle, terminology and prose rules apply.

Project-specific fact representations MAY have their own stable local
structure; that contract remains owned by the project domain.

Length, repetition counts and heading counts are diagnostic signals only; they
MUST NOT become quality rules on their own.

## 6. Proposal convention

Identity:

```text
P###
```

Filename once adopted:

```text
P###-<durable-design-area>.md
```

Rules:

- IDs are three digits, zero-padded, and immutable.
- Historical/rejected/superseded IDs are never reused.
- New Proposals use the next unused numeric ID of the independent Proposal
  sequence.
- Proposal and Decision sequences are independent.
- Slug is lowercase ASCII kebab-case expressing the durable design/problem
  area. Version, status and timestamps never enter the filename. A title
  wording change does not rename the file automatically.
- A directory-organized Proposal domain uses `README.md` as its only stable
  entry.
- The authoritative lifecycle source is the Proposal front matter. The domain
  README lists only ID/title/navigation.

Required front matter:

```yaml
---
id: P005
status: draft
---
```

Status values:

```text
draft
accepted
implemented
rejected
superseded
```

Optional context:

```yaml
target_scope: v1.4
decisions:
  - D65
superseded_by: P009
```

- `target_scope` is context, not identity.
- `decisions` allows 0..N.
- `superseded_by` is used only when `status: superseded`.

Template sections (in order):

```md
## Summary
## Problem
## Scope
## Non-goals
## Proposal
## Migration
## Verification
```

`implemented` / `rejected` / `superseded` additionally require a final
`## Outcome` section.

Deterministic recognition: a file is a Proposal when its filename matches
`P###-*.md`, OR its YAML front matter contains `id: P###`. Once recognized,
Proposal checks apply; when both filename and metadata exist, the numeric ID
MUST agree. `README.md` is never a Proposal artifact.

## 7. Decision convention

Identity:

```text
D<n>
```

Rules:

- New Decisions use the next unused numeric ID of the independent Decision
  sequence; historical IDs are never reused.
- Proposal and Decision numbering are independent.

Required semantic fields:

```text
ID + Title
Decision
Rationale
Consequences
Reconsider when
```

Optional: Context, Rejected alternatives, Supersedes, Related decisions.

Per-file convention:

```text
D###-<adopted-conclusion>.md
```

The in-body identity stays `D<n>`; e.g. `D065-*` corresponds to `D65`.
Zero-padding exists only for filename sorting. The slug prefers the adopted
conclusion; a concise stable topic is acceptable for historical decisions that
cannot be safely summarized.

A directory-organized Decision domain uses `README.md` as its only stable
entry and lifecycle owner; decision bodies never copy status. The lifecycle
table uses exactly `Decision | Lifecycle | Lifecycle detail`, and these values:

```text
current
partially-superseded
superseded
void
```

`current` means the adopted conclusion is currently applicable. Adoption is a
historical event, not a lifecycle value. `partially-superseded` and
`superseded` link the successor Decision. `void` preserves an immutable ID for
a record that never constituted a valid Decision. Pending choices belong in a
Proposal, Issue or execution-state surface, never in the Decision index.
The generic validator recognizes this table from its headers and `D###-*.md`
links, never from a directory name. Project-specific paths and governed sets
remain the project validator's responsibility.

Template headings (in order):

```md
# D65 <title>

## Context                  (optional)
## Decision
## Rationale
## Consequences
## Rejected alternatives    (optional)
## Supersedes               (optional)
## Related decisions        (optional)
## Reconsider when
```

Deterministic recognition: filename matches `D###-*.md`. Once recognized, the
first H1 MUST declare the corresponding `D<n>` and the numeric identity MUST
match the filename. `README.md` is never a Decision body artifact.

## 8. Runbook convention

A Runbook is used only when a durable operational procedure exists:

```text
Purpose
Preconditions
Procedure
Verification
Rollback / Recovery
Failure modes / Escalation
```

If there is no rollback, say so explicitly. The Runbook is an authoring
template; the generic validator does not guess which ordinary Markdown files in
a project are Runbooks.

## 9. Canonical summary rule

Non-owner documents MAY summarize for navigation/onboarding, but MUST:

- link the canonical owner;
- add no new normative detail absent from the owner;
- not copy volatile status/count/taxonomy needing ongoing synchronization;
- defer to the owner as the only authority on conflict, and eliminate the
  conflict.

## 10. Generic validator

```bash
python3 <skill-root>/scripts/validate.py <documentation-root>
```

Resolve `<skill-root>` to the active `docs-system` directory. The target
repository does not need to contain its own copy of the Skill.

The validator only enforces reusable deterministic contracts that can be
judged from the artifact/path itself. It does not import project modules, does
not call project validators, does not run project hooks, and contains no
project-specific branches.

Checks where applicable:

- generic local Markdown link integrity in the scanned root;
- Proposal recognition / filename / ID / front matter / status / required
  sections / terminal `Outcome`;
- duplicate Proposal IDs;
- per-file Decision filename / numeric identity / required sections;
- duplicate Decision IDs (where deterministically identifiable);
- reusable template starter validity;
- this skill's own stable `SKILL.md` structure (self-validation only).

Scan boundary:

- Normal project scan: `<root>` project documentation/content.
- Docs-system self-validation: `SKILL.md`, `references/`, `templates/`
  (auto-detected when the scanned root contains this skill's `SKILL.md`).
- Test fixtures: `tests/` fixtures are intentionally-invalid or non-governed
  content and never participate in a normal project scan.

Project-specific topology, reachability and required-entry enforcement remain
the project validator's or agent verification's responsibility.
