# Restricted application recovery design

Each candidate must derive its proposed data shape from the operator calling restore and receiving an application-read recovery receipt. The writer and provider activation decisions remain separately controlled.

Score each criterion from zero through two.

- Supports real ordinary application reads after restore while preserving all authority checks.
- Cannot enable financial writes or provider work through restricted recovery admission.
- Retains release, migration, role, original-byte, receipt and closure witnesses.
- Uses existing owners with a small interface and avoids scattered recovery conditionals.
- Defines independently specified E2E pass, refusal, corruption, replay and no-write expectations before implementation.

Choose the safest complete design with the least duplicated policy. Candidate outputs are design proposals, not implemented behavior.
