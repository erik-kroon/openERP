# Functions and resources

Use `Effect.gen` for a composed program and `Effect.fn` for named effectful operations. A meaningful name provides a tracing boundary. Use `Effect.fnUntraced` when an additional span would add noise, such as a per-row helper. Keep pure calculations as ordinary functions.

```ts
import * as Clock from "effect/Clock";
import * as Effect from "effect/Effect";

export const checkedAt = Effect.fn("System.checkedAt")(function* () {
  return yield* Clock.currentTimeMillis;
});
```

Additional arguments to `Effect.fn` transform the returned Effect and can receive the original call arguments. Apply `.pipe(...)` to an Effect value, not to the function returned by `Effect.fn`. Standalone `Effect.gen(...)` programs support `.pipe(...)` normally.

Use `return yield* Effect.fail(error)` or `return yield* error` for a terminal failure so TypeScript can narrow the remaining path. Use `Effect.gen({ self: this }, function* () { ... })` only when the generator actually requires `this`.

## External synchronous and Promise APIs

- Use `Effect.sync` for a synchronous action whose exceptions are defects.
- Use `Effect.try({ try, catch })` when a synchronous boundary can fail in an expected way.
- Use `Effect.tryPromise({ try: (signal) => sdkCall(signal), catch })` for Promise APIs with expected failures. Pass the signal when the SDK supports cancellation; mapping a Promise into Effect does not make an uncancellable SDK cancellable.
- Keep service methods Effect-returning. Promise conversion belongs at framework or runtime entrypoints. Do not call `Effect.runPromise` inside an Effect workflow.
- Prefer the Effect HTTP client for owned outbound HTTP; see [HTTP and observability](http-and-observability.md).

Use `Clock.currentTimeMillis` for the current instant inside Effect. Use the installed `DateTime` APIs when time zones or calendar arithmetic are required. A date-only accounting value is a separate domain concept, not an instant to infer from the machine's timezone.

## Sequencing and concurrency

Use `Effect.forEach` for independent per-item effects and choose an explicit finite concurrency bound for external work. Use `Effect.all` for a fixed set of independent effects. Keep dependent or ordered work sequential.

An imperative loop is appropriate for pagination, early returns, or state-dependent stopping conditions. Do not change those semantics to fit a collection combinator. Native array methods are appropriate for pure data transformations.

Choose shared-state tools for their actual purpose:

- `Ref` for shared in-process Effect state.
- `Deferred` for one eventual result shared by fibers.
- `Semaphore` for bounded access within one runtime.

None of these coordinates separate Worker isolates or makes database writes atomic. Use the owning database transaction and persisted constraints for that boundary.

## Resource and fiber lifetime

Use `Effect.acquireRelease` to pair acquisition with a finalizer, and `Effect.scoped` or a resource-owning Layer to delimit its lifetime. Register cleanup as soon as a resource exists, including resources whose connection/setup can subsequently fail. Preserve the original failure when handling cleanup errors; report relevant cleanup failures without exposing credentials.

Select the fiber lifetime deliberately:

- `Effect.forkChild` follows the parent fiber.
- `Effect.forkScoped` follows its Scope.
- `Effect.forkIn` attaches to an explicit Scope.
- `Effect.forkDetach` is detached in-process work, not a durable job.

Do not detach required writes or external delivery, or hide their failures with `Effect.ignore`. A Worker can end after the response. Await request-critical work; use the platform lifetime mechanism for bounded permitted background work, and persisted admission plus recovery for work that must survive termination.

Place timeouts around the intended operation. A timeout inside retry bounds each attempt; outside retry it bounds the whole sequence. Retry only explicitly transient failures, with a finite budget and a command contract that makes repetition safe.
