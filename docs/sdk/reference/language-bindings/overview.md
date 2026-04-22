# How Language Bindings Work

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->

The language bindings in `ant-sdk` are clients for the `antd` daemon. They share the same daemon surface, but they do not currently expose identical constructors, transports, or helper APIs.

## Architecture

Each binding translates language-native inputs into requests to `antd`, then maps daemon responses back into that language's models and errors.

The pattern is:

1. your application talks to a language client
2. the language client talks to `antd`
3. `antd` talks to the Autonomi network through `ant-core`

## Current defaults

The daemon defaults are:

- REST: `http://localhost:8082`
- gRPC: `localhost:50051`

Bindings usually default to those same endpoints when you do not supply an override.

## Current transport split

At this commit:

- JavaScript and TypeScript use REST
- Python supports REST and gRPC
- Go supports REST and gRPC
- Rust supports REST and gRPC

Check the individual page before assuming a transport is available in your language.

## Discovery helpers

Several bindings include daemon discovery helpers based on the `daemon.port` file written by `antd` on startup.

Examples from the current packages:

- JavaScript: `RestClient.autoDiscover()`
- Python: `discover_daemon_url()` and `discover_grpc_target()`
- Go: `NewClientAutoDiscover()`
- Rust: `discover_daemon_url()` and `discover_grpc_target()`

Some bindings use discovery only through explicit helper APIs rather than by default constructors.

## Current naming differences

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
