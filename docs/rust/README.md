# Developing in Rust

<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 71ad53b047f7fc6b55e73ce6008d0a834feebbd6
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

Rust gives you two supported ways to build on Autonomi.

## Choose how you'll work in Rust

### Rust through the SDK daemon

Use the Rust SDK when you want Rust code to talk to `antd` just like the other SDK languages do.

Choose the Rust SDK if you want:

- the same daemon-based model used by Python, Node.js / TypeScript, Go, and the other SDKs
- REST or gRPC access through a stable local gateway
- a Rust app that fits into the broader SDK workflow

See [Rust SDK](../sdk/reference/language-bindings/rust.md).

### Native Rust with ant-core

Use `ant-core` when you want direct, daemon-free Rust access to networking, uploads, and payment flows.

Choose native Rust with ant-core if you want:

- direct control over the network client in Rust
- no daemon process between your code and the network
- access to native Rust types, local devnet helpers, and direct client tuning such as loopback and timeout control

See [Build Directly in Rust](build-directly-in-rust.md) and [Rust Library Reference](library-reference.md).

## How the two Rust paths differ

| | Rust SDK | `ant-core` |
|---|---|---|
| Interface model | daemon-based | direct Rust library |
| Network access | through `antd` | direct |
| Good fit | SDK-style app development | native Rust control |
| Closest equivalent | Python / Node.js / TypeScript SDKs | no daemon equivalent |

## Upstream sources

- [ant-sdk](https://github.com/WithAutonomi/ant-sdk)
- [ant-client](https://github.com/WithAutonomi/ant-client)

## Related pages

- [Build Directly in Rust](build-directly-in-rust.md)
- [Rust SDK](../sdk/reference/language-bindings/rust.md)
- [Rust Library Reference](library-reference.md)
