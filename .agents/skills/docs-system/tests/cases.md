# Behavior Cases

Use these cases when changing skill routing or judgment. Review observable
decisions and proposed repository changes; synonymous wording is acceptable.

## Trigger routing

Should trigger:

- Bootstrap repository documentation that has no clear entry or owners.
- Refactor durable claims so each has one canonical owner.
- Repair broken documentation links, orphans, or duplicate truth.
- Create a durable architecture document and register it through its owner.
- Resolve conflicting terminology across governed documentation.
- Clarify durable documentation prose when ambiguity changes maintained meaning
  or hides whether a statement is fact, inference, assumption, or example.

Should not trigger:

- Polish one-off prose, perform cosmetic copy editing without semantic impact,
  translate without structural change, or summarize without changing repository
  documentation.
- Change only code while leaving documentation untouched.
- Follow an established, more-specific generated-documentation workflow.
- Draft an artifact in chat without creating or changing repository files.

## Workflow behavior

### Bootstrap without speculative domains

Given an approved migration from the root README to `docs/README.md` and one
existing `docs/api.md`, preserve the approved entry and route the API document.
Do not create empty facts, proposals, or decisions domains.

Pass when the proposed graph is reachable and creates no empty domain.

### Reject a parallel entry

Given `docs/facts/README.md` already owns and routes the facts domain, reject a
request to add `docs/facts.md` with copied links.

Pass when the existing owner remains unique and no duplicate routing is added.

### Move implemented truth to its owner

Given an implemented Proposal records a 45-second timeout while `docs/api.md`
still says 30 seconds, update `docs/api.md` and retain the Proposal as history.

Pass when current truth and historical rationale have distinct owners without
conflicting canonical values.

### Stop on unresolved ownership

Given two competing documents and no applicable project entry or evidence of
which one owns the claim, do not select an owner or delete either document.

Pass when the result reports the evidence gap and requests the missing routing
or ownership decision.

### Resolve terminology through the canonical owner

Given a canonical Reference uses `workspace` for a concept while two governed
consumers call it `project`, confirm the Reference owns the term and update the
consumers. Do not create a parallel glossary merely to synchronize both names.

Pass when one established term remains and the canonical owner is unchanged.

### Clarify prose without changing truth

Given a current-state Architecture document mixes verified behavior, an
unmarked assumption, and historical narration, preserve the verified claim,
label the assumption, and move or link the history to its proper artifact.

Pass when readers can distinguish current fact, assumption, and history without
new normative detail or changed technical meaning.
