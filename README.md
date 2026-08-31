# Common Skills

Project-local Codex skills for durable goal execution and parallel coding with a mandatory review gate.

## Skills

### Codex Goal Loop

`$codex-goal-loop` pursues an explicitly requested bounded goal through evidence-driven Observe, Decide, Act, and Verify iterations.

A structured contract owns the objective, acceptance criteria, constraints, and non-goals. Native Codex Goal owns lifecycle, budget, and usage. Working State remains a replaceable evidence checkpoint and never duplicates `CONTINUE`, `BLOCKED`, or `DONE` as lifecycle state.

- [Skill instructions](.agents/skills/codex-goal-loop/SKILL.md)
- [Behavior cases](.agents/skills/codex-goal-loop/tests/cases.md)

### Codex–Luna Swarm

`$codex-luna-swarm` delegates independent investigation or implementation units to GPT-5.6 Luna workers at max reasoning effort. GPT-5.6 Sol remains the sole coordinator, resolves conflicts, personally reviews integrated code, and owns final delivery.

- [Skill instructions](.agents/skills/codex-luna-swarm/SKILL.md)
- [Behavior cases](.agents/skills/codex-luna-swarm/tests/cases.md)

### Claude Advisor

`$claude-advisor` runs an independent, read-only Claude review with stable finding IDs and resumable follow-up review.

- [Skill instructions](.agents/skills/claude-advisor/SKILL.md)
- [Behavior cases](.agents/skills/claude-advisor/tests/cases.md)

### Docs System

`$docs-system` maintains reachable repository documentation with one canonical owner and one canonical term for each maintained claim and concept.

- [Skill instructions](.agents/skills/docs-system/SKILL.md)
- [Behavior cases](.agents/skills/docs-system/tests/cases.md)

## Design Proposals

- [Proposal index](docs/proposals/README.md)
