# LUMEN — Applied library-services constellation entry

LUMEN is registered as `LIBRARY_SERVICES_VERTICAL` / `APPLIED` / `APPLIED_SURFACE`.
The registry does not add an explicit ROA→LUMEN formal-derivation edge, because existing applied surfaces (ICTC, Juriscribe) are classified as programme applications without that claim.

The reciprocal LUMEN documentation uses the exact canonical `roa-programme-header:v1` syntax and links back to this programme hub. LUMEN remains the sole runtime/Koha/IdP/PWA/Render authority.

## 100 falsifiable alternatives

[`evidence/lumen-crossref-100-hypotheses.json`](../evidence/lumen-crossref-100-hypotheses.json) lists exactly 100 **synthetic hypotheses**, ten each across: programme hub, theoretical anchor, repository identity, application role, class, lifecycle status, ROA relation, non-entailments, badge header and false explicit ROA edges. Every alternative is treated as a test mutant, not as a historical claim or a real-world user experiment.

Run locally: `python3 scripts/check_lumen_constellation.py`. The script checks the canonical registry and README, then applies all 100 counterfactual mutations and rejects any surviving mutation. An additional 20-case resampling tail is only a local check within these ten modelled families. The synthetic count cannot prove actual conformity, scientific validity, production readiness, code integration or external GitHub link freshness.

## Reciprocal merge protocol

1. Merge [LUMEN badge PR #23](https://github.com/Luke883i/lumen/pull/23).
2. Recheck that its merged README preserves the exact marker, role and backlinks.
3. Merge the academics registry PR. The independent local CI validates programme semantics; it does **not** fetch an external repository during CI.
4. Re-run the local checks after either repository changes its programme header or membership policy.

Avoid automatically modifying any runtime/dependencies. Do not upgrade the legacy [hub semantic receipt](../evidence/hub-semantic-falsification-v1.json) to an external proof claim: it must be regenerated for the new README/registry candidate and remains synthetic.
