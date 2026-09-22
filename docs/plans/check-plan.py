"""Regenerate the planning index and check documentation integrity (no product tests)."""

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "docs/plans"
PACKET_ID = r"(?:FND|PST|COR|IMP|COM|VAT|PAY|AST|FX|END|OPS)-\d{2}"
OWNERS = {
    "FND": "Shared contracts/runtime integrator",
    "PST": "Posting and approval",
    "COR": "Corrections with affected register owners",
    "IMP": "Source intake, matching and reconciliation",
    "COM": "Commerce and open-item registers",
    "VAT": "VAT and tax-account profiles",
    "PAY": "Payroll and declaration profiles",
    "AST": "Assets and deferrals",
    "FX": "Currency valuation and settlement",
    "END": "Closing, reports and obligations",
    "OPS": "Operational tooling and deployment integrator",
}
MAINTAINED = [
    "README.md", "architecture.md", "domain.md", "operations.md", "compliance.md",
    "roadmap.md", "open-decisions.md", "verification.md", "adr/README.md",
    "adr/0002-exact-posting-and-approval.md",
    "adr/0004-complete-accounting-delivery-contract.md",
]


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def ids_with_ranges(text, prefix):
    found = set(re.findall(rf"\b{prefix}-\d{{2}}\b", text))
    for first, last in re.findall(rf"{prefix}-(\d{{2}})[–-](?:{prefix}-)?(\d{{2}})", text):
        found.update(f"{prefix}-{value:02}" for value in range(int(first), int(last) + 1))
    return found


def anchors(text):
    found = set()
    occurrences = {}
    for heading in re.findall(r"^#{1,6}\s+(.+)$", text, re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        duplicate = occurrences.get(slug, 0)
        occurrences[slug] = duplicate + 1
        found.add(slug if duplicate == 0 else f"{slug}-{duplicate}")
    return found


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    files = sorted(PLAN.glob("*.md")) + [ROOT / "docs" / name for name in MAINTAINED]
    texts = {path: path.read_text() for path in files}
    packets = []
    for path in sorted(PLAN.glob("0[0-7]-*.md")):
        for line_number, line in enumerate(texts[path].splitlines(), 1):
            if not re.match(rf"^\| {PACKET_ID} \|", line):
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            require(len(cells) == 4 and all(cells), f"Incomplete packet: {path}:{line_number}")
            identifier, deliverable, dependencies, acceptance = cells
            packets.append({
                "id": identifier,
                "owner": OWNERS[identifier.split("-")[0]],
                "source": str(path.relative_to(ROOT)),
                "sourceLine": line_number,
                "deliverable": deliverable,
                "dependsOn": re.findall(PACKET_ID, dependencies),
                "acceptance": acceptance,
                "scenarioIds": sorted(ids_with_ranges(acceptance, "E")),
                "status": "planned_scope_not_implementation_status",
            })
    by_id = {packet["id"]: packet for packet in packets}
    require(len(by_id) == len(packets), "Duplicate packet ID")
    require(len(packets) == 53, f"Expected 53 packets; found {len(packets)}. Review intentional scope changes.")
    for packet in packets:
        require(set(packet["dependsOn"]) <= by_id.keys(), f"Unknown dependency: {packet['id']}")
    pending = set(by_id)
    ordered = []
    while pending:
        ready = sorted(identifier for identifier in pending if set(by_id[identifier]["dependsOn"]) <= set(ordered))
        require(ready, f"Mandatory dependency cycle among: {sorted(pending)}")
        ordered.extend(ready)
        pending.difference_update(ready)

    conditional_section = texts[PLAN / "08-delivery.md"].split("## Mandatory versus conditional dependencies", 1)[1].split("## Ownership", 1)[0]
    conditional = []
    for line in conditional_section.splitlines():
        if re.match(rf"^\| {PACKET_ID}\b", line):
            consumer, gate = [cell.strip() for cell in line.strip("|").split("|")]
            references = re.findall(PACKET_ID, line)
            require(set(references) <= by_id.keys(), f"Unknown conditional reference: {line}")
            conditional.append({"consumer": consumer, "gate": gate, "referencedPackets": references})

    traceability = texts[PLAN / "09-acceptance.md"]
    coverage = {}
    for prefix, source, count in [("R", "product.md", 12), ("I", "domain.md", 12), ("E", "verification.md", 21)]:
        defined = set(re.findall(rf"^\| ({prefix}-\d{{2}}) \|", (ROOT / "docs" / source).read_text(), re.MULTILINE))
        referenced = ids_with_ranges(traceability, prefix)
        require(len(defined) == count and referenced == defined, f"Incomplete/unknown {prefix} traceability: {sorted(defined ^ referenced)}")
        coverage[prefix] = sorted(referenced)
    require(ids_with_ranges(texts[PLAN / "10-external-inputs.md"], "D") == {f"D-{n:02}" for n in range(1, 11)}, "External input coverage incomplete")
    area_files = [path for path in texts if path.parent == PLAN and re.match(r"0[1-7]-", path.name)]
    require(len(area_files) == 7, "Seven area specifications required")
    for path in area_files:
        require("Owner:" in texts[path] and "Phase:" in texts[path], f"Missing owner/phase: {path}")

    generated_paths = {PLAN / "evidence/work-packages.json", PLAN / "evidence/planning-integrity.json"}
    local_links = 0
    for path, body in texts.items():
        require(not any(line.rstrip() != line for line in body.splitlines()), f"Trailing whitespace: {path}")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            require(destination.exists() or destination in generated_paths, f"Broken link: {path.relative_to(ROOT)} -> {target}")
            if parsed.fragment and destination.suffix == ".md":
                require(unquote(parsed.fragment) in anchors(destination.read_text()), f"Broken anchor: {path.relative_to(ROOT)} -> {target}")
            local_links += 1

    subprocess.run(["git", "diff", "--check", "--", *[str(path.relative_to(ROOT)) for path in files]], cwd=ROOT, check=True, capture_output=True)
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    captured = datetime.now(timezone.utc).isoformat()
    index = {
        "generatedAt": captured, "headObservedAtValidation": revision,
        "authority": "Derived from domain packet tables and the conditional-gate table; not an implementation/proof status report.",
        "packetCount": len(packets), "packets": packets, "mandatoryTopologicalOrder": ordered,
        "conditionalGates": conditional,
        "conditionalGateMeaning": "Applicability gates are not added to the engineering DAG. Runtime sequencing and branch applicability remain as specified in 08-delivery.md.",
    }
    write_json(PLAN / "evidence/work-packages.json", index)
    hashed = files + [Path(__file__).resolve(), PLAN / "evidence/work-packages.json", PLAN / "evidence/planning-baseline.json"]
    integrity = {
        "checkedAt": captured, "headObservedAtValidation": revision,
        "result": "passed_document_integrity_only", "reproduce": "python3 docs/plans/check-plan.py",
        "checks": {
            "areaSpecifications": len(area_files), "workPackages": len(packets),
            "mandatoryDependencyEdges": sum(len(packet["dependsOn"]) for packet in packets),
            "mandatoryDependencyCycles": 0, "conditionalGateRows": len(conditional),
            "localLinksAndAnchorsChecked": local_links, "documentsChecked": len(files),
            "coverage": coverage, "externalInputs": [f"D-{n:02}" for n in range(1, 11)],
            "trailingWhitespace": "passed", "gitDiffCheck": "passed",
        },
        "manualReview": "See 09-acceptance.md: monetary compatibility, atomic correction, source multiplicity, distinct capacities, completeness, close/tax sequencing and old-writer fencing. Manual review is not mechanically proven by this script.",
        "limitations": [
            "No product tests or proposed acceptance scenarios executed by this planning task.",
            "No legal rule bundle, provider protocol or company applicability certified.",
            "Concurrent implementation may differ from the dated planning baseline.",
            "Web links are excluded from local-link validation; source observations/access limits are recorded in 10-external-inputs.md.",
            "Documentation/index validation does not establish runtime correctness or production readiness.",
        ],
        "files": [{"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in sorted(hashed)],
    }
    write_json(PLAN / "evidence/planning-integrity.json", integrity)
    print(json.dumps({"result": integrity["result"], **{k: v for k, v in integrity["checks"].items() if k != "coverage"}}, indent=2))


if __name__ == "__main__":
    main()
