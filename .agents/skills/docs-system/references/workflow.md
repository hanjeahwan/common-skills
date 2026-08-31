# Documentation Workflow

Detailed execution rules for bootstrap, maintenance, integration and recovery.
The contracts for ownership, artifact types and lifecycle remain authoritative
in [`standard.md`](standard.md).

## Bootstrap an unintegrated repository

Use bootstrap when the project lacks an applicable instruction route, a stable
documentation entry or clear canonical owners.

1. Read applicable project instructions, preferring `AGENTS.md` when present,
   and identify any project-approved target topology or migration contract.
2. Inventory human-maintained README files, docs, contracts, historical records,
   operations material and their links.
3. Classify artifacts by responsibility: Entry/Index, Architecture,
   Reference/Contract, Facts, Decision, Proposal, Operations, Execution State or
   a project-owned type.
4. Build the Markdown link graph and identify entry candidates, broken links,
   orphans, duplicate claims and competing owners.
5. Assign each durable claim by asking which document must change when the claim
   changes.
6. When the project defines a target topology, migrate existing artifacts and
   links toward it while preserving their valid content ownership. Otherwise,
   preserve valid owners and structure and add only a missing entry, owner or
   lifecycle boundary.
7. Use the project-designated entry. Without one, select the best existing entry
   or create a minimal project-owned index.
8. Establish one project-level instruction route to this skill and the project
   documentation entry when the project uses agent instructions.
9. Make governed documentation reachable and repair dead links and unintended
   orphans.
10. Run the generic validator and the project's established validation entry
    when it provides project-specific documentation checks.

## Maintain an integrated repository

1. Read applicable instructions and enter through this skill.
2. Follow the project documentation entry to relevant canonical owners.
3. Classify the information type and choose strong template, stable skeleton or
   free prose.
4. Read the owner and directly relevant producers, consumers and links.
5. Modify the owner; elsewhere use a link or short non-normative summary.
6. Remove statements made stale or duplicate by the change.
7. Register new or moved artifacts in their domain/project entry path.
8. Update domain entry, project entry and backlinks only when topology changes.
9. Apply `prose.md`, reusable templates and project-local contracts.
10. Run generic and project validation, then report changed owners, routing,
    lifecycle, removed duplicates and validation evidence.
11. When real use exposes a repeatable failure, add the smallest regression at
    its owner: routing failures to trigger evals, workflow failures to output
    evals, and deterministic validator failures to unit tests.

## Integration boundary

A project uses one downward entry chain:

```text
applicable AGENTS.md
  -> project documentation entry
       -> domain index / standalone owner
            -> owned child documentation
```

`AGENTS.md` routes agent work; project documentation routes knowledge. Ordinary
canonical docs do not duplicate this skill workflow. The generic validator does
not parse agent instructions or infer project topology.

## Failure and recovery

- Heavy conflict with no clear entry: preserve current structure and add only a
  minimal entry before later convergence.
- Unclear validator error: stop and report the exact error and files.
- Unreadable or missing input: state the evidence boundary and request the path
  or permission.
