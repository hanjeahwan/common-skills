#!/usr/bin/env python3
"""Project-independent checks for the reusable docs-system validator."""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate.py"

VALID_PROPOSAL = """---
id: P001
status: draft
---

# Change

## Summary
Summary.
## Problem
Problem.
## Scope
Scope.
## Non-goals
None.
## Proposal
Proposal.
## Migration
Migration.
## Verification
Verification.
"""

VALID_DECISION = """# D1 Adopt the change

## Decision
Decision.
## Rationale
Rationale.
## Consequences
Consequences.
## Reconsider when
Conditions change.
"""

VALID_DECISION_INDEX = """# Decisions

| Decision | Lifecycle | Lifecycle detail |
| --- | --- | --- |
| [D001-adopt-change.md](D001-adopt-change.md) | current | — |
"""


class ValidatorTests(unittest.TestCase):
    def run_validator(self, root: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", str(VALIDATOR), str(root)],
            text=True,
            capture_output=True,
            check=False,
        )

    def validate(self, files: dict[str, str]) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative, content in files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            return self.run_validator(root)

    def self_validate(
        self, mutate=None,
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "docs-system"
            shutil.copytree(SKILL_ROOT, root, ignore=shutil.ignore_patterns("__pycache__"))
            if mutate:
                mutate(root)
            return self.run_validator(root)

    def assert_fails(self, files: dict[str, str], message: str) -> None:
        result = self.validate(files)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stdout)

    def test_generic_valid_fixture_passes(self) -> None:
        result = self.validate({
            "README.md": "[Proposal](P001-change.md)\n",
            "P001-change.md": VALID_PROPOSAL,
            "D001-adopt-change.md": VALID_DECISION,
        })
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_broken_local_link_fails(self) -> None:
        self.assert_fails(
            {"README.md": "[Missing](missing.md)\n"},
            "broken link -> missing.md",
        )

    def test_common_markdown_link_forms(self) -> None:
        valid = self.validate({
            "README.md": (
                "[Inline](docs/owner.md \"Owner\")\n"
                "[Encoded](docs/space%20name.md)\n"
                "[Reference][owner]\n\n"
                "[owner]: docs/owner.md\n"
            ),
            "docs/owner.md": "# Owner\n",
            "docs/space name.md": "# Space\n",
        })
        self.assertEqual(valid.returncode, 0, valid.stdout)
        self.assert_fails(
            {"README.md": "[Missing][owner]\n\n[owner]: missing.md\n"},
            "broken link -> missing.md",
        )

    def test_invalid_proposal_status_fails(self) -> None:
        self.assert_fails(
            {"P001-change.md": VALID_PROPOSAL.replace("draft", "unknown")},
            "invalid proposal status",
        )

    def test_proposal_filename_contract_fails(self) -> None:
        for filename in ("P002-change.md", "P001-.md", "P001-Upper.md"):
            with self.subTest(filename=filename):
                result = self.validate({filename: VALID_PROPOSAL})
                self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_duplicate_proposal_ids_fail(self) -> None:
        self.assert_fails(
            {"P001-one.md": VALID_PROPOSAL, "nested/P001-two.md": VALID_PROPOSAL},
            "duplicate proposal ID",
        )

    def test_proposal_requires_h1(self) -> None:
        self.assert_fails(
            {"P001-change.md": VALID_PROPOSAL.replace("# Change\n\n", "")},
            "requires a non-empty H1 title",
        )

    def test_proposal_section_contract_fails(self) -> None:
        cases = {
            "missing": (
                VALID_PROPOSAL.replace("## Migration\nMigration.\n", ""),
                "missing required section `## Migration`",
            ),
            "empty": (
                VALID_PROPOSAL.replace("## Migration\nMigration.", "## Migration\n"),
                "section `## Migration` is empty",
            ),
            "duplicate": (
                VALID_PROPOSAL.replace(
                    "## Migration\nMigration.",
                    "## Migration\nFirst.\n## Migration\nSecond.",
                ),
                "duplicate section `## Migration`",
            ),
        }
        for name, (content, message) in cases.items():
            with self.subTest(name=name):
                self.assert_fails({"P001-change.md": content}, message)

    def test_proposal_custom_layout_and_fenced_headings_pass(self) -> None:
        content = VALID_PROPOSAL.replace(
            "## Scope\nScope.\n## Non-goals\nNone.",
            "## Non-goals\nNone.\n## Evidence\nObserved.\n## Scope\nScope.",
        ) + "\n```md\n## Migration\nExample only.\n```\n"
        result = self.validate({"P001-change.md": content})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_proposal_lifecycle_contract_fails(self) -> None:
        cases = {
            "terminal_without_outcome": (
                VALID_PROPOSAL.replace("draft", "implemented"),
                "requires `## Outcome`",
            ),
            "draft_with_outcome": (
                VALID_PROPOSAL + "\n## Outcome\nDone.\n",
                "only allowed",
            ),
            "invalid_superseded_by": (
                VALID_PROPOSAL.replace("status: draft", "status: draft\nsuperseded_by: P002"),
                "superseded_by is only valid",
            ),
        }
        for name, (content, message) in cases.items():
            with self.subTest(name=name):
                self.assert_fails({"P001-change.md": content}, message)

    def test_terminal_proposal_custom_outcome_placement_passes(self) -> None:
        content = VALID_PROPOSAL.replace(
            "status: draft", "status: implemented"
        ).replace(
            "## Summary\nSummary.",
            "## Outcome\nImplemented.\n## Summary\nSummary.",
        )
        result = self.validate({"P001-change.md": content})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_valid_decision_passes(self) -> None:
        result = self.validate({"D001-adopt-change.md": VALID_DECISION})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_decision_lifecycle_index_passes_in_arbitrary_directory(self) -> None:
        result = self.validate({
            "records/design-history.md": VALID_DECISION_INDEX,
            "records/D001-adopt-change.md": VALID_DECISION,
        })
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_superseded_decision_with_successor_passes(self) -> None:
        index = VALID_DECISION_INDEX.replace(
            "| current | — |",
            "| superseded | [D002-replace-change.md](D002-replace-change.md) |",
        ) + (
            "| [D002-replace-change.md](D002-replace-change.md) | current | — |\n"
        )
        result = self.validate({
            "decisions/README.md": index,
            "decisions/D001-adopt-change.md": VALID_DECISION,
            "decisions/D002-replace-change.md": VALID_DECISION.replace(
                "# D1 ", "# D2 ", 1),
        })
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_decision_lifecycle_contract_fails(self) -> None:
        cases = {
            "extra_header": (
                VALID_DECISION_INDEX.replace(
                    "| Decision | Lifecycle | Lifecycle detail |",
                    "| Decision | Title | Lifecycle | Lifecycle detail |",
                ).replace(
                    "| [D001-adopt-change.md](D001-adopt-change.md) | current | — |",
                    "| [D001-adopt-change.md](D001-adopt-change.md) | Adopt | current | — |",
                ),
                "index table headers must be",
            ),
            "alias": (
                VALID_DECISION_INDEX.replace("current", "adopted"),
                "invalid Decision lifecycle",
            ),
            "missing_successor": (
                VALID_DECISION_INDEX.replace("current", "superseded"),
                "must link a successor Decision",
            ),
        }
        for name, (index, message) in cases.items():
            with self.subTest(name=name):
                self.assert_fails(
                    {
                        "decisions/README.md": index,
                        "decisions/D001-adopt-change.md": VALID_DECISION,
                    },
                    message,
                )

    def test_decision_body_cannot_copy_lifecycle(self) -> None:
        self.assert_fails(
            {
                "D001-adopt-change.md": (
                    VALID_DECISION + "\n> Status: current\n"
                ),
            },
            "Decision lifecycle belongs only in the domain README",
        )

    def test_decision_fenced_lifecycle_example_passes(self) -> None:
        content = VALID_DECISION.replace(
            "## Consequences\nConsequences.",
            "```yaml\nstatus: draft\n```\n\n## Consequences\nConsequences.",
        )
        result = self.validate({"D001-adopt-change.md": content})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_directory_names_do_not_infer_document_types(self) -> None:
        result = self.validate({
            "research/body.md": "> 状态:项目自定义 ｜ 日期:2026-01-01\n",
            "findings/README.md": (
                "| Finding | Status |\n| --- | --- |\n| one | project-defined |\n"
            ),
            "postmortem/README.md": (
                "| Rule | Status | Source |\n| --- | --- | --- |\n"
                "| one | project-defined | "
                "[D1](../D001-adopt-change.md) |\n"
            ),
            "postmortems/README.md": "# Project-owned directory\n",
            "D001-adopt-change.md": VALID_DECISION,
        })
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_fixed_index_headers_reject_extra_columns(self) -> None:
        cases = {
            "docs_entry": {
                "README.md": (
                    "| Question | Owner | Notes |\n"
                    "| --- | --- | --- |\n| Where? | Here | extra |\n"
                ),
            },
            "proposal": {
                "README.md": (
                    "| Proposal | Topic | Status |\n| --- | --- | --- |\n"
                    "| [P001](P001-change.md) | Change | draft |\n"
                ),
                "P001-change.md": VALID_PROPOSAL,
            },
            "evidence": {
                "README.md": (
                    "| Question | Record | Date |\n| --- | --- | --- |\n"
                    "| What? | Finding | today |\n"
                ),
            },
            "postmortem": {
                "README.md": (
                    "| Postmortem | Lesson | Lifecycle |\n"
                    "| --- | --- | --- |\n| Incident | Learn | effective |\n"
                ),
            },
        }
        for name, files in cases.items():
            with self.subTest(name=name):
                self.assert_fails(files, "index table headers must be")

    def test_decision_filename_and_identity_contract_fails(self) -> None:
        cases = {
            "numeric_identity": ("D002-adopt-change.md", "H1 declares D1"),
            "empty_slug": ("D001-.md", "lowercase-ascii-kebab-case"),
            "uppercase_slug": ("D001-Adopt.md", "lowercase-ascii-kebab-case"),
        }
        for name, (filename, message) in cases.items():
            with self.subTest(name=name):
                self.assert_fails({filename: VALID_DECISION}, message)

    def test_duplicate_decision_ids_fail(self) -> None:
        self.assert_fails(
            {
                "D001-one.md": VALID_DECISION,
                "nested/D001-two.md": VALID_DECISION,
            },
            "duplicate decision ID",
        )

    def test_decision_section_contract_fails(self) -> None:
        cases = {
            "missing": (
                VALID_DECISION.replace("## Rationale\nRationale.\n", ""),
                "missing required section `## Rationale`",
            ),
            "empty": (
                VALID_DECISION.replace("## Rationale\nRationale.", "## Rationale\n"),
                "section `## Rationale` is empty",
            ),
            "duplicate": (
                VALID_DECISION.replace(
                    "## Rationale\nRationale.",
                    "## Rationale\nFirst.\n## Rationale\nSecond.",
                ),
                "duplicate section `## Rationale`",
            ),
        }
        for name, (content, message) in cases.items():
            with self.subTest(name=name):
                self.assert_fails({"D001-adopt-change.md": content}, message)

    def test_decision_custom_layout_and_fenced_headings_pass(self) -> None:
        content = VALID_DECISION.replace(
            "## Decision\nDecision.\n## Rationale\nRationale.",
            "## Rationale\nRationale.\n## Evidence\nObserved.\n## Decision\nDecision.",
        ) + "\n```md\n## Decision\nExample only.\n```\n"
        result = self.validate({"D001-adopt-change.md": content})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_template_starters_pass(self) -> None:
        result = self.run_validator(SKILL_ROOT)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_invalid_template_fails_self_validation(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "templates" / "runbook.md"
            path.write_text(path.read_text().replace("## Purpose", "## Goal"))

        result = self.self_validate(mutate)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("templates/runbook.md: missing sections", result.stdout)

    def test_template_requires_extension_placeholder(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "templates" / "proposal.md"
            text = path.read_text().replace(
                "## <additional section when needed>\n\n"
                "<Describe the additional concern. Remove this section when it is not needed.>\n\n",
                "",
            )
            path.write_text(text)

        result = self.self_validate(mutate)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("requires one `## <additional section when needed>`", result.stdout)

    def test_template_custom_layout_and_extra_h2_are_allowed(self) -> None:
        def mutate(root: Path) -> None:
            for name in ("proposal.md", "decision.md", "runbook.md", "index.md"):
                path = root / "templates" / name
                text = path.read_text()
                headings = list(re.finditer(r"(?m)^## ", text))
                first, second = headings[0], headings[1]
                first_block = text[first.start():second.start()]
                text = (
                    text[:first.start()]
                    + text[second.start():headings[2].start()]
                    + "## Local section\n\nLocal content.\n\n"
                    + first_block
                    + text[headings[2].start():]
                )
                path.write_text(text)

        result = self.self_validate(mutate)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_invalid_skill_anatomy_fails_self_validation(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "SKILL.md"
            path.write_text(
                path.read_text().replace("## Boundaries", "## Notes", 1))

        result = self.self_validate(mutate)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("SKILL.md: required sections", result.stdout)

    def test_additional_skill_section_passes_self_validation(self) -> None:
        def mutate(root: Path) -> None:
            path = root / "SKILL.md"
            path.write_text(
                path.read_text().replace(
                    "## Quality Standard", "## Local Notes\n\nNone.\n\n## Quality Standard", 1))

        result = self.self_validate(mutate)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_tests_fail_self_validation(self) -> None:
        def mutate(root: Path) -> None:
            (root / "tests" / "test_validate.py").unlink()

        result = self.self_validate(mutate)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("tests/test_validate.py: missing required skill artifact", result.stdout)

    def test_test_fixtures_do_not_pollute_normal_scan(self) -> None:
        result = self.validate({
            ".agents/skills/docs-system/tests/P001-invalid.md": "invalid",
            "README.md": "# Project\n",
        })
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
