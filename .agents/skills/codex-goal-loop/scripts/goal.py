#!/usr/bin/env python3
"""State machine and validator for Codex Goal Loop contracts.

A contract is one JSON file, normally `.goal/<title>-<YYYYMMDD-HHmmss>.json`,
validated against `../schemas/goal.schema.json` plus the cross-field
invariants in `check_invariants`. Every command that mutates the contract
validates the result before writing it, so an invalid contract is never
persisted.

The contract stores facts only. Criterion state is derived, never stored:

    verified   evidence is present
    blocked    an open decision blocks the criterion
    exhausted  failed attempts reached protected.max_attempts
    open       none of the above

Authority split (see SKILL.md):

- `protected` is the semantic authority. Only `decision resolve --approve` on a
  refinement decision may change it.
- `working` is a replaceable evidence checkpoint keyed by criterion id.
- `current` resolves the contract by scanning `.goal/`; the contract is the only
  state this script reads or writes.

Requires Python 3.10+ and the `jsonschema` package.

Usage:
    python3 goal.py [--root DIR] <command> ...
    python3 goal.py <command> --help
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from jsonschema import Draft202012Validator, FormatChecker
except ImportError:  # pragma: no cover - reported to the caller
    sys.stderr.write(
        "goal.py requires the `jsonschema` package "
        "(python3 -m pip install jsonschema)\n"
    )
    sys.exit(2)

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "goal.schema.json"
CONTRACT_DIR = ".goal"
DEFAULT_MAX_ATTEMPTS = 10
GITIGNORE_ENTRIES = {"/.goal/", ".goal/", ".goal", "/.goal"}



class GoalError(Exception):
    """A contract or command precondition failed."""


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or "goal"


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def load_schema() -> dict:
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def schema_errors(contract: dict) -> list[str]:
    # `format: date-time` is enforced only when jsonschema's optional
    # rfc3339-validator dependency is installed; otherwise jsonschema skips it.
    # Timestamps are only written by this script, so that is acceptable.
    validator = Draft202012Validator(load_schema(), format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(contract), key=lambda e: [str(p) for p in e.absolute_path])
    return [
        f"{'/'.join(str(p) for p in error.absolute_path) or '<root>'}: {error.message}"
        for error in errors
    ]


def check_invariants(contract: dict) -> list[str]:
    """Cross-field rules the schema cannot express."""
    errors: list[str] = []
    protected = contract["protected"]
    working = contract["working"]
    ids = [a["id"] for a in protected["acceptance"]]
    if len(ids) != len(set(ids)):
        errors.append("protected.acceptance ids must be unique")
    if set(ids) != set(working["acceptance"]):
        errors.append(
            "working.acceptance keys must equal protected.acceptance ids "
            f"(protected={sorted(ids)}, working={sorted(working['acceptance'])})"
        )
    decision_ids = [d["id"] for d in working["decisions"]]
    if len(decision_ids) != len(set(decision_ids)):
        errors.append("decision ids must be unique")
    for decision in open_decisions(contract):
        for cid in decision["blocks"]:
            if cid not in ids:
                errors.append(f"{decision['id']} blocks unknown criterion {cid}")
        refinement = decision.get("refinement")
        if refinement:
            errors.extend(_refinement_shape_errors(decision["id"], refinement))
    return errors


def _refinement_shape_errors(did: str, refinement: dict) -> list[str]:
    """Rules that stay true for the life of the decision, whatever `protected` becomes."""
    target, op = refinement["target"], refinement["operation"]
    proposed = refinement.get("proposed")
    errors: list[str] = []
    if target in ("objective", "max_attempts") and op != "set":
        errors.append(f"{did}: {target} supports only operation=set")
    if target in ("constraints", "non_goals") and op == "set":
        errors.append(f"{did}: {target} supports only add or remove")
    if target == "max_attempts" and not (proposed and proposed.isdigit() and int(proposed) >= 1):
        errors.append(f"{did}: max_attempts requires a positive integer in proposed")
    if op in ("set", "add") and not proposed:
        errors.append(f"{did}: operation {op} requires proposed text")
    if op == "remove" and target not in ("constraints", "non_goals") and proposed:
        errors.append(f"{did}: operation remove must not carry proposed text")
    if target in ("constraints", "non_goals") and not proposed:
        errors.append(f"{did}: {target} {op} requires the exact text in proposed")
    return errors


def refinement_conflict(contract: dict, refinement: dict) -> str | None:
    """Why this refinement cannot be applied to `protected` as it stands now.

    Checked when the decision is opened and again when it is approved, because an
    earlier approval can invalidate a later proposal. It is not a stored-contract
    invariant: an open decision that has gone stale must stay writable so the user
    can still reject it.
    """
    protected = contract["protected"]
    ids = [a["id"] for a in protected["acceptance"]]
    target, op = refinement["target"], refinement["operation"]
    proposed = refinement.get("proposed")
    if target in ("constraints", "non_goals"):
        if op == "add" and proposed in protected[target]:
            return f"{target} already contains that text"
        if op == "remove" and proposed not in protected[target]:
            return f"{target} does not contain that text"
        return None
    if target in ("objective", "max_attempts"):
        return None
    if op == "add" and target in ids:
        return f"{target} already exists"
    if op in ("set", "remove") and target not in ids:
        return f"{target} does not exist"
    if op == "remove" and len(ids) == 1:
        return "a contract keeps at least one acceptance criterion"
    return None


def validate(contract: dict) -> list[str]:
    errors = schema_errors(contract)
    if errors:
        return errors
    return check_invariants(contract)


# --------------------------------------------------------------------------
# Persistence
# --------------------------------------------------------------------------

def resolve_contract(root: Path, raw: str, must_exist: bool = True) -> Path:
    """Resolve a locator and require it to stay below the workspace root.

    Absolute paths, `..`, and symlink escapes all fail the containment check.
    """
    path = (root / raw).resolve()
    if root not in path.parents:
        raise GoalError(f"contract path must be workspace-relative and stay inside the workspace: {raw}")
    if must_exist and not path.is_file():
        raise GoalError(f"contract not found: {raw}")
    return path


def load(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as handle:
            contract = json.load(handle)
    except json.JSONDecodeError as error:
        raise GoalError(f"contract is not valid JSON: {error}") from error
    errors = validate(contract)
    if errors:
        raise GoalError("contract is invalid:\n  " + "\n  ".join(errors))
    return contract


def save(path: Path, contract: dict) -> None:
    errors = validate(contract)
    if errors:
        raise GoalError("refusing to write invalid contract:\n  " + "\n  ".join(errors))
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as handle:
        json.dump(contract, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    os.replace(tmp, path)


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


# --------------------------------------------------------------------------
# Derived state
# --------------------------------------------------------------------------

def new_criterion_facts() -> dict:
    return {"approach": None, "steps": [], "attempts": [], "evidence": None}


def undone_steps(facts: dict) -> list[dict]:
    return [s for s in facts["steps"] if s["done_at"] is None]


def next_step(facts: dict) -> str | None:
    pending = undone_steps(facts)
    return pending[0]["text"] if pending else None


def facts_of(contract: dict, cid: str) -> dict:
    try:
        return contract["working"]["acceptance"][cid]
    except KeyError:
        raise GoalError(f"unknown criterion {cid}") from None


def statement(contract: dict, cid: str) -> str:
    for item in contract["protected"]["acceptance"]:
        if item["id"] == cid:
            return item["statement"]
    raise GoalError(f"unknown criterion {cid}")


def open_decisions(contract: dict) -> list[dict]:
    return [d for d in contract["working"]["decisions"] if d["resolution"] is None]


def blocked_ids(contract: dict) -> dict[str, list[str]]:
    """Map criterion id -> open decision ids that block it."""
    blocked: dict[str, list[str]] = {}
    for decision in open_decisions(contract):
        ids = set(decision["blocks"])
        refinement = decision.get("refinement")
        if refinement:
            target = refinement["target"]
            if target == "objective":
                ids.update(criterion_ids(contract))
            elif re.fullmatch(r"A[1-9][0-9]*", target):
                ids.add(target)
        for cid in ids:
            blocked.setdefault(cid, []).append(decision["id"])
    return blocked


def is_verified(contract: dict, cid: str) -> bool:
    return facts_of(contract, cid)["evidence"] is not None


def is_exhausted(contract: dict, cid: str) -> bool:
    return len(facts_of(contract, cid)["attempts"]) >= contract["protected"]["max_attempts"]


def state_of(contract: dict, cid: str) -> str:
    if is_verified(contract, cid):
        return "verified"
    if cid in blocked_ids(contract):
        return "blocked"
    if is_exhausted(contract, cid):
        return "exhausted"
    return "open"


def criterion_ids(contract: dict) -> list[str]:
    return [a["id"] for a in contract["protected"]["acceptance"]]


def require_unblocked(contract: dict, cid: str) -> None:
    blockers = blocked_ids(contract).get(cid)
    if blockers:
        raise GoalError(
            f"{cid} is blocked by open decision(s) {', '.join(blockers)}; resolve them first"
        )


def next_decision_id(contract: dict) -> str:
    numbers = [int(d["id"][1:]) for d in contract["working"]["decisions"]]
    return f"D{max(numbers, default=0) + 1}"


def ensure_gitignored(root: Path, contract_path: Path) -> None:
    gitignore = root / ".gitignore"
    existing = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
    lines = {line.strip() for line in existing.splitlines()}
    if not lines & GITIGNORE_ENTRIES:
        with gitignore.open("a", encoding="utf-8") as handle:
            if existing and not existing.endswith("\n"):
                handle.write("\n")
            handle.write("/.goal/\n")
    if not (root / ".git").exists():
        return
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "check-ignore", "-q", "--", relative(root, contract_path)],
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        raise GoalError("git is not available; cannot confirm that the contract path is ignored") from None
    if result.returncode == 1:
        raise GoalError(
            f"{relative(root, contract_path)} is not ignored by git; fix .gitignore before creating the contract"
        )
    if result.returncode != 0:
        raise GoalError(f"git check-ignore failed: {result.stderr.strip()}")


def choose_next(contract: dict) -> dict:
    """Deterministically pick what the loop works on next."""
    states = {cid: state_of(contract, cid) for cid in criterion_ids(contract)}
    pending = open_decisions(contract)
    if all(state == "verified" for state in states.values()):
        if pending:
            return {"kind": "await", "decisions": [d["id"] for d in pending]}
        return {"kind": "ready"}
    candidates = [cid for cid, state in states.items() if state == "open"]
    if not candidates:
        stuck = [cid for cid, state in states.items() if state == "exhausted"]
        if stuck:
            return {"kind": "exhausted", "criteria": stuck, "max_attempts": contract["protected"]["max_attempts"]}
        return {"kind": "await", "decisions": [d["id"] for d in pending]}
    in_progress = [cid for cid in candidates if facts_of(contract, cid)["approach"]]
    cid = in_progress[0] if in_progress else candidates[0]
    facts = facts_of(contract, cid)
    return {
        "kind": "pursue",
        "criterion": cid,
        "statement": statement(contract, cid),
        "reason": "approach already in progress" if in_progress else "first open criterion",
        "approach": facts["approach"],
        "next_step": next_step(facts),
        "attempts": facts["attempts"],
    }


def readiness(contract: dict) -> list[str]:
    """Reasons the contract is not finished."""
    reasons = [f"{cid} is {state_of(contract, cid)}" for cid in criterion_ids(contract) if not is_verified(contract, cid)]
    reasons.extend(f"{d['id']} ({d['kind']}) is unresolved" for d in open_decisions(contract))
    return reasons


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def cmd_init(args: argparse.Namespace) -> int:
    root = args.root
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if args.path:
        path = resolve_contract(root, args.path, must_exist=False)
        if path.parent == (root / CONTRACT_DIR).resolve():
            raise GoalError(f"--path is for tracked contracts; {CONTRACT_DIR}/ is ignored by git")
    else:
        path = resolve_contract(root, f"{CONTRACT_DIR}/{slugify(args.title)}-{stamp}.json", must_exist=False)
        ensure_gitignored(root, path)
    if path.exists():
        raise GoalError(f"refusing to overwrite existing contract {relative(root, path)}")
    ids = [f"A{n}" for n in range(1, len(args.accept) + 1)]
    contract = {
        "schema_version": 1,
        "title": args.title,
        "created_at": now(),
        "protected": {
            "objective": args.objective,
            "acceptance": [{"id": cid, "statement": text} for cid, text in zip(ids, args.accept)],
            "constraints": args.constraint,
            "non_goals": args.non_goal,
            "max_attempts": args.max_attempts,
        },
        "working": {
            "acceptance": {cid: new_criterion_facts() for cid in ids},
            "risks": args.risk,
            "decisions": [],
        },
    }
    save(path, contract)
    locator = relative(root, path)
    print(f"Contract: {locator}\n")
    print("If a runtime goal is set for this work, use this objective verbatim:")
    print(f"  Pursue the contract at {locator} with $codex-goal-loop until `ready` passes.")
    return 0


def cmd_current(args: argparse.Namespace) -> int:
    """Resolve the single unfinished contract under .goal/.

    Unfinished means `ready` would fail. A finished contract stays on disk as a
    record and is never returned here, so a new goal does not collide with it.
    """
    directory = args.root / CONTRACT_DIR
    unfinished: list[str] = []
    finished: list[str] = []
    invalid: list[str] = []
    for path in sorted(directory.glob("*.json")) if directory.is_dir() else []:
        rel = relative(args.root, path)
        try:
            contract = load(path)
        except GoalError as error:
            sys.stderr.write(f"warning: ignoring {rel}: {error}\n")
            invalid.append(rel)
            continue
        (unfinished if readiness(contract) else finished).append(rel)
    legacy = sorted(relative(args.root, p) for p in directory.glob("*.md")) if directory.is_dir() else []
    if len(unfinished) == 1:
        print(unfinished[0])
        return 0
    if not unfinished:
        tail = "".join(
            f"; {label}: {', '.join(items)}"
            for label, items in (("invalid", invalid), ("legacy", legacy), ("finished", finished))
            if items
        )
        raise GoalError(f"no unfinished contract in {CONTRACT_DIR}/{tail}")
    raise GoalError(
        "more than one unfinished contract; name the one to use: " + ", ".join(unfinished)
    )


def cmd_validate(args: argparse.Namespace) -> int:
    path = resolve_contract(args.root, args.contract)
    with path.open(encoding="utf-8") as handle:
        try:
            contract = json.load(handle)
        except json.JSONDecodeError as error:
            print(f"INVALID {args.contract}: not JSON ({error})")
            return 1
    errors = validate(contract)
    if errors:
        print(f"INVALID {args.contract}")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"VALID {args.contract}")
    return 0


def summary(contract: dict) -> dict:
    blocked = blocked_ids(contract)
    return {
        "title": contract["title"],
        "objective": contract["protected"]["objective"],
        "constraints": contract["protected"]["constraints"],
        "non_goals": contract["protected"]["non_goals"],
        "max_attempts": contract["protected"]["max_attempts"],
        "acceptance": [
            {
                "id": item["id"],
                "statement": item["statement"],
                "state": state_of(contract, item["id"]),
                "blocked_by": blocked.get(item["id"], []),
                **facts_of(contract, item["id"]),
            }
            for item in contract["protected"]["acceptance"]
        ],
        "risks": contract["working"]["risks"],
        "decisions": contract["working"]["decisions"],
        "next": choose_next(contract),
        "not_ready_because": readiness(contract),
    }


def print_status(contract: dict) -> None:
    protected = contract["protected"]
    working = contract["working"]
    blocked = blocked_ids(contract)
    print(f"# {contract['title']}")
    print(f"Objective: {protected['objective']}")
    for label, items in (("Constraints", protected["constraints"]), ("Non-goals", protected["non_goals"])):
        if items:
            print(f"{label}:")
            for item in items:
                print(f"  - {item}")
    print(f"Acceptance (max_attempts={protected['max_attempts']}):")
    for item in protected["acceptance"]:
        cid = item["id"]
        facts = facts_of(contract, cid)
        flags = f" blocked-by={','.join(blocked[cid])}" if cid in blocked else ""
        if facts["attempts"]:
            flags += f" failed={len(facts['attempts'])}/{protected['max_attempts']}"
        print(f"  {cid} [{state_of(contract, cid).upper()}]{flags} {item['statement']}")
        if facts["approach"]:
            print(f"      approach: {facts['approach']}")
        for index, step in enumerate(facts["steps"], start=1):
            mark = "x" if step["done_at"] else " "
            print(f"      [{mark}] {index}. {step['text']}")
        for attempt in facts["attempts"]:
            print(f"      failed: {attempt['approach']} -> {attempt['outcome']} ({attempt['observed_at']})")
        if facts["evidence"]:
            ev = facts["evidence"]
            print(f"      evidence: {ev['summary']} @ {ev['locator']} ({ev['observed_at']})")
            print(f"      invalidated by: {'; '.join(ev['invalidated_by'])}")
    if working["risks"]:
        print("Risks:")
        for index, risk in enumerate(working["risks"], start=1):
            print(f"  {index}. {risk}")
    if working["decisions"]:
        print("Decisions:")
        for decision in working["decisions"]:
            res = decision["resolution"]
            status = f"{res['outcome']} {res['at']}" if res else "OPEN"
            blocks = f" blocks={','.join(decision['blocks'])}" if decision["blocks"] else ""
            print(f"  {decision['id']} [{status}] {decision['kind']}{blocks}: {decision['request']}")
            if decision.get("refinement"):
                ref = decision["refinement"]
                proposed = f" -> {ref['proposed']}" if ref.get("proposed") else ""
                print(f"      {ref['operation']} {ref['target']}{proposed}")
    print_next(contract)


def print_next(contract: dict) -> None:
    choice = choose_next(contract)
    if choice["kind"] == "ready":
        print("Next: every criterion is verified and no decision is open; run `ready` to finish")
    elif choice["kind"] == "await":
        print(f"Next: awaiting user decision(s) {', '.join(choice['decisions'])}; no criterion can advance")
    elif choice["kind"] == "exhausted":
        print(
            f"Next: {', '.join(choice['criteria'])} reached {choice['max_attempts']} failed approaches; "
            "open a refinement or input decision instead of trying again"
        )
    else:
        print(f"Next: pursue {choice['criterion']} ({choice['reason']}): {choice['statement']}")
        if choice["approach"]:
            print(f"  approach: {choice['approach']}")
        if choice["next_step"]:
            print(f"  next step: {choice['next_step']}")
        if choice["attempts"]:
            print(f"  failed approaches: {len(choice['attempts'])} (do not repeat them unchanged)")


def cmd_status(args: argparse.Namespace) -> int:
    contract = load(resolve_contract(args.root, args.contract))
    if args.json:
        print(json.dumps(summary(contract), indent=2, ensure_ascii=False))
    else:
        print_status(contract)
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    contract = load(resolve_contract(args.root, args.contract))
    if args.json:
        print(json.dumps(choose_next(contract), indent=2, ensure_ascii=False))
    else:
        print_next(contract)
    return 0


def cmd_approach(args: argparse.Namespace) -> int:
    path = resolve_contract(args.root, args.contract)
    contract = load(path)
    cid = args.criterion
    require_unblocked(contract, cid)
    facts = facts_of(contract, cid)
    if is_verified(contract, cid):
        raise GoalError(f"{cid} is verified; invalidate it before changing its approach")
    if any(a["approach"] == args.approach for a in facts["attempts"]):
        raise GoalError(f"{cid}: this approach already failed; choose a different one")
    if is_exhausted(contract, cid):
        raise GoalError(
            f"{cid}: {len(facts['attempts'])} failed approaches reached max_attempts="
            f"{contract['protected']['max_attempts']}; open a decision instead of trying again"
        )
    facts["approach"] = args.approach
    save(path, contract)
    print(f"{cid}: approach set")
    return 0


def cmd_attempt(args: argparse.Namespace) -> int:
    path = resolve_contract(args.root, args.contract)
    contract = load(path)
    cid = args.criterion
    facts = facts_of(contract, cid)
    if is_verified(contract, cid):
        raise GoalError(f"{cid} is verified; invalidate it before recording a failure")
    approach = args.approach or facts["approach"]
    if not approach:
        raise GoalError(f"{cid} has no current approach; pass --approach")
    if approach != facts["approach"]:
        # Recording an approach that was never set is the same as setting it: same gates apply.
        require_unblocked(contract, cid)
        if any(a["approach"] == approach for a in facts["attempts"]):
            raise GoalError(f"{cid}: this approach is already recorded as failed")
        if is_exhausted(contract, cid):
            raise GoalError(
                f"{cid}: max_attempts={contract['protected']['max_attempts']} already reached; open a decision"
            )
    facts["attempts"].append({"approach": approach, "outcome": args.outcome, "observed_at": now()})
    if facts["approach"] == approach:
        facts["approach"] = None
    save(path, contract)
    limit = contract["protected"]["max_attempts"]
    tail = "limit reached, open a decision" if is_exhausted(contract, cid) else "choose a new approach"
    print(f"{cid}: recorded failed approach ({len(facts['attempts'])}/{limit}); {tail}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    path = resolve_contract(args.root, args.contract)
    contract = load(path)
    cid = args.criterion
    require_unblocked(contract, cid)
    facts = facts_of(contract, cid)
    pending = undone_steps(facts)
    if pending:
        raise GoalError(
            f"{cid} has {len(pending)} undone step(s); mark each `step done` or `step drop` before verifying"
        )
    facts["evidence"] = {
        "summary": args.summary,
        "locator": args.locator,
        "observed_at": now(),
        "invalidated_by": args.invalidated_by,
    }
    save(path, contract)
    print(f"{cid}: verified")
    print_next(contract)
    return 0


def cmd_invalidate(args: argparse.Namespace) -> int:
    path = resolve_contract(args.root, args.contract)
    contract = load(path)
    cid = args.criterion
    if not is_verified(contract, cid):
        raise GoalError(f"{cid} is not verified")
    facts_of(contract, cid)["evidence"] = None
    save(path, contract)
    print(f"{cid}: invalidated ({args.reason})")
    print_next(contract)
    return 0


def cmd_step(args: argparse.Namespace) -> int:
    path = resolve_contract(args.root, args.contract)
    contract = load(path)
    cid = args.criterion
    facts = facts_of(contract, cid)
    if not (args.add or args.done or args.drop):
        raise GoalError("nothing to change; pass --add, --done, or --drop")
    steps = facts["steps"]
    for index in sorted(set(args.done)):
        if not 1 <= index <= len(steps):
            raise GoalError(f"{cid} step {index} does not exist")
        if steps[index - 1]["done_at"]:
            raise GoalError(f"{cid} step {index} is already done")
        steps[index - 1]["done_at"] = now()
    for index in sorted(set(args.drop), reverse=True):
        if not 1 <= index <= len(steps):
            raise GoalError(f"{cid} step {index} does not exist")
        steps.pop(index - 1)
    steps.extend({"text": text, "done_at": None} for text in args.add)
    save(path, contract)
    pending = next_step(facts)
    print(f"{cid}: {len(undone_steps(facts))} step(s) undone" + (f"; next: {pending}" if pending else ""))
    return 0


def cmd_risk(args: argparse.Namespace) -> int:
    path = resolve_contract(args.root, args.contract)
    contract = load(path)
    risks = contract["working"]["risks"]
    if not (args.add or args.drop):
        raise GoalError("nothing to change; pass --add or --drop")
    for index in sorted(set(args.drop), reverse=True):
        if not 1 <= index <= len(risks):
            raise GoalError(f"risk {index} does not exist")
        risks.pop(index - 1)
    risks.extend(args.add)
    save(path, contract)
    print(f"risks: {len(risks)} open")
    return 0


def cmd_decision_open(args: argparse.Namespace) -> int:
    path = resolve_contract(args.root, args.contract)
    contract = load(path)
    blocks = list(dict.fromkeys(args.blocks))
    for cid in blocks:
        facts_of(contract, cid)
    decision = {
        "id": next_decision_id(contract),
        "kind": args.kind,
        "request": args.request,
        "blocks": blocks,
        "opened_at": now(),
        "resolution": None,
    }
    if args.kind == "refinement":
        if not (args.target and args.operation):
            raise GoalError("refinement requires --target and --operation")
        refinement = {"target": args.target, "operation": args.operation}
        if args.proposed:
            refinement["proposed"] = args.proposed
        conflict = refinement_conflict(contract, refinement)
        if conflict:
            raise GoalError(f"cannot propose that refinement: {conflict}")
        decision["refinement"] = refinement
    elif args.target or args.operation or args.proposed:
        raise GoalError("--target/--operation/--proposed apply only to kind=refinement")
    contract["working"]["decisions"].append(decision)
    save(path, contract)
    print(f"{decision['id']}: opened; report the exact request to the user and wait")
    return 0


def apply_refinement(contract: dict, refinement: dict) -> None:
    protected = contract["protected"]
    working = contract["working"]
    target, op = refinement["target"], refinement["operation"]
    if target == "objective":
        protected["objective"] = refinement["proposed"]
        for facts in working["acceptance"].values():
            facts["evidence"] = None
    elif target == "max_attempts":
        protected["max_attempts"] = int(refinement["proposed"])
    elif target in ("constraints", "non_goals"):
        if op == "add":
            protected[target].append(refinement["proposed"])
        else:
            protected[target].remove(refinement["proposed"])
    elif op == "set":
        for item in protected["acceptance"]:
            if item["id"] == target:
                item["statement"] = refinement["proposed"]
        working["acceptance"][target] = new_criterion_facts()
    elif op == "add":
        protected["acceptance"].append({"id": target, "statement": refinement["proposed"]})
        working["acceptance"][target] = new_criterion_facts()
    elif op == "remove":
        protected["acceptance"] = [a for a in protected["acceptance"] if a["id"] != target]
        working["acceptance"].pop(target)
        for decision in open_decisions(contract):
            decision["blocks"] = [c for c in decision["blocks"] if c != target]


def cmd_decision_resolve(args: argparse.Namespace) -> int:
    path = resolve_contract(args.root, args.contract)
    contract = load(path)
    decision = next((d for d in contract["working"]["decisions"] if d["id"] == args.decision), None)
    if decision is None:
        raise GoalError(f"unknown decision {args.decision}")
    if decision["resolution"] is not None:
        raise GoalError(f"{args.decision} is already resolved")
    outcome = "approved" if args.approve else "rejected"
    refinement = decision.get("refinement")
    if outcome == "approved" and refinement:
        conflict = refinement_conflict(contract, refinement)
        if conflict:
            raise GoalError(
                f"{args.decision} no longer applies: {conflict}; reject it or propose a new refinement"
            )
    decision["resolution"] = {"outcome": outcome, "at": now()}
    if args.note:
        decision["resolution"]["note"] = args.note
    if outcome == "approved" and refinement:
        apply_refinement(contract, refinement)
    elif outcome == "approved":
        # The user supplied what was missing: the blocked criteria get a fresh attempt budget.
        for cid in decision["blocks"]:
            facts_of(contract, cid)["attempts"] = []
    save(path, contract)
    print(f"{args.decision}: {outcome}")
    print_next(contract)
    return 0


def cmd_ready(args: argparse.Namespace) -> int:
    contract = load(resolve_contract(args.root, args.contract))
    reasons = readiness(contract)
    if reasons:
        print("NOT READY:")
        for reason in reasons:
            print(f"  - {reason}")
        return 1
    print("READY once every falsifier below has been checked:")
    for cid in criterion_ids(contract):
        ev = facts_of(contract, cid)["evidence"]
        print(f"  {cid}: {ev['summary']} @ {ev['locator']} ({ev['observed_at']})")
        print(f"      would be invalidated by: {'; '.join(ev['invalidated_by'])}")
    return 0


def cmd_handoff(args: argparse.Namespace) -> int:
    path = resolve_contract(args.root, args.contract)
    contract = load(path)
    ids = criterion_ids(contract)
    verified = [cid for cid in ids if is_verified(contract, cid)]
    unverified = [f"{cid} ({state_of(contract, cid)})" for cid in ids if not is_verified(contract, cid)]
    evidence = [
        f"{cid}: {facts_of(contract, cid)['evidence']['summary']} @ {facts_of(contract, cid)['evidence']['locator']}"
        for cid in verified
    ]
    pending = [f"{d['id']} ({d['kind']}): {d['request']}" for d in open_decisions(contract)]
    choice = choose_next(contract)
    if choice["kind"] == "ready":
        next_line = "all criteria verified; run `ready` to finish"
    elif choice["kind"] == "await":
        next_line = f"await decision(s) {', '.join(choice['decisions'])}"
    elif choice["kind"] == "exhausted":
        next_line = f"{', '.join(choice['criteria'])} exhausted max_attempts; open a decision"
    else:
        next_line = f"pursue {choice['criterion']}"
        if choice["next_step"]:
            next_line += f": {choice['next_step']}"
    print(f"Contract: {relative(args.root, path)}")
    print(f"Acceptance: verified [{', '.join(verified) or '-'}]; unverified [{', '.join(unverified) or '-'}]")
    print(f"Evidence: {'; '.join(evidence) or 'none yet'}")
    print(f"Pending decision: {'; '.join(pending) or 'none'}")
    print(f"Next: {next_line}")
    return 0


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="workspace root (default: cwd)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="create a contract and print its path")
    p.add_argument("--title", required=True)
    p.add_argument("--objective", required=True, help="L0 objective")
    p.add_argument("--accept", action="append", required=True, metavar="TEXT", help="L1 acceptance criterion; repeat, ids are assigned A1..An in order")
    p.add_argument("--constraint", action="append", default=[], metavar="TEXT")
    p.add_argument("--non-goal", action="append", default=[], metavar="TEXT")
    p.add_argument("--risk", action="append", default=[], metavar="TEXT", help="known risk to seed working state")
    p.add_argument("--max-attempts", type=int, default=DEFAULT_MAX_ATTEMPTS, help=f"failed approaches allowed per criterion before a decision is required (default {DEFAULT_MAX_ATTEMPTS})")
    p.add_argument("--path", help="tracked workspace-relative path instead of .goal/ (skips .gitignore handling)")
    p.set_defaults(func=cmd_init)

    def contract_parser(name: str, help_text: str) -> argparse.ArgumentParser:
        q = sub.add_parser(name, help=help_text)
        q.add_argument("contract", help="workspace-relative contract path")
        return q

    sub.add_parser("current", help="print the single unfinished contract under .goal/").set_defaults(func=cmd_current)

    contract_parser("validate", "validate a contract against the schema and invariants").set_defaults(func=cmd_validate)

    p = contract_parser("status", "print the whole checkpoint with derived states and the next step")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_status)

    p = contract_parser("next", "print only the next step")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_next)

    p = contract_parser("approach", "set the current L2 approach for a criterion")
    p.add_argument("criterion")
    p.add_argument("--approach", required=True)
    p.set_defaults(func=cmd_approach)

    p = contract_parser("step", "break a criterion into steps, mark them done, or drop them")
    p.add_argument("criterion")
    p.add_argument("--add", action="append", default=[], metavar="TEXT", help="step text; name something re-observable (a command, file, or id list)")
    p.add_argument("--done", action="append", type=int, default=[], metavar="N", help="1-based index from status")
    p.add_argument("--drop", action="append", type=int, default=[], metavar="N")
    p.set_defaults(func=cmd_step)

    p = contract_parser("attempt", "record that the current approach failed verification")
    p.add_argument("criterion")
    p.add_argument("--outcome", required=True, help="what was observed")
    p.add_argument("--approach", help="override the recorded approach text")
    p.set_defaults(func=cmd_attempt)

    p = contract_parser("verify", "mark a criterion verified with observable evidence")
    p.add_argument("criterion")
    p.add_argument("--summary", required=True)
    p.add_argument("--locator", required=True, help="file, command, URL, or artifact where the evidence can be re-observed")
    p.add_argument("--invalidated-by", action="append", required=True, metavar="CONDITION", help="change that requires re-verification; repeat")
    p.set_defaults(func=cmd_verify)

    p = contract_parser("invalidate", "drop a criterion's evidence because an invalidation condition occurred")
    p.add_argument("criterion")
    p.add_argument("--reason", required=True)
    p.set_defaults(func=cmd_invalidate)

    p = contract_parser("risk", "add or drop open risks")
    p.add_argument("--add", action="append", default=[], metavar="TEXT")
    p.add_argument("--drop", action="append", type=int, default=[], metavar="N", help="1-based index from status")
    p.set_defaults(func=cmd_risk)

    d = sub.add_parser("decision", help="open or resolve a pending user decision")
    dsub = d.add_subparsers(dest="decision_command", required=True)
    p = dsub.add_parser("open", help="record a decision only the user can make")
    p.add_argument("contract")
    p.add_argument("--kind", choices=["refinement", "input"], required=True)
    p.add_argument("--request", required=True, help="exact text to present to the user")
    p.add_argument("--blocks", nargs="*", default=[], metavar="ID")
    p.add_argument("--target", help="refinement: objective, max_attempts, constraints, non_goals, or a criterion id")
    p.add_argument("--operation", choices=["set", "add", "remove"], help="refinement operation (objective/max_attempts: set; constraints/non_goals: add/remove; criterion: set/add/remove)")
    p.add_argument("--proposed", help="refinement: new text, or the exact list entry to add/remove, or the new max_attempts")
    p.set_defaults(func=cmd_decision_open)
    p = dsub.add_parser("resolve", help="record the user's answer; approved refinements are applied")
    p.add_argument("contract")
    p.add_argument("decision")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--approve", action="store_true")
    group.add_argument("--reject", action="store_true")
    p.add_argument("--note")
    p.set_defaults(func=cmd_decision_resolve)

    contract_parser("ready", "exit 0 only when the contract is finished").set_defaults(func=cmd_ready)

    contract_parser("handoff", "print the end-of-invocation handoff block").set_defaults(func=cmd_handoff)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.root = args.root.resolve()
    try:
        return args.func(args)
    except GoalError as error:
        sys.stderr.write(f"error: {error}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
