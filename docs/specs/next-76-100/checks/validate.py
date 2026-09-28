#!/usr/bin/env python3
"""Check generated work-packet structure and independent example arithmetic only.
No OpenERP import, database, browser, provider or network action occurs.
"""
from __future__ import annotations
import hashlib,hmac,itertools,json,re
from fractions import Fraction
from pathlib import Path
R=Path(__file__).resolve().parents[1]
checks=[]
def test(name, condition, group='arithmetic'):
    checks.append(dict(name=name,passed=bool(condition),group=group))
def half_up(n,d):
    if d<=0:raise ValueError('positive denominator required')
    q,r=divmod(abs(n),d)
    return (-1 if n<0 else 1)*(q+int(2*r>=d))
def allocate(total,weights):
    if total<0 or any(v<0 for v in weights) or not weights or sum(weights)<=0:raise ValueError('bad weights')
    W=sum(weights);q=[total*w//W for w in weights];rs=[total*w%W for w in weights]
    for i in sorted(range(len(weights)),key=lambda i:(-rs[i],i))[:total-sum(q)]:q[i]+=1
    return q
def union_size(ranges):
    end=None;total=0
    for a,b in sorted(ranges):
        if b<a:raise ValueError('invalid interval')
        if end is None or a>end:total+=b-a;end=b
        elif b>end:total+=b-end;end=b
    return total
def capacity(available,request):
    if request<0 or request>available:raise ValueError('capacity exceeded')
    return available-request
def must_refuse(fn):
    try:fn()
    except ValueError:return True
    return False
def journal(name,values):test(name,sum(values)==0)
def quorum(slots,roles,exclude=frozenset()):
    def recurse(i,used):
        if i==len(slots):return True
        return any(recurse(i+1,used|{person}) for person,rr in roles.items() if person not in used and person not in exclude and slots[i] in rr)
    return recurse(0,set())
def covers(target,candidates,max_k=5,budget=100000,pool_complete=True):
    seen=0
    for k in range(1,min(max_k,len(candidates))+1):
        hits=[]
        for indices in itertools.combinations(range(len(candidates)),k):
            if seen==budget:return {'kind':'incomplete','hits':hits}
            seen+=1
            if sum(candidates[i] for i in indices)==target:hits.append(indices)
        if hits:return {'kind':('ambiguous' if len(hits)>1 else 'unique_within_pool') if pool_complete else 'incomplete','hits':hits}
    return {'kind':'none_within_pool' if pool_complete else 'incomplete','hits':[]}
def error_parts(p,a,tp,ta,d):
    if p==0 or a==0 or (p<0)!=(a<0):raise ValueError('requires matched same sign')
    sign=-1 if p<0 else 1;w=min(abs(p),abs(a));ip=int(tp<=d);ia=int(ta<=d)
    return sign*w*(ia-ip),sign*((abs(a)-w)*ia-(abs(p)-w)*ip)

idx=json.loads((R/'solution-index.json').read_text());tasks=idx['solutions'];ids=[f'NEXT-{i}' for i in range(76,101)]
test('exact25 consecutive task identities',[t['id'] for t in tasks]==ids,'structure')
test('exact25 packet files',len(list((R/'packets').glob('NEXT-*.md')))==25,'structure')
test('no identical new-scope descriptions',len({t['new_scope'] for t in tasks})==25,'structure')
test('source checkpoint retained',idx['baseline']=='66355b62b23e3b8007c2d324f3739fbbcc96cdc0','structure')
order=idx['new_wave_order_including_conditional_edges'];rank={k:i for i,k in enumerate(order)}
test('new-wave topological order contains25 once',len(order)==25 and set(order)==set(ids),'structure')
master=(R/'MASTER-PSEUDOCODE.md').read_text()
known_refs={f'P{i:02}' for i in range(1,76)}|{f'R{i:02}' for i in range(1,7)}|{f'X{i:02}' for i in range(1,7)}
for t in tasks:
    p=R/t['file'];body=p.read_text()
    test(t['id']+' file matches recorded hash',hashlib.sha256(p.read_bytes()).hexdigest()==t['file_sha256'],'structure')
    deps=set(t['dependencies'])|{x['task'] for x in t['conditional_dependencies'] if x['task'] in rank}
    test(t['id']+' dependencies ordered',all(rank[d]<rank[t['id']] for d in deps),'structure')
    test(t['id']+' prior dependencies valid',all(re.fullmatch(r'NEXT-\d{2}',v) and 1<=int(v[-2:])<=75 for v in t['prior_dependencies']),'structure')
    test(t['id']+' source references known',set(t['source_refs'])<=known_refs,'structure')
    test(t['id']+' appears once in master',len(re.findall(r'^# '+t['id']+r':',master,re.M))==1,'structure')
missing=[]
for p in R.rglob('*.md'):
    text=p.read_text()
    test(str(p.relative_to(R))+' paired fences',sum(line.startswith('```') for line in text.splitlines())%2==0,'documents')
    test(str(p.relative_to(R))+' no em dash','\u2014' not in text,'documents')
    for link in re.findall(r'\]\(([^)]+)\)',text):
        if link.startswith(('https:','http:','mailto:')):continue
        path,sep,anchor=link.partition('#')
        if path:
            dest=(p.parent/path).resolve()
            if not dest.exists() and dest!=(R/'checks/results.json').resolve():missing.append((str(p),link))
        elif anchor.startswith('part-') and f'id="{anchor}"' not in text:missing.append((str(p),link))
test('local links and master anchors resolve',not missing,'documents')
test('five earlier WIP reservations retained',all(k in idx['reserved_work'] for k in ['VAT-03','FX-02-P1','AST-03','VAT-04-A1','COM-2-W1']),'structure')
# Independent expected arithmetic, not calls to production calculators.
test('positive half-up tie',half_up(5,2)==3)
test('negative half-up tie',half_up(-5,2)==-3)
test('zero denominator refused',must_refuse(lambda:half_up(1,0)))
test('equal installment residual',[41667,41667,41666]==allocate(125000,[1,1,1]))
test('zero weight gets no amount',allocate(100,[0,1,1])==[0,50,50])
test('all zero weights refused',must_refuse(lambda:allocate(100,[0,0])))
test('contract cap after increase',120-40-10==70)
test('reduction below consumed cap refuses',45 < 40+10)
test('time billing exact minute conversion',Fraction(90*120000,60)==180000)
test('time remaining after reservations',10-4-2==4)
test('retention preserves original gross',112500+12500==125000)
journal('unbilled recognition',[60000,-60000])
journal('invoice releases prior earnings',[100000,-60000,-20000,-20000])
test('unbilled lifetime revenue only once',60000+20000==80000)
test('held slices union does not double count',union_size([(0,30000),(0,30000)])==30000)
test('overlapping holds union exact',union_size([(0,30000),(20000,40000)])==40000)
test('hold plus distinct reserved leaves no new capacity',100000-union_size([(0,30000),(30000,100000)])==0)
journal('asset commissioning no new payable',[120000,-120000])
test('partial commissioning preserves remainder',120000-70000==50000)
journal('component retirement and replacement',[60000,10000,30000,-100000,80000,-80000])
test('indexed rent',half_up(10000*103,100)==10300)
journal('apply refundable rental deposit',[15000,-15000])
test('deposit remaining',30000-15000==15000)
test('synthetic tax deduction ceiling',1000000-700000==300000)
test('chosen tax deduction and reserve',1000000-250000==750000 and 800000-750000==50000)
test('tax reserve posts only delta',50000-30000==20000)
journal('excess depreciation delta',[20000,-20000])
test('synthetic periodic reserve choice below ceiling',200000<=half_up(1000000,4)==250000)
test('vintage tax versus book reversal difference',half_up(100000*104,100)-100000==4000)
journal('ROT reclassification changes no consideration',[25000,-25000])
journal('ROT claim cash receipt',[25000,-25000])
journal('pension provision true-up',[10000,1000,-11000])
journal('pension fee tax counted separately',[10000,1000,250,-11250])
test('SLP target delta synthetic',half_up(50000,5)-8000==2000)
test('final holiday expense only unprovided part',15000-12000==3000)
test('dividend entitlement conservation',allocate(100000,[3,2])==[60000,40000])
test('dividend liability after partial cash',100000-20000==80000)
journal('grant cash before earned',[50000,-50000])
journal('grant later earns through deferred plus receivable',[20000,20000,-40000])
journal('grant negative revision removes receivable and creates liability',[30000,-20000,-10000])
test('supplier credit two applications',capacity(capacity(30000,20000),8000)==2000)
test('supplier credit excess refuses',must_refuse(lambda:capacity(10000,10001)))
journal('supplier credit applies to payable',[20000,-20000])
journal('bilateral setoff no bank movement',[80000,-80000])
test('bilateral setoff both balances update',150000-80000==70000 and 100000-80000==20000)
test('one human cannot fill two distinct approval slots',not quorum(['finance','director'],{'p1':{'finance','director'}}))
test('two distinct eligible humans fill slots',quorum(['finance','director'],{'p1':{'finance'},'p2':{'director'}}))
test('revoked human invalidates unconsumed quorum',not quorum(['finance','director'],{'p1':{'finance'},'p2':{'director'}},frozenset({'p2'})))
test('batch risk is gross not one leg',sum([600000,600000])>1000000)
cs=covers(100,[70,30,60,40]);test('two exact covers remain ambiguous',cs['kind']=='ambiguous' and len(cs['hits'])==2)
test('smallest complete cover selected',covers(100,[100,70,30])['kind']=='unique_within_pool')
test('incomplete search not false no-match',covers(100,[70,30,60,40],budget=2)['kind']=='incomplete')
test('truncated candidate pool not global uniqueness',covers(100,[100],pool_complete=False)['kind']=='incomplete')
test('full selected pool no solution',covers(99,[70,30,60,40])['kind']=='none_within_pool')
test('forecast timing amount day5',error_parts(100,80,5,7,5)==(-80,-20))
test('forecast total error day7',sum(error_parts(100,80,5,7,7))==-20)
test('negative cash-flow error has correct sign',sum(error_parts(-100,-80,5,7,7))==20)
for p,a,tp,ta in [(100,80,5,7),(100,120,5,3),(-100,-80,5,7),(-100,-120,5,3)]:
    test('forecast exact decomposition '+str((p,a,tp,ta)),all(sum(error_parts(p,a,tp,ta,d))==a*int(ta<=d)-p*int(tp<=d) for d in range(1,10)))
test('opposite cash signs require explicit classification',must_refuse(lambda:error_parts(100,-80,5,7,7)))
raw=b'{"eventId":"fixture-1","amountMinor":"10000"}';key=b'public-test-key-not-a-credential'
msg=b'v1\nsubscription-fixture\n2026-09-28T12:00:00Z\nfixture-1\n'+hashlib.sha256(raw).hexdigest().encode()
sig=hmac.new(key,msg,hashlib.sha256).digest()
test('HMAC fixture verifies exact bytes',hmac.compare_digest(sig,hmac.new(key,msg,hashlib.sha256).digest()))
changed=msg.replace(hashlib.sha256(raw).hexdigest().encode(),hashlib.sha256(raw.replace(b'10000',b'10001')).hexdigest().encode())
test('changed event body does not verify',not hmac.compare_digest(sig,hmac.new(key,changed,hashlib.sha256).digest()))
report=dict(scope='Dossier structural and independent synthetic calculation checks only',application_executed=False,sql_executed=False,provider_executed=False,repository_modified=False,results=checks,passed=sum(x['passed'] for x in checks),failed=sum(not x['passed'] for x in checks),count=len(checks))
(R/'checks/results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='results'},indent=2))
if report['failed']:
 for row in checks:
  if not row['passed']:print(row)
 raise SystemExit(1)
