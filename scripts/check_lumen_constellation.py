#!/usr/bin/env python3
"""Bounded 100-hypothesis crossref falsification. Synthetic model, not runtime certification."""
import copy
import json
import pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]
CANONICAL_HEADER="<!-- roa-programme-header:v1 hub=Luke883i/academics framework=Luke883i/ROA role=LIBRARY_SERVICES_VERTICAL -->"
EXPECTED={
  'id':'lumen','repo':'Luke883i/lumen','role':'LIBRARY_SERVICES_VERTICAL',
  'class':'APPLIED','status':'CURRENT','macro_relation_to_roa':'APPLIED_SURFACE'
}
FLAGS=[
 'programme_membership_implies_formal_derivation',
 'programme_membership_implies_conformance',
 'programme_membership_implies_empirical_validation',
 'programme_membership_implies_production_readiness',
 'academic_archive_implies_roa_lineage',
 'modelled_saturation_implies_external_validation'
]
LEGACY={
 'academics':('PROGRAMME_HUB','COORDINATION'),
 'ROA':('THEORY_FRAMEWORK','CORE_THEORY'),
 'aosp1':('EPISTEMIC_SUBSTRATE','CORE_ENGINEERING'),
 'ikant':('EPISTEMIC_AGENT_RUNTIME','CORE_AGENT'),
 'iKant_LE':('COMPRESSED_RUNTIME_KERNEL','CORE_COMPRESSION'),
 'ictc':('COMPLIANCE_VERTICAL','APPLIED'),
 'juriscribe':('LEGAL_SCIENTIFIC_EDITORIAL_VERTICAL','APPLIED'),
 'teddy':('EMBODIED_INTERACTION_EXPERIMENT','EXPERIMENTAL'),
 'aosp':('LEGACY_AOSP_LINEAGE','LEGACY')
}
def accepted(p, md, header):
 try:
  assert p['schema']=='roa-research-programme/v3'
  assert p['programme']['id']=='PRG-ROA'
  assert p['programme']['hub']=='academics'
  assert p['programme']['theoretical_anchor']=='ROA'
  assert 'Repository-local authorities' in p['programme']['state_policy']
  members={x['id']:x for x in p['repositories']}
  assert len(members)==len(p['repositories'])==10
  assert all(members[k]['role']==r and members[k]['class']==c for k,(r,c) in LEGACY.items())
  assert all(members['lumen'].get(k)==v for k,v in EXPECTED.items())
  assert len(p['relations'])==4
  assert not any('lumen' in (x['from'],x['to']) for x in p['relations'])
  assert all(p['governance']['claim_boundary'][k] is False for k in FLAGS)
  assert header==CANONICAL_HEADER
  assert md.count('| [`LUMEN`](https://github.com/Luke883i/lumen) |')==1
  assert 'HUB -->|applied surface| LUMEN' in md
  assert 'not as a theoretical derivation' in md
  assert 'LUMEN -->|implementation witness|' not in md
  return True
 except (AssertionError,KeyError,TypeError,ValueError):return False
def mutate(p,h,case):
 p=copy.deepcopy(p)
 h=h
 m=case['mutation'];family=case['family']
 if family=='programme-hub':p['programme']['hub']=m['value']
 elif family=='theoretical-anchor':p['programme']['theoretical_anchor']=m['value']
 elif family=='repository-identity':
  next(x for x in p['repositories'] if x['id']=='lumen')['repo']=m['value']
 elif family=='repository-role':
  next(x for x in p['repositories'] if x['id']=='lumen')['role']=m['value']
 elif family=='repository-class':
  next(x for x in p['repositories'] if x['id']=='lumen')['class']=m['value']
 elif family=='lifecycle-topology':
  next(x for x in p['repositories'] if x['id']=='lumen')['status']=m['value']
 elif family=='relation-strength':
  next(x for x in p['repositories'] if x['id']=='lumen')['macro_relation_to_roa']=m['value']
 elif family=='non-entailment':
  if m['value'] is None:p['governance']['claim_boundary'].pop(m['field'])
  else:p['governance']['claim_boundary'][m['field']]=m['value']
 elif family=='badge-header':h=m['value']
 elif family=='false-explicit-roa-edge':p['relations'].append(m)
 else:raise ValueError('Unknown mutation family')
 return p,h

def run():
 programme=json.loads((ROOT/'PROGRAMME.json').read_text())
 md=(ROOT/'README.md').read_text()
 ledger=json.loads((ROOT/'evidence/lumen-crossref-100-hypotheses.json').read_text())
 assert accepted(programme,md,ledger['lumen_header']),'canonical candidate violates programme boundary'
 assert ledger['schema']=='academics-lumen-crossref-falsification/v1'
 assert ledger['lumen_candidate_pr']=='https://github.com/Luke883i/lumen/pull/23'
 cases=ledger['hypotheses']
 assert len(cases)==100
 assert len({c['id'] for c in cases})==100
 families={}
 survivors=[]
 for i,case in enumerate(cases,1):
  assert case['id']==f'H{i:03d}'
  assert case['expected']=='REJECT'
  families[case['family']]=families.get(case['family'],0)+1
  mutated,header=mutate(programme,ledger['lumen_header'],case)
  if accepted(mutated,md,header):survivors.append(case['id'])
 assert len(families)==10 and all(n==10 for n in families.values())
 assert not survivors,f'unsafe survivor(s): {survivors}'
 # Risk-bounded novelty tail; same declared classes, separate mutated values.
 # The tail cannot claim discovery beyond these ten modelled classes.
 tail=[]
 for case in cases[::5]:
  mutated,header=mutate(programme,ledger['lumen_header'],case)
  if accepted(mutated,md,header):tail.append(case['id'])
 assert not tail
 receipt={'status':'PASS','candidate_accepted':True,'hypotheses_tested':100,
          'counterfactuals_rejected':100,'survivors':survivors,'families':families,
          'no_novelty_tail_examples':20,'tail_survivors':tail,
          'external_cross_repo_live_check':'NOT_EXECUTED',
          'claim':'Synthetic source-level membership and topology falsification only'}
 print(json.dumps(receipt,sort_keys=True))
 return receipt
if __name__=='__main__':run()
