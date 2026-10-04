# Common Skills

Project-local Codex skills for durable goal execution and parallel coding with a mandatory review gate.

## Skills

### Codex Goal Loop

`$codex-goal-loop` pursues an explicitly requested bounded goal by driving every acceptance criterion of a schema-validated JSON contract to verified evidence. `scripts/goal.py` owns the contract state machine, and the contract is the only state the skill keeps.

- [Skill instructions](.agents/skills/codex-goal-loop/SKILL.md)
- [Behavior cases](.agents/skills/codex-goal-loop/tests/cases.md)

### Define Goal

`$define-goal` defines or updates one persistent Goal document at `docs/goals/YYYYMMDD-<title>.md` and restates the user's goals and problem in the conversation. When advancement is authorized, it tracks dependency-aware phases through verification, review, repair, and evidence-backed final acceptance. Defining the document alone does not authorize the underlying work.

- [Skill instructions](.agents/skills/define-goal/SKILL.md)
- [Behavior cases](.agents/skills/define-goal/tests/cases.md)

### Codex–Luna Swarm

`$codex-luna-swarm` delegates independent investigation or implementation units to native workers on `gpt-6-luna` at max reasoning effort. The invoking host remains the sole coordinator on its current model and reasoning settings, resolves conflicts, personally reviews integrated code, and owns final delivery.

- [Skill instructions](.agents/skills/codex-luna-swarm/SKILL.md)
- [Behavior cases](.agents/skills/codex-luna-swarm/tests/cases.md)