from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StructureTests(unittest.TestCase):
    def test_top_level_folder_limit(self) -> None:
        config = json.loads((ROOT / "config" / "vault_structure.json").read_text(encoding="utf-8"))
        self.assertLessEqual(len(config["top_level_folders"]), config["max_top_level_folders"])
        self.assertEqual(len(config["top_level_folders"]), len(set(config["top_level_folders"])))

    def test_required_connectors_present(self) -> None:
        config = json.loads((ROOT / "config" / "connectors.json").read_text(encoding="utf-8"))
        names = {connector["name"] for connector in config["connectors"]}
        self.assertTrue({"Obsidian", "Notion", "Gmail", "Granola", "Crisp"}.issubset(names))

    def test_prompts_keep_one_question_rule(self) -> None:
        prompt = (ROOT / "prompts" / "OBSIDIAN_STRUCTURE_INTERVIEW.md").read_text(encoding="utf-8")
        self.assertIn("Ask one question at a time", prompt)
        self.assertIn("Do not ask more than one question", prompt)

    def test_bootstrap_demo_vault(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "bootstrap_client.py"),
                    "--vault",
                    str(vault),
                    "--allow-non-obsidian",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((vault / "START HERE - POS FOR BEGINNERS Setup.md").is_file())
            self.assertTrue((vault / "90-Operations" / "Setup" / "MCP Readiness Report.md").is_file())
            self.assertTrue((vault / "60-Rules" / "Agent Working Agreement.md").is_file())


if __name__ == "__main__":
    unittest.main()
