#!/usr/bin/env python3
"""Validate this design dossier and independent synthetic model examples.

This script never imports OpenERP, connects to SQL, calls providers or mutates a
repository. Passing examples do not prove application transaction behavior, real
concurrency, legal applicability or provider acceptance.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(group, name, condition, detail=''):
    checks.append({'group':group,'name':name,'passed':bool(condition),'detail':detail})
def eq(group, name, actual, expected):
    check(group,name,actual==expected,repr(actual)+' == '+repr(expected))
def journal(name, amounts):
    eq('arithmetic',name,sum(amounts),0)
def reject(fn):
    try:fn()
    except (ValueError,PermissionError):return True
    return False

def round_ratio(n:int,d:int,mode:str='half_up')->int:
    if d<=0:raise ValueError('denominator')
    q,r=divmod(abs(n),d);sign=-1 if n<0 else 1
    if mode=='exact':
        if r:raise ValueError('nonexact')
        add=0
    elif mode=='toward_zero':add=0
    elif mode=='floor':add=int(n<0 and r>0)
    elif mode=='half_up':add=int(2*r>=d)
    elif mode=='half_even':add=int(2*r>d or (2*r==d and q%2==1))
    else:raise ValueError('mode')
    return sign*(q+add)

def allocate(total:int,weights:dict[str,int])->dict[str,int]:
    if total<0 or not weights or any(v<0 for v in weights.values()) or sum(weights.values())<=0:
        raise ValueError('weights/total')
    W=sum(weights.values());parts={k:total*v//W for k,v in weights.items()}
    rem={k:total*v%W for k,v in weights.items()}
    left=total-sum(parts.values())
    for key in sorted(weights,key=lambda k:(-rem[k],k.encode('utf-8')))[:left]:parts[key]+=1
    return parts

def cumulative(component:int,total:int,used:int,next_:int)->int:
    if component<0 or total<=0 or not 0<=used<=total or not 0<=next_<=total-used:
        raise ValueError('coverage')
    after=component if used+next_==total else round_ratio(component*(used+next_),total)
    return after-round_ratio(component*used,total)

@dataclass
class MandateModel:
    limit:int
    used:int
    receipts:dict=field(default_factory=dict)
    effects:set=field(default_factory=set)
    def execute(self,key,event,amount,*,has_access=True,active=True,crash=False):
        if not has_access:raise PermissionError('access')
        payload=(event,amount)
        if key in self.receipts:
            if self.receipts[key]!=payload:raise ValueError('conflict')
            return self.receipts[key]
        if not active:raise ValueError('expired/revoked')
        if event in self.effects:raise ValueError('already applied')
        if amount<=0 or self.used+amount>self.limit:raise ValueError('limit')
        candidate_used=self.used+amount
        candidate_effects=self.effects|{event}
        candidate_receipts={**self.receipts,key:payload}
        if crash:raise ValueError('simulated rollback before model commit')
        self.used=candidate_used;self.effects=candidate_effects;self.receipts=candidate_receipts
        return payload

@dataclass
class RefundModel:
    liability:int
    reserved:int=0
    transit:int=0
    processor_delta:int=0
    discharged:int=0
    debit_ids:set=field(default_factory=set)
    def reserve(self,amount):
        if amount<=0 or amount>self.liability-self.reserved:raise ValueError('capacity')
        self.reserved+=amount
    def processor_debit(self,identity,amount):
        if identity in self.debit_ids:return
        if amount<=0 or amount>self.reserved-self.transit:raise ValueError('debit')
        self.processor_delta-=amount;self.transit+=amount;self.debit_ids.add(identity)
    def complete(self,amount):
        if amount<=0 or amount>min(self.transit,self.reserved,self.liability):raise ValueError('discharge')
        self.liability-=amount;self.reserved-=amount;self.transit-=amount;self.discharged+=amount
    def return_before_completion(self,amount,*,final_no_execution):
        if amount<=0 or amount>self.transit:raise ValueError('return')
        self.processor_delta+=amount;self.transit-=amount
        if final_no_execution:self.reserved-=amount
    def reverse_completed(self,amount):
        if amount<=0 or amount>self.discharged:raise ValueError('reversal')
        self.processor_delta+=amount;self.liability+=amount;self.discharged-=amount

def search_finite(opening:int,base_path:list[int],options:list[list[tuple]],floor:int,limit:int):
    """Enumerate one small declared payment model, not a production optimizer."""
    best=None;visited=0;exhausted=False
    for selection in product(*options):
        if visited>=limit:exhausted=True;break
        visited+=1
        balance=opening;path=[]
        for day,base in enumerate(base_path):
            balance+=base
            balance-=sum(amount for due,amount,score in selection if due==day)
            path.append(balance)
        if all(x>=floor for x in path):
            score=sum(s for due,a,s in selection)
            if best is None or score>best['score']:
                best={'score':score,'selection':selection,'path':path}
    status=('feasible_bounded' if best else 'exhausted_no_candidate') if exhausted else ('optimal_within_model' if best else 'infeasible_within_model')
    return status,best,visited

def provider_unique(records,proven_aliases):
    values={}
    for identity,amount in records:
        canonical=proven_aliases.get(identity,identity)
        if canonical in values and values[canonical]!=amount:raise ValueError('conflicting source facts')
        values[canonical]=amount
    return values

# Structural and non-overlap declarations.
idx=json.loads((ROOT/'solution-index.json').read_text())
tasks=idx['solutions'];expected={f'NEXT-{i}' for i in range(101,126)}
check('structure','exactly 25 unique IDs',len(tasks)==25 and {t['id'] for t in tasks}==expected)
check('structure','source checkpoint has 40 hex digits',bool(re.fullmatch('[0-9a-f]{40}',idx['baseline'])))
check('structure','earlier completion not claimed',idx['prior_status']=='not assumed complete')
check('structure','only new graph completeness asserted','no full125-node' in idx['graph_scope'] or 'no full125' in idx['graph_scope'] or 'no full125-node' in idx.get('graph_scope','').replace(' ',''))
check('structure','all five historical reservations remain',len(idx['reserved_work'])>=5)
source=json.loads((ROOT/'source-manifest.json').read_text())
# Collect the explicit R/X keys regardless of manifest grouping representation.
def keys(o):
    out=set()
    if isinstance(o,dict):
        for k,v in o.items():
            if re.fullmatch('[RX]\\d{2}',k):out.add(k)
            out|=keys(v)
    elif isinstance(o,list):
        for v in o:out|=keys(v)
    return out
source_ids=keys(source)|{f'P{i:02}' for i in range(1,101)}
for t in tasks:
    p=ROOT/t['file'];text=p.read_text()
    check('structure',t['id']+' file and correct heading',p.is_file() and text.startswith('# '+t['id']+':'))
    check('structure',t['id']+' declares new scope and original owner','**New scope:**' in text and '**Existing owner to extend:**' in text)
    check('structure',t['id']+' references resolve',set(t['source_refs'])<=source_ids)
    check('structure',t['id']+' example body included','```' in text and len(text.split())>=500)
    check('structure',t['id']+' is not marked complete','not implemented' in t['status'] or 'proposed' in t['status'])
    old=t['prior_dependencies'];new=t['dependencies'];conds=[x['task'] for x in t['conditional_dependencies']]
    check('dependencies',t['id']+' earlier dependencies are prior contracts',all(re.fullmatch('NEXT-\\d{2,3}',d) and 1<=int(d[5:])<=100 for d in old))
    check('dependencies',t['id']+' new prerequisites resolve',set(new)<=expected and t['id'] not in new)
    check('dependencies',t['id']+' conditional prerequisites resolve',all(re.fullmatch('NEXT-\\d{2,3}',d) and 1<=int(d[5:])<=125 and d!=t['id'] for d in conds))
graph=json.loads((ROOT/'dependency-graph.json').read_text())
order=graph['topological_order'];rank={x:i for i,x in enumerate(order)}
check('dependencies','new graph contains 25 distinct nodes',set(order)==expected and len(order)==25)
check('dependencies','declared conditional graph is acyclic',all(rank[d]<rank[t] for t,deps in graph['new_nodes'].items() for d in deps))
master=(ROOT/'MASTER-PSEUDOCODE.md').read_text()
for t in tasks:check('documents',t['id']+' master heading once',len(re.findall(r'^# '+t['id']+':',master,re.M))==1)
for p in sorted(ROOT.rglob('*.md')):
    s=p.read_text()
    check('documents',str(p.relative_to(ROOT))+' paired fences',len(re.findall(r'^```',s,re.M))%2==0)
    check('documents',str(p.relative_to(ROOT))+' no em dash','\u2014' not in s)
    for target in re.findall(r'\]\(([^)]+)\)',s):
        if target.startswith(('http:','https:','mailto:')):continue
        path,_,anchor=target.partition('#')
        if path:
            resolved=(p.parent/path).resolve()
            check('links',p.name+' -> '+target,resolved.exists() or resolved==(ROOT/'checks/results.json').resolve())
        elif anchor.startswith('part-'):
            check('links',p.name+' #'+anchor,'id="'+anchor+'"' in s)
check('documents','no font files distributed',not any(p.suffix.lower() in {'.ttf','.otf','.woff','.woff2'} for p in ROOT.rglob('*')))

# Independent named arithmetic and state examples. They never load the repository.
eq('arithmetic','positive floor',round_ratio(101,4,'floor'),25)
eq('arithmetic','negative exact floor',round_ratio(-100,100,'floor'),-1)
eq('arithmetic','negative nonexact floor',round_ratio(-101,100,'floor'),-2)
eq('arithmetic','half-up positive tie',round_ratio(5,2),3)
eq('arithmetic','half-up negative tie',round_ratio(-5,2),-3)
eq('arithmetic','half-even even tie',round_ratio(5,2,'half_even'),2)
eq('arithmetic','half-even odd tie',round_ratio(7,2,'half_even'),4)
check('arithmetic','zero denominator refused',reject(lambda:round_ratio(1,0)))
check('arithmetic','nonexact exact mode refused',reject(lambda:round_ratio(1,2,'exact')))
eq('access_model','delegated permissions intersect',set(['read','prepare','payroll_read']) & {'read','prepare'} & {'read'} & {'read','payroll_read'},{'read'})
check('access_model','revoked client grant yields no rights',not ({'read','prepare'} & set() & {'read'}))
check('access_model','firm role cannot enlarge client grant','payroll_read' not in ({'read'}&{'read','payroll_read'}&{'read','payroll_read'}))
# Original source line count remains separate from an aggregate equality.
check('accounting_models','offsetting unexplained rows do not establish completeness',sum([500,-500])==0 and bool([500,-500]))
eq('arithmetic','shared cost split',allocate(10001,{'A':1,'B':2}),{'A':3334,'B':6667})
eq('arithmetic','zero weight receives no residual',allocate(7,{'A':0,'B':1}),{'A':0,'B':7})
eq('arithmetic','tie-break stable identity',allocate(1,{'B':1,'A':1}),{'B':0,'A':1})
check('arithmetic','all-zero allocation weights refused',reject(lambda:allocate(10,{'A':0,'B':0})))
eq('arithmetic','negative source allocation conserves amount',sum(-x for x in allocate(10001,{'A':1,'B':2}).values()),-10001)
eq('arithmetic','project revenue bridge',80000+10000-(-5000),95000)
eq('arithmetic','project margin with one cost allocation',95000-40000-10000,45000)
eq('arithmetic','retainer first release',cumulative(100000,600,0,150),25000)
eq('arithmetic','retainer final release consumes residual',cumulative(100000,600,599,1),100000-round_ratio(100000*599,600))
check('arithmetic','retainer overuse refuses',reject(lambda:cumulative(100000,600,590,11)))
journal('retainer earned revenue release',[25000,-25000])
eq('arithmetic','remaining retainer units and value',(600-150,100000-25000),(450,75000))
eq('arithmetic','onerous first target',max(260000-200000,0),60000)
eq('arithmetic','onerous revised target delta',max(125000-100000,0)-(60000-30000),-5000)
journal('provision target recognition',[60000,-60000])
journal('provision release',[30000,-30000])
eq('arithmetic','warranty synthetic expected value',round_ratio(100*1*10000,20),50000)
eq('arithmetic','warranty remaining after actual claim',50000-12000,38000)
eq('arithmetic','warranty remeasurement delta',40000-38000,2000)
journal('direct insurer settlement',[10000,-10000])
eq('arithmetic','supplier residual after direct insurer payment',12500-10000,2500)
journal('recognized principal forgiveness',[20000,-20000])
eq('arithmetic','loan balances after principal forgiveness',(100000-20000,5000),(80000,5000))
journal('VAT deduction true-up',[6500-4000,-(6500-4000)])
eq('arithmetic','VAT repeat target changes nothing',6500-(4000+2500),0)
eq('arithmetic','VAT reduced eligible basis delta',5200-6500,-1300)
journal('construction full deduction',[100000,25000,-25000,-100000])
journal('construction half deduction',[112500,12500,-25000,-100000])
net=round_ratio(12000*5,6);tax=12000-net
eq('arithmetic','OSS inclusive price decomposition',(net,tax),(10000,2000))
journal('OSS booked sale',[12000*11,-net*11,-tax*11])
journal('OSS tax settlement FX loss',[tax*11,22400-tax*11,-22400])
journal('foreign tax recovery of expensed cost',[1500,-1500])
eq('arithmetic','travel cash/benefit partition',(2500-500,3000-(2500-500),400),(2000,1000,400))
eq('arithmetic','travel noncash benefit does not increase cash',2000+1000,3000)
eq('arithmetic','car actual net contribution reduces qualified base',max(50000-10000,0),40000)
eq('arithmetic','car excess cannot create negative benefit',max(50000-60000,0),0)
eq('arithmetic','gross reduction not a benefit payment',max(50000-0,0),50000)
eq('arithmetic','interest gross amount vs withholding',6000+2000,8000)
eq('arithmetic','interest accrual/reporting bridge',12000-8000,4000)
eq('arithmetic','salary exchange cash gross',6000000-500000,5500000)
journal('extra pension accrual',[530000,-530000])
eq('arithmetic','share nominal/premium split',(100*1000,100*200,100*(1000-200)),(100000,20000,80000))
eq('arithmetic','subscription excess is not shares',105000-100*1000,5000)
journal('paid allotment classification',[100000,-20000,-80000])
eq('arithmetic','preliminary forecast change',90000-120000,-30000)
# State uses the actual decision, not a forecast field.
actual_installment={'decision':10000,'proposal':6000}
eq('accounting_models','tax proposal does not amend authoritative installment',actual_installment['decision'],10000)

# Finite mandate state model: serialized abstract commits, not PostgreSQL concurrency proof.
m=MandateModel(100000,70000)
m.execute('k1','invoice1',25000)
eq('mandate_model','successful amount consumes gross budget',m.used,95000)
m.execute('k1','invoice1',25000,active=False)
eq('mandate_model','replay after expiry consumes no new budget',m.used,95000)
check('mandate_model','new event above budget refused',reject(lambda:m.execute('k2','invoice2',10000)))
check('mandate_model','same economic event new key refused',reject(lambda:m.execute('k3','invoice1',25000)))
check('mandate_model','same key changed amount refused',reject(lambda:m.execute('k1','invoice1',20000)))
check('mandate_model','current access required even for replay',reject(lambda:m.execute('k1','invoice1',25000,has_access=False)))
m2=MandateModel(100000,70000);before=deepcopy(m2)
check('mandate_model','model fault before commit aborts',reject(lambda:m2.execute('k','i',20000,crash=True)))
eq('mandate_model','fault retains all original state',m2,before)
for seq in [('A','B'),('B','A')]:
 mm=MandateModel(100000,70000);accepted=0
 for event in seq:
  try:mm.execute(event,event,20000);accepted+=1
  except ValueError:pass
 eq('mandate_model','serialized competing events '+''.join(seq),accepted,1)
 eq('mandate_model','serialized budget after '+''.join(seq),mm.used,90000)

status,best,_=search_finite(100000,[0],[[(0,60000,0)],[(0,50000,10)]],0,100)
eq('planner_model','both full mandatory choices cannot fit',status,'infeasible_within_model')
status,best,_=search_finite(100000,[0],[[(0,60000,0)],[(0,40000,8)]],0,100)
eq('planner_model','allowed installment feasible',status,'optimal_within_model')
eq('planner_model','permitted choices produce exact floor',best['path'],[0])
status,best,_=search_finite(100000,[0],[[(0,60000,0)],[(0,0,0),(0,40000,8)]],0,1)
eq('planner_model','interrupted feasible result not optimum',status,'feasible_bounded')
status,best,_=search_finite(100000,[0],[[(0,60000,0)],[(0,50000,10),(0,40000,8)]],0,1)
eq('planner_model','interrupted before feasible choice not infeasibility proof',status,'exhausted_no_candidate')
eq('planner_model','candidate outflow replaced rather than added twice',100000-60000,40000)
journal('direct debit settles AR',[100000,-100000])
journal('returned unconsumed collection restores AR',[100000,-100000])
eq('accounting_models','accepted instruction leaves AR outstanding',125000-25000,100000)
eq('provider_model','proven source aliases share one observation',sum(provider_unique([('old:1',5000),('new:1',5000)],{'new:1':'old:1'}).values()),5000)
eq('provider_model','equal amounts without proven identity both retained',sum(provider_unique([('old:1',5000),('new:1',5000)],{}).values()),10000)
check('provider_model','conflicting same identity is not silently merged',reject(lambda:provider_unique([('old:1',5000),('new:1',6000)],{'new:1':'old:1'})))
f=RefundModel(50000);f.reserve(20000)
eq('refund_model','instruction reduces available not liability',(f.liability-f.reserved,f.liability),(30000,50000))
f.processor_debit('txn1',20000)
eq('refund_model','pending movement creates transit',(f.liability,f.transit,f.processor_delta),(50000,20000,-20000))
f.processor_debit('txn1',20000)
eq('refund_model','duplicate provider movement does not repost',(f.transit,f.processor_delta),(20000,-20000))
f.complete(20000)
eq('refund_model','qualified discharge settles once',(f.liability,f.transit,f.reserved),(30000,0,0))
f.reverse_completed(20000)
eq('refund_model','returned completed refund restores original liability',(f.liability,f.transit,f.processor_delta),(50000,0,0))
f2=RefundModel(50000);f2.reserve(20000);f2.processor_debit('t',20000)
f2.return_before_completion(20000,final_no_execution=False)
eq('refund_model','returned funds without final proof retain reservation',(f2.liability,f2.transit,f2.reserved),(50000,0,20000))
f3=RefundModel(50000);f3.reserve(20000);f3.processor_debit('t',20000);f3.return_before_completion(20000,final_no_execution=True)
eq('refund_model','final failed refund releases reservation',(f3.liability,f3.transit,f3.reserved),(50000,0,0))
check('refund_model','over-reservation fails',reject(lambda:RefundModel(50000).reserve(50001)))
journal('refund pending transit',[20000,-20000])
journal('refund liability discharge',[20000,-20000])

# Validate published compact example metadata rather than falsely calling it app fixtures.
e=json.loads((ROOT/'design-examples.json').read_text())['examples']
eq('structure','example covers every new packet',{x['packet'] for x in e},expected)
check('structure','examples explicitly marked synthetic',all('synthetic' in x['scope'] for x in e))
by_packet={x['packet']:x for x in e}
def expected_fields(packet, actual):
    saved=by_packet[packet]['expected']
    for name,value in actual.items():
        normalized=str(value) if isinstance(saved[name],str) and isinstance(value,int) else value
        eq('published_vectors',packet+' '+name,normalized,saved[name])
expected_fields('NEXT-101',{'effective':sorted({'read','prepare','payroll_read'}&{'read','prepare'}&{'read'}&{'read','payroll_read'})})
expected_fields('NEXT-103',{'difference':10000-10000,'complete':False})
expected_fields('NEXT-104',{**allocate(10001,{'A':1,'B':2}),'sum':sum(allocate(10001,{'A':1,'B':2}).values())})
expected_fields('NEXT-105',{'earnedRevenue':80000+10000-(-5000),'totalCost':40000+10000,'margin':95000-50000})
expected_fields('NEXT-106',{'release':cumulative(100000,600,0,150),'minutesRemaining':600-150,'deferredRemaining':100000-25000})
expected_fields('NEXT-107',{'initialTarget':60000,'remainingBeforeRemeasurement':60000-30000,'revisedTarget':125000-100000,'delta':25000-30000})
expected_fields('NEXT-108',{'initialTarget':round_ratio(100*10000,20),'remaining':50000-12000,'newAdjustment':40000-38000})
expected_fields('NEXT-109',{'payableRemaining':12500-10000,'insuranceReceivableRemaining':10000-10000,'bankDelta':0})
expected_fields('NEXT-110',{'principalRemaining':100000-20000,'accruedInterestRemaining':5000,'bookGain':20000})
expected_fields('NEXT-111',{'inputVatDelta':6500-4000,'expenseDelta':4000-6500,'payableDelta':0})
expected_fields('NEXT-112',{'costDebit':100000+25000-12500,'inputDebit':12500,'outputCredit':25000,'payableCredit':100000})
expected_fields('NEXT-113',{'netEURMinor':round_ratio(12000*5,6),'taxEURMinor':2000,'grossSEKMinor':12000*11,'netSEKMinor':10000*11,'taxSEKMinor':2000*11,'settlementFxLoss':22400-22000})
expected_fields('NEXT-114',{'recoveryReceivableDebit':1500,'expenseRecoveryCredit':1500,'swedishInputVatDelta':0})
expected_fields('NEXT-115',{'exemptCash':2500-500,'taxableCash':3000-2000,'noncashBenefit':400,'cashTotal':3000})
expected_fields('NEXT-116',{'benefitAfterNetPayment':max(50000-10000,0),'benefitWithOnlyGrossReduction':50000})
expected_fields('NEXT-117',{'statementGross':6000+2000,'unreportedTimingBridge':12000-8000,'paymentReconciles':6000+2000==8000})
expected_fields('NEXT-118',{'cashGrossAfter':6000000-500000,'pensionAccrual':530000,'secondNetDeduction':0})
expected_fields('NEXT-119',{'subscriptionAmount':100*1000,'nominal':100*200,'premium':100*(1000-200),'unallocatedExcess':105000-100000})
expected_fields('NEXT-120',{'estimateDelta':90000-120000,'actualNextInstallmentBeforeDecision':10000})
expected_fields('NEXT-121',{'usedAfterFirst':m.used,'usedAfterReplay':m.used,'nextEvent':'refused'})
expected_fields('NEXT-122',{'bothFullFeasible':False,'qualifiedInstallmentFeasible':True,'fullPaymentShortfall':60000+50000-100000})
expected_fields('NEXT-123',{'remainingBeforeCash':125000-25000,'remainingAfterCash':125000-25000-100000,'remainingAfterUnconsumedReturn':125000-25000-100000+100000})
expected_fields('NEXT-124',{'newOpeningJournal':0,'canonicalTransactionAmount':sum(provider_unique([('o',5000),('n',5000)],{'n':'o'}).values())})
expected_fields('NEXT-125',{'reserved':20000,'freeInstructionCapacity':50000-20000,'liabilityWhilePending':50000,'transitAfterDebit':20000,'liabilityAfterQualifiedDischarge':50000-20000,'transitAfterDischarge':0})
summary={}
for item in checks:
 g=summary.setdefault(item['group'],{'total':0,'passed':0,'failed':0})
 g['total']+=1;g['passed']+=int(item['passed']);g['failed']+=int(not item['passed'])
failures=[x for x in checks if not x['passed']]
report={'scope':'local dossier and independent synthetic arithmetic/finite models only',
        'repository_modified':False,'application_executed':False,'database_executed':False,
        'browser_executed':False,'provider_executed':False,'legal_release_qualified':False,
        'actual_concurrency_proved':False,'full_125_dependency_audit':False,
        'total':len(checks),'passed':len(checks)-len(failures),'failed':len(failures),'groups':summary,'checks':checks}
(ROOT/'checks/results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('total','passed','failed','groups')},indent=2))
for failure in failures:print('FAILED:',failure)
if failures:raise SystemExit(1)
