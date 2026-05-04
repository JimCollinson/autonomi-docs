# How Language Bindings Work

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

The language bindings in `ant-sdk` are clients for the `antd` daemon. They share the same daemon surface, but they do not expose identical constructors, transports, or helper APIs.

## Architecture

Each binding translates language-native inputs into requests to `antd`, then maps daemon responses back into that language's models and errors.

The pattern is:

1. your application talks to a language client
2. the language client talks to `antd`
3. `antd` talks to the Autonomi network through `ant-core`

## Defaults

The daemon defaults are:

- REST: `http://localhost:8082`
- gRPC: `localhost:50051`

Bindings usually default to those same endpoints when you do not supply an override.

## Transport Split

- JavaScript and TypeScript are documented as REST-based
- Python, Go, and Rust document both REST and gRPC support
- other bindings vary by package and docs coverage

Check the individual page before assuming a transport is available in your language.

## Discovery helpers

Several bindings include daemon discovery helpers based on the `daemon.port` file written by `antd` on startup.

Examples from the current packages:

- JavaScript: `RestClient.autoDiscover()`
- Python: `discover_daemon_url()` and `discover_grpc_target()`
- Go: `NewClientAutoDiscover()`
- Rust: `discover_daemon_url()` and `discover_grpc_target()`

Some bindings use discovery only through explicit helper APIs rather than by default constructors.

## Naming Differences

The bindings use different entry points:

| Language | Current entry point |
|------|------|
| JavaScript | `createClient()` or `new RestClient(...)` |
| TypeScript | `createClient()` with exported types from the same `antd` package |
| Python | `AntdClient()` / `AsyncAntdClient()` |
| Go | `NewClient(...)` |
| Rust | `Client::new(...)` from the `antd-client` crate |

Use the package-specific page when you need exact constructors, install commands, or transport notes.

## Related pages

- [Python SDK](python.md)
- [JavaScript SDK](javascript.md)
- [TypeScript SDK](typescript.md)
- [Rust SDK](rust.md)
- [Go SDK](go.md)
- [REST API](../rest-api.md)
