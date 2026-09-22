# HTTP and observability

## Shared API definitions

Use the existing `HttpApi` in `packages/contracts/src/api.ts`. Define endpoint inputs, outputs, and safe errors there. Implement the group with `HttpApiBuilder.group` in `apps/api`, compose its layers at the API boundary, and expose OpenAPI from that same definition.

Use `HttpRouter.toWebHandler` for the Worker adapter. It returns a `handler` and `dispose`; tie application-resource disposal to the host lifecycle rather than disposing a shared application after every request. Supply request-specific context to the handler instead of caching actor or book identity globally.

Keep handlers focused on authentication, decoding, invoking the owning operation, and HTTP response semantics. Derive identity and book access on the trusted side. A body field, hidden UI action, or supplied book ID is not proof of permission.

Use Effect's `HttpRouter` for special HTTP semantics such as cookies, signed callbacks, streaming, and multipart requests. Make dispatch method-aware and preserve signature verification over the required bytes. Do not introduce another HTTP framework for a new route.

## First-party browser calls

Build the client from the shared definition with `HttpApiClient.make`. The existing system query illustrates the integration:

```ts
import { Api } from "@open-erp/contracts/api";
import { queryOptions } from "@tanstack/react-query";
import * as Effect from "effect/Effect";
import { FetchHttpClient } from "effect/unstable/http";
import { HttpApiClient } from "effect/unstable/httpapi";

const readStatus = Effect.fn("ApiClient.readStatus")(function* (origin: string) {
  const client = yield* HttpApiClient.make(Api, { baseUrl: origin });
  return yield* client.system.status();
});

export const statusQuery = (origin: string) => queryOptions({
  queryKey: ["system", "status"],
  queryFn: ({ signal }) => Effect.runPromise(
    readStatus(origin).pipe(
      Effect.timeout("10 seconds"),
      Effect.provide(FetchHttpClient.layer),
    ),
    { signal },
  ),
  retry: 1,
});
```

This Promise conversion is the TanStack Query adapter boundary, not a backend workflow. Do not copy it as a second system query; reuse the existing owner. Resolve the origin in the caller's environment. Do not access `window` during server rendering or forward authentication to a caller-supplied origin.

Share query options between route loading and components when both load the same data. Keep a request-scoped QueryClient, include entity/book identity in scoped keys, and pass cancellation to the Effect execution. The example's retry is for a read; mutations need their own repetition and recovery contract.

## Outbound provider HTTP

Inside Effect programs, use `HttpClient` from `effect/unstable/http`. Provide `FetchHttpClient.layer` where the host supplies Fetch. Its requests participate in Effect interruption; avoid a parallel timer/AbortController implementation.

Check status before treating the body as success. `HttpClient.filterStatusOk` rejects non-success statuses; explicit status mapping is useful when the provider has distinct retryable and terminal responses. Decode the response with the provider schema and map transport/decoding failures at the adapter boundary.

Use bounded timeouts and retries only for the actual provider contract. Consider response loss and repeated side effects. Raw Fetch or Promise ports can remain appropriate at an external SDK or non-Effect platform boundary; that does not justify using them throughout owned Effect workflows.

## Logs, spans, and Worker lifetime

- Use named `Effect.fn` operations and `Effect.log*` for useful diagnostics. Avoid a span per row or duplicate spans around the same operation.
- Annotate bounded IDs, operation names, counts, durations, and safe outcomes. Do not log tokens, raw evidence, journal descriptions, provider bodies, or arbitrary causes containing customer data.
- Record request diagnostics separately from durable accounting history and receipts. A successful log entry does not prove a committed transaction.
- Compose logger/tracer layers into the runtime that executes the operation. A separate default runtime does not inherit them.
- Reuse the configured telemetry. Add an exporter only when required; inspect `effect/unstable/observability` and the host's flush/lifetime support first. Do not import Sellfinity's logging stack as a prerequisite.
- Distinguish expected business rejections from unexpected system failure in telemetry. Follow the configured tracer's semantics rather than changing span status by convention.
- A buffered exporter in a short-lived Worker needs an explicit flush path supported by the platform. Neither a detached fiber nor a timer guarantees delivery after the request ends.

Effect fibers, Layers, and retries operate within a running process. Work that must survive a Worker restart needs persisted state and a real recovery mechanism; do not describe an in-memory Effect as durable execution.
