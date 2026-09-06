"""Deterministic contract rules for scripts/goal.py.

Run: python3 -m unittest discover -s <skill-root>/tests -v
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import goal  # noqa: E402


class GoalScriptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        (self.root / ".gitignore").write_text("node_modules/\n", encoding="utf-8")
        self.addCleanup(self.tmp.cleanup)
        out = self.run_ok(
            "init", "--title", "Auth Migration", "--objective", "Move auth to v2",
            "--accept", "v1 proxies to v2", "--accept", "no failed logins",
        )
        self.contract = out.splitlines()[0].split("Contract: ", 1)[1]
        self.init_output = out

    def run_cli(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = goal.main(["--root", str(self.root), *args])
        return code, out.getvalue(), err.getvalue()

    def run_ok(self, *args: str) -> str:
        code, out, err = self.run_cli(*args)
        self.assertEqual(code, 0, err or out)
        return out

    def run_fail(self, *args: str, code: int = 2) -> str:
        actual, out, err = self.run_cli(*args)
        self.assertEqual(actual, code, out)
        return err or out

    def read(self) -> dict:
        return json.loads((self.root / self.contract).read_text(encoding="utf-8"))

    def states(self) -> dict[str, str]:
        contract = self.read()
        return {cid: goal.state_of(contract, cid) for cid in goal.criterion_ids(contract)}

    def verify(self, cid: str) -> None:
        self.run_ok("verify", self.contract, cid, "--summary", "seen", "--locator", "log", "--invalidated-by", "config change")

    def test_init_writes_valid_ignored_contract(self) -> None:
        self.assertTrue(self.contract.startswith(".goal/auth-migration-"))
        self.assertIn("/.goal/", (self.root / ".gitignore").read_text(encoding="utf-8"))
        self.assertEqual(goal.validate(self.read()), [])
        self.assertEqual(self.states(), {"A1": "open", "A2": "open"})
        self.assertIn("VALID", self.run_ok("validate", self.contract))
        self.assertIn(f"Pursue the contract at {self.contract} with $codex-goal-loop until `ready` passes.", self.init_output)
        self.assertNotIn("Move auth to v2", self.init_output.split("Contract:", 1)[1])

    def test_state_is_derived_not_stored(self) -> None:
        self.verify("A1")
        self.assertEqual(self.states()["A1"], "verified")
        self.assertNotIn('"state"', (self.root / self.contract).read_text(encoding="utf-8"))
        self.run_fail("invalidate", self.contract, "A2", "--reason", "x")
        self.run_ok("invalidate", self.contract, "A1", "--reason", "config changed")
        self.assertEqual(self.states()["A1"], "open")
        self.assertIsNone(self.read()["working"]["acceptance"]["A1"]["evidence"])

    def test_failed_approach_cannot_be_repeated(self) -> None:
        self.run_ok("approach", self.contract, "A1", "--approach", "nginx rewrite")
        self.run_ok("attempt", self.contract, "A1", "--outcome", "cannot rewrite POST")
        a1 = self.read()["working"]["acceptance"]["A1"]
        self.assertIsNone(a1["approach"])
        self.assertEqual(len(a1["attempts"]), 1)
        self.assertIn("already failed", self.run_fail("approach", self.contract, "A1", "--approach", "nginx rewrite"))
        self.run_ok("approach", self.contract, "A1", "--approach", "envoy filter")
        self.assertIn("approach already in progress", self.run_ok("next", self.contract))

    def test_max_attempts_forces_decision_and_refinement_resets(self) -> None:
        for n in range(10):
            self.run_ok("approach", self.contract, "A1", "--approach", f"approach {n}")
            self.run_ok("attempt", self.contract, "A1", "--outcome", "failed")
        self.assertEqual(self.states()["A1"], "exhausted")
        self.assertIn("max_attempts=10", self.run_fail("approach", self.contract, "A1", "--approach", "approach 11"))
        self.assertIn("pursue A2", self.run_ok("next", self.contract))
        self.verify("A2")
        self.assertIn("A1 reached 10 failed approaches", self.run_ok("next", self.contract))
        self.assertIn("A1 is exhausted", self.run_fail("ready", self.contract, code=1))
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "relax A1", "--target", "A1", "--operation", "set", "--proposed", "v1 proxies to v2 for GET only")
        self.assertEqual(self.states()["A1"], "blocked")
        self.run_ok("decision", "resolve", self.contract, "D1", "--approve")
        self.assertEqual(self.read()["working"]["acceptance"]["A1"]["attempts"], [])
        self.assertIn("pursue A1", self.run_ok("next", self.contract))

    def test_init_max_attempts_override(self) -> None:
        out = self.run_ok("init", "--title", "small", "--objective", "o", "--accept", "a", "--max-attempts", "2")
        contract = out.splitlines()[0].split("Contract: ", 1)[1]
        self.assertEqual(json.loads((self.root / contract).read_text())["protected"]["max_attempts"], 2)
        self.assertIn("minimum", self.run_fail("init", "--title", "zero", "--objective", "o", "--accept", "a", "--max-attempts", "0"))

    def test_refinement_blocks_until_resolved_and_applies_on_approval(self) -> None:
        self.verify("A2")
        self.run_ok(
            "decision", "open", self.contract, "--kind", "refinement", "--request", "A2 is unmeasurable",
            "--target", "A2", "--operation", "set", "--proposed", "failure rate below 0.1%",
        )
        self.assertEqual(self.read()["protected"]["acceptance"][1]["statement"], "no failed logins")
        self.assertIn("blocked by open decision", self.run_fail("verify", self.contract, "A2", "--summary", "s", "--locator", "l", "--invalidated-by", "c"))
        self.run_ok("decision", "resolve", self.contract, "D1", "--approve")
        contract = self.read()
        self.assertEqual(contract["protected"]["acceptance"][1]["statement"], "failure rate below 0.1%")
        self.assertEqual(self.states()["A2"], "open")
        self.assertEqual(contract["working"]["decisions"][0]["resolution"]["outcome"], "approved")
        self.run_fail("decision", "resolve", self.contract, "D1", "--reject")

    def test_rejected_refinement_leaves_protected_unchanged(self) -> None:
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "r", "--target", "objective", "--operation", "set", "--proposed", "other")
        self.run_ok("decision", "resolve", self.contract, "D1", "--reject", "--note", "keep scope")
        self.assertEqual(self.read()["protected"]["objective"], "Move auth to v2")

    def test_objective_refinement_invalidates_all_verified(self) -> None:
        self.verify("A1")
        self.verify("A2")
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "narrow", "--target", "objective", "--operation", "set", "--proposed", "Move auth to v2 with <1min downtime")
        self.run_ok("decision", "resolve", self.contract, "D1", "--approve")
        self.assertEqual(self.states(), {"A1": "open", "A2": "open"})

    def test_add_and_remove_criterion(self) -> None:
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "add", "--target", "A3", "--operation", "add", "--proposed", "rollback drill passes")
        self.run_ok("decision", "resolve", self.contract, "D1", "--approve")
        self.assertIn("A3", self.read()["working"]["acceptance"])
        self.run_fail("decision", "open", self.contract, "--kind", "refinement", "--request", "dup", "--target", "A3", "--operation", "add", "--proposed", "x")
        self.run_ok("decision", "open", self.contract, "--kind", "input", "--request", "prod access", "--blocks", "A3")
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "drop", "--target", "A3", "--operation", "remove")
        self.run_ok("decision", "resolve", self.contract, "D3", "--approve")
        contract = self.read()
        self.assertNotIn("A3", contract["working"]["acceptance"])
        self.assertEqual(contract["working"]["decisions"][1]["blocks"], [])

    def test_ready_requires_all_verified_and_no_open_decision(self) -> None:
        self.assertIn("A1 is open", self.run_fail("ready", self.contract, code=1))
        self.verify("A1")
        self.verify("A2")
        self.run_ok("decision", "open", self.contract, "--kind", "input", "--request", "prod approval")
        self.assertIn("D1 (input) is unresolved", self.run_fail("ready", self.contract, code=1))
        self.assertIn("awaiting user decision", self.run_ok("next", self.contract))
        self.run_ok("decision", "resolve", self.contract, "D1", "--approve")
        self.assertIn("READY once every falsifier", self.run_ok("ready", self.contract))
        self.assertIn("verified [A1, A2]", self.run_ok("handoff", self.contract))

    def test_attempt_with_new_approach_passes_the_same_gates(self) -> None:
        self.run_ok("approach", self.contract, "A1", "--approach", "x")
        self.run_ok("attempt", self.contract, "A1", "--outcome", "f")
        self.assertIn("already recorded as failed", self.run_fail("attempt", self.contract, "A1", "--approach", "x", "--outcome", "f"))
        self.run_ok("decision", "open", self.contract, "--kind", "input", "--request", "q", "--blocks", "A1")
        self.assertIn("blocked", self.run_fail("attempt", self.contract, "A1", "--approach", "y", "--outcome", "f"))
        self.run_ok("decision", "resolve", self.contract, "D1", "--reject")
        for n in range(9):
            self.run_ok("attempt", self.contract, "A1", "--approach", f"y{n}", "--outcome", "f")
        self.assertIn("already reached", self.run_fail("attempt", self.contract, "A1", "--approach", "z", "--outcome", "f"))
        self.assertEqual(len(self.read()["working"]["acceptance"]["A1"]["attempts"]), 10)

    def test_approved_input_decision_restores_attempt_budget(self) -> None:
        for n in range(10):
            self.run_ok("attempt", self.contract, "A1", "--approach", f"a{n}", "--outcome", "f")
        self.assertEqual(self.states()["A1"], "exhausted")
        self.run_ok("decision", "open", self.contract, "--kind", "input", "--request", "grant prod access", "--blocks", "A1", "A1")
        self.assertEqual(self.read()["working"]["decisions"][0]["blocks"], ["A1"])
        self.run_ok("decision", "resolve", self.contract, "D1", "--reject")
        self.assertEqual(self.states()["A1"], "exhausted")
        self.run_ok("decision", "open", self.contract, "--kind", "input", "--request", "grant prod access", "--blocks", "A1")
        self.run_ok("decision", "resolve", self.contract, "D2", "--approve")
        self.assertEqual(self.states()["A1"], "open")
        self.run_ok("approach", self.contract, "A1", "--approach", "with prod access")

    def test_reverify_replaces_evidence(self) -> None:
        self.verify("A1")
        self.run_ok("verify", self.contract, "A1", "--summary", "fresher", "--locator", "l2", "--invalidated-by", "c")
        self.assertEqual(self.read()["working"]["acceptance"]["A1"]["evidence"]["summary"], "fresher")

    def test_open_objective_refinement_blocks_everything(self) -> None:
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "narrow", "--target", "objective", "--operation", "set", "--proposed", "other")
        self.assertEqual(self.states(), {"A1": "blocked", "A2": "blocked"})
        self.assertIn("awaiting user decision(s) D1", self.run_ok("next", self.contract))
        self.assertIn("blocked", self.run_fail("verify", self.contract, "A1", "--summary", "s", "--locator", "l", "--invalidated-by", "c"))

    def test_protected_lists_and_max_attempts_refine_through_decisions(self) -> None:
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "add constraint", "--target", "constraints", "--operation", "add", "--proposed", "no schema changes")
        self.run_ok("decision", "resolve", self.contract, "D1", "--approve")
        self.assertEqual(self.read()["protected"]["constraints"], ["no schema changes"])
        self.assertIn("already contains", self.run_fail("decision", "open", self.contract, "--kind", "refinement", "--request", "dup", "--target", "constraints", "--operation", "add", "--proposed", "no schema changes"))
        self.assertIn("does not contain", self.run_fail("decision", "open", self.contract, "--kind", "refinement", "--request", "x", "--target", "non_goals", "--operation", "remove", "--proposed", "missing"))
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "drop", "--target", "constraints", "--operation", "remove", "--proposed", "no schema changes")
        self.run_ok("decision", "resolve", self.contract, "D2", "--approve")
        self.assertEqual(self.read()["protected"]["constraints"], [])
        self.assertIn("positive integer", self.run_fail("decision", "open", self.contract, "--kind", "refinement", "--request", "cap", "--target", "max_attempts", "--operation", "set", "--proposed", "0"))
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "cap", "--target", "max_attempts", "--operation", "set", "--proposed", "3")
        self.run_ok("decision", "resolve", self.contract, "D3", "--approve")
        self.assertEqual(self.read()["protected"]["max_attempts"], 3)
        self.assertEqual(self.states(), {"A1": "open", "A2": "open"})

    def test_a_stale_refinement_never_blocks_another_approval(self) -> None:
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "reword", "--target", "A2", "--operation", "set", "--proposed", "new text")
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "drop", "--target", "A2", "--operation", "remove")
        self.run_ok("decision", "resolve", self.contract, "D2", "--approve")
        self.assertEqual(list(self.read()["working"]["acceptance"]), ["A1"])
        self.assertIn("D1 no longer applies: A2 does not exist", self.run_fail("decision", "resolve", self.contract, "D1", "--approve"))
        self.run_ok("decision", "resolve", self.contract, "D1", "--reject")
        self.assertIn("a contract keeps at least one", self.run_fail("decision", "open", self.contract, "--kind", "refinement", "--request", "drop last", "--target", "A1", "--operation", "remove"))

    def test_duplicate_proposal_is_refused_at_open_not_at_write(self) -> None:
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "c1", "--target", "constraints", "--operation", "add", "--proposed", "no schema changes")
        self.run_ok("decision", "open", self.contract, "--kind", "refinement", "--request", "c2", "--target", "non_goals", "--operation", "add", "--proposed", "no schema changes")
        self.run_ok("decision", "resolve", self.contract, "D1", "--approve")
        self.assertEqual(self.read()["protected"]["constraints"], ["no schema changes"])
        self.assertIn("already contains", self.run_fail("decision", "open", self.contract, "--kind", "refinement", "--request", "dup", "--target", "constraints", "--operation", "add", "--proposed", "no schema changes"))
        self.run_ok("decision", "resolve", self.contract, "D2", "--approve")
        self.assertEqual(self.read()["protected"]["non_goals"], ["no schema changes"])

    def test_steps_gate_verify_and_derive_next(self) -> None:
        self.run_ok("approach", self.contract, "A1", "--approach", "envoy filter")
        self.run_ok("step", self.contract, "A1", "--add", "migrate /login", "--add", "run scripts/unmigrated.sh until empty")
        self.assertIn("next step: migrate /login", self.run_ok("next", self.contract))
        self.assertIn("undone step", self.run_fail("verify", self.contract, "A1", "--summary", "s", "--locator", "l", "--invalidated-by", "c"))
        self.run_ok("step", self.contract, "A1", "--done", "1")
        self.assertIn("already done", self.run_fail("step", self.contract, "A1", "--done", "1"))
        self.assertIn("next step: run scripts/unmigrated.sh", self.run_ok("next", self.contract))
        self.run_ok("step", self.contract, "A1", "--drop", "2")
        self.assertNotIn("next step", self.run_ok("next", self.contract))
        self.verify("A1")
        steps = self.read()["working"]["acceptance"]["A1"]["steps"]
        self.assertEqual([s["text"] for s in steps], ["migrate /login"])
        self.assertIsNotNone(steps[0]["done_at"])
        self.run_fail("step", self.contract, "A1")
        self.run_fail("step", self.contract, "A1", "--done", "9")

    def test_non_ascii_title_gets_fallback_slug(self) -> None:
        out = self.run_ok("init", "--title", "认证迁移", "--objective", "o", "--accept", "a")
        contract = out.splitlines()[0].split("Contract: ", 1)[1]
        self.assertTrue(contract.startswith(".goal/goal-"))
        self.assertEqual(json.loads((self.root / contract).read_text())["title"], "认证迁移")

    def test_current_resolves_only_unfinished_contracts(self) -> None:
        self.assertEqual(self.run_ok("current").strip(), self.contract)
        second = self.run_ok("init", "--title", "other", "--objective", "o", "--accept", "a").splitlines()[0].split("Contract: ", 1)[1]
        self.assertIn("more than one unfinished contract", self.run_fail("current"))
        self.run_ok("verify", second, "A1", "--summary", "s", "--locator", "l", "--invalidated-by", "c")
        self.assertEqual(self.run_ok("current").strip(), self.contract)
        self.verify("A1")
        self.verify("A2")
        out = self.run_fail("current")
        self.assertIn("no unfinished contract", out)
        self.assertIn(self.contract, out)

    def test_current_ignores_unreadable_contracts(self) -> None:
        (self.root / ".goal" / "broken.json").write_text("{not json", encoding="utf-8")
        self.assertEqual(self.run_ok("current").strip(), self.contract)

    def test_current_names_invalid_and_legacy_contracts(self) -> None:
        (self.root / ".goal" / "legacy.md").write_text("# Goal: old\n", encoding="utf-8")
        data = self.read(); data["bogus"] = 1
        (self.root / self.contract).write_text(json.dumps(data), encoding="utf-8")
        code, out, err = self.run_cli("current")
        self.assertEqual(code, 2)
        self.assertIn("Additional properties are not allowed", err)
        self.assertIn("invalid: " + self.contract, err)
        self.assertIn("legacy: .goal/legacy.md", err)

    def test_blocking_decision_skips_criterion_in_next(self) -> None:
        self.run_ok("decision", "open", self.contract, "--kind", "input", "--request", "need dataset", "--blocks", "A1")
        self.assertEqual(self.states()["A1"], "blocked")
        self.assertIn("pursue A2", self.run_ok("next", self.contract))

    def test_risks_add_and_drop(self) -> None:
        self.run_ok("risk", self.contract, "--add", "prod access unknown", "--add", "schema drift")
        self.run_ok("risk", self.contract, "--drop", "1", "--drop", "1")
        self.assertEqual(self.read()["working"]["risks"], ["schema drift"])
        self.run_fail("risk", self.contract, "--drop", "5")
        self.run_fail("risk", self.contract)

    def test_validate_reports_corruption(self) -> None:
        path = self.root / self.contract
        data = self.read()
        data["working"]["acceptance"]["A1"]["state"] = "verified"
        data["working"]["lifecycle"] = "active"
        path.write_text(json.dumps(data), encoding="utf-8")
        out = self.run_fail("validate", self.contract, code=1)
        self.assertIn("lifecycle", out)
        self.assertIn("state", out)
        data["working"].pop("lifecycle")
        data["working"]["acceptance"]["A1"].pop("state")
        data["working"]["acceptance"]["A9"] = data["working"]["acceptance"]["A2"]
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertIn("working.acceptance keys must equal", self.run_fail("validate", self.contract, code=1))
        self.assertIn("contract is invalid", self.run_fail("status", self.contract))

    def test_rejects_unsafe_paths(self) -> None:
        self.assertIn("inside the workspace", self.run_fail("status", "../x.json"))
        self.assertIn("inside the workspace", self.run_fail("status", os.path.abspath(os.sep)))
        self.assertIn("inside the workspace", self.run_fail("status", ""))
        self.assertIn("not found", self.run_fail("status", ".goal/missing.json"))
        self.assertIn("ignored by git", self.run_fail("init", "--title", "t", "--objective", "o", "--accept", "a", "--path", self.contract))
        self.run_ok("init", "--title", "t", "--objective", "o", "--accept", "a", "--path", "docs/goal.json")
        self.assertIn("refusing to overwrite", self.run_fail("init", "--title", "t", "--objective", "o", "--accept", "a", "--path", "docs/goal.json"))


if __name__ == "__main__":
    unittest.main()
