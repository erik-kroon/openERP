# Raw JSON admission boundary

Before implementation, these are the failure modes to preserve/refuse:
- Duplicate keys (including escaped-equivalent keys) must not be silently replaced before REST/MCP schema validation.
- Check every nested object, including objects in arrays. The same key in distinct objects is valid.
- Quotes, backslashes, colons and braces inside string values are data, not structure. Embedded evidence JSON strings must remain byte-for-byte unchanged.
- Invalid UTF-8 must not be replacement-decoded into another command. Bound nesting before downstream JSON materialization.
- Invalid syntax still fails downstream JSON/schema decoding; this scanner is not a replacement JSON parser.
- Preserve streamed byte limits/timeouts and exact original request bytes. Better Auth non-JSON form handling remains owned by Better Auth.
- Do not print credentials, add test files/suites, dispatch a mutation, or treat a manual observation as whole-system acceptance.

Proposed decisive observation: send a duplicate-method MCP ping (no mutation) through the existing owned local Worker. Before the fix, native JSON parsing can choose the last method; after it, the boundary must return HTTP400 before dispatch. Repeat with escaped-equivalent keys and a valid ordinary ping. Record exact non-secret request bodies/status/result.

## Observed local result

The same duplicate-method MCP ping changed from HTTP200 (last member selected) to HTTP400 before dispatch. Escaped-equivalent keys, nested duplicates, invalid UTF-8 and129 containers were also refused. Distinct-object keys, quoted embedded JSON text and128 containers remained accepted. Exact harmless request bodies/results are in `openerp-implementation/manual-json-admission.json`. Earlier `/mcp` was the wrong path; observations use `/api/mcp` with the supported protocol header and an existing private token. No mutation was dispatched. API/script typecheck passed. No tests or fixtures were added.

The shared boundary leaves syntax/schema parsing to the normal adapters and retains original bytes. Non-JSON Better Auth form parsing is unchanged. This is not full protocol, auth, concurrency or company-accounting acceptance.
