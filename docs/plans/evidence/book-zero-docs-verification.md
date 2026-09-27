# Book Zero documentation integration — 27 September 2026

This record covers documentation only. The user requested updates to the openERP docs and clarified that the Book Zero file is the relevant source. No application code, tests, migrations, company records or provider operations are changed by this work.

## Provenance

| Artifact | Recorded identity |
| --- | --- |
| Supplied archive | `Drastic_Financial_Platform_PRD_v1.zip` |
| Archive SHA-256 | `b884b83af6ea5d45441f40f740ad866386ea270d448c263d0e7f963f8b744c0b` |
| Imported entry | `drastic_financial_platform_prd_v1/PRD_openERP_Book_Zero_Workflow_Drastic_Cash_v1.md` |
| Source bytes | 80,645 |
| Source SHA-256 | `6dee5e41e75373722a443f23b2aa6f3b3329dcad862b3c6284a07ac1aa263afd` — matches the supplied archive's manifest |
| Source's selective review revision | `41410fd75e96361b7c2f407d456019500f39bfbe` |
| HEAD observed during integration | `09fdb19837bb1535b1b4c060e68a0b237858b0a5`, with pre-existing staged and unstaged implementation changes |
| Maintained destination | [Book Zero delivery plan](../15-book-zero-workflow-cash.md), linked from the product, architecture, domain, frontend, operations, roadmap, decisions, coverage and verification docs |

Only the openERP Book Zero document is vendored. Its bytes remain unchanged. The adjacent checksum file was generated on import, while the expected source hash was read from the supplied archive manifest. The broader platform PRD and its machine-readable requirements/acceptance registers were not imported as openERP requirements. Source instructions, proposed file paths and reported company/legal facts are treated as reference material rather than current operational authority or proof.

## Repeatable document checks

From the repository root, verify the original and regenerate the existing plan integrity record:

```bash
(cd docs/specs/book-zero-v1 && shasum -a 256 -c SHA256SUMS.txt)
python3 docs/plans/check-plan.py
```

The checker validates the existing 53-packet graph, R/I/E/D coverage and maintained plan links. It regenerates `work-packages.json` and `planning-integrity.json`; it runs no application tests. The following additional document check verifies the imported requirement/case sets and the synthetic Cash arithmetic using integer minor units, independently of application code:

```python
import hashlib
import json
import re
from pathlib import Path

root = Path.cwd()
source = root / "docs/specs/book-zero-v1/PRD_openERP_Book_Zero_Workflow_Drastic_Cash_v1.md"
assert hashlib.sha256(source.read_bytes()).hexdigest() == "6dee5e41e75373722a443f23b2aa6f3b3329dcad862b3c6284a07ac1aa263afd"
assert len(source.read_bytes()) == 80645
body = source.read_text()
plan = (root / "docs/plans/15-book-zero-workflow-cash.md").read_text()
mapping = plan.split("## Requirement ownership\n", 1)[1].split("## Book Zero proof and handoff\n", 1)[0]
requirements = set(re.findall(r"^### ((?:BZ|WF|AI|CASH|NFR)-\d{2}):", body, re.M))
assert len(requirements) == 49
assert requirements == set(re.findall(r"\b(?:BZ|WF|AI|CASH|NFR)-\d{2}\b", mapping))
cases = set(re.findall(r"^\| (AT-\d{2}) \|", body, re.M))
acceptance = (root / "docs/verification.md").read_text().split("## Book Zero acceptance\n", 1)[1]
acceptance = acceptance.split("### Independent Cash example\n", 1)[0]
mapped_cases = set(re.findall(r"\bAT-\d{2}\b", acceptance))
for first, last in re.findall(r"AT-(\d{2})–AT-(\d{2})", acceptance):
    mapped_cases.update(f"AT-{n:02}" for n in range(int(first), int(last) + 1))
assert cases == mapped_cases == {f"AT-{n:02}" for n in range(1, 46)}

opening = 10000000  # SEK minor units; these are synthetic values.
buffer = 1000000
tax_funding = max(0, 5000000 - 3000000)
assert tax_funding == 2000000
def scenario(customer_day):
    flows = {5: -4000000, 10: -4000000, 11: -tax_funding, 20: 6000000}
    flows[customer_day] = flows.get(customer_day, 0) + 3000000
    balances = [opening]
    for day in range(1, 31):
        balances.append(balances[-1] + flows.get(day, 0))
    return {"closingMinor": balances[-1], "minimumMinor": min(balances),
            "headroomMinor": min(balances) - buffer}
base, delayed = scenario(8), scenario(22)
assert base == {"closingMinor": 9000000, "minimumMinor": 3000000, "headroomMinor": 2000000}
assert delayed == {"closingMinor": 9000000, "minimumMinor": 0, "headroomMinor": -1000000}
print(json.dumps({"result": "passed_document_checks_only", "requirementsMapped": len(requirements),
                  "casesMapped": len(cases), "base": base, "delayed": delayed}, indent=2))
```

Run the Python block from the repository root with Python 3. The retained [check result](book-zero-docs-verification.json) records the observed outcome, local-link check and file hashes. The original source remains the full specification for the cases; the mapping and example do not claim an executed E2E journey.

## Limits

The documentation update does not change the existing accounting packet count, dependency graph or completion status. Company originals, the reported fiscal year/bank, legal rules, recipient SIE import, runtime/browser behavior and external outcomes were not qualified here. Existing source-review observations were used to identify owner paths, not to claim those implementations are complete or absent.

No product tests, browser sessions or databases were run. The source-only `check:changed`/`check:changed:full` runners were not applicable to the Markdown/checksum/evidence edits; in this shared dirty checkout they would select and format unrelated implementation changes. Documentation checks cover this change. Pre-existing implementation work, including `docs/verification-strategy.md` and the Bend qualification work, is outside this edit.
