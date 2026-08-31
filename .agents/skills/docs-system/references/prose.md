# Prose and Terminology Rules

This is the single prose policy for governed documentation. Apply rules from
the meaning of each sentence. Do not select a writing mode for an entire
document or vary the policy according to the runtime environment.

## Invariants

1. **Preserve meaning.** A rewrite MUST NOT change facts, modality, negation,
   scope, numbers, conditions, safety constraints, uncertainty, or causal
   relationships.
2. **Do not add facts.** Keep verified fact, inference, assumption, and example
   distinct. A clearer sentence is still wrong when it strengthens the evidence.
3. **Use canonical terminology.** Use the established term for each concept.
   Do not rotate synonyms for variety or create a second term when one already
   has an owner.
4. **Keep clear prose unchanged.** Do not rewrite text only to demonstrate that
   this policy ran.

## Rule activation

| Sentence meaning | Required behavior |
| --- | --- |
| Action, procedure, requirement, or safety condition | State the actor, condition, action, and observable result when each affects correct execution. |
| Explanation, rationale, tradeoff, or uncertainty | Preserve the causal relationship, qualification, and necessary nuance. |
| Maintained claim | State its evidence or applicable boundary when readers cannot otherwise verify where it holds. |

One document can contain several sentence functions. Apply the relevant rules
to each sentence without changing the document to another prose system.

## Composition

- Put the conclusion before support when a reader needs the conclusion to act.
- Keep one primary claim or topic per paragraph.
- Prefer active voice when the actor affects responsibility or execution. Use
  passive voice when the actor is unknown or irrelevant.
- Split combined actions or claims when their combination creates ambiguity.
  Sentence length alone is only a diagnostic signal.
- Prefer direct verbs and concrete wording over nominalizations, ambiguous
  phrasal verbs, and promotional adjectives without measurements.
- Use a list for three or more parallel steps, conditions, or alternatives when
  the list makes their boundaries clearer.
- Treat long noun clusters as a review signal. Do not shorten precise wording
  when the shorter form changes meaning.

## Rewrite check

Before accepting a prose change:

1. Identify the canonical owner, established terminology, verified facts, and
   applicable boundaries.
2. Identify the meaning carried by the affected sentences.
3. Apply only the rules triggered by that meaning.
4. Compare the result with the original for facts, modality, negation, scope,
   numbers, conditions, safety constraints, uncertainty, causal relationships,
   and terminology.
5. Restore or revise any wording that changed protected meaning. Leave the
   original unchanged when no clearer correct version exists.

## Current state and evidence

- Architecture, Reference, Facts, and Operations documents describe current
  state. Historical narration, investigation process, and superseded
  alternatives belong in Decision, Proposal, or explicit history content.
- Claims based on evidence identify the source path, symbol, endpoint, snapshot,
  reproducible quantity, or canonical owner needed to verify them.
- Claims with limited applicability state the condition or boundary under which
  they stop holding.

## Non-English prose

Apply the language-neutral invariants: preserve meaning, make conditions
explicit, use canonical terminology, and keep paragraphs focused. Do not impose
English word counts, tense rules, phrasal-verb rules, or controlled vocabulary
on another language.

## Normative language

In a document that explicitly adopts RFC 2119-style normative keywords, use
their exact meanings:

| Term | Meaning |
| --- | --- |
| MUST / MUST NOT | Hard requirement / hard prohibition |
| SHOULD | Strong default with justified exceptions |
| MAY | Optional |

Ordinary operational and agent instructions can use direct imperatives such as
"Do not" and "never" as hard prohibitions. Do not replace them mechanically
with `MUST NOT`. Within a document that adopts the formal keyword vocabulary,
preserve its uppercase keywords and their declared meanings.

## Boundaries

- This policy improves governed technical prose; it does not certify compliance
  with an external controlled-language standard.
- Keep the policy self-contained. Installed Skills do not change its rules or
  execution path.
- Deterministic document validation does not prove semantic preservation.
  Perform the rewrite check against the actual source meaning.
