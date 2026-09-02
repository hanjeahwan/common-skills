# Common Skills

Project-local Codex skills for durable goal execution and parallel coding with a mandatory review gate.

## Skills

### Codex Goal Loop

`$codex-goal-loop` pursues an explicitly requested bounded goal through evidence-driven Observe, Decide, Act, and Verify iterations.

- [Skill instructions](.agents/skills/codex-goal-loop/SKILL.md)
- [Behavior cases](.agents/skills/codex-goal-loop/tests/cases.md)

### Codex–Luna Swarm

`$codex-luna-swarm` delegates independent investigation or implementation units to GPT-5.6 Luna workers at max reasoning effort. GPT-5.6 Sol remains the sole coordinator, resolves conflicts, personally reviews integrated code, and owns final delivery.

- [Skill instructions](.agents/skills/codex-luna-swarm/SKILL.md)
- [Behavior cases](.agents/skills/codex-luna-swarm/tests/cases.md)

### Orca–Luna Swarm

`$orca-luna-swarm` runs the same pattern inside Orca: whichever agent invokes it is the coordinator, each Luna worker is a supervised Orca Dispatch, noisy investigation is delegated so the coordinator's context stays clean, and the coordinator personally reviews the integrated code before delivery.

- [Skill instructions](.agents/skills/orca-luna-swarm/SKILL.md)
- [Behavior cases](.agents/skills/orca-luna-swarm/tests/cases.md)

### Claude Advisor

`$claude-advisor` runs an independent, read-only Claude review with stable finding IDs and resumable follow-up review.

- [Skill instructions](.agents/skills/claude-advisor/SKILL.md)
- [Behavior cases](.agents/skills/claude-advisor/tests/cases.md)

### Architect

`$architect` reviews a repository as an independent architect, security reviewer, and code reviewer, settling whether the current approach should stand before judging any implementation detail, then stopping for the user's decision.

- [Skill instructions](.agents/skills/architect/SKILL.md)
- [Behavior cases](.agents/skills/architect/tests/cases.md)

### Docs System

`$docs-system` maintains reachable repository documentation with one canonical owner and one canonical term for each maintained claim and concept.

- [Skill instructions](.agents/skills/docs-system/SKILL.md)
- [Behavior cases](.agents/skills/docs-system/tests/cases.md)

## Design Proposals

- [Proposal index](docs/proposals/README.md)
