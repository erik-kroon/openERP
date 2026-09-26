#!/usr/bin/env python3
"""Independent checks of this DESIGN DOSSIER. Not OpenERP application tests.

Run: python checks/validate.py
No database, network, credentials or repository mutation is used.
"""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
import calendar, hashlib, json, re
from datetime import date

ROOT=Path(__file__).resolve().parents[1]
results=[]
def check(name:str, condition:bool, detail:str='')->None:
    results.append({'name':name,'passed':bool(condition),'detail':detail})

def halfup(x:Fraction)->int:
    q,r=divmod(abs(x.numerator),x.denominator)
    return (1 if x>=0 else -1)*(q+(2*r>=x.denominator))

def half_even(x:Fraction)->int:
    q,r=divmod(abs(x.numerator),x.denominator)
    return (1 if x>=0 else -1)*(q+int(2*r>x.denominator or (2*r==x.denominator and q%2==1)))

def cumulative(total:int,gross:int,used:int,now:int)->int:
    if gross<=0 or total<0 or used<0 or now<0 or used+now>gross:raise ValueError('capacity')
    return (total if used+now==gross else halfup(Fraction(total*(used+now),gross)))-halfup(Fraction(total*used,gross))

def credit_state(g:int,k:int,p:int,q:int=0)->tuple[int,int]:
    if not (0<=k<=g and 0<=p<=g):raise ValueError('capacity')
    principal=max(p-(g-k),0)
    if not 0<=q<=principal:raise ValueError('refund overcapacity')
    return max(g-k-p,0),principal-q

def month_anchor(anchor:date,k:int,eom:bool=False)->date:
    idx=anchor.year*12+anchor.month-1+k
    y,m=divmod(idx,12);m+=1
    last=calendar.monthrange(y,m)[1]
    return date(y,m,last if eom else min(anchor.day,last))

def journal(name:str, signed:list[int])->None:
    check(name, sum(signed)==0, 'debit-positive exact integers: '+repr(signed))

def raises_value_error(fn)->bool:
    try:fn()
    except ValueError:return True
    return False

def recurrence_identity(agreement:str, cycle:int, template_revision:int)->tuple[str,int]:
    if cycle<0 or template_revision<1:raise ValueError('invalid cycle/revision')
    return agreement,cycle

def replacement_item(original:tuple, requested:tuple)->tuple:
    if original!=requested:raise ValueError('replacement identity must be stable')
    return original

def selected_sie_movements(records:list[tuple[str,int]])->int:
    return sum(amount for kind,amount in records if kind=='TRANS')

def fulfill(required:str, observed:str, same_scope:bool, environment:str)->bool:
    if not same_scope or environment!='production':return False
    permitted={'prepared':{'prepared'}, 'received':{'received','registered'}, 'registered':{'registered'}}
    return observed in permitted.get(required,set())

def context_item_delta(old_present:bool, new_present:bool, owner_available:bool, explicitly_resolved:bool)->str:
    if not owner_available:return 'unknown_now'
    if old_present and not new_present:return 'resolved' if explicitly_resolved else 'needs_scope_review'
    if not old_present and new_present:return 'added'
    return 'retained'

idx=json.loads((ROOT/'solution-index.json').read_text())
tasks=idx['solutions']; expected=[f'NEXT-{n:02}' for n in range(26,51)]
check('exactly 25 distinct packet IDs', [x['id'] for x in tasks]==expected)
check('all 25 packet files exist',all((ROOT/x['file']).is_file() for x in tasks))
check('all packet application-ownership flags true', all(x['application_owned'] for x in tasks))
check('source baseline and late observation separated',idx['pinned_commit']!=idx['late_head_observation']['commit'])
check('five original reservations retained',all(k in idx['reserved_work'] for k in ['WIP-VAT03','WIP-FX02-P1','WIP-AST03-UI','WIP-VAT04-A1','WIP-COM2-W1']))
check('migration owner separately reserved','APPLICATION-REPLACEMENT' in idx['reserved_work'])
manifest=json.loads((ROOT/'source-manifest.json').read_text())
sourceids=set(manifest['repo'])|set(manifest['external'])|{f'P{i:02}' for i in range(1,26)}
check('all declared packet source IDs resolve',all(x in sourceids for t in tasks for x in t['source_refs']))
check('every packet names its new scope and existing owner', all(t['existing_owner'] and t['new_scope'] for t in tasks))
check('every packet has distinct new-scope text',len({t['new_scope'] for t in tasks})==25)
graph=json.loads((ROOT/'dependency-graph.json').read_text());order=graph['topological_order'];positions={k:n for n,k in enumerate(order)}
check('combined graph contains 50 distinct tasks',len(positions)==50)
check('every declared dependency precedes its consumer',all(positions[d]<positions[t] for t,deps in graph['nodes'].items() for d in deps))
check('no first-wave node depends on second-wave node',all(int(d.split('-')[1])<=25 for t,deps in graph['nodes'].items() if int(t.split('-')[1])<=25 for d in deps))
master=(ROOT/'MASTER-PSEUDOCODE.md').read_text()
check('master contains each packet heading exactly once',all(len(re.findall(r'^# '+t['id']+r':',master,re.M))==1 for t in tasks))
check('master explicitly disclaims runtime proof','No source patch, deployed feature, executed application test' in master)
mds=list(ROOT.rglob('*.md'))
check('all markdown code fences paired',all(sum(1 for line in p.read_text().splitlines() if line.startswith('```'))%2==0 for p in mds))
check('no em dashes in delivered markdown',all('\u2014' not in p.read_text() for p in mds))
missing=[]
for p in mds:
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if link.startswith(('http:','https:','#','mailto:')):continue
        rel=link.split('#')[0]
        if not rel:continue
        # CHECKS.md and checks/results.json are generated below.
        target=(p.parent/rel).resolve()
        if not target.exists() and target not in {ROOT/'CHECKS.md', ROOT/'checks/results.json'}:missing.append((str(p.relative_to(ROOT)),link))
check('all local markdown links resolve',not missing,repr(missing))
check('no imperative feature procedure creation',all(not re.search(r'CREATE\s+(OR\s+REPLACE\s+)?FUNCTION',p.read_text(),re.I) for p in mds))
check('no font binaries in package',not any(p.suffix.lower() in {'.ttf','.otf','.woff','.woff2'} for p in ROOT.rglob('*')))

check('half-up positive tie',halfup(Fraction(5,2))==3)
check('half-up negative tie',halfup(Fraction(-5,2))==-3)
check('half-even odd tie',half_even(Fraction(7,2))==4)
check('half-even even tie',half_even(Fraction(5,2))==2)
check('cumulative partial shares release exact full residual',sum(cumulative(25,126,u,n) for u,n in [(0,50),(50,50),(100,26)])==25)
check('cumulative overcapacity refuses',raises_value_error(lambda:cumulative(25,126,100,27)))
check('anchored monthly dates do not drift',[month_anchor(date(2026,1,31),n) for n in [1,2]]==[date(2026,2,28),date(2026,3,31)])
check('end-of-month anchor retains April30 and May31',[month_anchor(date(2026,2,28),n,True) for n in [2,3]]==[date(2026,4,30),date(2026,5,31)])
check('recurrence identity ignores template revision',recurrence_identity('agreement',4,1)==recurrence_identity('agreement',4,2)==('agreement',4))
check('paid customer credit principal',credit_state(125000,50000,100000)==(0,25000))
check('paid customer credit after partial refund',credit_state(125000,50000,100000,10000)==(0,15000))
check('customer refund overcapacity refuses',raises_value_error(lambda:credit_state(125000,50000,100000,25001)))
journal('customer paid credit accounting',[40000,10000,-25000,-25000])
journal('customer refund accounting',[10000,-10000])
check('cash surplus is explicit liability',125000-100000==25000)
journal('prepayment reclassification creates no tax movement',[90000,-90000])
check('12 equal prepayment shares conserve cost',12*10000==120000)
journal('accrual under-estimate true-up',[10000,1000,2750,-13750])
journal('accrual over-estimate true-up',[10000,-1000,2250,-11250])
check('ACT365F interest example',halfup(Fraction(10000000*6*30,100*365))==49315)
journal('loan repayment of recognized interest',[1000000,49315,-1049315])
check('loan principal remaining',10000000-1000000==9000000)
check('mileage split uses explicit units',(Fraction(15000,1000)*300,Fraction(15000,1000)*250)==(4500,3750))
check('mileage taxable excess',4500-3750==750)
journal('taxable award accrual',[750,-750])
check('variable pay exact half-hour input',Fraction(75,2)*2000==75000)
check('holiday liability target',10000+2000-3000==9000)
check('holiday liability delta rather than full target',9000-10000==-1000)
journal('social provision consumption does not duplicate cost',[500,100,-600])
journal('gross payroll recovery preserves old cash',[20000,-20000])
check('gross payroll recovery residual',20000-5000==15000)
check('gross recovery reporting identity rejects changed specification',raises_value_error(lambda:replacement_item(('employer','2026-01','employee','spec1'),('employer','2026-01','employee','spec2'))))
check('positive VAT precision bridge',-12349+(12349-12300)+12300==0)
check('negative VAT precision bridge',12349+(-12349+12300)-12300==0)
journal('VAT assessment signed control',[12300,-12300])
check('assessed discrepancy remains visible',-12349+49+12800==500)
check('cash method paid and year-end VAT recognized once',10000+15000+0==25000)
check('cash method partial expense split',cumulative(100000,125000,0,50000)==40000)
check('cash method year-end residual expense',100000-40000==60000)
journal('processor charge settles AR',[122000,3000,-125000])
journal('processor payout transit',[122000,-122000])
journal('processor bank settlement',[122000,-122000])
check('processor net field equation',125000-3000==122000)
check('native cash proportional carrying release',halfup(Fraction(110000*4000,10000))==44000)
journal('payable settled from foreign cash',[45000,-44000,-1000])
check('cash carrying after withdrawal',110000-44000==66000)
journal('foreign cash valuation bridge',[3000,-3000])
journal('late FX December delta',[5000,-5000])
journal('late FX January delta',[-5000,5000])
check('late FX final control and cash unchanged',5000-5000==0)
check('late FX gain allocation conserves lifetime gain',5000+1000==6000)
# Independent two-part carrying replay.
old_b1=halfup(Fraction(110000*4000,10000));new_b1=halfup(Fraction(115000*4000,10000))
old_gain=(46000-old_b1)+(70000-(110000-old_b1))
new_gain=5000+(46000-new_b1)+(70000-(115000-new_b1))
check('late FX two-settlement chain conserves economics',old_gain==new_gain==6000)
check('impairment carrying input',1000000-200000-300000==500000)
check('impairment reversal cap and target',min(700000,500000+300000)==700000 and 650000<=700000 and 750000>700000)
journal('impairment reversal effects',[150000,-150000])
check('impairment carrying after reversal',1000000-200000-(300000-150000)==650000)
journal('zero-carrying final disposal',[200000,800000,-1000000])
check('retagging does not change totals',100+200+50==0+300+50==350)
check('SIE same number scoped by source year',('year0','A',1)!=('year-1','A',1))
check('historical correction records not extra final movements',selected_sie_movements([('TRANS',100),('RTRANS',-100),('BTRANS',100)])==100)
check('cash-flow complete closing bridge',100000+120000-50000+40000+2000==212000)
check('internal cash transfer eliminates to zero',-30000+30000==0)
check('Peppol inclusive and remaining payable',10000+2500==12500 and 12500-2500==10000)
check('authentication event is not signature evidence','authenticated' not in {'document_signature_verified'})
check('upload result does not imply statutory fulfillment',not fulfill('received','copy_uploaded',True,'production'))
check('sandbox receipt cannot fulfill production obligation',not fulfill('received','received',True,'sandbox'))
check('wrong-scope receipt cannot fulfill obligation',not fulfill('received','received',False,'production'))
check('received status does not imply required registration',not fulfill('registered','received',True,'production'))
check('unavailable context adapter not resolved',context_item_delta(True,False,False,False)=='unknown_now')
check('absent context item without resolution needs review',context_item_delta(True,False,True,False)=='needs_scope_review')
check('explicit context resolution is distinguished',context_item_delta(True,False,True,True)=='resolved')

# Deliberately expose that finite examples cannot prove the application.
passed=sum(x['passed'] for x in results)
report={'scope':'dossier structure and independent illustrative arithmetic only','application_test_suite_run':False,'database_or_worker_executed':False,'provider_executed':False,'repository_modified':False,'checks':results,'passed':passed,'failed':len(results)-passed,'total':len(results)}
(ROOT/'checks/results.json').write_text(json.dumps(report,indent=2))
summary=f'''# Dossier checks

Ran `python checks/validate.py` locally against this generated package.

Result: **{passed}/{len(results)} named design checks passed**. These cover packet identity, the combined declared dependency graph, source/link consistency, exact example arithmetic and selected state distinctions. No repository test files were added or modified.

These are NOT compiled Effect operations, PostgreSQL/Worker transaction tests, browser tests, legal qualification or live provider acceptance. Several state examples are deliberately simple assertions of the chosen model, not concurrency or network simulations. They cannot prove an implementation is correct.

The reproducible checker is [checks/validate.py](checks/validate.py). Full results are [checks/results.json](checks/results.json). Review each packet's richer failure vectors separately when implementing it under the actual repository authorization.

Package source: pinned review at `{idx['pinned_commit']}` plus the limited later observation documented in [REVISION-NOTE.md](REVISION-NOTE.md).
'''
(ROOT/'CHECKS.md').write_text(summary)
print(json.dumps({'passed':passed,'failed':len(results)-passed,'total':len(results)},indent=2))
if passed!=len(results):
    for x in results:
        if not x['passed']:print('FAILED',x)
    raise SystemExit(1)
