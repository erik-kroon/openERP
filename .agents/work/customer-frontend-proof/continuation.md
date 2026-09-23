# Customer frontend continuation — 23 September 2026

Working implementation record. Desktop UX is the requested priority. No test files are authorized or added. Existing company/provider release gates remain independent.

Completed implementation phases so far:
- Direct invoice entry; automatic retention of entered facts; inline customer creation.
- Original document → expense creation, decimal amounts, immutable source reference, addressable detail and review.
- One scoped attention projection for journal proposals, invoice drafts and expense reviews, with matching counts, bounded pagination and URL filters.
- Named statement register/upload/preview flow, readable reconciliation amounts, named invoice issue accounts and periods.
- Addressable report registers and focused review-pack preparation.

Before adding workspace coordination, failure cases to preserve:
- A user cannot read another book's members, views or assignments through changed scope/record IDs.
- A saved personal view is visible only to its owner; a team view can only be authored by an operator in that book.
- Assignment accepts an existing record and current member in the same book. It grants no accounting authority.
- Removed membership must not be blocked by coordination data; stale assignees are labelled unavailable.
- A stale expected assignment revision cannot overwrite a newer handoff.
- Retrying the same request replays its result; reusing its key with another payload fails.
- Notes and filter state persist remotely; no financial payload or evidence is stored in browser preferences.
- List bounds are explicit; failure does not turn unknown assignment state into unassigned.

Remaining local phases: finish persisted coordination, inspect creation/edit/review and queue transitions in the local browser, finish integration checks and update maintained frontend status. Production identity, legal tax activation and provider submission are externally gated; no frontend implementation implies them.
