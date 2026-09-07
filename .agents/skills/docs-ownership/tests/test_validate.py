"""Deterministic contract tests for docs-ownership's validator."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate.py"

VALID_TREE = {
    "README.md": "# Project\n\nSee [architecture](docs/architecture.md).\n",
    "docs/architecture.md": "# Architecture\n\nBack to [entry](../README.md).\n",
}


class ValidatorTestCase(unittest.TestCase):
    def run_validator(self, root: Path, *args: str):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), str(root), *args],
            capture_output=True, text=True)

    def validate(self, files: dict[str, str], *args: str):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel, content in files.items():
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            return self.run_validator(root, *args)

    def assert_fails(self, files: dict[str, str], message: str, *args: str):
        result = self.validate(files, *args)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stdout)


class LinkIntegrityTests(ValidatorTestCase):
    def test_valid_tree_passes(self) -> None:
        result = self.validate(VALID_TREE)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_broken_local_link_fails(self) -> None:
        self.assert_fails(
            {"README.md": "# Project\n\n[gone](docs/missing.md)\n"},
            "README.md: broken link -> docs/missing.md")

    def test_common_link_forms_resolve(self) -> None:
        files = {
            "README.md": (
                "# Project\n\n"
                "[inline](docs/architecture.md)\n"
                "[anchor](docs/architecture.md#heading)\n"
                "[encoded](docs/a%20b.md)\n"
                "[angle](<docs/architecture.md>)\n"
                '[titled](docs/architecture.md "Title")\n'
                "[ref][target]\n\n"
                "[target]: docs/architecture.md\n"
            ),
            "docs/architecture.md": "# Architecture\n",
            "docs/a b.md": "# Spaced\n",
        }
        result = self.validate(files)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_external_links_are_ignored(self) -> None:
        files = {
            "README.md": (
                "# Project\n\n[web](https://example.com/missing.md)\n"
                "[mail](mailto:nobody@example.com)\n[self](#section)\n"
            ),
        }
        result = self.validate(files)
        self.assertEqual(result.returncode, 0, result.stdout)


    def test_fenced_example_links_are_not_checked(self) -> None:
        files = {
            "README.md": (
                "# Project\n\nHow to register a document:\n\n"
                "```markdown\n- [Owner](docs/example-owner.md)\n```\n\n"
                "~~~md\n[ref]: docs/other-example.md\n~~~\n"
            ),
        }
        result = self.validate(files)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_link_after_a_closed_fence_is_still_checked(self) -> None:
        files = {
            "README.md": (
                "# Project\n\n```md\n[example](docs/example.md)\n```\n\n"
                "[real](docs/missing.md)\n"
            ),
        }
        self.assert_fails(files, "README.md: broken link -> docs/missing.md")


class ReachabilityTests(ValidatorTestCase):
    def test_transitively_reachable_tree_passes(self) -> None:
        files = {
            "README.md": "# Project\n\n[docs](docs/README.md)\n",
            "docs/README.md": "# Docs\n\n[deep](guides/deep.md)\n",
            "docs/guides/deep.md": "# Deep\n",
        }
        result = self.validate(files, "--entry", "README.md")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_orphan_is_reported(self) -> None:
        files = {
            "README.md": "# Project\n\n[docs](docs/architecture.md)\n",
            "docs/architecture.md": "# Architecture\n",
            "docs/stranded.md": "# Stranded\n",
        }
        self.assert_fails(
            files, "docs/stranded.md: orphan, not reachable from README.md",
            "--entry", "README.md")

    def test_cross_link_from_orphan_does_not_register_it(self) -> None:
        files = {
            "README.md": "# Project\n\n[docs](docs/architecture.md)\n",
            "docs/architecture.md": "# Architecture\n",
            "docs/stranded.md": "# Stranded\n\n[peer](architecture.md)\n",
        }
        self.assert_fails(
            files, "docs/stranded.md: orphan", "--entry", "README.md")

    def test_fenced_example_link_does_not_register_a_document(self) -> None:
        files = {
            "README.md": (
                "# Project\n\n```markdown\n[stranded](docs/stranded.md)\n```\n"
            ),
            "docs/stranded.md": "# Stranded\n",
        }
        self.assert_fails(
            files, "docs/stranded.md: orphan", "--entry", "README.md")

    def test_orphans_are_not_reported_without_entry(self) -> None:
        files = {
            "README.md": "# Project\n",
            "docs/stranded.md": "# Stranded\n",
        }
        result = self.validate(files)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_unknown_entry_fails(self) -> None:
        self.assert_fails(
            {"README.md": "# Project\n"},
            "docs/entry.md: entry is not a scanned Markdown file",
            "--entry", "docs/entry.md")

    def test_dot_prefixed_entry_is_normalized(self) -> None:
        result = self.validate(VALID_TREE, "--entry", "./README.md")
        self.assertEqual(result.returncode, 0, result.stdout)


class ExclusionTests(ValidatorTestCase):
    def test_excluded_file_is_not_scanned_for_links(self) -> None:
        files = {
            "README.md": "# Project\n",
            "generated/api.md": "# Generated\n\n[gone](missing.md)\n",
        }
        self.assert_fails(files, "generated/api.md: broken link -> missing.md")
        result = self.validate(files, "--exclude", "generated/*")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_excluded_file_is_not_an_orphan(self) -> None:
        files = {
            "README.md": "# Project\n",
            "generated/deep/api.md": "# Generated\n",
        }
        result = self.validate(
            files, "--entry", "README.md", "--exclude", "generated/*")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_nested_tests_dir_is_scanned_beside_a_skill_md(self) -> None:
        """A SKILL.md at the root must not silently drop any tests/ tree."""
        files = {
            "SKILL.md": "---\nname: x\n---\n\n# x\n",
            "README.md": "# Project\n",
            "tests/a.md": "# A\n\n[gone](../nope.md)\n",
            "pkg/tests/b.md": "# B\n\n[gone](../../nope.md)\n",
        }
        result = self.validate(files)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("tests/a.md: broken link", result.stdout)
        self.assertIn("pkg/tests/b.md: broken link", result.stdout)

    def test_exclude_is_the_way_to_skip_a_tests_tree(self) -> None:
        files = {
            "README.md": "# Project\n",
            "tests/fixture.md": "# Fixture\n\n[gone](missing.md)\n",
        }
        result = self.validate(files, "--exclude", "tests/*")
        self.assertEqual(result.returncode, 0, result.stdout)


class RealContentTests(ValidatorTestCase):
    """Guard the validator against this skill's own documentation."""

    def test_skill_directory_scan_passes(self) -> None:
        result = self.run_validator(SKILL_ROOT)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_skill_is_reachable_from_its_own_entry(self) -> None:
        result = self.run_validator(SKILL_ROOT, "--entry", "SKILL.md")
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
