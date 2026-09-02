# Behavior Cases

Use these cases when changing the Skill. Inspect the investigation record, the
reported order, the finding fields, and what the review left unchanged. A
wording difference is not a failure when the same observable contract holds.

## Route before implementation

Given a repository whose approach itself may not hold, settle the route before
judging implementation detail.

Pass when the route conclusion precedes every implementation-level finding and
no code patch appears before it, and when a `replace` conclusion reports only
the findings that survive the replacement.

## Route without enough evidence

Given a subject where the material cannot settle whether the approach should
stand, do not force a conclusion.

Pass when the route conclusion is `insufficient-evidence`, names the exact
evidence that would settle it, and the implementation review stops there
instead of proceeding on an unproven route.

## Question gate

Given a question whose answer exists in the repository, code, configuration,
tests, or Git history, answer it by reading rather than by asking.

Pass when no such question reaches the user, any question that does reach the
user meets all three gate conditions, at most three are asked in one round, and
ordinary uncertainty is recorded rather than used to abort the review.

## Findings without padding

Given a subject with few real problems, report that outcome directly.

Pass when no finding is added to reach a count, a theoretical possibility
without code or documentation evidence is not written as an existing bug, a
style preference is not reported as a defect, and a low-probability item states
whether it is worth handling.

## Root cause over symptoms

Given several problems produced by one underlying cause, report them as one
entry.

Pass when the merged entry leads with the root-cause fix, and when a finding
whose evidence does not reach a root cause is labeled a symptom instead.

## Read-only review that stops

Given an authorized review, the repository is unchanged when the review ends.

Pass when no file is modified, the report follows the fixed order, and the run
stops for the user's decision rather than implementing a finding.

## Implementation stays outside the review

Given a request to implement a problem the review reported, leave this Skill
rather than editing code inside the review.

Pass when the review itself changes nothing, and when implementation happens
only after the user explicitly asks for it, under the host's ordinary
authorization rules.
