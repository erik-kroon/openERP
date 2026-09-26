# Preserved-rule audit and proposed replacements

Scope: R1 through R25 in `docs/plans/11-parity-backlog.md` at `ac9e1a918d86c6872f415e3a988cbc7d25b6f9fb`. These are critiques of the **planning document**, not findings that the current application implements every recipe. The upstream Accounted revision/files behind the comparison were not identified by the plan, so none of these rules is called upstream-verified here.

A deterministic algorithm can encode a legally wrong formula, an unsafe default or an arbitrary product policy. A/B/C classification must be applied to components and behavior, not merely to literal rates. Every replacement below is a proposed target contract; relevant normative data and company applicability still need qualification. The present review does not activate any profile.

## R1: Check digits and generated references

**Keep:** one exact check-digit calculation, independent examples and explicit unsupported input. **Reclassify:** the arithmetic is A; accepted length ranges, normalization and supported reference families are B format rules. **Change:** returning the input unchanged when OCR generation fails is not a typed refusal. A caller receiving a string can mistake failure for success.

```text
generateReference(input, qualifiedFormat):
  parsed = parseIdentifierUnderExplicitFormat(input)
  if parsed invalid: return Invalid(reason, originalInput)
  if format does not permit generation: return Unsupported(formatId)
  generated = parsed.payloadDigits + checksum(parsed.payloadDigits)
  return Generated(generated, algorithmVersion, formatVersion)
```

Do not strip arbitrary meaningful characters to make an unrelated identifier appear valid. Format-valid is not an existing account, verified payee or authority to pay. PRY-16 owns the shared implementation, not a new financial workflow.

## R2: Clearing rules and modulus-11 alignment

The rule lists bank-specific ranges and exact exceptions while declaring the whole rule class A. Those tables are external facts, class B, even if implemented as an `if` chain.

The written weight selection, “last `11 - length(digits) + 1` elements”, cannot supply one weight per digit for all supported lengths: an 11-digit input selects one weight. This is a defect in the specification as written, independent of whether the unseen reference code is correct.

```text
validateWeightedDigits(digits, approvedWeightsForVariant):
  require approvedWeightsForVariant.length == digits.length
  require every input character is a digit
  total = sum(digits[i] * approvedWeightsForVariant[i])
  return the qualified modulus predicate
```

Do not guess which weights or padding are legally correct for each clearing family. Acquire and version the actual format, then use complete independent length/exception examples. Preserve `UnknownFormat`, `InvalidFormat` and `FormatValid` separately.

## R3: Taxpayer representation

**Keep:** one shared renderer for the supported taxpayer representation. **Change:** a 12-digit input must not bypass parsing and entity-kind validation merely because its length matches. Century inference, coordination-number dates, entity kind and permitted prefixes are B/C facts rather than a universal A-only conversion.

Return `{sourceIdentity, renderedIdentity, formatRelease, evidence}` or a typed missing/invalid result. Where age-dependent payroll needs actual birth-date evidence, identifier formatting alone must not silently fill an uncertain century. This review does not certify the stated tax-account OCR format or destination.

## R4: A parsed voucher reference is not a join key by itself

`A123` can occur in multiple companies, fiscal years, provider connections and imports. The series/number parser is useful but needs a lossless original and a qualified provider format.

```text
parseSourceReference(raw, providerProfile) ->
  Parsed(series?, number, raw)
  | NotBooked(raw, providerEvidence)
  | Unreadable(raw, diagnostics)

resolveSourceVoucher(parsed, context):
  require context identifies provider connection + source company + fiscal year
  candidates = exact preserved source-reference matches in that context
  if exactly one: Resolved(sourceVoucherIdentity)
  if none: Unresolved(context, parsed)
  else: Ambiguous(candidateIds)
```

Do not collapse “source says not booked” into “we could not parse it”. Do not link to the target system's coincidentally equal voucher number. A default series or year is not an acceptable repair.

## R5: Filename candidates and incomplete pseudocode

The placeholder prefix string is not an implementable parser specification. Camera/paper/form-name heuristics and blanket rejection of three-letter series are product heuristics, not proof about every source exporter.

Use a versioned source-filename profile, original path/name, parsed candidate, confidence reason and complete scoped match set. With no series or ambiguous year, require review. Never auto-select from a collision-prone heuristic just because today's candidate inventory contains one item. Retain failed files and allow post-hoc evidence linking without reposting.

## R6: Exact cover, ambiguity and bounded search

The current algorithm discards equally ranked solutions and returns a single deterministic best result. R14 separately requires ambiguity to downgrade to suggestion. These contracts need to agree. A capped search also cannot prove there is no solution outside the search scope.

```text
findCover(target, eligibleCandidates, policy):
  require exact compatible units and financial direction
  pool = canonical remaining-capacity candidates, sorted by declared rank
  candidateScopeComplete = pool selection is complete for the declared scope
  selectedPool = first policy.maxCandidates candidates
  truncated = len(pool) > len(selectedPool)
  bestRank = none; bestSets = []; searchIncomplete = false
  for cardinality in 1..policy.maxSetSize:
    enumerate distinct resource-ID sets under an explicit step/time budget
    compare exact sums; never use float tolerance as exact equality
    retain ALL equal-best rank witnesses, or at least two plus an ambiguity flag
    if budget exhausted: searchIncomplete = true; stop
    if at least one solution at this cardinality: stop after this rank is resolved
  if no solution:
    return NoMatchWithinScope(scope, truncated, searchIncomplete, maxSetSize)
  if multiple best witnesses:
    return Ambiguous(bestSets, searchCoverage)
  return Candidate(bestSet, uniqueWithinDeclaredSearch, searchCoverage)
```

Target 100 with same-date candidates 70, 30, 60 and 40 has two equally sized exact covers. Choosing 70+30 by ID order does not make it economically unique. Date rank, four-leg limit and 40-candidate cap are product/search policy, not accounting evidence.

Confirmation still calls the existing bank-allocation owner, rechecks each source/line capacity under the application transaction and keeps bank matching distinct from invoice settlement. Truncated or ambiguous discovery never grants auto-apply authority.

## R7: Rates, caches and as-of semantics

**Keep:** exact requested date, retained observation date, no fabricated rate, bounded retry and evidence. **Change:** do not assume provider ordering, interpret every 404 as a missing observation or allow an unbounded old-cache fallback after a bounded network search.

```text
eligibleObservation(o, request, policy):
  return pair/direction/source/scale match
     AND o.observationDate <= request.asOf
     AND age(o, request.asOf) <= policy.maximumAge
     AND o.permittedUse covers request.valuationPurpose
     AND not withdrawn_for_new_use

selectObservation(results):
  choose maximum observationDate among eligible observations
  handle same-date conflicts through explicit source precedence or review
```

The cache key includes the pair, provider/source policy and relevant request semantics. Cached evidence passes the same eligibility function as fresh evidence. A cached observation can be a valid fallback only under that rule. Retain unavailable-provider, no-published-observation, stale-only and conflicting-observation outcomes separately. Identity conversion for the actual same monetary unit may use exact one without inventing external evidence.

## R8: Employer-contribution order is itself a rule

The order “truncate employee basis, aggregate category/rate, truncate amount” is not independently safe merely because it contains no hardcoded rate. Grouping, stage of rounding, scope and exceptions determine a statutory result. These are B/C inputs to an A arithmetic implementation.

Remove the two broadly “acceptable approximations” until they are supported by the actual applicable specification and exact cases. Independently verify multiple employees, multiple runs, categories, bands and fractions. Retain separate values for booked accrual, period declaration, assessed liability and actual remittance, with an explicit reconciliation. A salary-net payment file is not the employer-contribution amount.

This review does not replace R8 with another unverified universal contribution formula. Its immediate improvement is to prohibit that unqualified norm from becoming executable by virtue of an A label.

## R9: Sick-pay entitlement and waiting deduction

R9 removes the first day's sick pay and then adds a waiting deduction. This combines two different mechanisms and can over-deduct. Försäkringskassan describes sick pay within the employer period and a karens deduction from that entitlement, with schedule/agreement-dependent calculation. The source is listed in SOURCES.md; the complete payroll rule set is not qualified here.

**Quarantine the written formula, not merely its percentages.** A supported target calculation must first derive the eligible sick-pay entitlement from actual scheduled absence and the qualified period/exception policy. It then applies the remaining permitted waiting deduction once, with any carry/recovery behavior from that same policy. It does not first suppress a paid day unconditionally.

A mechanical counterexample: given normal lost pay 1,000, eligible sick pay 800 and remaining permitted deduction 800, the supported simple calculation deducts `1,000 - (800 - 800) = 1,000`. The written first-day-removal recipe yields `1,000 - 0 + 800 = 1,800`. This is an illustrative diagnosis, not a universal payroll prescription.

Preserve the wanted period-state and explainable intermediates. Re-derive relapse, partial-day, work-pattern, agreement and exemption cases before release. PRY-65 belongs under PAY-02/03, not a parallel salary system.

## R10: Comparable money and residuals

Same currency code is insufficient without its amount scale and financial direction. Comparing absolute magnitudes can hide opposite-sign movements. Two stored converted amounts are not automatically comparable if their purposes, dates or bases differ.

```text
compareMoney(a, b, purpose):
  require permitted signed direction relationship
  normalize exact units without floating point
  if same currency and unit basis: return exact signed difference
  require compatible retained conversion witnesses for this comparison purpose
  otherwise return NotComparable(reason, affectedIds)
```

A residual is a fact to explain, not permission to book. A valid fee, FX or rounding policy may compile a proposal with evidence and exact remaining capacities. “Small enough” alone cannot authorize an expense, income or cash adjustment. Execution belongs to the native posting/settlement owner and cannot double-consume the selected source.

## R11: Detector failure must block the guarded financial action

This is a direct contradiction inside the plan. PRY-39 says detection failure never passes; R11 returns `CLEAR` for detector failure without force. Replace it before agent dispatch.

```text
decideAlreadyExplained(detectorResult, reviewedResolution):
  match detectorResult:
    Unavailable(error, scope):
      return BlockedCheckUnavailable(error, retryableAction)
    CompleteNoConflict(basis):
      return EligibleForRemainingChecks(basis)
    FoundConflicts(conflicts, basis):
      if no reviewedResolution: return ReviewRequired(conflicts, basis)
      require exact resolution digest binds:
        source identities/revisions, detected entry IDs/versions,
        amounts/currencies/scales, relevant capacity state and policy
      require caller holds the explicit resolution authority
      require resolution does not bypass duplicate-effect or conservation invariants
      return ExplicitlyResolved(resolutionId, basis)
    IncompleteSearch(scope):
      return IncompleteAssessment(scope)  # Not a clear result for automation.
```

The final financial operation rechecks this basis inside its existing Effect transaction. A failure can still permit source retention, diagnostic reads or preparation of independent work. It does not permit committing a financial action whose required check did not run.

## R12: Diagnostics are separate from financial admission

The plan calls for three severities, labels unbalanced data NOTICE in one place and ERROR in another, and classifies unknown record meaning as INFO. Define a stable diagnostic model instead:

```text
Diagnostic {
  code, severity: info | warning | error,
  sourceLocator, affectedEntities,
  blocks: [] | [mapping] | [financial_admission] | [reconciliation] | [release]
}
```

A parser may retain an entire file despite unsupported records. Financial admission must not discard consequential controls, dimensions or corrections because the unknown record did not visibly alter an amount. An unknown record's financial effect is not known to be zero. Any tolerated source imbalance requires an explained, supported accounting treatment; it cannot pass into the exact ledger as an implicit plug.

Encoding selection uses header/BOM, byte validity, decoded content and semantic controls as evidence. Some wrong decodes contain no replacement character. Ambiguous taxpayer/payee or amount content must block the affected use even if a cosmetic mojibake warning alone would not block unrelated records. Valid balance-only files are not automatically broken because they contain no vouchers.

## R13: Chart suggestions do not establish meaning

Retain ranked candidates and explicit unmatched/ambiguous accounts. Exact account code and label agreement do not prove that a custom source account has the same control/tax meaning as a target standard account. Account classification and mapped tax treatment must be independently reviewed where required. Suggestions must preserve prior operator decisions and must not silently rename existing target accounts.

## R14: Scores and automation are distinct authority

Ordering and threshold evaluation can be deterministic. Threshold values, accepted false-positive behavior and permitted actions are product/empirical policy. The plan supplies no observed calibration evidence for them.

Separate `candidate score`, `ambiguity`, `search completeness`, `eligibility` and `execution authority`. Auto-apply requires a current explicit mandate and the same complete financial checks as the human path. Unknown detector output, incomplete pool and equal-ranked alternatives cannot be turned into permission by a high score. Begin with suggestions and measure independently before adding unattended changes.

## R15: Replace the circular VAT-box specification

The text introduces an “investment-return box” and defines it by subtracting itself. It is not a usable VAT dependency graph. Do not silently reinterpret it as a correct tax formula.

```text
calculateNetPayable(qualifiedReturnSchema, exactContributions):
  require schema identifies taxable bases, output-tax components,
          deductible-input components and calculated result separately
  require graph acyclic and every mandatory component known
  output = sum(schema.outputTaxComponentValues)
  input = sum(schema.deductibleInputComponentValues)
  exactNet = output-input
  reported = apply qualified field-level rules in the prescribed order
  return values + contribution lineage + rounding witnesses
```

The exact Swedish box membership and reporting rules remain a qualified release. The review corrects the graph and terminology, not every current tax mapping. Ledger-account cross-checking is corroboration, not a replacement for source-linked treatment facts.

## R16: Define ROT/RUT consideration before splitting it

The current definition calls “gross” the customer-paid amount and then subtracts the reduction again. Replace it with unambiguous full consideration `G`, qualified reduction `D`, customer portion `G-D` and separately tracked claim/conditional authority portion `D`.

`customerPortion + authorityPortion = G` is arithmetic. Whether/when an authority receivable may be recognized, the actual eligible work/customer limits, who bears rejection and whether a claim can be recovered from the customer are C decisions. A book's own claims do not necessarily establish a person's unused annual entitlement. Claim rejection must not automatically assert a legally enforceable customer debt without the required agreement/rule facts.

## R17: Holiday balances and reconciliation

A mandatory payout of all expired saved days is not established by a generic rollforward. Entitlement, carry-forward, expiry, payout and valuation need applicable employment/legal/agreement rules. Retain separate unit and monetary effects and known opening evidence.

A reviewed target liability can produce a supported adjustment. An unexplained difference between GL and register is not enough to post a single balancing adjustment. First identify missing/duplicate/misclassified effects, then correct through their owner. Do not distribute unexplained drift across employees or erase it with a tolerance.

## R18: Duration bands must have explicit exclusivity

The two `if` clauses multiply both reduction factors when the second duration threshold is passed. The source does not establish whether the factors are cumulative or alternatives. The rule is therefore underspecified, not a ready-to-adopt algorithm.

A qualified per-diem policy explicitly selects the band, its continuity/reset rules, meal deductions and entitlement versus tax exemption. Use one absolute band rate where that is the rule; compound only when the actual rule requires compounding. Keep actual trip dates/location and already consumed coverage so retries cannot restart the allowance clock.

## R19: Fiscal duration and employee averages

The prose says fiscal-year denominator; the pseudocode always divides by 12 and rounds to whole employees. Those statements conflict for non-12-month fiscal years and do not fully specify partial-month changes.

A proposed calculation integrates reviewed employment degree over the selected fiscal interval using the **qualified disclosure definition**, then divides by that definition's actual reference duration and applies its rounding rule. Do not assert that a generic days-weighted or month-weighted formula is legally correct for every disclosure. An example of the stated time-weighted intention is one full-time employee for an entire 18-month year: the average is one, not 1.5 from division by 12.

Keep evidenced manual overrides separate from computed results, with reason and scope. A declared zero employment population can be valid without a completed payroll engine.

## R20: Obligation, item, document version and attempt are distinct

PRY-72 says a correction must not read the original receipt; R20 says resolve the original's receipt instead of the correction's. Both original baseline and the new attempt are needed for different questions.

```text
PayrollReportingItemKey = employer + reportingPeriod + payee + specificationIdentity
DeclarationRevision = immutable payload for the selected item set and revision
SubmissionAttempt = exact declaration revision + environment + provider request identity
ProviderReceipt = observed outcome of THAT attempt
```

Preserve original receipts as history and amendment basis. A correction's current status comes from its own attempt/receipt, not the original's successful outcome. A changed reporting period is not achieved by mutating an accepted item's key; use the provider/schema's actual replacement/removal/new-period process. Paid/provided reporting facts remain distinct from earning and bookkeeping dates.

## R21: Complete Peppol monetary graph

The official Peppol rules distinguish line-level and document-level allowances, tax-exclusive/tax-inclusive totals, prior paid amounts and payable rounding. The current recipe conflates these and omits components.

```text
lineNetSum = sum(retained line extension amounts)
exclusive = lineNetSum - documentAllowances + documentCharges
vat = sum(qualified tax category amounts)
inclusive = exclusive + vat
amountDue = inclusive - prepaidAmount + payableRounding
```

Line-level allowances/charges already belong in their line extension and must not be deducted again as document allowances. Derive from the qualified semantic invoice and **also validate** the resulting schema/business rules and independent totals. Missing mandatory amounts are not implicit zero. Do not change an issued document to fit an XML validator.

Illustrative values: line net 100, VAT 25, prepaid 20, rounding zero gives 105 due, not the current simplified 100. The official rule sources are in SOURCES.md. Exact schemas/code lists and special credit/tax profiles still require qualification.

## R22: Rounding is a recorded financial decision

The default-enabled choice is product policy, not a general accounting requirement. Keep source net/tax, exact computed total, displayed/payable total and actual settlement separate. The rounding effect must conserve those specific components and be approved as part of the operation.

A legitimate qualified small settlement difference can have a reviewed rounding treatment; a small amount alone is not evidence of rounding. Do not adjust cash or tax implicitly, and never use this path to consume unrelated residual capacities.

## R23: Cash method needs recognition coverage, not an invoice flag

The core COM-02 plan already specifies unpaid year-end recognition and later settlement. The parity recipe must extend it, not replace it with “payment date only” and “invoice has a voucher”.

```text
for each original invoice component:
  retain disjoint recognizedCoverage and unrecognizedCommercialCoverage
on actual payment:
  settle already-recognized AP/AR coverage
  recognize only the supported remaining unrecognized paid portion
at applicable year-end:
  capture the complete eligible unpaid population
  recognize only its still-unrecognized portion into AP/AR and tax facts
on next payment:
  consume those recognized open positions; do not recognize the same expense/revenue/tax again
```

Illustrative invoice 125 gross with 100 net and 25 VAT: payment 50 recognizes 40/10; qualified year-end recognition of remaining 75 recognizes 60/15; next-year payment 75 creates no additional tax fact. Skatteverket's cash-method guidance supports the year-end distinction; actual eligibility and detailed tax rules remain profile inputs.

## R24: Zero cash payment is not zero accounting

Refusing unrepresentable bank details is right. Omit zero-valued **payment instructions**, not the entire pay run. Gross salary, withholding, employer contributions or benefits can exist when the employee's net cash is zero.

For an illustrative supported fact set, gross 1,000 and withholding 1,000 create salary expense 1,000 and withholding liability 1,000, with no employee cash instruction. The employer's contribution effects, if applicable, are separate. This example does not authorize an arbitrary withholding override.

A withholding decision changes the approved payroll calculation and downstream liabilities/reporting. It must not be a payment-file-only knob that avoids reapproval. Validate encoded field widths and actual representation, not only character count if the target is byte-width constrained.

## R25: Extraction agreement is evidence, not truth

Two model readings can share errors. Different tiers or prompts do not establish statistical independence. Always running both increases cost/latency without evidence that this is the best strategy for every input, particularly existing native text or already reviewed matches.

```text
FieldObservation = LocatedValue(value, sourceLocator)
                 | NotPresentInSource
                 | Unreadable(reason)
                 | Conflicting(values, locators)
                 | NotApplicable(qualifiedReason)
```

Preserve the distinction between extraction observations and reviewed accounting facts. Use structured/native extraction first; escalate ambiguous or high-risk fields through a measured strategy. Agreement may improve a candidate score but never proves document authenticity or legal correctness. XML paths, cell references and native text spans can be valid source locators without invented page boxes.

Keep field-specific validation, but apply it by document type: a legitimate credit/refund can contain negative amounts. A failed line/tax field may block accepting the invoice while unrelated header fields remain reviewable. Retain immutable original bytes; a downscaled image is a derivative. Re-extraction cannot silently revise a reviewed or posted record.

## How these replacements are adopted

Change the affected PRY deliverable and the rule together. Record the original finding, rejected/qualified behavior, exact new owner contract and its counterexample. Do not call any R rule certified because this review supplied a plausible replacement. Full source/format/legal evidence and authorized runtime cases are separate gates. No new application tests were added by this document.
