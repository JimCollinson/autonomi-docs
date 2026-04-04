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
  source_commit: 796d0df75d748419a004aec6f5e288b41d8b496e
  verified_date: 2026-04-04
  verification_mode: current-merged-truth
-->

Autonomi is a decentralized peer-to-peer network for permanent, immutable data storage. Data is encrypted client-side before upload, and the network's transport and security model uses post-quantum cryptography. You pay once in Autonomi Network Token (ANT) when you upload data, then retrieve it later with a public address or a DataMap.

## Choose your path

### Build an app with the SDKs

Use the SDKs if you want a local daemon plus SDKs in Python, Node.js / TypeScript, Go, Rust, Java, C#, Kotlin, Swift, Ruby, PHP, Dart, Zig, and other supported languages. `antd` runs on your machine and exposes REST and gRPC so your application can talk to Autonomi through a stable local API.

Start with [Build with the SDKs](getting-started/install.md), then [Your First Upload with the SDKs](getting-started/hello-world.md).

### Use the ant CLI

Use the CLI when you want direct shell access to the network for uploads, downloads, wallet checks, chunk operations, or node-management workflows.

Start with [Use the ant CLI](getting-started/using-ant-client.md).

### Build in Rust with ant-core

Build in Rust with `ant-core` when you want daemon-free, programmatic control over networking, payments, and uploads.

Start with [Build in Rust with ant-core](getting-started/build-directly-in-rust.md).

## Core ideas

- [Data Types](core-concepts/data-types.md)
- [Self-Encryption](core-concepts/self-encryption.md)
- [Payment Model](core-concepts/payment-model.md)

## Reference material

- [REST API](sdk-reference/rest-api.md)
- [Daemon Command Reference](sdk-reference/daemon-cli.md)
- [CLI Command Reference](cli-reference/command-reference.md)
- [Rust Library Reference](cli-reference/ant-core-library.md)
