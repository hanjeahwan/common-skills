---
name: autopilot
description: 将 define-goal、pstack:poteto-mode 和 pstack:show-me-your-work 连接成一条长期 Goal 工作流，在 notes topic 中持续推进、记录和验收跨 session 的目标。在用户调用 $autopilot 或明确要求以 notes 持续推进长期目标时使用，不用于无需持久 Goal 的一次性任务。
---

# Autopilot

## 目标

将长期目标从 notes topic 中的 Goal 定义推进到可验证的最终结果。使用既有 Skill 完成目标对齐、自治执行、决策记录和最终验收，并让每个阶段的状态与证据保持可恢复。

## 顺序

1. 使用 `$define-goal` 建立或复用唯一 Goal，并按其 workflow 推进。创建、搜索、编辑和校验遵循 notes 当前规范，Goal 正文不放在主题 README 中。
2. Goal 对齐、下一步明确且已获授权后，使用 `pstack:poteto-mode` Skill，并遵循其中的 `Autonomous run` playbook（`playbooks/autonomous-run.md`）。
3. 使用 `pstack:show-me-your-work` 维护同一份 TSV 决策日志，格式、追加规则和位置由它负责。重要动作、阶段结束或状态实质变化时，将结果更新到同一 topic 的 Goal 对应字段，不只追加总结。
4. 完成前回到 `$define-goal` 做验证、审查和最终验收，同时完成 `pstack:show-me-your-work` 要求的日志核对与跨模型审查。未完成的必要门槛如实记录，不声明目标完成。

长期 Goal 存放在 /Users/codeartz/workspaces/notes/projects/<project>/<topic>/ 的 notes topic 中。优先复用已有 topic 和 Goal 路径；新建时显式选用 topic 内的 goal.md，正文使用 `define-goal` 模板，不另建 docs/goals 副本。Goal 文档保存唯一任务定义、计划和验收状态。TSV 保存历史决策与证据，Goal 引用它，不复制当前状态。用户明确要求设置 Codex runtime Goal 时，将其关联到该文档，用于执行控制，不独立维护另一份目标或计划。

## 原则

- 先对齐目标，再开始实现。仅定义 Goal 文档不授权实施；调用本技能也不扩大授权。
- 目标不能漂移。新信息只能更新计划和证据，不能未经授权改变 objective、范围或验收标准。
- 继续调查直到得到足以决定下一步的答案，或确认真实 blocker。
- 任务结束必须自己验收，不能把命令成功当作目标完成。
- 优先验证真实链路、真实消费者、真实状态变化和副作用。
- 保留用户指定的环境、数据来源、消费入口和验收路径，除非用户明确授权替换。
- 可解决的可逆工作在已有授权范围内直接推进。`Autonomous run` playbook 的自动提交、PR 和任务外修复默认值不扩大授权。不可逆操作、生产变更、删除、强推和外部消息需要必要授权。
- 记录关键决策，但不制造膨胀的流水账或重复状态系统。
- 跨 session 恢复或上下文压缩后时使用 $pstack:recall，结合当前 Goal 和 TSV 决策日志恢复上下文、核实状态并确定下一步。中断操作先核实副作用是否已经发生。
- 发现既有决策时继续使用它，不要求用户重复确认已经明确的选择。
- 发现与目标无关的问题时记录并报告，不擅自扩大范围。
