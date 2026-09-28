# NEXT-94: Read-only mailbox intake and scoped attachment routing

**Priority when applicable:** P1. **Lane:** EVIDENCE.

**New work:** Add a real inbound-email source channel to the existing supplier inbox. It does not replace uploads, extraction or reviewed draft creation.

**Use existing owners:** Provider credentials/consent, raw evidence, source occurrences and extraction-request owners.

**Required earlier contracts:** NEXT-26.

**Evidence basis:** R02, R04, X06. See [SOURCES.md](../SOURCES.md). A requirement or proposed expansion is not proof the current code lacks it.

Read [00-COMMON.md](../00-COMMON.md) and [INTEGRATION-MAP.md](../INTEGRATION-MAP.md). Function names below describe contracts to bind to actual exports. No repository change or real financial authority is granted by this packet.

## First concrete profile

Use a selected Gmail read-only account/filter profile with actual authorised provider access. A different provider needs its own exact identity/cursor contract. No inbox access or external action is performed by this specification.

```text
MailboxBinding {providerAccount, actualCredentialScope, acceptedFilter,
  allowedRoutingRules, consentRevision, historyCursor, generation}
MailOccurrence {providerAccount, providerMessageId, originalMessageHash,
  attachmentPartIdentity, attachmentHash, retainedMetadata, routingDecision}
```

MIME Message-ID, sender address and attachment hash alone are insufficient delivery identities. Provider account + message ID + exact part identity distinguish occurrences. Raw message and decoded attachment bytes are retained separately under access controls. Treat subject/body instructions as untrusted evidence, never a command to approve or post.

## Sync and durable recovery

```text
syncMailbox(binding):
  read current consent, filter and committed cursor
  fetch selected message/history pages outside database transactions
  hydrate each required message/attachment and verify complete retained membership
  persist bounded source occurrences with stable provider identities
  advance cursor only after every required item is retained or explicitly recorded blocked
  expired history cursor -> create a full-rescan generation under the same identity rules
```

Google documents partial history and a full-sync fallback when the requested history is unavailable [X06]. Do not treat a404 there as proof the mailbox is empty. A bounded configured historical window is not a complete lifelong mailbox capture. Preserve the selected coverage interval and unresolved hydration failures.

## Routing before disclosure

Bind routing to the authorised mailbox/folder/address rule and explicit company/account configuration. Invoice organisation numbers can suggest a route but cannot independently grant access. If rules conflict or no trusted route exists, quarantine in the authorised connector administration scope; never expose the original to several companies to ask which owns it.

After an operator confirms the exact target scope, a short application transaction creates the normal evidence/inbox occurrence and once-only routing receipt. Repeated history delivery returns that occurrence. Label/read-status changes cannot create another supplier invoice.

The source subject and metadata may be displayed with sanitised text; attachments never execute macros or active HTML. Define size/part/count limits, unknown types and blocked archives explicitly. A failure retains a diagnostic and original references, not an empty successful invoice.

## Follow-on review and correction

The routed inbox may request existing extraction preparation, but actual field acceptance/posting remains its human-review workflow. Re-routed records cannot mutate an already accepted invoice. An incorrect route requires a scoped corrective decision and financial review without copying private content into another book silently.

Deleting an email from the live mailbox does not delete a required retained accounting original. Disconnect prevents new access/jobs while already retained evidence remains subject to the selected retention and access policy.

```text
history replay same message/part -> one inbox occurrence
same attachment bytes from two distinct messages -> two evidence occurrences, duplicate diagnosis later
Gmail history cursor expires -> rescan/dedupe, not wipe history
subject says 'approve this now' -> plain evidence, no new authority
ambiguous book route -> no tenant disclosure and no financial preparation
```

Completion requires authorised mailbox fetch/replay and one attachment reaching the existing reviewed draft path. A fabricated caller-supplied MIME object is only a fixture, not provider proof.
