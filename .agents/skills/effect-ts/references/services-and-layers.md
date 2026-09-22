# Services and layers

Define dependencies with `Context.Service`. Use a domain-specific interface when it improves clarity or has multiple consumers; a small inline service contract is also valid. The runtime identifier must be unique and should name its owning package/module.

```ts
import * as Context from "effect/Context";
import * as Effect from "effect/Effect";
import * as Layer from "effect/Layer";
import * as Redacted from "effect/Redacted";

export interface ProviderConfiguration {
  readonly baseUrl: string;
  readonly token: Redacted.Redacted<string>;
}

export class ProviderConfig extends Context.Service<ProviderConfig, ProviderConfiguration>()(
  "@open-erp/api/ProviderConfig",
) {}

export const providerConfigLayer = (configuration: ProviderConfiguration) =>
  Layer.succeed(ProviderConfig, configuration);

export const providerOrigin = Effect.fn("Provider.origin")(function* () {
  const configuration = yield* ProviderConfig;
  return configuration.baseUrl;
});
```

The example supplies configuration; it does not prescribe a new provider integration. Keep services near the operation or adapter they support.

## Construction

- `Layer.succeed` provides a value that already exists.
- `Layer.effect` acquires an implementation through an Effect and owns scoped resources acquired during construction.
- `Context.Service` does not automatically create an implementation or default layer. A static `layer` or a clearly named local layer is sufficient.
- Yield the service to access its methods. Explicit `Service.use(...)` access is also valid; do not create forwarding accessors without a caller need.

When using an inline `make` option in the class base, avoid referring back to the class from that same inference expression. Return an object checked with `satisfies` against the service interface, or move construction to an explicitly typed Effect. `Service.of(...)` is valid after the class exists. Do not impose a separate interface file or one file per function.

## Composition and sharing

Use `Layer.mergeAll` for independent layers. Use `Layer.provide` to satisfy a consumer's dependencies; use `Layer.provideMerge` when those provided services also need to remain available in the output context.

Reuse the same layer value when a resource should be shared within a layer build. Layer memoization is based on identity within the build/memo map; reconstructing equivalent layers does not guarantee one resource. Separate runtimes do not automatically share a layer instance or resource lifetime.

Compose at the API entrypoint. Keep book scope, actor identity, transaction state, and request-specific bindings in the request context or operation arguments. Never capture the first request's mutable identity in a globally memoized layer.

## Configuration and secrets

Read and validate Cloudflare bindings at the runtime boundary, then provide the required services or a suitable `ConfigProvider`. Use the installed `Config` APIs for process configuration when applicable. Do not scatter `process.env` reads through services or assume a Bun process environment exists in a Worker.

Keep credentials redacted within owned configuration and unwrap them only at the driver/provider boundary. Never include the unwrapped value in errors, logs, span attributes, or returned contracts.

Use `Context.Reference` only for values with a legitimate default. Missing database credentials, identity, or book authorization must not silently receive a permissive default. Handle configuration failure at the runtime boundary according to its actual failure contract; do not turn every configuration problem into a defect by convention.

For database resources, follow the repository's selected adapter. Establish connection ownership, one-connection transaction scope, cancellation behavior, and cleanup in the deployed runtime before relying on the adapter. A Layer is dependency management, not persistence or a transaction.
