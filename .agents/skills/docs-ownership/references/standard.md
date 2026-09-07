# Reference Standard

This document is the normative reference for docs-ownership: the ownership
boundary, reachability, document classification, structure policy, the
canonical summary rule, and the duplicate-truth patterns this skill repairs.

Record-keeping formats are out of scope. Identity schemes, front matter,
lifecycle tables, and supersession contracts for numbered records belong to a
records-specific workflow. This reference governs only where their claims live
and how those claims read.

## 1. Ownership boundary

Every durable claim has exactly one authoritative owner. Ownership is decided by
responsibility, not by location, audience, or which document is easiest to edit:

> Which document must change when this information changes?

- When the answer names one document, that document is the owner.
- When the answer names two, the claim is duplicated. Keep the owner, and
  replace the other copy with a link or a conforming summary.
- When the answer names none, the claim has no owner yet. Establish one before
  writing it down, or stop and report the ambiguity.
- When the answer depends on who is asking, the claim is mis-scoped. Split it
  into the parts that have distinct owners.

A durable claim is a fact, contract, rule, definition, or procedure that the
project maintains. Transient execution state is not a durable claim; route it to
Issues, PRs, or the project's execution surface rather than to a document.

One fact, one term, one status, one routing rule: never maintain parallel copies
that must be kept in sync.

## 2. Reachability

**Governed documentation** is any human-maintained document that owns a durable
claim, whatever its name or location. A file that tooling loads by convention
rather than by navigation — `AGENTS.md`, `CLAUDE.md`, a contributor guide — is
governed as soon as it owns one; register it in the entry instead of treating
it as infrastructure. Generated output, vendored third-party text and test
fixtures own no durable claim and are not governed.

**The applicable project entry** is the one the project's instructions name.
When they name none, default to the repository `README.md` and report that
assumption with the result. An agent instruction file routes agent work and
sits upstream of the documentation entry; do not treat it as the entry merely
because it is read first.

Hard constraints:

- Every governed documentation artifact MUST be reachable from the applicable
  project entry through repository-internal documentation links.
- Every repository-internal link on that entry graph MUST resolve.
- A file that exists but cannot be reached from the entry chain is an orphan.
- A link whose target does not exist is a broken link.
- Cross-links do not replace registration: child docs of a directory-organized
  domain MUST be navigated by that domain's entry.
- Leaf documents do not need to backlink every ancestor. Reachability is
  required downward from the entry.
- A document that owns a durable claim but is deliberately held outside the
  governed set MUST be recorded as an exemption in the entry or the project
  instructions, with its reason. A `--exclude` glob on a validator invocation
  carries out that record; it is never the only place the exemption exists.

Existing project structure outranks this reference when it is **valid**: every
durable claim it holds has exactly one owner, and every governed document has a
reach path from the entry. Structure failing either test does not outrank the
hard constraints above; repair it, or record the exemption.

The validator checks link integrity within the scanned root, and reports orphans
only when the caller names the entry. It never guesses a project's entry root,
governed set, or topology; those remain project validation or agent
verification.

## 3. Directory-domain entry convention

When a documentation domain is organized as a directory, its single stable entry
is:

```text
<domain>/README.md
```

The README provides index and routing, and brings domain-owned child docs and
child domains into the reachable graph. Do not maintain a sibling `<domain>.md`
as a second stable entry.

Whether a directory is a documentation domain is judged by project context. The
validator never scans directory names to infer domains.

## 4. Document classification

Types are information types, not a mandatory document set. A project MAY have
any subset. Never create a domain because a type is supported.

| Type | Answers | Owns |
| --- | --- | --- |
| Entry / Index | "Where do I start, where next" | Navigation and the summaries needed to route. Never a second source of facts, contracts, or conclusions. |
| Architecture | "How does the system work now" | Current flow, components, boundaries, invariants, relationships. No intent, rationale history, execution status, or operational procedure. |
| Reference / Contract | "What is the precise definition" | Schema, fields, request and response shape, API contract, enums, terminology. |
| Facts | "What is currently verifiable" | Facts with explicit scope, evidence, and boundaries where needed. The concrete fact representation is project-owned. |
| Operations | "How to execute, verify, recover" | Durable operational procedure, kept separate from Architecture. |
| History | "Why was this adopted, what did we intend" | Adopted rationale and prior intent. History is not rewritten to match the current implementation, and it is not current truth. |
| Evidence | "What did we observe within this boundary" | Observation, date, scope, and invalidation conditions. Do not use it to imply current truth outside its boundary. |
| Execution State | Tasks, progress, follow-ups | Not durable knowledge. The project chooses Issues, PRs, or another execution surface. |

The separation that matters most is between **current state**, **history**, and
**intent**. Current-state documents describe what holds now. History records why
a choice was adopted. Intent records what someone means to change. When an
intended change lands, its current behavior moves to the current-state owner;
the intent record stays as history and never becomes the source of truth.

The format used to store history or intent is a project choice, and this skill
does not define it.

## 5. Structure policy

- **Strong structure** — for artifacts whose fields carry a stable semantic or
  operational contract, such as numbered records. The required-section contract
  belongs to the workflow owning that artifact type, not to this skill.
- **Stable skeleton** — for documents needing a predictable reader model while
  the content varies per project, such as Entry, Architecture, and Reference.
  It constrains responsibility, not exact headings.
- **Free prose** — for explanation, examples, and local rationale. Only
  ownership, reachability, terminology, and prose rules apply.

Length, repetition counts, and heading counts are diagnostic signals only. They
MUST NOT become quality rules on their own.

## 6. Canonical summary rule

A non-owner document MAY summarize for navigation or onboarding, but MUST:

- link the canonical owner;
- add no normative detail absent from the owner;
- copy no volatile status, count, or taxonomy that would need ongoing
  synchronization;
- defer to the owner as the only authority on conflict, and eliminate the
  conflict rather than describe it.

## 7. Duplicate-truth patterns

These are the recurring failures this skill repairs. Each names its fix.

| Pattern | Why it fails | Fix |
| --- | --- | --- |
| Parallel entry: `<domain>.md` beside `<domain>/README.md` | Two stable entries diverge; readers and links split | Keep one entry; redirect or delete the other |
| Non-owner copies a status, count, or list | Requires ongoing synchronization and silently goes stale | Link the owner; delete the copy |
| Summary adds a detail absent from the owner | Creates a second normative source under a navigation label | Move the detail to the owner, or delete it |
| Entry or index accumulates facts | The index becomes an unowned source of truth | Move each fact to its owner; leave routing |
| Current-state doc narrates history | Readers cannot tell what holds now | Move the narration to history; state the current behavior |
| Intent record treated as current truth | The system is documented as the change intended, not as built | Move landed behavior to the current-state owner |
| Two terms for one concept | Search, review, and automation split | Establish the canonical term; apply it to governed consumers |
| Doc restates code with no maintained meaning | Duplicates a source that already changes independently | Delete it, or replace it with the constraint the code cannot express |
| Cross-link used instead of registration | The document stays an orphan from the entry | Register it in its domain entry |
| Domain created for a type nobody uses | Empty structure invites speculative content | Delete the domain until a real claim needs it |

## 8. Generic validator

```bash
python3 <skill-root>/scripts/validate.py <root>
python3 <skill-root>/scripts/validate.py <root> --entry README.md --exclude 'generated/*'
```

Resolve `<skill-root>` to the active `docs-ownership` directory. The target
repository does not need its own copy of the Skill.

The validator enforces only what a link graph proves:

- every local Markdown link in the scanned root resolves;
- with `--entry`, which Markdown files the entry cannot reach.

Links inside fenced code blocks are examples, not links, and are ignored by
both checks.

It imports no project modules, calls no project validators, runs no project
hooks, and contains no project-specific branches. Ownership correctness,
terminology consistency, prose accuracy, and the absence of duplicate truth are
not machine-checkable here; verify them against the claims themselves.

Scan boundary:

- `<root>` is the project documentation or content root. The validator judges
  no document by its type, name, or location, and skips only version-control
  and cache directories.
- Everything else stays in scope until `--exclude` names it, so skipping a file
  is always the caller's explicit choice. When the skipped document owns a
  durable claim, §2 also requires the exemption to be recorded.
