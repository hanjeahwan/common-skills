# Investigation Targets And Question Gate

## Investigation targets

Reconstruct the objective, constraints, and current approach from the repository itself. Check first:

- project statements such as `README`, `AGENTS.md`, and `CLAUDE.md`;
- requirement and design material under `docs`, `spec`, `requirements`, issues, and tickets;
- the current branch's Git diff and the recent commits that touch it;
- dependency manifests, build configuration, environment configuration, and deployment configuration;
- program entry points, core modules, and how they call each other;
- data models, permission control, and external service interfaces;
- existing tests and the critical scenarios they actually cover;
- the code and documentation directly related to the change under review.

Locate the relevant scope first. Do not scan the whole repository without a target, and do not report a file as reviewed
when only its name was seen.

Record what was actually read. The report's investigation scope is that record, not an aspiration.

## Question gate

Never ask for information the repository, code, configuration, tests, or Git history can answer.

Ask the user only when all three hold at once:

1. the repository genuinely does not contain the answer;
2. different answers would materially change the review conclusion;
3. no reasonable read-only check can settle it.

Raise at most three questions per round. Mark ordinary uncertainty in the report instead of stopping the review for it.

An unanswered question does not become an assumption. Carry it into the unconfirmed-information section, and when it
blocks the route judgment, the route conclusion is `insufficient-evidence`.

## Evidence discipline

Separate observed facts, inferences, unknowns, and decisions that belong to the owner. When documentation and code
disagree, state the difference and which one is treated as the current fact. Git history explains intent and past
constraints; it does not prove that an old implementation must be preserved.
