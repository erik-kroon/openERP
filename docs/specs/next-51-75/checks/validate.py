#!/usr/bin/env python3
"""Standalone validation of a design dossier, NOT the OpenERP test suite.

Uses only Python's standard library. No repo imports, network, database,
credentials, application writes or financial actions are performed.
"""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
RESULTS: list[dict] = []

def check(name: str, ok: bool, detail: str = '') -> None:
    RESULTS.append({'name': name, 'passed': bool(ok), 'detail': detail})

def round_ratio(n: int, d: int, mode: str = 'half_up') -> int:
    if d <= 0:
        raise ValueError('positive denominator required')
    q, r = divmod(abs(n), d)
    if mode == 'exact':
        if r:
            raise ValueError('inexact result')
        a = q
    elif mode == 'toward_zero':
        a = q
    elif mode == 'floor':
        a = q + int(n < 0 and r != 0)
    elif mode == 'half_up':
        a = q + int(2 * r >= d)
    elif mode == 'half_even':
        a = q + int(2 * r > d or (2 * r == d and q % 2 == 1))
    else:
        raise ValueError('unsupported rounding')
    return -a if n < 0 else a

def allocate(total: int, weights: dict[str, int]) -> dict[str, int]:
    if total < 0 or not weights or min(weights.values()) < 0 or sum(weights.values()) <= 0:
        raise ValueError('invalid allocation')
    W = sum(weights.values())
    shares = {k: total * w // W for k, w in weights.items()}
    remainders = {k: total * w % W for k, w in weights.items()}
    order = sorted(weights, key=lambda k: (-remainders[k], k))
    for k in order[:total - sum(shares.values())]:
        shares[k] += 1
    return shares

def pay_in_order(values: list[int], payment: int) -> list[int]:
    if payment < 0 or payment > sum(values):
        raise ValueError('overcapacity')
    result = []
    for remaining in values:
        applied = min(remaining, payment)
        result.append(remaining - applied)
        payment -= applied
    return result

def raises_value(fn) -> bool:
    try:
        fn()
    except ValueError:
        return True
    return False

def journal(name: str, values: list[int]) -> None:
    check(name, sum(values) == 0, 'Synthetic debit-positive integer vector: ' + repr(values))

def source_entry_amount(entry: int, details: list[int]) -> int:
    if sum(details) != entry:
        raise ValueError('unreconciled detail amount')
    return entry

def fulfill(required: str, state: str, entity_matches: bool, production: bool) -> bool:
    if not entity_matches or not production:
        return False
    # This is a deliberately declared example profile, not a universal authority API.
    accepted = {'submitted': {'signed_submitted', 'accepted'}, 'accepted': {'accepted'}}
    return state in accepted.get(required, set())

index = json.loads((ROOT/'solution-index.json').read_text())
tasks = index['solutions']
expected_ids = [f'NEXT-{i:02}' for i in range(51, 76)]
check('Exactly 25 new IDs in order', [t['id'] for t in tasks] == expected_ids)
check('Exactly 25 packet files', len(list((ROOT/'packets').glob('NEXT-*.md'))) == 25)
check('No first-wave file overwritten in the new packet folder', not any(int(p.stem[-2:]) <= 50 for p in (ROOT/'packets').glob('NEXT-*.md')))
check('Every packet has a distinct explicit delta', len({t['new_scope'] for t in tasks}) == 25 and all(t['non_overlap'] for t in tasks))
check('Every packet names current ownership and complete atomic result', all(t['existing_owner'] and t['atomic_scope'] and t['canonical_owner_family'] for t in tasks))
check('Every packet requires more than a leaf', all(len(t['complete_requires']) >= 4 for t in tasks))
check('All delivered packet hashes agree with the index', all(hashlib.sha256((ROOT/t['file']).read_bytes()).hexdigest() == t['packet_sha256'] for t in tasks))
check('Old dependencies remain in the existing namespace', all(1 <= int(x[-2:]) <= 50 for t in tasks for x in t['prior_wave_dependencies']))
check('New dependencies resolve inside this wave', all(x in expected_ids for t in tasks for x in t['dependencies']))
check('All conditional dependencies resolve in NEXT-01..75', all(re.fullmatch(r'NEXT-\d{2}',x['task']) and 1 <= int(x['task'][-2:]) <= 75 for t in tasks for x in t['conditional_dependencies']))
sources = json.loads((ROOT/'source-manifest.json').read_text())
source_ids = set(sources['repository']) | set(sources['external'])
check('All packet evidence labels resolve', all(x in source_ids for t in tasks for x in t['source_refs']))
check('Source pins agree', index['baseline'] == sources['baseline'])
graph = json.loads((ROOT/'dependency-graph.json').read_text())
positions = {k: n for n, k in enumerate(graph['topological_order'])}
check('New-wave dependency graph has 25 unique nodes', len(positions) == 25)
check('All declared new-wave edges are acyclic', all(positions[d] < positions[t] for t,ds in graph['nodes'].items() for d in ds))
by = {t['id']:t for t in tasks}
check('Services-only sales list does not hard-depend on goods support', 'NEXT-53' not in by['NEXT-55']['dependencies'])
check('SEK bank import does not hard-depend on foreign cash', 'NEXT-40' not in by['NEXT-70']['prior_wave_dependencies'])
check('Portal does not require payment-link delivery', 'NEXT-64' not in by['NEXT-65']['dependencies'])
check('Whole-invoice payment link does not require installments', 'NEXT-59' not in by['NEXT-64']['dependencies'])
master = (ROOT/'MASTER-PSEUDOCODE.md').read_text()
check('Master contains every new packet heading once', all(len(re.findall('^# '+t['id']+':',master,re.M)) == 1 for t in tasks))
check('Master discloses no application test claim', 'No repository patch, live accounting, application test or provider qualification is claimed.' in master)
mds = list(ROOT.rglob('*.md'))
check('All Markdown code fences paired', all(sum(line.startswith('```') for line in p.read_text().splitlines()) % 2 == 0 for p in mds))
check('No em dashes in delivered Markdown', all('\u2014' not in p.read_text() for p in mds))
missing = []
for p in mds:
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if link.startswith(('https:', 'http:', '#', 'mailto:')):
            continue
        path = link.split('#',1)[0]
        if not path:
            continue
        target = (p.parent/path).resolve()
        if not target.exists() and target not in {(ROOT/'CHECKS.md').resolve(), (ROOT/'checks/results.json').resolve()}:
            missing.append((str(p.relative_to(ROOT)),link))
check('All local document links resolve', not missing, repr(missing))
check('No font files included', not any(p.suffix.lower() in {'.ttf','.otf','.woff','.woff2'} for p in ROOT.rglob('*')))
check('No executable feature stored-procedure instruction', not any(re.search(r'CREATE\s+(OR\s+REPLACE\s+)?FUNCTION',p.read_text(),re.I) for p in mds))

check('Floor exact negative division is unchanged', round_ratio(-100,100,'floor') == -1)
check('Floor positive inexact division rounds down', round_ratio(101,4,'floor') == 25)
check('Floor negative inexact division rounds down', round_ratio(-101,4,'floor') == -26)
check('Half-up is sign-symmetric', round_ratio(5,2) == 3 and round_ratio(-5,2) == -3)
check('Half-even distinguishes odd/even ties', round_ratio(5,2,'half_even') == 2 and round_ratio(7,2,'half_even') == 4)
check('Exact mode refuses discarded residual', raises_value(lambda:round_ratio(1,3,'exact')))
check('Zero denominator refuses', raises_value(lambda:round_ratio(1,0)))
# Cross-check the explicitly selected mathematical floor rule independently with Python integer floor.
check('Signed floor agrees on a finite independent grid', all(round_ratio(n,d,'floor') == n//d for n in range(-51,52) for d in range(1,14)), '1339 synthetic rational inputs; not statutory qualification or repository calculator tests.')
check('Largest-remainder allocation conserves exact amounts', all(sum(allocate(total,{'a':1,'b':2,'c':3}).values())==total for total in range(201)))
check('Allocation ties are deterministic by stable ID', allocate(2,{'c':1,'b':1,'a':1}) == {'c':0,'b':1,'a':1})
check('Zero weight gets no allocation', allocate(101,{'a':0,'b':1}) == {'a':0,'b':101})
check('All-zero weights refuse', raises_value(lambda:allocate(100,{'a':0,'b':0})))
check('Mixed domestic amounts reconcile', 10000+20000+5000+round_ratio(10000,4)+round_ratio(20000*3,25) == 39900)
check('Gross-preserving inclusive backout example', (round_ratio(12500*4,5),12500-round_ratio(12500*4,5)) == (10000,2500))
journal('Mixed invoice payable-rounding effect', [39901,-35000,-4900,-1])
journal('EU acquisition partial deduction', [112500,12500,-100000,-25000])
check('Import tax base includes only uncounted charges', round_ratio((100000+5000+2000),4)==26750)
check('Import charge already included is not added twice', round_ratio((100000+5000),4)==26250)
check('EU original-error correction replaces total', 60000+35000 == 95000 and (60000+40000)+(35000-40000)==95000)
journal('Customer advance initial receipt', [12500,-10000,-2500])
journal('Customer advance final application', [25000,10000,-30000,-5000])
check('Customer advance lifetime tax is final supply tax', 2500+5000 == 7500)
journal('Unused customer advance refund', [10000,2500,-12500])
journal('Supplier advance receipt', [10000,2500,-12500])
journal('Supplier advance final deduction and payable', [30000,5000,-10000,-25000])
journal('Supplier advance with initial deduction deferred', [30000,7500,-12500,-25000])
check('Advance formula conserves partial components', all((GF-GA)+NA-NF-(TF-TA)==0 for NF,TF,NA,TA in [(30000,7500,10000,2500),(80000,20000,30000,7500),(10000,0,4000,0)] for GF,GA in [(NF+TF,NA+TA)]))
check('Revenue deferral example retains remaining source capacity', 120000-30000-60000==30000)
installments = list(allocate(125000,{'1':1,'2':1,'3':1}).values())
check('Installments partition invoice exactly', installments==[41667,41667,41666] and sum(installments)==125000)
check('Partial payment conserves installment residual', pay_in_order(installments,50000)==[0,33334,41666])
check('Payment cannot consume excess installment principal', raises_value(lambda:pay_in_order(installments,125001)))
journal('Qualified cash discount', [9800,160,40,-10000])
check('Unqualified short payment leaves unpaid principal', 10000-9800==200)
for A in [0,40000,100000,125000]:
    journal('Confirmed loss with allowance '+str(A), [A,125000-25000-A,25000,-125000])
journal('Qualified late bad-debt cash recovery', [25000,-20000,-5000])
check('Synthetic single-segment interest', round_ratio(100000*30,10*365)==822)
exact_interest = Fraction(100000*15,10*365) + Fraction(60000*15,10*365)
check('Synthetic reduced-principal interest sums before rounding', round_ratio(exact_interest.numerator,exact_interest.denominator)==658)
check('Budget exposure replaces rather than adds stages', 30000+20000+10000 == 30000+30000+0)
check('Budget shortfall example', (30000+20000+10000+45000)-100000==5000)
check('Serialized competing budget requests cannot both fit', 60000+30000<=100000 and 60000+30000+30000>100000)
check('Three-way accepted-unbilled quantity is disjoint', 10-6==4 and 6-4==2)
check('Statement entry is not summed with details', 100000-source_entry_amount(30000,[10000,20000])+5000==75000)
check('Unreconciled bank detail decomposition refuses', raises_value(lambda:source_entry_amount(30000,[10000,19999])))
check('Accepted bank instruction does not settle entire principal', 100000-40000==60000)
check('Uploaded tax draft is not submitted fulfillment', not fulfill('submitted','uploaded',True,True))
check('Missing external signature remains pending', not fulfill('submitted','awaiting_external_signature',True,True))
check('Signed-submitted is still not guaranteed accepted', not fulfill('accepted','signed_submitted',True,True))
check('Wrong entity receipt cannot fulfill obligation', not fulfill('accepted','accepted',False,True))
check('Sandbox receipt cannot fulfill production obligation', not fulfill('accepted','accepted',True,False))
check('Correct observed accepted receipt can satisfy declared profile', fulfill('accepted','accepted',True,True))
recognized_net=round_ratio(100000*50000,125000)
recognized_tax=round_ratio(25000*50000,125000)
check('Method-change recognized/unrecognized coverage conserves tax', recognized_net==40000 and recognized_tax==10000 and 25000-recognized_tax==15000)
check('Already year-end-recognized method-change residual has no new tax', 25000-(10000+15000)==0)

failed = [r for r in RESULTS if not r['passed']]
report = {
    'scope':'Standalone dossier structure and independent synthetic mathematical examples only',
    'baseline':index['baseline'],
    'application_code_imported':False,'repository_tests_run':False,'database_run':False,
    'provider_run':False,'repository_modified':False,
    'named_checks':len(RESULTS),'passed':len(RESULTS)-len(failed),'failed':len(failed),'results':RESULTS
}
(ROOT/'checks/results.json').write_text(json.dumps(report,indent=2)+'\n')
(ROOT/'CHECKS.md').write_text(f'''# Actual dossier validation

Executed `python checks/validate.py` against this generated package.

**{report['passed']}/{report['named_checks']} named checks passed; {report['failed']} failed.** They cover exact packet IDs, declared conditional dependencies, file hashes, document links and independent synthetic arithmetic/state examples. The finite floor/allocation grids are grouped mathematical checks, not thousands of separately claimed application tests.

This checker imports no OpenERP code and does not run Effect Schema, PostgreSQL, Workers, Bun jobs, a browser or any provider. It cannot prove transaction atomicity, actual access policy, legal applicability or live acceptance. The packet vectors and implementation proof obligations still require execution under the repository's actual authorization.

Reproduce with [checks/validate.py](checks/validate.py). Full named results: [checks/results.json](checks/results.json). The checker is part of the design archive, not added to the application repository.
''')
print(json.dumps({k:report[k] for k in ['named_checks','passed','failed']},indent=2))
if failed:
    for r in failed:
        print('FAILED:',r)
    raise SystemExit(1)
