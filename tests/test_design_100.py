"""Compare 100 complete README-text / filesystem-path proposals.

This is a deterministic MODELLED design comparison, not 100 repository
checkouts, independent readers, native product runs or economic measurements.
Ten full-text candidates x ten full-path inventories = 100 distinct proposals.
"""
from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from scripts import verify

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = (ROOT / "README.md").read_text(encoding="utf-8")
REGISTRY = json.loads((ROOT / "PROGRAMME.json").read_text(encoding="utf-8"))
# The paths here are required owners, not arbitrary minimal file-count targets.
ESSENTIAL = {
    "README.md", "PROGRAMME.json", "history/README.md",
    "scripts/verify.py", "tests/test_verify.py",
    "tests/test_design_100.py", ".github/workflows/verify.yml",
    *(p for p, _ in verify.THESIS_BLOBS.values()),
}
def swap_roa_aosp(text):
    first = text.index("## ROA — theoretical research programme")
    second = text.index("## AOSP — engineering programme")
    third = text.index("## CORA — flagship experimental witness")
    return text[:first] + text[second:third] + text[first:second] + text[third:]


CONTENT_ALTERNATIVES = (
    ("full-guided-walkthrough", lambda r: r),
    ("extra-executive-summary", lambda r: r.replace(
        "## Founder", "A second introductory briefing repeats the programme identity.\n\n## Founder", 1)),
    ("extra-navigational-note", lambda r: r.replace(
        "## CORA", "## Reader notes\n\nThe evidence is described in the sections below.\n\n## CORA", 1)),
    ("more-technical-preface", lambda r: r.replace(
        "## AOSP", "Readers must distinguish Git, state, authority and host checks.\n\n## AOSP", 1)),
    ("roa-aosp-inverted", swap_roa_aosp),
    ("missing-counterexample", lambda r: r.replace(
        "CORA does not seek superiority over a strong engineering checklist.",
        "CORA guarantees superiority over engineering checklists.", 1)),
    ("removed-diagram", lambda r: r.replace(chr(96) * 3 + "mermaid", chr(96) * 3 + "text", 1)),
    ("lost-original-commit", lambda r: r.replace(
        "f98690d0b19b9e40dae05ebfccb70afedaee2bbc",
        "0000000000000000000000000000000000000000")),
    ("unearned-release", lambda r: r.replace(
        "First-release target: Q1 2027", "Released: Q1 2027", 1)),
    ("thesis-link-omitted", lambda r: r.replace(
        "theses/2025-reticular-local-abstraction.pdf", "theses/missing-2025.pdf")),
)
PATH_ALTERNATIVES = (
    ("current-single-hub", lambda f: f),
    ("extra-long-form-case-file", lambda f: f | {"docs/CASE_STUDIES.md"}),
    ("separate-diagram-copy", lambda f: f | {"docs/DIAGRAMS.md"}),
    ("second-root-overview", lambda f: f | {"OVERVIEW.md"}),
    ("move-consumed-registry", lambda f: (f - {"PROGRAMME.json"}) | {"registry/PROGRAMME.json"}),
    ("move-original-pdf", lambda f: (f - {"theses/2025-reticular-local-abstraction.pdf"}) | {"archive/2025.pdf"}),
    ("drop-original-verifier", lambda f: f - {"scripts/verify.py"}),
    ("drop-negative-tests", lambda f: f - {"tests/test_verify.py"}),
    ("drop-ci", lambda f: f - {".github/workflows/verify.yml"}),
    ("duplicate-machine-registry", lambda f: f | {"programmes/PROGRAMME.json"}),
)
UNSAFE_NARRATIVES = {4, 5, 6, 7, 8, 9}
UNSAFE_PATHS = {4, 5, 6, 7, 8}


def compare():
    """Return exact candidate records; no AI judgement or implicit source edits."""
    records = []
    identities = set()
    for ci, (content_name, transform) in enumerate(CONTENT_ALTERNATIVES):
        text = transform(PUBLIC)
        for fi, (layout_name, alter) in enumerate(PATH_ALTERNATIVES):
            files = frozenset(alter(set(ESSENTIAL)))
            fingerprint = hashlib.sha256((text + "\0" + "\n".join(sorted(files))).encode("utf-8")).hexdigest()
            if fingerprint in identities:
                raise AssertionError("duplicate global candidate")
            identities.add(fingerprint)
            contract_errors = verify.check_contract(text, REGISTRY)
            missing = sorted(ESSENTIAL - files)
            unsafe = bool(contract_errors or missing)
            # After hard constraints, prefer less duplication and fewer extra surfaces.
            # This is an explicitly author-chosen editorial cost model, not measured UX.
            extra = files - ESSENTIAL
            editorial_overhead = max(0, len(text) - len(PUBLIC))
            score = 10000 - len(extra) * 100 - editorial_overhead
            records.append({
                "id": f"R{ci:02d}-F{fi:02d}",
                "readme_option": content_name,
                "filesystem_option": layout_name,
                "fingerprint": fingerprint,
                "accepted": not unsafe,
                "score_if_accepted": score if not unsafe else None,
                "contract_failures": contract_errors,
                "missing_required_paths": missing,
            })
    return records


class CandidateSelectionTests(unittest.TestCase):
    def test_all_100_global_candidates_are_distinct_and_scored(self):
        records = compare()
        self.assertEqual(len(records), 100)
        self.assertEqual(len({x["fingerprint"] for x in records}), 100)
        feasible = [r for r in records if r["accepted"]]
        self.assertGreaterEqual(len(feasible), 2, "comparator must admit credible alternatives")
        winner = max(feasible, key=lambda x: x["score_if_accepted"])
        self.assertEqual(winner["id"], "R00-F00")
        self.assertGreater(winner["score_if_accepted"], max(
            x["score_if_accepted"] for x in feasible if x["id"] != winner["id"]))
        print("MODELLED_100_REPOSITORY_README_ALTERNATIVES " + json.dumps({
            "all": len(records), "distinct": len({r["fingerprint"] for r in records}),
            "accepted": len(feasible), "rejected": 100 - len(feasible),
            "winner": winner["id"], "winner_fingerprint": winner["fingerprint"],
            "selection_rule": "hard contract first, then path duplication and editorial overhead",
            "claim_boundary": "deterministic text+path models only; not 100 physical repo clones, user trials or external consumer tests",
        }, sort_keys=True))

    def test_known_unsafe_families_are_rejected(self):
        records = compare()
        for r in records:
            ci = int(r["id"][1:3])
            fi = int(r["id"][5:7])
            if ci in UNSAFE_NARRATIVES or fi in UNSAFE_PATHS:
                with self.subTest(variant=r["id"]):
                    self.assertFalse(r["accepted"], r["id"])

    def test_real_filesystem_preserves_required_source_paths(self):
        for path in ESSENTIAL:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file(), path)


if __name__ == "__main__":
    unittest.main()
