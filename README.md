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

## Design Proposals

- [Codex Goal Loop refactor](docs/proposals/codex-goal-loop-refactor-proposal-20260831-134945.md) — implemented
