#!/usr/bin/env python3
"""Reusable deterministic documentation validation (docs-system).

Requires Python 3.10+; standard library only (no third-party packages).

Only enforces contracts that can be judged from an artifact or its path:

- generic local Markdown link integrity within the scanned root;
- Proposal recognition / filename / ID / front matter / status / required
  sections / terminal Outcome;
- duplicate Proposal IDs;
- per-file Decision filename / numeric identity / required sections;
- duplicate Decision IDs and structurally recognized lifecycle-table vocabulary;
- absence of lifecycle status in Decision bodies;
- reusable template starter validity;
- this skill's own stable SKILL.md structure (self-validation only).

It never infers repository-specific owners, required document sets, entry
roots, governed sets or monorepo topology. It imports no project modules, calls
no project validators and runs no project hooks.

Usage:
    python3 validate.py <root>

- Project scan: <root> is the project documentation/content root.
- Self-validation: <root> is this skill's directory (auto-detected when the
  scanned root contains SKILL.md at its top level).
- <root>/.agents/skills/docs-system/tests (or <root>/tests in self-scan) is
  test content and never participates in a normal project scan.
"""
from __future__ import annotations

import os
import re
import sys
from urllib.parse import unquote

PROPOSAL_SECTIONS = [
    "Summary", "Problem", "Scope", "Non-goals", "Proposal", "Migration",
    "Verification", "Outcome",
]
DECISION_SECTIONS = [
    "Context", "Decision", "Rationale", "Consequences", "Rejected alternatives",
    "Supersedes", "Related decisions", "Reconsider when",
]
DECISION_REQUIRED = ["Decision", "Rationale", "Consequences", "Reconsider when"]
RUNBOOK_SECTIONS = [
    "Purpose", "Preconditions", "Procedure", "Verification",
    "Rollback / Recovery", "Failure modes / Escalation",
]
INDEX_SECTIONS = [
    "Documentation entry", "Proposal index", "Decision index",
    "Research / Finding index", "Postmortem index",
]
EXTENSION_PLACEHOLDER = "<additional section when needed>"
INDEX_HEADERS = [
    ["Question", "Owner"],
    ["Proposal", "Topic"],
    ["Decision", "Lifecycle", "Lifecycle detail"],
    ["Question", "Record"],
    ["Postmortem", "Lesson"],
]
SKILL_REQUIRED_SECTIONS = [
    "Mission", "Principles", "Resource Guide", "Workflow", "Boundaries",
    "Quality Standard",
]
PROPOSAL_STATUSES = {"draft", "accepted", "implemented", "rejected", "superseded"}
TERMINAL_STATUSES = {"implemented", "rejected", "superseded"}
DECISION_LIFECYCLES = {
    "current", "partially-superseded", "superseded", "void",
}
LIFECYCLE_LINE_RE = re.compile(
    r"(?mi)^(?:[-*>]\s*)?(?:status|lifecycle|状态|生命周期)\s*[:：]")

INLINE_LINK_RE = re.compile(
    r"\]\(\s*(?:<([^>]+)>|([^\s)]+))"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)")
REFERENCE_LINK_RE = re.compile(
    r"(?m)^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))")
PROPOSAL_CANDIDATE_RE = re.compile(r"P\d{3}-.*\.md")
PROPOSAL_FILENAME_RE = re.compile(
    r"P(\d{3})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md")
DECISION_CANDIDATE_RE = re.compile(r"D\d{3}-.*\.md")
DECISION_FILENAME_RE = re.compile(
    r"D(\d{3})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md")
H2_RE = re.compile(r"(?m)^## ([^\n]+)$")
H1_RE = re.compile(r"(?m)^# ([^\n]+)$")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
FRONT_MATTER_RE = re.compile(
    r"^(?:---\s*\n(.*?)\n?---\s*\n)", re.DOTALL)
META_LINE_RE = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.+?)\s*$")


def walk_md(root: str):
    """Yield relative paths of all .md files, honoring the fixed exclusions."""
    excluded_parts = {".git", "__pycache__"}
    self_scan = os.path.isfile(os.path.join(root, "SKILL.md"))
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(
            directory for directory in dirs
            if directory not in excluded_parts
        )
        rel_base = os.path.relpath(base, root)
        parts = [] if rel_base == "." else rel_base.split(os.sep)
        is_test_fixture = parts[-1:] == ["tests"] and (
            self_scan or ("docs-system" in parts and ".agents" in parts))
        if is_test_fixture:
            dirs[:] = []
            continue
        for name in sorted(files):
            if name.endswith(".md"):
                yield os.path.join(rel_base, name) if rel_base != "." else name


def read(path: str) -> str:
    with open(path, encoding="utf-8-sig") as handle:
        return handle.read()


def structural_markdown(text: str) -> str:
    """Return Markdown with fenced code hidden from structural checks."""
    output: list[str] = []
    fence_char = ""
    fence_length = 0
    for line in text.splitlines(keepends=True):
        match = FENCE_RE.match(line)
        if not fence_char:
            if match:
                marker = match.group(1)
                fence_char = marker[0]
                fence_length = len(marker)
                output.append("\n" if line.endswith("\n") else "")
            else:
                output.append(line)
            continue
        if match:
            marker = match.group(1)
            if marker[0] == fence_char and len(marker) >= fence_length:
                fence_char = ""
                fence_length = 0
        output.append("\n" if line.endswith("\n") else "")
    return "".join(output)


def parse_front_matter(text: str):
    """Return (meta dict, error). Meta contains single-line key: value pairs."""
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None, "missing YAML front matter"
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("-"):
            continue
        field = META_LINE_RE.match(line)
        if field:
            meta[field.group(1)] = field.group(2).strip("\"'")
    return meta, None


def check_links(root: str, errors: list[str]) -> int:
    count = 0
    broken = 0
    for rel in walk_md(root):
        count += 1
        path = os.path.join(root, rel)
        text = read(path)
        base = os.path.dirname(path)
        for target in markdown_targets(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_target = unquote(target.split("#", 1)[0])
            if not path_target:
                continue
            resolved = os.path.normpath(os.path.join(base, path_target))
            if not os.path.exists(resolved):
                broken += 1
                errors.append(f"{rel}: broken link -> {target}")
    print(f"Markdown scan: {count} files, {broken} broken links")
    return broken


def markdown_targets(text: str):
    """Yield inline and reference-definition Markdown link destinations."""
    for pattern in (INLINE_LINK_RE, REFERENCE_LINK_RE):
        for match in pattern.finditer(text):
            yield match.group(1) or match.group(2)


def check_proposals(root: str, errors: list[str]) -> None:
    files: list[str] = []
    for rel in walk_md(root):
        name = os.path.basename(rel)
        if PROPOSAL_CANDIDATE_RE.fullmatch(name) or (
                name != "README.md" and _front_id(root, rel)):
            files.append(rel)
    seen: dict[str, str] = {}
    for rel in files:
        path = os.path.join(root, rel)
        text = read(path)
        structure = structural_markdown(text)
        meta, meta_error = parse_front_matter(text)
        name = os.path.basename(rel)
        if meta_error:
            errors.append(f"{rel}: {meta_error}")
            continue
        name_match = PROPOSAL_FILENAME_RE.fullmatch(name)
        front_id = None
        if meta and "id" in meta:
            front_id = re.fullmatch(r"P(\d{3})", str(meta["id"]))
        if not name_match or front_id is None:
            if name_match and front_id is None:
                errors.append(
                    f"{rel}: proposal filename requires matching `id: P###` "
                    f"front matter")
            elif front_id is not None and not name_match:
                errors.append(
                    f"{rel}: proposal front matter id={meta['id']} requires "
                    f"filename P###-*.md")
            else:
                errors.append(f"{rel}: unparseable proposal identity")
            continue
        numeric = name_match.group(1)
        if front_id.group(1) != numeric:
            errors.append(
                f"{rel}: front matter id P{front_id.group(1)} does not match "
                f"filename P{numeric}")
        if numeric in seen:
            errors.append(
                f"{rel}: duplicate proposal ID P{numeric} (also {seen[numeric]})")
        seen[numeric] = rel
        status = str(meta.get("status", ""))
        if status not in PROPOSAL_STATUSES:
            errors.append(f"{rel}: invalid proposal status {status!r}")
            continue
        if "superseded_by" in meta and status != "superseded":
            errors.append(
                f"{rel}: superseded_by is only valid for status: superseded")
        h1 = H1_RE.search(structure)
        if not h1:
            errors.append(f"{rel}: proposal requires a non-empty H1 title")
        headings = H2_RE.findall(structure)
        core = PROPOSAL_SECTIONS[:7]
        for section in core:
            count = headings.count(section)
            if count == 0:
                errors.append(f"{rel}: missing required section `## {section}`")
            elif count > 1:
                errors.append(f"{rel}: duplicate section `## {section}`")
        outcome_count = headings.count("Outcome")
        if outcome_count > 1:
            errors.append(f"{rel}: duplicate section `## Outcome`")
        if outcome_count:
            if status not in TERMINAL_STATUSES:
                errors.append(
                    f"{rel}: `## Outcome` is only allowed for implemented/"
                    f"rejected/superseded proposals")
        elif status in TERMINAL_STATUSES:
            errors.append(
                f"{rel}: terminal proposal (status: {status}) requires "
                f"`## Outcome`")
        for section in PROPOSAL_SECTIONS:
            if section in headings and not _section_body(structure, section).strip():
                errors.append(f"{rel}: section `## {section}` is empty")
    print(f"Proposal scan: {len(files)} proposal(s)")


def check_decisions(root: str, errors: list[str]) -> None:
    files = [
        rel for rel in walk_md(root)
        if DECISION_CANDIDATE_RE.fullmatch(os.path.basename(rel))
    ]
    seen: dict[str, str] = {}
    for rel in files:
        path = os.path.join(root, rel)
        name = os.path.basename(rel)
        name_match = DECISION_FILENAME_RE.fullmatch(name)
        if not name_match:
            errors.append(
                f"{rel}: decision filename must be "
                f"D###-<lowercase-ascii-kebab-case>.md")
            continue
        numeric = name_match.group(1)
        if numeric in seen:
            errors.append(
                f"{rel}: duplicate decision ID D{int(numeric)} "
                f"(also {seen[numeric]})")
        seen[numeric] = rel
        text = read(path)
        structure = structural_markdown(text)
        h1 = H1_RE.search(structure)
        body_id = None
        if h1:
            declared = re.fullmatch(r"D(\d+)\s+(.+)", h1.group(1))
            if declared:
                body_id = declared.group(1)
        if body_id is None:
            errors.append(
                f"{rel}: first H1 must declare `# D<n> <title>` matching "
                f"filename D{numeric}")
        elif int(body_id) != int(numeric):
            errors.append(
                f"{rel}: H1 declares D{int(body_id)}, filename declares "
                f"D{int(numeric)}")
        headings = H2_RE.findall(structure)
        for section in DECISION_SECTIONS:
            if headings.count(section) > 1:
                errors.append(f"{rel}: duplicate section `## {section}`")
        for section in DECISION_REQUIRED:
            if section not in headings:
                errors.append(f"{rel}: missing required section `## {section}`")
            elif not _section_body(structure, section).strip():
                errors.append(f"{rel}: section `## {section}` is empty")
        if LIFECYCLE_LINE_RE.search(text):
            errors.append(
                f"{rel}: Decision lifecycle belongs only in the domain README")
    print(f"Decision scan: {len(files)} decision(s)")


def check_index_tables(root: str, errors: list[str]) -> None:
    """Validate canonical index tables by content, independent of location."""
    for rel in walk_md(root):
        for headers, rows in markdown_tables(read(os.path.join(root, rel))):
            lowered = [header.lower() for header in headers]
            expected = None
            if "decision" in lowered and any(
                    re.search(r"D\d{3}-[a-z0-9-]+\.md", " | ".join(row))
                    for row in rows):
                expected = INDEX_HEADERS[2]
            elif "proposal" in lowered and any(
                    re.search(r"P\d{3}-[a-z0-9-]+\.md", " | ".join(row))
                    for row in rows):
                expected = INDEX_HEADERS[1]
            elif "postmortem" in lowered:
                expected = INDEX_HEADERS[4]
            elif "question" in lowered and "owner" in lowered:
                expected = INDEX_HEADERS[0]
            elif "question" in lowered and "record" in lowered:
                expected = INDEX_HEADERS[3]
            if expected is None:
                continue
            if headers != expected:
                errors.append(
                    f"{rel}: index table headers must be {expected}, got {headers}")
                continue
            if expected != INDEX_HEADERS[2]:
                continue
            lifecycle_index = headers.index("Lifecycle")
            for row in rows:
                if lifecycle_index >= len(row):
                    continue
                row_text = " | ".join(row)
                decision_links = set(re.findall(
                    r"D\d{3}-[a-z0-9-]+\.md", row_text))
                if not decision_links:
                    continue
                lifecycle = row[lifecycle_index].strip().strip("`")
                if lifecycle not in DECISION_LIFECYCLES:
                    errors.append(
                        f"{rel}: invalid Decision lifecycle {lifecycle!r}")
                    continue
                if (
                        lifecycle in {"partially-superseded", "superseded"}
                        and len(decision_links) < 2):
                    errors.append(
                        f"{rel}: {lifecycle} row must link a successor Decision")


def markdown_tables(text: str):
    """Return simple Markdown tables as (headers, body rows)."""
    lines = text.splitlines()
    tables = []
    index = 0
    while index + 1 < len(lines):
        header = _table_cells(lines[index])
        separator = _table_cells(lines[index + 1])
        if header and separator and all(
                re.fullmatch(r":?-{3,}:?", cell) for cell in separator):
            rows = []
            index += 2
            while index < len(lines):
                row = _table_cells(lines[index])
                if not row:
                    break
                rows.append(row)
                index += 1
            tables.append((header, rows))
            continue
        index += 1
    return tables


def _table_cells(line: str):
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def check_templates(root: str, errors: list[str]) -> None:
    templates = os.path.join(root, "templates")
    expected = {
        "proposal.md": PROPOSAL_SECTIONS,
        "decision.md": DECISION_SECTIONS,
        "runbook.md": RUNBOOK_SECTIONS,
        "index.md": INDEX_SECTIONS,
    }
    for name, sections in expected.items():
        path = os.path.join(templates, name)
        if not os.path.isfile(path):
            errors.append(f"templates/{name}: missing template starter")
            continue
        headings = H2_RE.findall(structural_markdown(read(path)))
        missing = [section for section in sections if section not in headings]
        duplicates = [section for section in sections if headings.count(section) > 1]
        if missing or duplicates:
            errors.append(
                f"templates/{name}: missing sections {missing}; "
                f"duplicate sections {duplicates}")
        if headings.count(EXTENSION_PLACEHOLDER) != 1:
            errors.append(
                f"templates/{name}: requires one "
                f"`## {EXTENSION_PLACEHOLDER}` placeholder")
    index_path = os.path.join(templates, "index.md")
    if os.path.isfile(index_path):
        headers = [table[0] for table in markdown_tables(read(index_path))]
        missing = [header for header in INDEX_HEADERS if header not in headers]
        duplicates = [
            header for header in INDEX_HEADERS if headers.count(header) > 1
        ]
        unexpected = [header for header in headers if header not in INDEX_HEADERS]
        if missing or duplicates or unexpected:
            errors.append(
                f"templates/index.md: missing table headers {missing}; "
                f"duplicate table headers {duplicates}; "
                f"unexpected table headers {unexpected}")


def check_skill(root: str, errors: list[str]) -> None:
    path = os.path.join(root, "SKILL.md")
    if not os.path.isfile(path):
        return
    text = read(path)
    meta, meta_error = parse_front_matter(text)
    if meta_error:
        errors.append(f"SKILL.md: {meta_error}")
    else:
        for field in ("name", "description"):
            if not meta.get(field):
                errors.append(
                    f"SKILL.md: front matter requires a non-empty `{field}` "
                    f"(used for skill discovery and routing)")
    headings = H2_RE.findall(structural_markdown(text))
    observed_required = [
        heading for heading in headings if heading in SKILL_REQUIRED_SECTIONS
    ]
    if observed_required != SKILL_REQUIRED_SECTIONS:
        errors.append(
            "SKILL.md: required sections must appear once and in order: "
            f"{SKILL_REQUIRED_SECTIONS}; got {observed_required}")
    for name in ("references/standard.md", "references/prose.md",
                 "references/workflow.md",
                 "scripts/validate.py", "templates/proposal.md",
                 "templates/decision.md", "templates/runbook.md",
                 "templates/index.md", "tests/test_validate.py",
                 "tests/cases.md"):
        if not os.path.exists(os.path.join(root, name)):
            errors.append(f"{name}: missing required skill artifact")


def _front_id(root: str, rel: str) -> str | None:
    text = read(os.path.join(root, rel))
    meta, error = parse_front_matter(text)
    if error or not meta or "id" not in meta:
        return None
    match = re.fullmatch(r"P(\d{3})", str(meta["id"]))
    return match.group(1) if match else None


def _section_body(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?ms)^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)")
    match = pattern.search(text)
    return match.group(1) if match else ""


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: python3 validate.py <root>")
        return 2
    root = os.path.abspath(argv[1])
    if not os.path.isdir(root):
        print(f"error: not a directory: {root}")
        return 2
    self_scan = os.path.isfile(os.path.join(root, "SKILL.md"))
    errors: list[str] = []
    check_links(root, errors)
    check_proposals(root, errors)
    check_decisions(root, errors)
    check_index_tables(root, errors)
    if self_scan:
        check_skill(root, errors)
        check_templates(root, errors)
    if errors:
        print(f"\n{docs_system_label(root)} failed, {len(errors)} issue(s):")
        for item in errors[:40]:
            print(f"  x {item}")
        if len(errors) > 40:
            print(f"  ... {len(errors) - 40} more")
        return 1
    kind = "docs-system self-validation" if self_scan else "docs scan"
    print(f"\n{kind}: all checks passed")
    return 0


def docs_system_label(root: str) -> str:
    return os.path.basename(root) or root


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
