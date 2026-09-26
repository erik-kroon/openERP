# NEXT-46: Peppol invoice and credit exchange through a selected access point

**Priority:** P1. **Owner lane:** DELIVERY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing semantic invoice/credit models, retained artifacts, supplier intake and authorized external-delivery owner. Add a selected access-point adapter, not a Peppol network implementation.

**New scope, not repeated work:** First-wave packets issue documents and generate local reports. This adds a concrete structured e-invoice/credit format and transport boundary, with inbound review distinct from posting.

**Dependencies:** NEXT-03, NEXT-15. **Integrate after:** APP-SLICE-READY(invoice-delivery).

**Conditional gates:** NEXT-26: inbound documents enter the assisted supplier-review workflow.

**Evidence:** R03, R09, X05 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Pinned exchange profile

```text
PeppolRelease {
  version, exact CustomizationID/ProfileID,
  supportedUBLDocumentTypes, schemaHashes, schematronHashes,
  codeListVersions, countryRuleVersions, monetaryRules
}
ParticipantBinding {book, schemeId, participantId, verifiedRevision, providerAccount}
ExchangeArtifact {semanticInvoiceRevision, release, exactXMLHash, validationReport}
ExchangeAttempt {artifactId, senderBinding, recipientBinding, externalMessageId, providerKey}
IncomingEnvelope {providerAccount, messageId, participant, rawBytesHash, signatureOrAuthWitness}
```

The checked official BIS index identifies a May 2026 release [X05]. Pin actual schema/rule bytes before activation; a page title is not a validation bundle. No access-point vendor or credential has been selected by this design. Its concrete adapter must implement the declared send/status/inbound-proof contract before external acceptance can be claimed.

## Semantic rendering

```text
renderBIS(document, release):
  require document is an immutable issued invoice OR legal credit, not a draft
  require seller/buyer endpoint schemes and legal identities explicitly mapped
  require supported currency/tax categories and exact line price-base quantities
  emit selected UBL Invoice or CreditNote root and matching type-specific fields
  per line:
    retain quantity, unit, price/baseQuantity, allowances and charges
    compute/check line extension under the release's exact rounding rules
    emit original tax category/rate with exemption/reverse-charge reason where applicable
  documentNet = sum(lineNet) - documentAllowances + documentCharges
  tax = sum(taxCategorySubtotals)
  inclusive = documentNet+tax
  payable = inclusive-prepaidAmount+documentRounding
  require every amount matches the retained semantic document and original rules
  emit legal references, payment means and original-invoice references for credits
  return exact UTF-8 XML
```

Credit documents use their own UBL structure and economic direction. Do not blindly negate every field from an Invoice. The first implementation can support only the existing domestic invoice/credit profiles; other BIS categories remain named unsupported cases. It must not change a legally issued total merely to satisfy a validator.

## Validation and outbound delivery

Run strict XML parsing, XSD and Schematron plus semantic reconciliation against the source invoice. A valid syntax with the wrong party, amount or original invoice reference fails. Retain validator versions, complete diagnostics and no-network schema resolution. Validation unavailable is not pass.

```text
prepareOutbound(artifact, recipient):
  require exact artifact validation and current sender/recipient bindings
  seal external target, document hash and delivery purpose
approveOutbound -> existing authorized-delivery operation
admitDispatch -> current binding/authority check + one stable attempt in tx
sendOutsideTx -> selected access point
recordOutcome -> retain actual transport acknowledgment/status with exact message identity
```

Transport accepted, recipient delivered and invoice paid are different states. An unknown outcome is resolved by provider correlation/idempotency, not a new invoice number or repeated send with a new identity. A replacement delivery intentionally references the same legal document and its prior attempt.

## Inbound path

```text
receiveEnvelope(raw, providerProof):
  verify selected provider authentication and destination participant scope
  key = providerAccount + recipientParticipant + transportMessageId
  if key already retained:
    require identical content hash; return same receipt
  retain envelope/original XML under authorized source intake
  validate supported BIS content and extract structured SOURCE assertions
  create supplier inbox occurrence with sender/message/document provenance
  run ordinary duplicate diagnosis and human review
  do not accept/pay/post solely because Peppol delivered it
```

A new message ID for the same supplier invoice is additional evidence or a duplicate candidate, not another expense. Conflicting bytes under the same transport identity are an integrity incident. A legitimate repeat document with different business identity remains representable.

## Controls and vectors

Link outbound delivery to immutable issue/credit and retain incoming source-to-draft-to-recognition lineage. API/MCP inspect format and delivery state through existing permissions. Approval/signing remain separate where needed.

```text
line10000 + tax2500 -> exclusive10000/inclusive12500/payable12500
same invoice with prepaid2500 -> payable10000; no reduction of original tax by default
credit4000+1000 -> CreditNote for5000 with original invoice reference
XSD-valid XML changed buyer -> semantic mismatch, no send
provider retry same message/hash -> one inbox occurrence
provider accepted, response lost -> recover attempt, no second legal issue
```

Scope is a qualified BIS subset and one actually configured access point. No claim of automatic support for all e-invoicing networks, national rules or receipt types is made.
