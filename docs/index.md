# Introduction

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 71f9e0fbdc6189e8fa0dc12887339ac52769b1ee
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 97587c248ce6410edc1c6ee28846216ef82145eb
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 23aee15cae33a17257ba833b2b98ed8a7a12e684
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->

Autonomi is a decentralized peer-to-peer network for permanent, immutable data storage. Data is encrypted before upload, stored using content addressing, and paid for once at upload.

These guides will help you get started building with the Autonomi Network!

## How to build on Autonomi

You can build on Autonomi in several ways, from SDKs in more than 15 languages through a local daemon that exposes REST and gRPC, to direct CLI access, to native Rust with `ant-core`.

### Build with the SDKs

Use the SDKs if you want the easiest starting point for application development in Python, Node.js / TypeScript, Go, Rust, Java, C#, Kotlin, Swift, Ruby, PHP, Dart, Zig, and other supported languages.

`antd` runs on your machine and exposes REST and gRPC endpoints, giving your application a stable local interface to the network.

Start with [Build with the SDKs](getting-started/install.md), then [Using the Autonomi Daemon](getting-started/using-the-autonomi-daemon.md), then [Your First Upload with the SDKs](getting-started/hello-world.md).

### Use the CLI

[Use the ant CLI](getting-started/using-ant-client.md) when you want direct shell access for uploads, downloads, wallet checks, chunk operations, or node-management workflows.

### Build directly in Rust

Build in Rust without the daemon when you want direct programmatic control over networking, uploads, and payments in your application.

Start with [Build in Rust with ant-core](getting-started/build-directly-in-rust.md).

## Core Concepts

* [Data Types](core-concepts/data-types.md)
* [Keys, Addresses, and DataMaps](core-concepts/keys-addresses-and-datamaps.md)
* [Self-Encryption](core-concepts/self-encryption.md)
* [Payment Model](core-concepts/payment-model.md)
* [Post-Quantum Cryptography](core-concepts/post-quantum-cryptography.md)

## Reference

* [REST API](sdk-reference/rest-api.md)
* [SDK Overview](sdk-reference/overview.md)
* [CLI Command Reference](cli-reference/command-reference.md)
* [Rust Library Reference](cli-reference/ant-core-library.md)
* [MCP Server Reference](sdk-reference/mcp-server.md)

## Go Deeper

* [System Overview](architecture/system-overview.md)
* [GitHub](github.md)
