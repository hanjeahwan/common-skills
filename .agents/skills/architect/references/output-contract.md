# Finding Fields And Report Format

## Finding fields

Every implementation-level problem must carry:

- **Severity**: critical, high, medium, or low;
- **Confidence**: high, medium, or low;
- **Evidence**: the file, code, or configuration it rests on;
- **Trigger**: the concrete scenario that produces the problem;
- **Consequence**: what it causes when it happens;
- **Suggested direction**: how to handle it, not a patch;
- **Root cause or symptom**: which one this finding is.

Findings that share one root cause are merged into a single entry that leads with the root-cause fix rather than the
individual symptoms. When the evidence does not reach a root cause, say the finding is still a symptom.

Approach-level problems use the same fields and belong to the approach section, not the implementation section.

## Report format

Report in exactly this order:

1. **Investigation scope** — what was actually read, not what could have been read.
2. **Objective and current approach** — the problem being solved, the approach in use, and the files that produced that
   judgment.
3. **Unconfirmed key information** — including any question that reached the user and is still unanswered.
4. **Key assumptions of the current approach** — what must hold for the route to make sense.
5. **Approach-level problems** — problems no implementation fix can remove.
6. **Alternatives and trade-offs** — compared on requirement coverage, security risk, implementation complexity,
   maintenance cost, performance and resource cost, blast radius on failure, and migration or rollback difficulty. Write
   "none worth comparing" and the reason instead of inventing one.
7. **Route conclusion** — exactly one of `keep`, `adjust`, `replace`, or `insufficient-evidence`. An
   `insufficient-evidence` conclusion names the exact evidence that would settle the route.
8. **Implementation-level problems** — only when the route is worth keeping, using the finding fields above.
9. **Top three priorities** — at most three, in order. Write "none" when nothing requires action.
10. **Acceptable residual risk** — what can stand as-is for now, and why it is acceptable.
11. **Whether another review round is worth it** — recommend stopping when it has reached diminishing returns.

Sections 1 through 7 are produced before any implementation-level content. Section 8 is empty when the route conclusion
is `replace` and no finding survives the replacement, or when it is `insufficient-evidence`.

After the report, stop and wait for the user's decision. The review itself changes nothing in the repository.
