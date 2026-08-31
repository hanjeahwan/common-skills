# Prose and Terminology Rules

Rules for writing and editing governed documentation prose.

## Prose rules

1. **Conclusion first.** State the conclusion before the supporting detail.
   A reader scanning headings or first sentences must be able to act on the
   document.
2. **One primary claim per paragraph.** Each paragraph supports a single
   claim; supporting evidence belongs to that claim's paragraph. Split or
   restructure rather than stacking claims.
3. **Current-state prose outside decisions, proposals and explicit history.**
   Architecture, Reference, Facts and Operation documents describe the current
   state in the present tense. Historical narration, investigation process and
   superseded alternatives live in Decision/Proposal artifacts or explicit
   history sections, never in current-state docs.
4. **Canonical terminology.** Use the established canonical term for every
   concept. Do not invent a second term when a canonical term exists; when
   proposing a new term, check existing terminology first. Keep one name per
   concept across the whole documentation set.
5. **Evidence and boundaries.** Claims that rest on evidence state the evidence
   (source path, symbol, endpoint, snapshot, reproducible quantity). Claims
   that hold only under conditions state the boundary under which they stop
   holding, or where to read for the authoritative answer.
6. **Distinguish verified fact, inference, assumption and example.** Never
   present inference or assumption as fact, and never let an illustrative
   example read as verified truth.

## Normative language

Use the RFC 2119-style terms with their exact meanings:

| Term | Meaning |
| --- | --- |
| MUST / must not | Hard requirement / hard prohibition |
| SHOULD | Strong default with justified exceptions |
| MAY | Optional |

"Do not" / "never" in prose MUST NOT be used where "MUST NOT" is meant as a
normative prohibition; keep normative prohibitions machine-recognizable.