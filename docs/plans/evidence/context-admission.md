# Bounded context admission

This unit preserves the released context/ordinary attention contracts, current book authority and the selected status=all50-row admission bound. Packet6 remains incomplete: immutable capture, continuation, durable progress, complete adapter registry and delta delivery are separate work.

Failure-first context test source is committed at `f71fc67b4b50b36179db76fffbebb028d3e3f692`. Its exact committed-head run `test-results/context-admission-red-committed-20261001` retains5 failed/6 passed with stable source. Invoice/expense review digests were supplied to numeric context revision, selected-period attention used null date bounds, missing source facts returned500, and51 out-of-period rows incorrectly consumed the selected inventory bound. Supported51-selected refusal and current membership revocation controls passed.

The required actual expense ordinal2 owner fixture exposed a separate prerequisite: its current immutable revision read used FOR UPDATE/FOR SHARE and failed native42501 because the runtime role retains SELECT/INSERT but no UPDATE. Exact owner failure-first source is committed at `26219ba`; `test-results/context-expense-prerequisite-red-20261001` captures both initial getter500 and revision2 mutation500 before decoding. No grants were changed to reproduce or repair it.

The prerequisite removes only that immutable-row lock clause and its obsolete parameter. Record/review/withdraw retain the existing book UPDATE lock, and getter retains book SHARE. The same-row current revision read is now a plain SELECT. Actual owner HTTP proof `test-results/context-expense-prerequisite-green-20261001` passes1/1: revision2 and exact replay, old-digest409, two different-key concurrent contenders at expected2 yielding one ordinal3 and one409, exact history1/2/3, getter/review/withdraw, foreign-book404 and agent-review403. Financial fingerprints and effective grants remain identical; UPDATE/DELETE remainfalse. The context repair is still pending at this prerequisite checkpoint.

Repeat the dedicated owner proof on isolated synthetic infrastructure:

```sh
umask 077
OPENERP_E2E_ARTIFACTS=test-results/context-expense-unique \
bun run test:e2e apps/api/tests/agent-context.e2e.test.ts \
-t 'expense immutable revision admission'
```

Artifacts preserve actual request keys/status/body, retained owner responses, financial-state witnesses, effective privileges and source/migration manifest/integrity. No unit tests, schema exceptions, live provider/company data, deployment or production action are part of this evidence.
