#!/usr/bin/env python3
"""Check this pseudocode dossier's structure and independent arithmetic vectors.

This script does NOT import OpenERP code, execute SQL, call providers or verify legal
rules. A passing result is not evidence of implemented application behavior.
"""
from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import random
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
counts: dict[str, int] = defaultdict(int)
failures: list[dict[str, str]] = []


def check(group: str, condition: bool, description: str) -> None:
    counts[group] += 1
    if not condition:
        failures.append({'group': group, 'description': description})


def hu(n: int, d: int) -> int:
    """Independent integer implementation of signed nearest, ties away from zero."""
    if d <= 0:
        raise ValueError('Positive denominator required')
    sign = -1 if n < 0 else 1
    q, r = divmod(abs(n), d)
    return sign * (q + int(2 * r >= d))


def balanced(group: str, amounts: list[int], name: str) -> None:
    check(group, sum(amounts) == 0, name)


def structure() -> None:
    index = json.loads((ROOT / 'solution-index.json').read_text())
    expected = {f'NEXT-{n:02d}' for n in range(1, 26)}
    packets = sorted((ROOT / 'packets').glob('NEXT-*.md'))
    check('structure', {p.stem for p in packets} == expected, 'Exactly 25 numbered packet files')
    tasks = {t['id']: t for t in index['solutions']}
    check('structure', set(tasks) == expected, 'All packet identities in solution index')
    check('structure', len(index['solutions']) == 25, 'No duplicate index identity')
    required_wip = {'WIP-VAT03','WIP-FX02-P1','WIP-AST03-UI','WIP-VAT04-A1','WIP-COM2-W1'}
    check('structure', set(index['excluded_active_work']) == required_wip, 'All five WIP reservations preserved')

    dependencies: dict[str,set[str]] = {}
    for ident, task in tasks.items():
        check('structure', (ROOT / task['file']).is_file(), f'{ident} solution file exists')
        deps = set(task['depends_on']) | set(task['integrate_after'])
        deps |= {x['task'] for x in task['conditional_dependencies']}
        check('structure', deps <= expected and ident not in deps, f'{ident} prerequisite identities')
        check('structure', set(task['wait_for_handoff']) <= required_wip, f'{ident} WIP dependencies known')
        dependencies[ident] = deps
    emitted: list[str] = []
    while len(emitted) < len(dependencies):
        ready = sorted(t for t, ds in dependencies.items() if t not in emitted and ds <= set(emitted))
        if not ready:
            break
        emitted.extend(ready)
    check('structure', len(emitted) == 25, 'Prerequisites including conditional edges are acyclic')
    order = index['dependency_order_including_conditional_edges']
    rank = {t:n for n,t in enumerate(order)}
    check('structure', set(order) == expected and len(order)==25, 'Recorded order covers all packets once')
    for t, ds in dependencies.items():
        check('structure', all(rank[d]<rank[t] for d in ds), f'{t} recorded prerequisite order')

    source_doc = (ROOT/'SOURCES.md').read_text()
    defined_refs = set(re.findall(r'^### ([SX]\d{2}):', source_doc, re.M))
    for file in sorted(ROOT.rglob('*.md')):
        text = file.read_text()
        check('documents', '\u2014' not in text, f'{file.relative_to(ROOT)} has no em dash')
        check('documents', len(re.findall(r'^```', text,re.M)) % 2 == 0, f'{file.relative_to(ROOT)} balanced code fences')
        refs = set(re.findall(r'\b[SX]\d{2}\b', text))
        check('documents', refs <= defined_refs, f'{file.relative_to(ROOT)} source IDs resolve')
        for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',text):
            if re.match(r'^(https?:|mailto:)',target):
                continue
            path_part, _, anchor = target.partition('#')
            if path_part:
                target_path = (file.parent / path_part).resolve()
                generated_result = (ROOT/'checks'/'results.json').resolve()
                check('links', target_path.exists() or target_path == generated_result, f'{file.name} -> {target}')
                # results.json is generated after these checks, not an input dependency.
            elif anchor and anchor.startswith('part-'):
                check('links', f'id="{anchor}"' in text, f'{file.name} anchor {anchor}')
    master = (ROOT/'MASTER-PSEUDOCODE.md').read_text()
    for ident in sorted(expected):
        check('documents', len(re.findall(rf'^# {ident}:',master,re.M))==1, f'{ident} appears once in combined solution')


def arithmetic() -> None:
    # Rounding checked against Python decimal, not any repository implementation.
    for n in range(-151,152):
        for d in (1,2,3,4,7,10,100):
            expected = int((Decimal(n)/Decimal(d)).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
            check('rounding', hu(n,d)==expected, f'half_up {n}/{d}')
    check('rounding', hu(101,4)==25, 'Rounded 25% example')

    for net in (0,1,101,10000):
        tax = hu(net,4)
        for ratio in (Fraction(0),Fraction(1,3),Fraction(1,2),Fraction(1)):
            ded = hu(tax*ratio.numerator,ratio.denominator)
            expense = net+tax-ded
            balanced('purchase', [expense,ded,-(net+tax)], 'Purchase gross conservation')
            check('purchase', 0<=ded<=tax, 'Deduction bounded')

    rng = random.Random(20260925)
    for _ in range(500):
        tax = rng.randint(1,10000)
        deduction = rng.randint(0,tax)
        a = rng.randint(0,tax)
        b = rng.randint(a,tax)
        old = hu(deduction*a,tax)
        middle = hu(deduction*b,tax)
        release1 = middle-old
        release2 = deduction-middle
        check('credit', old+release1+release2==deduction, 'Final cumulative credit releases exact deduction')
        check('credit', release1>=0 and release2>=0, 'Credit releases nonnegative')

    for gross in range(1,32):
        for paid in range(0,gross+1):
            credit = rng.randint(0,gross)
            unpaid = max(gross-credit-paid,0)
            principal = max(paid-(gross-credit),0)
            received = rng.randint(0,principal)
            check('refund', unpaid-principal == gross-credit-paid, 'Signed AP/refund conservation')
            check('refund', principal-received>=0, 'Refund residual nonnegative')
            increment = rng.randint(0,gross-credit)
            ap_release = min(increment,unpaid)
            new_refund = increment-ap_release
            after_principal = max(paid-(gross-(credit+increment)),0)
            check('refund', principal+new_refund==after_principal, 'New credit creates exact refund capacity')
            balanced('refund',[ap_release,new_refund,-increment], 'Credit counterpart conservation')
    check('refund', max(100000-(125000-50000),0)-10000==15000, 'Published supplier refund example')

    balanced('owner',[12500,-12500], 'AP moved to owner liability without another expense')
    check('owner', 12500-5000==7500, 'Partial owner reimbursement')
    balanced('fx',[111000,1000,-110000,-2000], 'Receivable settlement with explicit fee')
    balanced('fx',[110000,2000,1000,-113000], 'Payable settlement with explicit fee')
    check('fx',(115000-110000)+(116000-115000)==6000, 'Incremental remeasurement and later settlement')
    # WIP partial FX release is deliberately not reimplemented here.

    G,A,I,P,V = 1000000,300000,100000,650000,162500
    B = G-A-I
    gain = P-B
    balanced('asset',[P+V,A,I,-G,-V,-gain], 'Cash asset sale and impairment disposal')
    check('asset',gain==50000, 'Disposal gain')
    check('asset',200+100+550+50==900,'Post-impairment schedule conservation')

    def contribution(base: int) -> int:
        return hu(min(base,100)+2*max(base-100,0),10)
    check('payroll',contribution(80)==8 and contribution(130)==16,'Synthetic contribution tiers')
    check('payroll',contribution(130)-contribution(80)==8,'Incremental monthly contribution band')
    balanced('payroll',[3000000,-2090000,-900000,-10000],'Payroll cash earnings distributed once')
    check('payroll',3000000+0-900000-10000==2090000,'Published payroll net amount')

    P, addback, deduction, rate = 1000000,50000,20000,Fraction(1,5)
    taxable = P+addback-deduction
    tax = hu(taxable*rate.numerator,rate.denominator)
    after = P-tax
    check('corporate_tax',taxable==1030000 and tax==206000 and after==794000,'Synthetic tax bridge values')
    check('corporate_tax',after+tax+addback-deduction==taxable,'After-tax form bridge equals pre-close taxable result')
    check('corporate_tax',tax-200000==6000,'Current-tax delta, not whole target again')

    check('reporting',60000-60000==0,'No virtual untransferred result after full transfer')
    check('reporting',50000-60000==-10000,'Reclosed year posts incremental result transfer')
    check('reporting',40000-10000==30000,'Historical adoption followed by new payment')
    check('reporting',100+200+50+25==375,'One dimension partitions full scope')

    for _ in range(500):
        total = rng.randrange(0,10000)
        weights = [rng.randrange(1,20) for _ in range(rng.randrange(1,12))]
        W = sum(weights)
        floors = [total*w//W for w in weights]
        residuals = [total*w%W for w in weights]
        left = total-sum(floors)
        check('allocation',0<=left<len(weights),'Largest-remainder leftover has bounded recipients')
        for ix in sorted(range(len(weights)),key=lambda i:(-residuals[i],i))[:left]:
            floors[ix] += 1
        check('allocation',sum(floors)==total,'Schedule shares conserve exact total')
        check('allocation',all(x>=0 for x in floors),'Schedule shares nonnegative')



def application_rewrite_checks() -> None:
    index = json.loads((ROOT/'solution-index.json').read_text())
    check('application_rewrite', index['schema_version'] == 2, 'v2 machine-readable edition')
    common = (ROOT/'00-COMMON.md').read_text()
    check('application_rewrite', 'effect-mq' in common and 'persistent Bun' in common, 'Selected queue runtime described')
    check('application_rewrite', 'withAdmittedPrincipal' in common and 'caller' in common, 'One actual caller transaction described')
    check('application_rewrite', 'deferred journal' in common, 'Narrow journal integrity retained')
    check('application_rewrite', 'pre-release' in common and 'PRODUCT FEATURE' in common, 'Schema replacement distinguished from real historical import')
    forbidden = ['BEGIN named SQL transition', 'Sql.captureNamedBasis', 'Sql.sealNamedPlan',
                 'Instantiate it inside each named PostgreSQL transition',
                 'SQL checks exact assignments', 'effectiveFunctionHashes',
                 'WipAsset.commitDispositionWithinTx']
    for task in index['solutions']:
        text = (ROOT/task['file']).read_text()
        check('application_rewrite', '## Application and persistence boundary' in text, task['id']+' application owner section')
        check('application_rewrite', 'Tx-passing reads and DML' in text, task['id']+' persistence owner section')
        check('application_rewrite', bool(task['ownership_changes']), task['id']+' explicit rewrite record')
        check('application_rewrite', hashlib.sha256((ROOT/task['file']).read_bytes()).hexdigest() != task['supersedes_original_packet_sha256'], task['id']+' differs from old packet')
        for needle in forbidden:
            check('application_rewrite', needle not in text, task['id']+' lacks superseded directive '+needle)
    for needle in forbidden:
        check('application_rewrite', needle not in common, 'Common contract lacks '+needle)

def main() -> int:
    structure()
    arithmetic()
    application_rewrite_checks()
    core_files=[ROOT/'00-COMMON.md',ROOT/'01-RULE-AND-FORM-DATA.md',*sorted((ROOT/'packets').glob('NEXT-*.md'))]
    result={
        'kind':'pseudocode dossier self-check',
        'repository_code_executed':False,
        'sql_or_worker_runtime_executed':False,
        'provider_calls_or_actual_company_data_used':False,
        'qualified_statutory_dataset_verified':False,
        'assertions':sum(counts.values()),'counts':dict(counts),
        'failures':failures,'passed':not failures,
        'solution_packets':25,
        'core_pseudocode_word_count':sum(len(f.read_text().split()) for f in core_files),
        'master_word_count':len((ROOT/'MASTER-PSEUDOCODE.md').read_text().split()),
        'checked_input_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in core_files}
    }
    (ROOT/'checks'/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='checked_input_sha256'},indent=2))
    return 1 if failures else 0


if __name__=='__main__':
    sys.exit(main())
