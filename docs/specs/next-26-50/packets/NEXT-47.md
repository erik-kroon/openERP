# NEXT-47: Document signatures bound to exact content and purpose

**Priority:** P1. **Owner lane:** DELIVERY. **Status:** proposed application-owned pseudocode; not implemented or runtime-verified.

**Existing owner:** Existing artifact, identity and external-attempt owners. Add document-signature intent and a selected BankID/signing adapter.

**New scope, not repeated work:** The first wave generates K2/iXBRL content but does not prove document signing. Add purpose-bound signature evidence without treating ordinary login or accounting approval as document signature.

**Dependencies:** NEXT-24. **Integrate after:** APP-SLICE-READY(artifacts).

**Evidence:** R03, R10, P24, X06 in [SOURCES.md](../SOURCES.md). Source observations support the entry point and requirement, not completion or a universal absence claim.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). `App`, `Db` and `Domain` symbols are proposed responsibilities to bind to existing exports, not a new framework.

## Signing scope

```text
SignatureManifest immutable {
  book, legalEntityRevision, purpose,
  semanticModelId/hash, renderedArtifactId/hash/length,
  reviewedDisplayRepresentation, requiredSignerSet,
  signaturePolicyRelease, artifactRelations, createdAt
}
SignatureIntent {
  manifestId, expectedSignerIdentity, consentTextHash,
  nonce, expiry, providerEnvironment, requestDigest
}
SignatureEvidence immutable {
  intentId, providerOrderRef, signedPayloadHash, actualSignerIdentity,
  signatureBytesRef, certificate/statusEvidenceRefs,
  verifierVersion, technicalResult, completionTime, usageEligibility
}
```

Purposes include signing the original annual report, approving an internal accounting plan and certifying an adopted copy. They are not equivalent. Authority for one purpose cannot satisfy another. A signature manifest names which exact bytes are signed and which semantic copy relationship is allowed.

## Start flow

```text
prepareSignature(document, signer):
  require immutable selected content and required document validation
  require actual required signer roles from reviewed company/governance facts
  require rendered content shown to signer agrees with semantic manifest
  freeze visible consent text and cryptographically bound document manifest
  select qualified signing profile, not authentication-only login
  persist intent and exact request identity

startSignature(intent):
  short tx: current authority + exact replay + admit one external start attempt
  outside tx: call selected provider with the exact visible text and bound data
  short tx: retain returned order/correlation identity and challenge metadata
```

An adapter exposing nonvisible signed data may bind the document digest there only when its qualified protocol and visible-consent presentation establish the intended document-signing relationship. Merely storing a PDF hash beside a successful login is insufficient. Do not label a hash-binding experiment a legally valid signing product.

BankID's public autostart guidance says client return is not sufficient outcome evidence and completion should be obtained from collect [X06]. Exact current signing request/response and cryptographic verification details were not fully extractable in this review; the adapter release must pin them before production activation. No invented API fields or endpoint version are mandated here.

## Completion and verification

```text
completeSignature(orderRef):
  read intent under current service retention authority
  query/receive authentic provider result OUTSIDE financial tx
  require returned orderRef matches original attempt and provider environment
  verify signature chain, signed data binding and status using qualified verifier
  require signed digest == exact manifest digest
  require signer identity == intended permitted signer under purpose policy
  App tx:
    replay known result first
    append raw completion and verification evidence
    evaluate current document revision/authority for intended use
    mark technical signature valid independently from current usage eligibility
    save receipt; do not mutate signed artifact or issue accounting
```

A role change can make a technically valid signature unusable for the intended submission without erasing the historical signature. A content change after any required signer signs produces a new manifest and new required signatures for that content. Do not silently combine signatures over different versions.

## Lost response, multiple signers and scope

Persist known provider references immediately. If the start response is lost and the provider offers no safe lookup, keep an unknown start attempt until the documented cancellation/expiry recovery proves how to proceed. Do not restart a second signature order merely because a local lease expired. A known pending order is collected/cancelled through its actual contract.

For multiple signers, each signs the same allowed content manifest with an independent intent. Completion requires exactly the required set under the chosen governance policy, not an arbitrary count. A duplicate signer does not replace another required role.

The app can orchestrate original-document signing. It does not replace an authority service's own later fastställelse signing ceremony. NEXT-48 keeps that distinct.

## Interface and vectors

Show actual document, purpose, signer role, version, technical completion and usable-for-submission status. Do not expose signature secrets/order challenge material in general accounting lists.

```text
login succeeds -> documentSignatures remains0
signature returns for artifact A while current selected artifact B -> retain A,
    cannot mark B signed
three required signers, same person signs twice -> still missing required distinct signer
provider order completion replay -> one signature evidence record
membership revoked after signature -> retain history; re-evaluate permitted future use
```

Completion requires configured provider access and observed end-to-end evidence. The pseudocode solves ownership and recovery, not the unavailable cryptographic/schema qualification bytes.
