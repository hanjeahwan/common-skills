---
name: autopilot
description: Connect $define-goal, $pstack:poteto-mode, and $pstack:show-me-your-work into a long-term Goal workflow to advance, record, and verify goals across sessions in a notes topic. Use when the user invokes $autopilot or explicitly requests ongoing advancement of a long-term goal through notes. Do not use for one-off tasks that need no persistent Goal.
---

# Autopilot

## Goal

Advance a long-term goal from its definition in a notes topic to a verifiable final result. Use existing Skills for goal alignment, autonomous execution, decision recording, and final acceptance, keeping each phase's state and evidence recoverable.

## Sequence

1. Use `$define-goal` to establish or reuse the single Goal and advance it through its workflow. Use `$pstack:technical-writing` when writing or updating the Goal document. Follow the current notes rules for creation, search, editing, and validation. Keep the Goal body out of the topic README.
2. Once the Goal is aligned, the next action is clear, and authorization is established, use the `$pstack:poteto-mode` Skill and follow its `Autonomous run` playbook (`playbooks/autonomous-run.md`).
3. Use `$pstack:show-me-your-work` to maintain the same TSV decision log. It owns the format, append rules, and location. After important actions, at phase completion, or when state materially changes, update the corresponding Goal fields in the same topic rather than only appending summaries.
4. Before completion, return to `$define-goal` for verification, review, and final acceptance. Also complete the log audit and cross-model review required by `$pstack:show-me-your-work`. Record any unmet required gates honestly and do not declare the goal complete.

Long-term Goals live in a notes topic at /Users/codeartz/workspaces/notes/projects/<project>/<topic>/. Prefer reusing an existing topic and Goal path. When creating one, explicitly use goal.md within the topic and the `$define-goal` template for its body. Do not create a separate copy under docs/goals. The Goal document holds the single task definition, plan, and acceptance state. The TSV holds historical decisions and evidence. The Goal references it without duplicating current state. When the user explicitly requests a Codex runtime Goal, link it to this document for execution control rather than maintaining a separate goal or plan.

## Principles

- Align the goal before starting implementation. Defining a Goal document alone does not authorize implementation, and invoking this Skill does not expand authorization.
- Do not let the goal drift. New information may update the plan and evidence, but must not change the objective, scope, or acceptance criteria without authorization.
- Continue investigating until you have enough evidence to decide the next action or confirm a genuine blocker.
- Verify acceptance yourself before ending the task. A successful command does not establish goal completion.
- Prioritize verification of the real workflow, actual consumers, actual state changes, and side effects.
- Preserve the user-specified environment, data sources, consumer entry points, and acceptance path unless the user explicitly authorizes a replacement.
- Proceed directly with solvable, reversible work within existing authorization. Obtain the necessary authorization for irreversible actions, production changes, deletion, force pushes, and external messages.
- Record key decisions without creating bloated activity logs or duplicate state systems.
- When resuming across sessions or after context compaction, use $pstack:recall with the current Goal and TSV decision log to restore context, verify state, and determine the next action. Before resuming an interrupted operation, check whether its side effects have already occurred.
- Reuse existing decisions when you find them. Do not ask the user to reconfirm choices that are already clear.
- Record and report problems unrelated to the goal without expanding scope on your own.
