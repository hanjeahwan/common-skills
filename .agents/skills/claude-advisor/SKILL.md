---
name: claude-advisor
description: Starts and resumes an independent, read-only Claude CLI advisor session for reviewing proposals, designs, code, or documentation with stable finding IDs and explicit follow-up dispositions. Use when the user asks for a Claude second opinion, independent review, architecture or proposal review, or wants the same Claude reviewer to continue after changes. Do not use for ordinary Claude implementation delegation or when the user only wants the current agent's own review.
---

# Claude Advisor

Act as an independent reviewer, not an implementer. The host agent selects the target, supplies evidence, decides which
findings to accept, performs any authorized changes, and verifies the result. Investigate read-only and return traceable
review findings.

## Resource Guide

- Load [`references/prompts.md`](references/prompts.md) for the initial and follow-up prompt contracts.
- Load [`examples/review-loop.md`](examples/review-loop.md) when checking expected two-turn behavior or regressions.

## Advisor Profiles

Support exactly two model profiles:

| Profile | Model | Effort | Selection |
| --- | --- | --- | --- |
| `fable` | `claude-fable-5` | `high` | Default when the user does not choose a profile |
| `opus` | `claude-opus-5` | `max` | Use only when the user explicitly chooses Opus |

Treat each row as an indivisible profile. Do not mix models and effort levels. On resume, keep the session's current
profile unless the user explicitly selects the other supported profile.

## Workflow

### 1. Choose start or resume

- Start a new review session only for the first Claude advisor turn on a review subject.
- Resume when the user asks to continue, run a second review, re-review changes, or use the same Claude reviewer.
- A resume requires the conversation `session_id` explicitly saved from the successful first call. Never use `-c` to
  guess the latest session. Never infer a conversation ID from `~/.claude/session-env`, a plan filename, process ID, or
  directory timestamp.
- If the current context has no trustworthy `session_id`, stop and report that continuity cannot be proven. Start a new
  session with the previous checkpoint only after the user agrees that it is a replacement rather than a true resume.

### 2. Establish the read-only boundary

State the objective, review target, constraints, non-goals, and acceptance checks before calling Claude. Grant access only
to paths required for the review. Use explicit `--add-dir` entries for additional directories; never expose a broad user
directory merely for convenience.

Every call must:

- use `--permission-mode plan`;
- use `--tools "Read,Glob,Grep"`, without Bash access;
- use `--disallowed-tools "Edit,Write,NotebookEdit"`;
- explicitly forbid file changes, commits, deployments, messages, or other external-state changes in the prompt;
- never use `--dangerously-skip-permissions`;
- exclude credentials, cookies, tokens, unrelated files, and raw private transcripts from the prompt;
- keep Git history, test output, and other shell evidence under host-agent control. The host may collect them read-only and
  label them as supplied evidence; missing evidence remains unverified instead of widening your permissions.

Your response is advice, not a source of truth. The host must verify cited paths, code, facts, and runtime evidence and
must not apply the response automatically.

Derive subject-specific review dimensions from material risks and evidence. The prompt contract owns the discovery rules;
its probes are neither a fixed checklist nor a ceiling.

### 3. Start the initial review

1. Select one profile from [Advisor Profiles](#advisor-profiles). Default to `fable`; use `opus` only when explicitly
   requested. Set `advisor_model` and `advisor_effort` from that row without accepting arbitrary combinations.
2. Build the prompt from [`references/prompts.md`](references/prompts.md#initial-review-prompt).
3. Write the prompt with a safe file-writing tool into an exact directory created by `mktemp -d`, then pass it through
   stdin. Never interpolate user text into a shell command and never use `eval`.
4. Run the command from the review target's owning working directory:

```sh
claude -p \
  --model "$advisor_model" \
  --effort "$advisor_effort" \
  --permission-mode plan \
  --tools "Read,Glob,Grep" \
  --disallowed-tools "Edit,Write,NotebookEdit" \
  --output-format json \
  < "$advisor_prompt_path"
```

5. Treat the session as established only when the process exits zero, the JSON result reports success, and it returns a
   non-empty `session_id`. Save that value as `advisor_session_id`, together with the profile, review target, turn number,
   verdict, and finding IDs required by later turns.
6. Remove the exact temporary prompt copy after capturing the result. Never store prompts, transcripts, or session state
   inside the Skill directory.

`-p` means print the response and exit. It does not disable persistence. Never add `--no-session-persistence`.

### 4. Decide finding dispositions

The host verifies your evidence before assigning one disposition to every finding:

- `accepted`: the evidence holds and the recommendation is adopted;
- `rejected`: the evidence or recommendation does not hold, with a recorded reason;
- `deferred`: valid but outside the current scope or awaiting authority;
- `unresolved`: the available evidence is insufficient.

Your `APPROVE` is not implementation verification, and `REVISE` does not authorize changes. If the user asks for
implementation, the host performs it separately under the current task's rules and validates it independently.

### 5. Resume the same session for follow-up review

Prepare four kinds of delta instead of replaying the entire history:

1. each previous finding's disposition and rationale;
2. the changes actually made since the last review;
3. new validation evidence and remaining unknowns;
4. scope and boundaries that remain unchanged.

The previous dimension map is context, not a frozen schema. Rebuild the map when the delta exposes a new risk, consumer,
lifecycle stage, interaction, or evidence gap.

Use the original session ID and review working directory. Default to the saved profile; change it only when the user
explicitly selects the other supported profile, then derive `advisor_model` and `advisor_effort` from the profile table.
Build the prompt from [`references/prompts.md`](references/prompts.md#follow-up-review-prompt):

```sh
claude -p \
  --resume "$advisor_session_id" \
  --model "$advisor_model" \
  --effort "$advisor_effort" \
  --permission-mode plan \
  --tools "Read,Glob,Grep" \
  --disallowed-tools "Edit,Write,NotebookEdit" \
  --output-format json \
  < "$advisor_prompt_path"
```

Never use `--fork-session`. The follow-up response must classify every previous finding as `closed`, `still-open`,
`regressed`, or `superseded-by-evidence`. New findings receive unused, monotonically increasing IDs.

## Boundaries

- `No conversation found`: stop immediately. Do not recreate a session under the same ID, silently switch sessions, or
  claim that context survived.
- Missing CLI, authentication failure, unavailable model, nonzero exit, or unsuccessful JSON: report the actual failure.
  Do not switch models or collaboration channels silently.
- Unsupported model or effort requests: offer only the `fable` and `opus` profiles. Do not synthesize a third profile.
- Unsupported claims in the response remain unverified; the host does not fill gaps with guesses.
- If the resumed conversation has drifted, first restate the checkpoint. If it remains inconsistent, stop
  and let the user decide whether to start a new review.
- A request to implement exits this Skill's read-only advisor boundary and returns to the host for a fresh
  authorization and Skill decision.

## Output Protocol

Report each completed turn in this form:

```md
Claude Advisor session: <session_id>
Turn: <number>
Profile: <fable | opus>
Model and effort: <model> / <effort>
Verdict: <APPROVE | REVISE>
Review dimensions: <selected, added, retired, and still-unverified dimensions>
Previous findings: <status summary; "none" for the first turn>
New findings: <IDs and one-line summaries; "none" when empty>
Host verification: <verified or unverified, with evidence boundary>
Next decision: <only when user input is still required>
```

## Quality Gate

Use [`examples/review-loop.md`](examples/review-loop.md) as the regression contract. A change passes only when its relevant
checks preserve resumable session identity, supported profiles, read-only operation, evidence boundaries, and dynamic
review dimensions.
