#!/usr/bin/env python3
"""Check the review dossier, not OpenERP or Swedish accounting compliance."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
results=[]
def check(name,condition,detail=''):
    results.append({'name':name,'passed':bool(condition),'detail':detail})

reg=json.loads((ROOT/'parity-register.json').read_text())
rows=reg['findings']; ids={x['id'] for x in rows}
check('85 unique original finding identities', len(rows)==85 and ids=={f'PRY-{i:02d}' for i in range(1,86)})
check('Original and revised prerequisite fields remain distinct',all('original_prerequisites' in x and 'proposed_implementation_dependencies' in x for x in rows))
check('Every finding has a canonical owner and scope',all(x['canonical_core_owners'] and x['revised_scope'] for x in rows))
check('Missing reference pin is not fabricated',all(x['reference_evidence']['commit'] is None and x['reference_evidence']['status'].startswith('missing') for x in rows))
check('Every finding status stays unverified',all(x['implementation_status']=='not determined by this plan review' for x in rows))
check('All proposed supplemental dependencies exist',all(d in ids for x in rows for d in x['proposed_implementation_dependencies']))
order=reg['proposed_supplemental_order'];pos={n:i for i,n in enumerate(order)}
check('Supplemental graph is acyclic',len(pos)==85 and all(pos[d]<pos[x['id']] for x in rows for d in x['proposed_implementation_dependencies']))
check('No claim of checking full 53-core release graph',reg['full_core_plus_release_graph_verified'] is False)
reviewedRules=json.loads((ROOT/'rule-review.json').read_text())
check('25 unique rule IDs',len(reviewedRules)==25 and {x['id'] for x in reviewedRules}=={f'R{i}' for i in range(1,26)})
ruleText=(ROOT/'RULE-CORRECTIONS.md').read_text()
check('All 25 rule headings exist once',all(len(re.findall(r'^## R'+str(i)+r':',ruleText,re.M))==1 for i in range(1,26)))
plan=(ROOT/'11-parity-backlog.REVISED.md').read_text()
check('All 85 revised table rows exist once',all(len(re.findall(r'^\| PRY-'+f'{i:02d}'+r' \|',plan,re.M))==1 for i in range(1,86)))
sourceIds=set(json.loads((ROOT/'source-manifest.json').read_text())['repository_sources'])
check('Finding source references resolve',all(x['plan_source_ref'] in sourceIds for x in rows))
missing=[];unpaired=[]
for p in ROOT.rglob('*.md'):
    t=p.read_text()
    if len(re.findall(r'^```',t,re.M))%2:unpaired.append(str(p))
    for link in re.findall(r'\]\(([^)]+)\)',t):
        if link.startswith(('http:','https:','#','mailto:')):continue
        target=(p.parent/link.split('#')[0]).resolve()
        if not target.exists() and target not in {ROOT/'CHECKS.md',ROOT/'checks/results.json'}:missing.append((str(p),link))
check('Markdown code fences paired',not unpaired,repr(unpaired))
check('Local document links resolve',not missing,repr(missing))

# Counterexamples to written planning recipes. These do not run repo code.
# Exact cover: choose all minimal-cardinality sets, retaining resource identities.
def covers(target,items,maxsize):
    for n in range(1,maxsize+1):
        matches=[tuple(k for k,v in c) for c in combinations(items,n) if sum(v for k,v in c)==target]
        if matches:return matches
    return []
check('R6 equal covers are ambiguous',len(covers(100,[('a',70),('b',30),('c',60),('d',40)],4))==2)
check('R6 truncation can hide a solution',not covers(100,[('a',80)],2) and len(covers(100,[('a',80),('b',70),('c',30)],2))==1)

def guard(result,explicit=False):
    if result=='unavailable':return 'blocked'
    if result=='incomplete':return 'incomplete'
    if result=='no_conflict':return 'continue_other_checks'
    return 'requires_exact_authorized_resolution'
check('R11 unavailable does not pass with or without override',guard('unavailable')=='blocked' and guard('unavailable',True)=='blocked')
check('R11 incomplete is not no conflict',guard('incomplete')!='continue_other_checks')
# Three source rows make the statement balance. Hiding one changes truth, not reconciliation.
opening=1000; actual=[100,-200,50];externalClosing=950
check('PRY35 full source reconciles',opening+sum(actual)==externalClosing)
check('PRY35 suppressing a genuine row cannot retain reconciled total',opening+sum([100,-200])!=externalClosing)
# A skipped balanced voucher may not create a trial-balance difference at all.
skipped={'expense':100,'bank':-100}
check('PRY25 balanced skipped entry can conceal missing economics',sum(skipped.values())==0 and skipped['expense']!=0)
# Written R2 selector cannot pair every digit with a weight for an 11-digit input.
weights=[1,10,9,8,7,6,5,4,3,2,1];length=11; selected=weights[-(11-length+1):]
check('R2 written weight selector has insufficient weights',len(selected)!=length)
# Same currency, different scales.
check('R10 same raw integer does not ensure same value',Fraction(100,100)!=Fraction(100,1))
check('R10 absolute equality hides direction',abs(-100)==abs(100) and -100!=100)
# Sick-day mechanical illustration, explicitly not a statutory profile.
normalLost=1000;sickEntitlement=800;remainingDeduction=800
supportedSimple=normalLost-(sickEntitlement-min(sickEntitlement,remainingDeduction))
writtenFirstDay=normalLost-0+remainingDeduction
check('R9 first-day removal plus deduction overstates illustrative loss',supportedSimple==1000 and writtenFirstDay==1800)
# Peppol example assumes the input amounts themselves have been qualified.
lineNet=10000;docAllowance=1000;docCharge=500;vat=2375;prepaid=2000;rounding=0
exclusive=lineNet-docAllowance+docCharge;inclusive=exclusive+vat;due=inclusive-prepaid+rounding
check('R21 complete document graph',exclusive==9500 and inclusive==11875 and due==9875)
check('R21 simple tax/prepaid counterexample',100+25-20==105 and 100!=105)
# Cash-method disjoint paid/year-end recognition.
check('R23 VAT recognized once across payment/year-end/later settlement',10+15+0==25)
check('R23 net coverage conserved',40+60==100)
check('R16 consideration not double-reduced',1000-300+300==1000 and (1000-300)-300!=1000-300)
check('R19 stated fiscal duration conflicts with fixed12',Fraction(18,12)!=1 and Fraction(18,18)==1)
# Zero net is not zero salary accounting.
journal=[1000,-1000];net=0
check('R24 zero net still has balanced nonzero effects',net==0 and sum(journal)==0 and any(journal))
# Rate eligibility cannot differ between live and cache.
observations=[{'date':6,'value':111},{'date':4,'value':109}]
eligible=[o for o in observations if o['date']<=6 and 6-o['date']<=2]
check('R7 latest eligible is not assumed last provider element',max(eligible,key=lambda o:o['date'])['date']==6 and observations[-1]['date']==4)
check('R7 overage cached observation ineligible',not (6-1<=2))
# Receipt identity includes the exact revision rather than only a period.
old=('entity','period','revision1','attempt1');new=('entity','period','revision2','attempt2')
check('R20 amendment status cannot reuse original receipt identity',old!=new)
check('R25 unreadable and absent are distinct',{'state':'unreadable'}!={'state':'not_present'})
passed=sum(r['passed'] for r in results)
report={'scope':'generated dossier structure and independent illustrative counterexamples',
 'application_or_repo_tests_run':False,'repo_check_plan_run':False,'full_upstream_reference_audit':False,
 'full_statutory_profile_qualified':False,'full_core_release_graph_verified':False,
 'total':len(results),'passed':passed,'failed':len(results)-passed,'checks':results}
(ROOT/'checks/results.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'CHECKS.md').write_text(f'''# Checks actually performed\n\nRan the local design checker against this generated package: **{passed}/{len(results)} named checks passed**. It checks stable identifiers, the proposed 85-row supplemental DAG, references, Markdown structure and explicitly illustrative counterexamples to the written recipes.\n\nIt does not run OpenERP, PostgreSQL, workerd, providers or the repository's `check-plan.py`. It does not reproduce the upstream comparison or qualify a current statutory profile. The original 53-packet graph plus all release gates was not independently reconstructed; this is recorded rather than claimed as passed.\n\nReproduce with `python checks/check_review.py`. Exact results are in [checks/results.json](checks/results.json). The checker is local to this artifact and was not added to the application repository.\n''')
print(json.dumps({k:report[k] for k in ['total','passed','failed']},indent=2))
if passed!=len(results):
    print(json.dumps([r for r in results if not r['passed']],indent=2));raise SystemExit(1)
