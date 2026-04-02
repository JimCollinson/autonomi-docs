# Autonomi Developer Documentation

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 1fb95f03f8010db60e4b1e9a26957b3bb2acd8bc
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Autonomi is a decentralized, encrypted, content-addressed network for permanent, immutable data storage. You pay once when you upload data, then retrieve it later with a public address or a DataMap.

## Choose your path

### Build an app with the SDKs

Use the SDK path if you want a local daemon plus SDKs in Python, JavaScript, TypeScript, Go, Rust, Java, C#, Kotlin, Swift, Ruby, PHP, Dart, Zig, and other supported languages. `antd` runs on your machine and exposes REST and gRPC so your application can talk to Autonomi through a stable local API.

Start with [Build with the SDKs](getting-started/install.md), then [Your First Upload with the SDKs](getting-started/hello-world.md).

### Use the ant CLI

Use the CLI when you want direct shell access to the network for uploads, downloads, wallet checks, chunk operations, or node-management workflows.

Start with [Use the ant CLI](getting-started/using-ant-client.md).

### Build directly in Rust

Use the direct Rust path when you want daemon-free, programmatic control over networking, payments, and uploads with `ant-core`.

Start with [Build Directly in Rust](getting-started/build-directly-in-rust.md).

## Core ideas

- [Data Types](core-concepts/data-types.md)
- [Self-Encryption](core-concepts/self-encryption.md)
- [Payment Model](core-concepts/payment-model.md)

## Reference material

- [REST API](sdk-reference/rest-api.md)
- [Daemon CLI: antd](sdk-reference/daemon-cli.md)
- [Command Reference](cli-reference/command-reference.md)
