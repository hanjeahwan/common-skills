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

## Canonical prose behavior

### Preserve protected meaning

Given a contract says a client MAY retry at most three times only after a
timeout, simplify the wording without changing permission to obligation, the
retry limit, or the timeout condition.

Pass when modality, number, condition, and scope are unchanged. Fail when the
rewrite says the client MUST retry, omits the limit, or permits other triggers.

### Apply rules from sentence meaning

Given one Runbook paragraph contains an action followed by its rationale, make
the action's actor, condition, and observable result explicit while preserving
the rationale's causal relationship and qualification.

Pass when one prose policy governs both sentence functions without selecting a
document-wide mode or removing necessary explanation.

### Keep the canonical term

Given the canonical owner uses `workspace` while a draft alternates between
`workspace`, `project`, and `working directory` for the same concept, revise the
draft to use `workspace` without creating a glossary or synonym mapping.

Pass when one term remains for the concept and unrelated meanings of `project`
or `working directory` are not changed.

### Leave clear prose unchanged

Given a paragraph already states one verified claim with its boundary and uses
canonical terminology, review it for clarity.

Pass when the paragraph remains unchanged unless a concrete semantic ambiguity
is identified.

### Treat length as a diagnostic

Given a long sentence whose clauses jointly define one precise condition and
scope, review it for clarity when splitting or shortening would change that
meaning.

Pass when the sentence remains intact or the unresolved clarity concern is
reported. Fail when a numeric length target causes a condition, scope, or
qualification to disappear.

### Preserve non-English meaning

Given a Chinese procedure contains a necessary condition, explicit prohibition,
and numerical limit, improve its clarity.

Pass when those meanings remain explicit and no English word-count, tense,
phrasal-verb, or controlled-vocabulary rule is imposed.

### Ignore installed prose Skills

Run the same governed-document task in environments where another prose Skill
is present and absent.

Pass when `docs-system` reads the same local `references/prose.md`, applies the
same rules and verification gates, and neither detects nor invokes the other
Skill. A request for certified external-standard output reports the capability
boundary instead of switching prose systems.

### Preserve the document's normative vocabulary

Given a formal contract declares RFC-style keywords and uses `MAY` and
`MUST NOT`, preserve those keywords and their meanings during a rewrite. Given
an ordinary agent instruction says "Do not delete the workspace," keep the
direct prohibition unless the document itself adopts the formal vocabulary.

Pass when the rewrite preserves the document's declared normative system and
does not mechanically convert ordinary direct instructions into RFC keywords.
