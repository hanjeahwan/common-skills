---
name: docs-system
description: Bootstrap and maintain a reachable, single-owner documentation system in any repository. Use for documentation create/change/review/refactor, missing documentation entry or owner routing, broken links, or duplicate truth. Do not use for one-off prose with no durable owner, general copy editing, or documentation already governed by a more specific project workflow.
---

# docs-system

## Mission

Given this skill and repository read/write access, bootstrap existing
human-maintained documentation into a reachable, single-owner system, then
preserve those invariants through later documentation changes.

Owned output: changed canonical documentation, minimal routing/index changes,
removed duplicate truth, and validation evidence. This skill does not prescribe
which document domains a repository must have.

## Principles

1. One durable claim has one authoritative owner.
2. Current truth stays separate from Decision/Proposal history.
3. Governed documentation is reachable from the applicable project entry.
4. Structure follows stable reader questions and semantics, not chronology.
5. Follow an explicit project migration target; otherwise preserve valid
   existing structure and add only what ownership, lifecycle or reachability
   requires.

## Heuristics

- Ask: *Which document should change when this information changes?*
- Classify conflicts as fact, terminology, ownership, format, reachability or
  lifecycle before editing.
- Compare duplicated meaning, not only duplicated text.
- Create a document or template only after identifying its owner and entry path.
- Treat size and heading counts as diagnostic signals, never automatic quality
  rules.

## Hard Constraints

- MUST NOT maintain duplicate canonical claims, lifecycle status or routing
  instructions.
- MUST NOT leave governed docs unreachable or repository-internal links broken.
- MUST NOT treat implemented Proposals as current truth or rewrite historical
  Decisions to match current implementation.
- MUST NOT edit generated documentation directly or invent a second canonical
  term.
- Create a documentation domain only when it owns current artifacts.
- Each directory-organized domain has one stable entry.
- MUST run applicable validation before reporting completion.

## Workflow

1. Read applicable project instructions and lock the documentation root.
2. Read [`references/workflow.md`](references/workflow.md), then
   [`references/standard.md`](references/standard.md) and
   [`references/prose.md`](references/prose.md) as needed.
3. Follow the project entry to the relevant owner; classify the artifact and
   verify its inputs, consumers, links and lifecycle.
4. Modify the canonical owner, remove obsolete duplicates, and update routing
   only when topology changes.
5. Run generic and project-specific validation.
6. Report canonical owners changed, routing/lifecycle effects, duplicates
   removed, checks run and unresolved evidence gaps.

Failure policy: stop on unreadable inputs, unclear ownership, validator errors
or a materially larger migration than established. Preserve unrelated work and
never guess past missing evidence.

## Verification

Requires Python 3.10+ and only the standard library:

```bash
python3 .agents/skills/docs-system/scripts/validate.py <root>
python3 -m unittest discover -s .agents/skills/docs-system/tests -v
```

The generic validator checks artifact-local contracts only. Project topology,
required owners and entry reachability remain project validation or human
judgment. Before completion, review ownership, current truth versus history and
canonical terminology by hand. Reusable starters: [`proposal.md`](templates/proposal.md),
[`decision.md`](templates/decision.md), and [`runbook.md`](templates/runbook.md).
Deterministic behavior lives in [`scripts/validate.py`](scripts/validate.py);
routing cases live in [`evals/trigger_cases.json`](evals/trigger_cases.json), and
reviewable evidence is indexed in [`reports/README.md`](reports/README.md).
