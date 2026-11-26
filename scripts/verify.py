#!/usr/bin/env python3
"""Source and historical-blob contract for the AOSP public programme hub.

This is repository validation, not evidence of product runtime, usability,
professional credentials, scientific validity or external live integrations.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "roa-research-programme/v3"  # retained for cross-repository readers
PUBLIC = (
    "academics", "ROA", "cora", "ictc", "juriscribe",
    "iKant_EDU", "lumen", "teddy", "NILO",
)
THESIS_BLOBS = {
    2009: ("theses/2009-game-theory-social-negotiations.pdf", "b263a67194b2e0f502a2acdea72cbc9ceca05fe2"),
    2011: ("theses/2011-corruption-risk-management.pdf", "995aad80d8933791b074e3c7c09535822cdccb63"),
    2022: ("theses/2022-information-security-governance.pdf", "783667705671e7274f0fee5b9b4e8d215b966655"),
    2025: ("theses/2025-reticular-local-abstraction.pdf", "7aa056bc5d50a6c62ce77debd8b04e8813db7e7e"),
}
RETIRED = (
    "AUTHOR.json", "PROGRAMME_HEADER_CONTRACT.md", "academic-lineage",
    "programme", "evidence", "scripts/check_lumen_constellation.py",
    "scripts/check_programme_v2.py", "scripts/falsify_hub_semantics.py",
    ".github/workflows/lumen-constellation.yml",
    ".github/workflows/programme-readme.yml",
)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def check_contract(readme: str, registry: dict) -> list[str]:
    errors = []
    def require(condition: bool, code: str) -> None:
        if not condition:
            errors.append(code)

    marker = "<!-- programme-header:v2 -->"
    require(readme.startswith(marker + "\n") and readme.count(marker) == 1, "canonical-header")
    require("# AOSP" in readme and "Augmented Ontological Semantic Platforms" in readme, "programme-identity")
    for phrase in (
        "Every repository is independently readable",
        "Membership does not imply formal derivation",
        "Repository-local code, evidence, and governance remain authoritative",
    ):
        require(phrase in readme[:700], "authority-boundary:" + phrase)
    for phrase in ("flagship", "CORA", "product", "software", "repository",
                   "Git blobs", "mutation", "roadmap", "iKant-EDU",
                   "First-release target: Q1 2027", "subject to validation",
                   "Gianluca Conte", "Closed and unmaintained"):
        require(phrase in readme, "missing:" + phrase)
    # Public entrypoint: seven bounded sections in the user's chosen order.
    sections = (
        "## Founder and academic trajectory",
        "## ROA — theoretical research programme",
        "## AOSP — engineering programme",
        "## CORA — flagship experimental witness",
        "## iKant-EDU",
        "## EVRIA",
        "## Experimental",
    )
    positions = [readme.find(item) for item in sections]
    require(all(p >= 0 for p in positions) and positions == sorted(positions)
            and len(set(positions)) == len(sections), "readme-section-order")
    diagrams = re.findall(r"```mermaid\n(.*?)\n```", readme, re.S)
    require(len(diagrams) == 2 and all(d.startswith("flowchart LR\n") for d in diagrams),
            "readme-two-horizontal-diagrams")
    for item in ("ICTC", "Teddy", "Juriscribe", "NILO", "LUMEN"):
        require(item.lower() in readme.lower(), "missing-prototype:" + item)
    require("not enterprise-ready" in readme and
            "safe enterprise use has not been demonstrated or claimed" in readme and
            "no independent enterprise certification" in readme,
            "prototype-status-boundary")
    require("replaceable AI coding agents" in readme and
            "not proof that CORA authored" in readme,
            "agent-attribution-boundary")
    require("CORA does not seek superiority" in readme,
            "checklist-comparator-boundary")
    require("16/16 fixed cases" in readme and "no people were tested" in readme,
            "research-negative-evidence")
    require("private iKant-EDU runtime" in readme
            and "public [iKant_EDU]" in readme, "edu-repository-distinction")
    require("to-be" in readme and "meta-controller" in readme
            and "verified integration" in readme, "evria-future-boundary")
    for sha in (
        "80a1e71b98f63a9f5a30d4398eefaadea27ba39c",
        "f04a124ac024988c1a55884be1560b156f6e574f",
        "1ccb6fd0f7b74832a2f5bf64e27e38704e15cb30",
        "32e7935fbf425c7c513c95862c019230e74d014c",
        "4db17ab598c1bfbee823d5161c536c29818fa181",
        "f98690d0b19b9e40dae05ebfccb70afedaee2bbc",
    ):
        require("/commit/" + sha in readme, "commit-case:" + sha[:10])
    require(registry.get("schema") == SCHEMA, "schema")
    p = registry.get("programme", {})
    require(p.get("id") == "PRG-ROA", "legacy-id")
    require(p.get("canonical_name") == "AOSP", "canonical-name")
    require(p.get("hub") == "academics", "hub")
    require(p.get("theoretical_anchor") == "ROA", "theory")
    require(p.get("flagship") == "cora", "flagship")
    rows = registry.get("repositories", [])
    ids = [r.get("id") for r in rows]
    repos = [r.get("repo") for r in rows]
    require(len(rows) == 12 and len(set(ids)) == len(rows) and
            len(set(repos)) == len(rows), "membership-uniqueness")
    require(set(PUBLIC) <= set(ids), "public-membership")
    for slug in PUBLIC:
        if slug == "academics":
            continue  # A public hub need not self-link; preserve the manual editorial choice.
        require("https://github.com/Luke883i/" + slug in readme, "public-route:" + slug)
    edges = registry.get("relations", [])
    require(len(edges) == 3 and
            all(e.get("from") and e.get("to") and e.get("type") for e in edges),
            "directional-relations")
    governance = registry.get("governance", {})
    header = governance.get("membership_header", {})
    require(header.get("marker") == "programme-header:v2", "header-version")
    boundaries = governance.get("claim_boundary", {})
    require(len(boundaries) >= 6 and all(v is False for v in boundaries.values()),
            "claim-boundary")
    tracks = registry.get("tracks", [])
    require(any(t.get("name") == "iKant-EDU" and
                t.get("first_release_target") == "2027-Q1" and
                t.get("target_status") == "PLANNED_NOT_VALIDATED" and
                t.get("public_repo_is_release") is False for t in tracks),
            "unvalidated-release-target")
    theses = registry.get("theses", [])
    years = [t.get("year") for t in theses]
    require(len(theses) == 4 and set(years) == set(THESIS_BLOBS)
            and len(set(years)) == 4, "thesis-inventory")
    for t in theses:
        year = t.get("year")
        if year not in THESIS_BLOBS:
            continue
        path, sha = THESIS_BLOBS[year]
        require(t.get("path") == path and t.get("blob_sha") == sha, "thesis-pin:" + str(year))
        require("](" + path + ")" in readme, "thesis-link:" + str(year))
        require(str(year) in readme and t.get("qualification", "") != "",
                "thesis-metadata:" + str(year))
    return errors


def verify(root: Path = ROOT) -> list[str]:
    errors = []
    try:
        readme = (root / "README.md").read_text(encoding="utf-8")
        registry = json.loads((root / "PROGRAMME.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["cannot-load-source:" + type(exc).__name__]
    if not isinstance(registry, dict):
        return ["invalid-registry-root"]
    errors.extend(check_contract(readme, registry))
    for year, (relative, expected) in THESIS_BLOBS.items():
        path = root / relative
        try:
            payload = path.read_bytes()
        except OSError:
            errors.append("missing-pdf:" + str(year))
            continue
        if not payload.startswith(b"%PDF-"):
            errors.append("not-a-pdf:" + str(year))
        if git_blob_sha(payload) != expected:
            errors.append("pdf-blob-drift:" + str(year))
    other_pdfs = {p.relative_to(root).as_posix() for p in (root / "theses").glob("*.pdf")}
    if other_pdfs != {path for path, _ in THESIS_BLOBS.values()}:
        errors.append("pdf-file-set")
    for path in RETIRED:
        if (root / path).exists():
            errors.append("legacy-current:" + path)
    for required in ("history/README.md", "scripts/verify.py",
                     "tests/test_verify.py", ".github/workflows/verify.yml"):
        if not (root / required).is_file():
            errors.append("missing-governance:" + required)
    return sorted(set(errors))


if __name__ == "__main__":
    faults = verify()
    print(json.dumps({
        "status": "PASS_SCOPED_SOURCE" if not faults else "FAIL",
        "pdf_blob_pins": len(THESIS_BLOBS),
        "public_routes": len(PUBLIC),
        "errors": faults,
        "not_attested": "product runtime, external live links, user acceptance and scientific validity",
    }, sort_keys=True))
    sys.exit(0 if not faults else 1)
