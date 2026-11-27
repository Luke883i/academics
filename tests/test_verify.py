"""Adversarial checks for the current AOSP repository contract.

Synthetic text mutants and physical temporary-file mutations are separate.
Neither is evidence of external product usability.
"""
from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import verify

ROOT = Path(__file__).resolve().parents[1]


class ProgrammeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.registry = json.loads((ROOT / "PROGRAMME.json").read_text(encoding="utf-8"))

    def test_positive_actual_repository(self):
        self.assertEqual(verify.verify(ROOT), [])

    def test_synthetic_negative_mutations(self):
        text_mutants = {
            "programme-identity": self.readme.replace("# AOSP", "# ROA", 1),
            "missing-header": self.readme.replace("<!-- programme-header:v2 -->", "", 1),
            "authority-launder": self.readme.replace(
                "Membership does not imply formal derivation",
                "Membership proves formal derivation", 1),
            "cora-route": self.readme.replace(
                "https://github.com/Luke883i/cora", "https://example.invalid/cora"),
            "release-overclaim": self.readme.replace(
                "subject to validation", "already validated", 1),
            "programme-map-omission": self.readme.replace(
                "### Programme structure", "### Programme directory", 1),
            "uncertified-prototype-overclaim": self.readme.replace(
                "**EXPERIMENTAL ONLY**", "**ENTERPRISE READY**", 1),
            "editorial-prompt-trace": self.readme.replace(
                "### From requirements to evidence", "### Two horizontal diagrams", 1),
            "academic-link": self.readme.replace(
                "theses/2025-reticular-local-abstraction.pdf", "theses/lost.pdf"),
        }
        for name, text in text_mutants.items():
            with self.subTest(mutation=name):
                self.assertTrue(verify.check_contract(text, self.registry), name)
        mutations = {}
        r = copy.deepcopy(self.registry)
        r["programme"]["canonical_name"] = "ROA"
        mutations["wrong-programme"] = r
        r = copy.deepcopy(self.registry)
        r["repositories"].append(copy.deepcopy(r["repositories"][0]))
        mutations["duplicate-member"] = r
        r = copy.deepcopy(self.registry)
        r["theses"] = r["theses"][1:]
        mutations["lost-thesis"] = r
        r = copy.deepcopy(self.registry)
        r["theses"][0]["blob_sha"] = "0" * 40
        mutations["tampered-thesis-pin"] = r
        r = copy.deepcopy(self.registry)
        key = next(iter(r["governance"]["claim_boundary"]))
        r["governance"]["claim_boundary"][key] = True
        mutations["authority-overclaim"] = r
        r = copy.deepcopy(self.registry)
        r["tracks"][0]["target_status"] = "RELEASED"
        mutations["unearned-release"] = r
        for name, mutant in mutations.items():
            with self.subTest(mutation=name):
                self.assertTrue(verify.check_contract(self.readme, mutant), name)

    def test_physical_pdf_byte_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            self._copy_fixtures(root)
            target = root / "theses/2009-game-theory-social-negotiations.pdf"
            target.write_bytes(target.read_bytes() + b"tamper")
            self.assertIn("pdf-blob-drift:2009", verify.verify(root))

    def test_physical_document_authority_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as dirname:
            root = Path(dirname)
            self._copy_fixtures(root)
            doc = root / "README.md"
            doc.write_text(doc.read_text(encoding="utf-8").replace(
                "Repository-local code, evidence, and governance remain authoritative",
                "Programme owns all runtime and releases", 1), encoding="utf-8")
            self.assertTrue(any(x.startswith("authority-boundary")
                                for x in verify.verify(root)))

    @staticmethod
    def _copy_fixtures(target: Path):
        for relative in ("README.md", "PROGRAMME.json", "history/README.md",
                         "scripts/verify.py", "tests/test_verify.py",
                         ".github/workflows/verify.yml",
                         *[path for path, _ in verify.THESIS_BLOBS.values()]):
            to = target / relative
            to.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, to)


if __name__ == "__main__":
    unittest.main()
