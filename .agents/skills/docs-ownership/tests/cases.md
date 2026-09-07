# Behavior Cases

Use these cases when changing skill routing or judgment. Review observable
decisions and proposed repository changes; synonymous wording is acceptable.

## Trigger routing

Should trigger:

- Decide which document owns a new durable fact, rule, or contract.
- Resolve two documents that state the same claim, or state it differently.
- Repair broken documentation links or documents orphaned from the entry.
- Judge whether a proposed document should exist at all.
- Resolve conflicting terminology across governed documentation.
- Clarify durable documentation prose when ambiguity changes maintained meaning
  or hides whether a statement is fact, inference, assumption, or example.

Should not trigger:

- Assign an identity, front matter, lifecycle value, or supersession link to a
  numbered record. Route that to the project's records workflow.
- Polish one-off prose, perform cosmetic copy editing without semantic impact,
  translate without structural change, or summarize without changing repository
  documentation.
- Change only code while leaving documentation untouched.
- Follow an established, more-specific generated-documentation workflow.
- Draft an artifact in chat without creating or changing repository files.

## Ownership behavior

### Place a claim by responsibility, not by audience

Given a retry limit that the client README, the API reference, and an onboarding
guide all mention, ask which document must change when the limit changes.

Pass when the API reference keeps the value, the other two link it, and no copy
of the number remains.

### Stop on unresolved ownership

Given a claim whose owner two domains contest with equal evidence, stop.

Pass when the report names both candidates and the missing evidence, and no
document is edited to force a resolution.

### Split a mis-scoped claim

Given one sentence stating both a wire-format constraint and a deployment
practice, treat it as two claims.

Pass when each part moves to its own owner rather than staying in one document
because it was written as one sentence.

### Reject a parallel entry

Given `docs/facts/README.md` already owns and routes the facts domain, reject a
request to add `docs/facts.md` with copied links.

Pass when the existing owner remains unique and no duplicate routing is added.

### Refuse a speculative domain

Given a request to create the standard domain set before any claim needs it,
create nothing.

Pass when only domains with real owned claims exist.

### Separate current state from history and intent

Given an architecture document that narrates why an approach was abandoned and
what the team intends to build next, keep only what currently holds.

Pass when the current behavior stays in the architecture document, the
narration moves to the project's history surface, and the intended change is
not described as current truth.

### Summarize without becoming a second owner

Given an onboarding page that summarizes an owned contract and adds one extra
condition, remove the addition.

Pass when the summary links the owner, carries no detail absent from it, and
copies no volatile status or count.

### Register instead of cross-linking

Given a new document that a sibling links but the domain entry does not list,
register it in the domain entry.

Pass when the document is reachable downward from the project entry, not only
through a peer link.

## Prose behavior

### Preserve protected meaning

Given a sentence carrying a condition, a negation, and an uncertainty
qualifier, rewrite only for clarity.

Pass when facts, modality, negation, scope, numbers, conditions, safety
constraints, and causal relationships are unchanged.

### Keep the canonical term

Given a document that alternates between two names for one concept, apply the
established term.

Pass when one term is used throughout governed consumers and no second term is
introduced.

### Leave clear prose unchanged

Given a correct, unambiguous paragraph, propose no rewrite.

Pass when the document is returned unchanged and the report says the policy
found nothing to correct.

### Treat length as a diagnostic

Given a long but precise sentence whose shorter form would drop a condition,
keep the original.

Pass when precision outranks the length signal.

### Preserve non-English meaning

Given a Chinese paragraph, apply the language-neutral invariants only.

Pass when meaning, conditions, and terminology are preserved and no English
word-count, tense, or controlled-vocabulary rule is imposed.

### Keep the document's normative vocabulary

Given a document that adopts RFC 2119 keywords, preserve them, and given one
that uses direct imperatives, do not convert them to `MUST NOT`.

Pass when each document keeps its declared normative vocabulary.

### Ignore installed prose Skills

Given another prose Skill is installed, apply this policy unchanged.

Pass when the rules and execution path do not vary with the environment.
