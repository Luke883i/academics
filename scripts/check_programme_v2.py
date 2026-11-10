#!/usr/bin/env python3
"""Programme v2 public navigation and epistemic boundary contract; source-level only."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PUBLIC=("academics","ROA","cora","ictc","juriscribe","iKant_EDU","lumen","teddy","NILO")
MARKER="<!-- programme-header:v2 -->"
def assess(md,registry):
    faults=[]
    if not md.startswith(MARKER) or md.count(MARKER)!=1: faults.append("header")
    h=md[:800]
    for name in ("academics","ROA","cora"):
        if "https://github.com/Luke883i/"+name not in h: faults.append("header-link:"+name)
    for name in PUBLIC:
        if "https://github.com/Luke883i/"+name not in md: faults.append("public-route:"+name)
    for phrase in ("Every repository is independently readable","Membership does not imply formal derivation","Repository-local code, evidence, and governance remain authoritative"):
        if phrase not in h: faults.append("boundary:"+phrase)
    rows=[x for x in registry["repositories"] if x["repo"].split("/")[-1] in PUBLIC]
    if len(rows)!=9 or {x["repo"].split("/")[-1] for x in rows}!=set(PUBLIC): faults.append("registry-public-topology")
    if registry["governance"]["membership_header"]["marker"]!="programme-header:v2": faults.append("registry-header-version")
    if "Closed and unmaintained" not in md and "Closed, unmaintained" not in md and "Closed and unmaintained" not in md: faults.append("archival-disclosure")
    return sorted(faults)
def main():
    md=(ROOT/"README.md").read_text()
    registry=json.loads((ROOT/"PROGRAMME.json").read_text())
    positive=assess(md,registry)
    assert not positive,positive
    mutants={}
    mutants["duplicate_header"]=md.replace(MARKER,MARKER+MARKER,1)
    mutants["remove_header"]=md.replace(MARKER,"",1)
    mutants["launder_membership"]=md.replace("Membership does not imply formal derivation","Membership proves formal derivation",1)
    mutants["launder_authority"]=md.replace("Repository-local code, evidence, and governance remain authoritative","Programme owns all code and releases",1)
    mutants["remove_archive"]=md.replace("Closed and unmaintained","Historical",1)
    for name in PUBLIC:
        mutants["drop_route_"+name]=md.replace("https://github.com/Luke883i/"+name,"https://example.invalid/"+name)
    for name in ("academics","ROA","cora"):
        mutants["drop_header_link_"+name]=md.replace("https://github.com/Luke883i/"+name,"https://example.invalid/"+name,1)
    passed={k:bool(assess(v,registry)) for k,v in mutants.items()}
    assert all(passed.values()),[k for k,v in passed.items() if not v]
    print(json.dumps({"status":"PASS_SCOPED_SOURCE","public_routes":9,"mutants":len(mutants),"killed":sum(passed.values()),"unverified":"runtime, external user, scientific, CV credentials","original_historical_receipt":"separate baseline"}))
if __name__=="__main__": main()
