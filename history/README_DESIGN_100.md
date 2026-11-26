# README and filesystem design experiment

**Purpose:** choose a source-preserving, beginner-readable AOSP programme entry point without creating duplicate document authorities.

**Baseline:** academics main `51eb6d3b46db90824c685125495738911b35739b`. The four academic PDFs, stable `PROGRAMME.json`, historical snapshot and native Python checks remain mandatory.

**Candidate generation:** `tests/test_design_100.py` creates **10 complete alternative README texts x 10 complete filesystem path manifests = 100 deterministic candidates**. The variations include the requested order, executive add-ons, extra documentation surfaces, misplaced registry/PDFs, missing verifiers or CI, absent diagrams, lost exact commits and unjustified release or checklist claims.

**Acceptance and selection:** hard semantic/order/source-path requirements first, then an explicit author-chosen penalty for extra files and duplicated introductory text. At least one credible alternative must pass; the winning candidate must be uniquely best. All 100 full-text/path alternatives are compared; only the selected design is written to the actual Git branch.

**Limits:** alternatives are **in-memory modelled proposals**. They are not 100 physical repository clones, Git commits, independent reader tests, all possible architectures or external validation. The original PDF blob tests and source contract run separately against the real checked-out candidate. The scoring rule is a transparent editorial preference, not a measured human usability or cost benefit.

**Next empirical gate:** test the resulting README with actual non-technical and technical readers, including whether they can explain CORA's product/software/repository distinction and locate a real commit; inspect the readback of cross-repository consumers before claiming full ecosystem acceptance.
