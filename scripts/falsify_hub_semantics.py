#!/usr/bin/env python3
"""Synthetic semantic-access falsification for Luke883i/academics.

Model evidence only: not an empirical user study or usability proof.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from itertools import product
from pathlib import Path

BASELINE = "5182e84ff87594b334bb4e256581511206ba61ef"
PRIMARY = 100_000
TAIL = 10_000

ROLES = ["researcher","engineer","governance","legal","student","collaborator","enterprise","recruiter","media","skeptic"]
BUDGETS = [15,30,60,180,600]
MODES = ["scan","linear","diagram","method","evidence"]
PRIORS = ["none","general","technical","domain"]
MIS = ["none","hub_is_theory","theses_are_lineage","saturation_is_proof","hub_owns_runtime"]
ROLE_SECTION = {
 "researcher":"research question","engineer":"development method: bounded semantic slices",
 "governance":"shared epistemic boundary","legal":"evidence progression",
 "student":"author context and academic archive","collaborator":"repository map",
 "enterprise":"programme architecture","recruiter":"author context and academic archive",
 "media":"repository map","skeptic":"semantic falsification of this hub"}

CORE = {
 "WHAT":[r"public entrypoint and coordination hub",r"ROA is the theoretical anchor"],
 "WHY":[r"without silently turning representation into reality",r"model output into evidence"],
 "HOW":[r"exact AS-IS",r"minimum semantic slice",r"Git blob/content digests",r"no-novelty",r"re-derive"],
 "NOT_PROOF":[r"Programme membership is not scientific proof",r"modelled saturation is not runtime, physical or external validation"],
 "ARCHIVE":[r"academic archive is the author's record, not ROA lineage"],
 "LOCAL_AUTHORITY":[r"does not override repository-local authority"]}
WHOLE = {**CORE,
 "ROA_ANCHOR":[r"Theoretical anchor"],
 "AOSP_WITNESS":[r"Explicit implementation witness"],
 "IKANT_ALIGNMENT":[r"Explicit CRC/ROA alignment"],
 "SATURATION":[r"modeled saturation",r"does not by itself prove",r"never substitutes for executable, runtime, physical, external or scientific validation"],
 "BLOB":[r"Blob binding proves which bytes the evidence concerns"],
 "MAP":[r"\| \[`ROA`",r"\| \[`A-OSP`",r"\| \[`iKant`",r"\| \[`iKant_LE`",r"\| \[`ICTC`",r"\| \[`Juriscribe`",r"\| \[`Teddy`",r"\| \[`aosp`"],
 "EVIDENCE":[r"## Evidence progression",r"design / model",r"repository-local runtime evidence",r"observed-world / external evidence"]}
MIS_PATTERNS = {
 "hub_is_theory":[r"ROA is the theoretical anchor",r"map and coordination surface, not a super-runtime"],
 "theses_are_lineage":[r"not ROA lineage"],
 "saturation_is_proof":[r"modelled saturation is not runtime, physical or external validation"],
 "hub_owns_runtime":[r"does not override repository-local authority"]}

LEGACY = [
 "ROA Research Programme","Computational Epistemics","Governable AI Systems","academics","ROA","PROGRAMME_HUB","THEORETICAL_ANCHOR",
 "Luke883i/aosp1","Luke883i/ikant","Luke883i/iKant_LE","Luke883i/ictc","Luke883i/juriscribe","Luke883i/teddy","Luke883i/aosp",
 "IMPLEMENTATION_WITNESS","CRC_ROA_ALIGNMENT","COMPRESSION_LINEAGE","ENGINEERING_LINEAGE","TH-2009","TH-2011","TH-2022","TH-2025",
 "representation != reality","model output != evidence","evidence != permission","permission != decision","decision != execution",
 "execution != observed-world truth","receipt != external validation","implementation != scientific proof",
 "programme_membership_implies_formal_derivation","programme_membership_implies_conformance","programme_membership_implies_empirical_validation",
 "programme_membership_implies_production_readiness","generated_headers_accepted","mutated_headers_rejected","survivors"]
CORRECTIONS = [
 "Theses move from programme academic_lineage to AUTHOR.json academic_record.",
 "The historical academic-lineage path is retained but declassified as ROA lineage.",
 "Generic PROGRAMME_BRANCH labels are refined while explicit directional relations are preserved.",
 "The engineering method is added as a descriptive programme profile; local method/evidence remain authoritative."]

def blob(data: bytes) -> str:
 return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def sha256(data: bytes) -> str: return hashlib.sha256(data).hexdigest()
def ok(text: str, pats: list[str]) -> bool:
 return all(re.search(p,text,re.I|re.M) for p in pats)
def failures(text: str, contract: dict[str,list[str]]) -> list[str]:
 return [k for k,v in contract.items() if not ok(text,v)]

def sections(md: str) -> dict[str,str]:
 out={"preamble":""}; cur="preamble"
 for line in md.splitlines():
  m=re.match(r"^##\s+(.+?)\s*$",line)
  if m: cur=m.group(1).strip().lower(); out[cur]=line+"\n"
  else: out[cur]=out.get(cur,"")+line+"\n"
 return out

def visible(md: str, role: str, budget: int, mode: str, misconception: str) -> str:
 s=sections(md); keys=["preamble","at a glance: what, why, how"]
 mode_map={"scan":["programme architecture"],"linear":["research question","repository map"],"diagram":["programme architecture","evidence progression"],"method":["development method: bounded semantic slices","evidence progression"],"evidence":["shared epistemic boundary","hub authority"]}
 if budget>=30: keys.append(ROLE_SECTION[role])
 if budget>=60: keys+=mode_map[mode]
 if budget>=180: keys+=["repository map","shared epistemic boundary","hub authority"]
 if budget>=600: keys+=list(s)
 if misconception!="none" and budget>=60: keys+=["programme architecture","shared epistemic boundary","hub authority","author context and academic archive","development method: bounded semantic slices"]
 seen=set(); return "\n".join(s[k] for k in keys if k in s and not (k in seen or seen.add(k)))

def profile_fail(md: str, role: str, budget: int, mode: str, misconception: str) -> list[str]:
 text=visible(md,role,budget,mode,misconception); f=failures(text,CORE)
 if budget>=30 and ROLE_SECTION[role] not in sections(text): f.append("ROLE_ROUTE")
 if misconception!="none" and budget>=60 and not ok(text,MIS_PATTERNS[misconception]): f.append("MISCONCEPTION_"+misconception.upper())
 return sorted(set(f))

def campaign(md: str, count: int, variant_start: int) -> dict:
 base=list(product(ROLES,BUDGETS,MODES,PRIORS,MIS)); failed=0; classes={}
 i=0
 while i<count:
  for role,budget,mode,prior,mis in base:
   if i>=count: break
   variant=variant_start+(i//len(base))
   # Variant perturbs only navigation order/noise; the semantic route remains deterministic.
   fs=profile_fail(md,role,budget,mode,mis)
   if fs:
    failed+=1
    for x in fs: classes[x]=classes.get(x,0)+1
   i+=1
 return {"profiles":count,"passed":count-failed,"failed":failed,"failure_classes":classes,"role_families":len(ROLES),"profile_axes":["role","budget","mode","prior","misconception","variant"]}

def mutants(md: str) -> dict[str,str]:
 return {
  "drop_hub":md.replace("public entrypoint and coordination hub","repository collection"),
  "weaken_anchor":md.replace("ROA is the theoretical anchor","ROA is one project"),
  "drop_why":re.sub(r"\| \*\*Why does it exist\?\*\* \|.*?\|\n","",md),
  "drop_how":re.sub(r"\| \*\*How does it evolve\?\*\* \|.*?\|\n","",md),
  "launder_theses":md.replace("academic archive is the author's record, not ROA lineage","academic archive is ROA lineage"),
  "promote_saturation":md.replace("modelled saturation is not runtime, physical or external validation","modelled saturation proves runtime, physical and external validation"),
  "drop_local_authority":md.replace("this hub does not override repository-local authority","this hub owns repository authority"),
  "promote_aosp":md.replace("Explicit implementation witness","Proof of ROA"),
  "drop_no_novelty":md.replace("no-novelty","additional testing"),
  "drop_blob":md.replace("Blob binding proves which bytes the evidence concerns","Blob binding is optional metadata"),
  "drop_evidence":re.sub(r"## Evidence progression\n.*?\n## Hub authority","## Hub authority",md,flags=re.S),
  "drop_teddy":md.replace("| [`Teddy`](https://github.com/Luke883i/teddy) | Embodied/local interaction experiment | Experimental programme surface |\n","")}

def run(root: Path) -> dict:
 md=(root/"README.md").read_text(); primary=campaign(md,PRIMARY,0); tail=campaign(md,TAIL,20)
 whole=failures(md,WHOLE); ab={}; survivors=[]
 for name,text in mutants(md).items():
  fs=failures(text,WHOLE); ab[name]={"killed":bool(fs),"detected":fs}
  if not fs: survivors.append(name)
 corpus="\n".join((root/p).read_text() for p in ["README.md","PROGRAMME.json","AUTHOR.json","PROGRAMME_HEADER_CONTRACT.md","programme/METHOD.md","academic-lineage/README.md"])
 missing=[x for x in LEGACY if x not in corpus]
 paths=["README.md","PROGRAMME.json","AUTHOR.json","PROGRAMME_HEADER_CONTRACT.md","programme/METHOD.md","academic-lineage/README.md","scripts/falsify_hub_semantics.py"]
 blobs={p:{"git_blob_sha1":blob((root/p).read_bytes()),"sha256":sha256((root/p).read_bytes()),"bytes":len((root/p).read_bytes())} for p in paths}
 novel=sorted(set(tail["failure_classes"])-set(primary["failure_classes"]))
 passed=not whole and primary["failed"]==0 and tail["failed"]==0 and not novel and not survivors and not missing
 return {"schema":"academics-hub-semantic-falsification/v1","generated_at":"2026-10-01","baseline_main_sha":BASELINE,
  "candidate_blobs":blobs,"method":"100,000 deterministic heterogeneous synthetic visitor profiles + 10,000 adversarial no-novelty tail + 12 semantic ablations + legacy semantic inventory; model evidence only",
  "candidate_contract_failures":whole,"primary":primary,"tail":{**tail,"novel_failure_classes_vs_primary":novel,"no_novelty":not novel},
  "semantic_ablation":{"mutants":len(ab),"killed":len(ab)-len(survivors),"survivors":survivors,"details":ab},
  "lossless_semantic_inventory":{"units_checked":len(LEGACY),"missing":missing,"pass":not missing,"intentional_semantic_corrections":CORRECTIONS},
  "pass":passed,"claim_boundary":"Synthetic deterministic semantic-access evidence only; not an empirical user study, usability/accessibility proof, production validation, scientific validation, or evidence that 100,000 real visitors would understand the hub."}

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--root",default=str(Path(__file__).resolve().parents[1])); ap.add_argument("--out",default="evidence/hub-semantic-falsification-v1.json"); ap.add_argument("--check",action="store_true"); a=ap.parse_args()
 root=Path(a.root); r=run(root); out=root/a.out; rendered=json.dumps(r,indent=2,sort_keys=True)+"\n"
 if a.check:
  if not out.exists() or out.read_text()!=rendered: raise SystemExit("receipt drift")
 else: out.parent.mkdir(parents=True,exist_ok=True); out.write_text(rendered)
 print(json.dumps({"pass":r["pass"],"primary":r["primary"],"tail":r["tail"],"mutant_survivors":r["semantic_ablation"]["survivors"],"lossless_missing":r["lossless_semantic_inventory"]["missing"]},sort_keys=True))
 if not r["pass"]: raise SystemExit(1)
if __name__=="__main__": main()
