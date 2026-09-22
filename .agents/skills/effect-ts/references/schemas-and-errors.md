# Schemas and errors

Shared input/output validation belongs in `packages/contracts`, using `effect/Schema`. Reuse those contracts in the API and browser client. Parse untrusted values at their boundary and keep trusted internal values typed afterward.

## New schema definitions

Use `Schema.Struct` for plain records. Use `Schema.Class` when a class has an actual modeling benefit; construct a class instance before handing it to a class encoder. A matching plain object is not necessarily an encodable class instance.

```ts
import * as Schema from "effect/Schema";

export const ImportSource = Schema.Struct({
  name: Schema.String.check(Schema.isMinLength(1), Schema.isMaxLength(200)),
  description: Schema.optional(Schema.String),
  format: Schema.Literals(["csv", "json"]),
});
```

Use `.check(...)` with the installed `Schema.is*` filters. `Schema.Union`, `Schema.Tuple`, and `Schema.Literals` take arrays. Use `Schema.NullOr` when the field must exist but can contain `null`.

Add brands when two otherwise identical primitive types must not be confused. Validate and construct them through their owning schemas; do not bypass validation with a type assertion or add generic brand factories without repeated need.

## Optionality and decoding

`Schema.optionalKey(S)` permits an absent key, but a present value must satisfy `S`. If `S` does not accept `undefined`, an explicitly present `undefined` fails. `Schema.optional(S)` also accepts explicit `undefined`.

Choose based on both incoming data and JavaScript construction/encoding sites. Use `optional` when callers intentionally pass `field: maybeUndefined`; use `optionalKey` when omission is the intended contract. Do not treat the choice as formatting.

- `Schema.decodeUnknownEffect` gives an Effect with a typed decoding failure.
- `Schema.decodeUnknownResult` gives a synchronous result to inspect explicitly.
- `Schema.decodeUnknownOption` is appropriate only when losing the failure detail is intentional.
- `Schema.decodeUnknownSync` throws; keep it at boundaries whose caller handles that behavior.

Do not turn invalid required rows into missing rows by filtering failed decodes. For exact monetary values or large integer identifiers, retain the contract's exact representation. Do not coerce values through JavaScript `number` merely to simplify a schema.

The installed release has both `Schema.Codec` and `Schema.Decoder`. For a generic schema parameter, preserve its decoding/encoding services in the type and confirm the installed signature rather than forcing `never` with a cast.

## Expected failures

Use schema-backed errors for values crossing a wire boundary, and `Data.TaggedError` for internal typed failures that do not need serialization. In the installed release the schema constructor is `Schema.TaggedError`:

```ts
import * as Schema from "effect/Schema";

export class SourceUnavailable extends Schema.TaggedError<SourceUnavailable>()(
  "SourceUnavailable",
  { message: Schema.String },
  { httpApiStatus: 503 },
) {}
```

Reuse the owning contract's error taxonomy. Register the error and its HTTP semantics in the endpoint contract. Keep raw driver failures, SQL details, stacks, credentials, and document content out of the wire error. Avoid class field names such as `pipe` that shadow inherited methods.

Use `return yield* error` or `return yield* Effect.fail(error)` for expected failure. Preserve specific error types. Use `Effect.catchTag` or `Effect.catchTags` for known recovery; use `Effect.catch` only when all remaining typed failures share the intended handling.

Logging a failure is not recovery. If the operation must remain failed, use an observation combinator such as `Effect.tapError` or re-fail after translating it. Do not return an empty list, default record, or success receipt after an unknown failure.

Distinguish transient provider failure from permanent rejection before adding retry. A lost response from a write may mean the write succeeded; recover using the operation's persisted identity rather than blindly issuing a new command.

## Defects and interruption

Defects represent unexpected bugs or broken internal assumptions. Keep them distinct from caller-visible validation, denial, conflict, and temporary unavailability. Observe unexpected causes at the runtime boundary without swallowing interruption or declaring success.

In this release, `Cause` contains a flat `reasons` array. Prefer supported selectors such as `Cause.findErrorOption`, `Cause.isFailReason`, and `Cause.hasInterrupts` over manually assuming a cause representation. Recheck the installed module when cause inspection is required.
