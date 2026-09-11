# Common Skills

Project-local Codex skills for durable goal execution and parallel coding with a mandatory review gate.

## Skills

### Codex Goal Loop

`$codex-goal-loop` pursues an explicitly requested bounded goal by driving every acceptance criterion of a schema-validated JSON contract to verified evidence. `scripts/goal.py` owns the contract state machine, and the contract is the only state the skill keeps.

- [Skill instructions](.agents/skills/codex-goal-loop/SKILL.md)
- [Behavior cases](.agents/skills/codex-goal-loop/tests/cases.md)

### Define Goal

`$define-goal` turns a stated objective into one standalone Goal document at `docs/goals/YYYYMMDD-<title>.md`, then advances that single document by evidence until the goal result holds.

- [Skill instructions](.agents/skills/define-goal/SKILL.md)
- [Behavior cases](.agents/skills/define-goal/tests/cases.md)

### Codex–Luna Swarm

`$codex-luna-swarm` delegates independent investigation or implementation units to GPT-5.6 Luna workers at max reasoning effort. The coordinator runs `gpt-6-astra` at `medium` reasoning effort, resolves conflicts, and personally reviews integrated code. It owns standalone delivery, or submits its reviewed team result to the lead when part of a lead-managed goal.

- [Skill instructions](.agents/skills/codex-luna-swarm/SKILL.md)
- [Behavior cases](.agents/skills/codex-luna-swarm/tests/cases.md)

### Orca Swarm Lead

`$orca-swarm-lead` keeps the invoking agent as lead on its current model and settings. The lead supervises multiple `gpt-6-astra` / `medium` coordinators in separate Orca terminals toward one shared goal. Each coordinator uses `codex-luna-swarm` for native `gpt-5.6-luna` / `max` workers, reviews its team's changes, and reports to the lead. The lead manages cross-team ownership and dependencies, personally reviews actual changes and the integrated result, and alone accepts the overall goal.

Use it in Orca with both skills available to coordinator sessions:

> Use $orca-swarm-lead to implement the API validation fix and its UI error handling as one goal. Coordinate the teams, review their actual changes, and verify the integrated behavior.

This requires a live Orca orchestration guide, verified coordinator launch settings, and a dispatch policy that permits native Codex subagents. Unsupported combinations stop at preflight rather than bypassing runtime limits. Unlike `orca-luna-swarm`, Orca supervises the coordinators here, not each native Luna worker.

- [Skill instructions](.agents/skills/orca-swarm-lead/SKILL.md)
- [Team contract](.agents/skills/orca-swarm-lead/references/team-contract.md)
- [Behavior cases](.agents/skills/orca-swarm-lead/tests/cases.md)

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

### Docs Ownership

`$docs-ownership` decides which document owns a durable claim, keeps governed documentation reachable from the project entry, and keeps terminology and prose faithful to the maintained meaning. It defines no record-keeping format.

- [Skill instructions](.agents/skills/docs-ownership/SKILL.md)
- [Behavior cases](.agents/skills/docs-ownership/tests/cases.md)

## Design Proposals

- [Proposal index](docs/proposals/README.md)
