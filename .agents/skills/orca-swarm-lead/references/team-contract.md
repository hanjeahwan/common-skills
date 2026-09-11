# Team Assignment And Reporting Contract

Use these fields to compose Orca Task specs and reports. They are message content, not new runtime commands, lifecycle states, or a second task database. Orca owns the active Task and Dispatch identities; the bound goal owns the current overall acceptance conditions.

## Team Task Packet

Fill concrete values before launch. An assignment is a bounded snapshot of the shared goal, not authority to rewrite that goal. The packet must be readable without the lead's conversation.

```yaml
goal_ref: authoritative goal or Orca Run reference
objective: one team subgoal and its contribution to the shared outcome
facts: verified context needed to begin; distinguish remaining hypotheses
baseline: workspace and starting revision when available; relevant existing changes to preserve
scope: allowed files, components, and questions
write_owner: files or components this team alone may modify; empty means read-only
dependencies: prerequisite evidence, interface expectations, and which team supplies each
acceptance: observable conditions for this subgoal, mapped to the overall goal
validation: applicable checks and the behavior each must establish
exclusions: do-not-touch areas, out-of-scope actions, and inherited authorization limits
team_skill: resolved codex-luna-swarm path available inside the coordinator session
report_to: lead's actual runtime-provided communication route
report_contract: startup; decision-relevant progress; immediate blockers; reviewed submission with evidence
```

Include the following composition instructions in every team assignment:

- Act as the coordinator of this team only. Use the resolved `codex-luna-swarm` for worker execution and personally review all team changes.
- Establish effective session configuration and permitted native collaboration before implementation. Report dependency or policy incompatibility rather than improvising another topology.
- Send startup readiness and report relevant progress, blockers, ownership conflicts, and the reviewed result to the lead. All teams report, including read-only teams and failed attempts.
- Do not change shared interfaces, team ownership, or the overall goal without a lead decision. Ask through the live preamble's blocking-question mechanism; continue only genuinely independent authorized work.
- Pass only bounded work and evidence to native workers, never the coordinator's Orca lifecycle authority. Workers report to you; you report to the lead.
- Check lead follow-ups at natural checkpoints and before submitting completion, using the live guide. A send receipt alone does not prove a scope change was read or accepted.
- Settle native worker assignments and personally review the team result before sending your own Dispatch's completion. Use the exact lifecycle arguments, explicit outcome, summary format, and idle rules required by the live preamble.
- Treat team success as a submission for lead acceptance, not completion of the shared user goal. A repair is subject to both review gates again.

Do not copy all of `codex-luna-swarm` into this packet. Its implementation and review rules remain authoritative for the team's internal work.

## Reports To The Lead

A report must answer what the lead can now decide and where it can verify the answer. Use the live guide's message and completion formats; the fields below describe the information, not a replacement wire schema.

| Report event | Required information |
|---|---|
| Startup | Actual Task/Dispatch/terminal references; resolved Skill; launch-evidence coordinates; native collaboration availability and policy; understood ownership; blockers |
| Decision-relevant progress | Subgoal advanced; concrete finding or change; evidence coordinates; effect on acceptance or dependencies |
| Blocker or conflict | What cannot proceed; conflicting evidence or ownership; affected files/teams; minimal lead decision needed; independent work still safe to continue |
| Reviewed submission | Subgoal result; actual changes; coordinator review findings and resolutions; checks and outcomes; outstanding risks; native-worker disposition |

A reviewed submission contains:

```yaml
assignment: actual Task and Dispatch references
result: direct answer or completed team subgoal, mapped to assigned acceptance
changes: changed files and symbols; real diff or patch coordinates and source revision when available
evidence: decision-bearing file locations, logs, artifacts, or authoritative sources
coordinator_review: inspected changes, concrete findings, fixes, and any self-authored portion
validation: commands actually run and results; failures, blocked checks, and omissions separately
remaining: unresolved risks, cross-team dependencies, and decisions still needed
worker_disposition: evidence that required native workers settled; disclose any unresolved resources
```

Report event names are not Orca lifecycle states. Use the runtime's actual success/failure outcome fields. If completion requires a short executive summary, put detailed evidence in supported messages or a real report artifact and reference it; do not invent a report path or overload the summary with a transcript.

## Lead Acceptance And Repair

The lead opens the actual owned diff and decision-bearing evidence, not just the report. A submission missing required evidence stays unaccepted. Successful team-local checks do not prove the final cross-team behavior.

For a concrete rejection, return the defect and its location, failed acceptance condition, authorized repair scope, and required verification. Use active-Dispatch guidance while running, a new Task on the exact retained terminal after settlement, or a fresh verified coordinator after release. A fresh session receives a complete packet; a label or old ID cannot restore lost context.

When assignments change, identify which prior outcome or assumption is superseded and notify each affected coordinator. Do not keep two concurrent authorities for the same file, and do not release dependent writes merely because the update was enqueued.

## Example: API And UI For One Error-Handling Goal

The shared goal is to reject invalid requests and display the resulting validation errors correctly.

The lead gives the API team ownership of server validation and the shared error contract. The UI team owns rendering and client error handling, but is read-only on that shared contract. Both teams may investigate immediately. UI implementation that depends on the error shape waits until the lead confirms evidence for that contract and the UI coordinator has received the decision.

Each coordinator may form its own useful Luna split and reviews its team's result. Both report to the lead. The lead inspects both actual diffs and checks the API-to-UI failure path in the integrated state; two separate green test reports are insufficient. A UI fix requiring a shared-contract change goes back through the lead to the contract's owning team.
