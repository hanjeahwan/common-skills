#!/usr/bin/env python3
"""Link-graph validation for governed documentation (docs-ownership).

Requires Python 3.10+; standard library only (no third-party packages).

Enforces only what a link graph proves:

- every local Markdown link in the scanned root resolves;
- with --entry, which Markdown files the named entry cannot reach.

Ownership correctness, terminology consistency, prose accuracy and the absence
of duplicate truth are not machine-checkable here. It never infers a project's
entry root, governed set or topology, imports no project modules, calls no
project validators and runs no project hooks.

Usage:
    python3 validate.py <root> [--entry <relative-path>] [--exclude <glob> ...]

Every Markdown file under <root> is scanned except what --exclude names, so an
exemption is always the caller's explicit choice.
"""
from __future__ import annotations

import argparse
import fnmatch
import os
import re
import sys
from urllib.parse import unquote

INLINE_LINK_RE = re.compile(
    r"\]\(\s*(?:<([^>]+)>|([^\s)]+))"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)")
REFERENCE_LINK_RE = re.compile(
    r"(?m)^\s*\[[^\]]+\]:\s*(?:<([^>]+)>|(\S+))")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def walk_md(root: str, excludes: list[str] | None = None):
    """Yield relative posix paths of .md files under root.

    Only version-control and cache directories are skipped. No document is
    judged by its type, name or location: a project that keeps non-governed
    Markdown excludes it with --exclude, so the exemption stays visible to the
    caller instead of being applied silently.
    """
    excluded_parts = {".git", "__pycache__"}
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(
            directory for directory in dirs if directory not in excluded_parts)
        rel_base = os.path.relpath(base, root)
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            rel = name if rel_base == "." else os.path.join(rel_base, name)
            rel = rel.replace(os.sep, "/")
            if excluded(rel, excludes):
                continue
            yield rel


def excluded(rel: str, excludes: list[str] | None) -> bool:
    """Report whether a relative path matches any caller-supplied glob."""
    return any(fnmatch.fnmatch(rel, pattern) for pattern in excludes or [])


def read(path: str) -> str:
    with open(path, encoding="utf-8-sig") as handle:
        return handle.read()


def strip_fenced_code(text: str) -> str:
    """Blank fenced code blocks, preserving line boundaries.

    A link inside a fence is an example of how to write a link, not a link.
    Indented blocks are left alone: four-space indentation also marks ordinary
    nested list content, and blanking it would hide real broken links.
    """
    output: list[str] = []
    fence = ""
    for line in text.splitlines(keepends=True):
        match = FENCE_RE.match(line)
        blank = "\n" if line.endswith("\n") else ""
        if not fence:
            if match:
                fence = match.group(1)
                output.append(blank)
            else:
                output.append(line)
            continue
        if match and match.group(1)[0] == fence[0] and len(
                match.group(1)) >= len(fence):
            fence = ""
        output.append(blank)
    return "".join(output)


def markdown_targets(text: str):
    """Yield inline and reference-definition Markdown link destinations."""
    body = strip_fenced_code(text)
    for pattern in (INLINE_LINK_RE, REFERENCE_LINK_RE):
        for match in pattern.finditer(body):
            yield match.group(1) or match.group(2)


def local_targets(text: str):
    """Yield link destinations that address a path inside the repository."""
    for target in markdown_targets(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        path_target = unquote(target.split("#", 1)[0])
        if path_target:
            yield target, path_target


def check_links(root: str, excludes: list[str], errors: list[str]) -> None:
    count = 0
    broken = 0
    for rel in walk_md(root, excludes):
        count += 1
        base = os.path.dirname(os.path.join(root, rel))
        for target, path_target in local_targets(read(os.path.join(root, rel))):
            resolved = os.path.normpath(os.path.join(base, path_target))
            if not os.path.exists(resolved):
                broken += 1
                errors.append(f"{rel}: broken link -> {target}")
    print(f"Markdown scan: {count} files, {broken} broken links")


def check_orphans(
        root: str, entry: str, excludes: list[str], errors: list[str]) -> None:
    """Report Markdown files the named entry cannot reach by local links."""
    entry = os.path.normpath(entry).replace(os.sep, "/")
    governed = set(walk_md(root, excludes))
    if entry not in governed:
        errors.append(f"{entry}: entry is not a scanned Markdown file")
        return
    reachable = {entry}
    queue = [entry]
    while queue:
        rel = queue.pop()
        base = os.path.dirname(rel)
        for _, path_target in local_targets(read(os.path.join(root, rel))):
            target = os.path.normpath(os.path.join(base, path_target))
            target = target.replace(os.sep, "/")
            if target in governed and target not in reachable:
                reachable.add(target)
                queue.append(target)
    for rel in sorted(governed - reachable):
        errors.append(f"{rel}: orphan, not reachable from {entry}")
    print(f"Reachability from {entry}: {len(reachable)}/{len(governed)} files")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="validate.py",
        description="Validate documentation link integrity and reachability.")
    parser.add_argument("root", help="documentation or content root to scan")
    parser.add_argument(
        "--entry",
        help="entry file relative to root; enables orphan reporting")
    parser.add_argument(
        "--exclude", action="append", default=[], metavar="GLOB",
        help="glob of root-relative paths to skip; repeatable")
    args = parser.parse_args(argv[1:])

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        print(f"error: not a directory: {root}")
        return 2
    errors: list[str] = []
    check_links(root, args.exclude, errors)
    if args.entry:
        check_orphans(root, args.entry, args.exclude, errors)
    if errors:
        label = os.path.basename(root) or root
        print(f"\n{label} failed, {len(errors)} issue(s):")
        for item in errors[:40]:
            print(f"  x {item}")
        if len(errors) > 40:
            print(f"  ... {len(errors) - 40} more")
        return 1
    print("\ndocs scan: all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
