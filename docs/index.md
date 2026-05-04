# What is Autonomi?

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 71ad53b047f7fc6b55e73ce6008d0a834feebbd6
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-transport
  source_ref: main
  source_commit: 9808c2782a5605a7cf728a4e2c756c4bf24eef40
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

Autonomi is a decentralized peer-to-peer network for permanent, immutable data storage. Data is encrypted before upload, stored using content addressing, and paid for once when you write it to the network.

## What makes Autonomi different

At a high level, Autonomi gives you:

- immutable storage, where changing the content produces a new address instead of mutating the old one
- client-side encryption through self-encryption before chunks are stored on the network
- public and private retrieval through addresses and DataMaps
- pay-once storage, where you pay in Autonomi Network Token (ANT) when you upload and downloads are free
- post-quantum cryptography in the transport and security model

## How you can build on Autonomi

You can work with Autonomi in four main ways.

### SDK

Use the SDK when you want to build an application in Python, Node.js / TypeScript, Go, Rust, Java, C#, Kotlin, Swift, Ruby, PHP, Dart, Zig, or another supported language.

The SDK uses a local daemon called `antd`, which exposes REST and gRPC and keeps the network-facing work out of your application.

Start with [Build with the SDKs](sdk/install.md).

### MCP

Use the MCP server when you want an AI tool such as Claude Desktop, Claude Code, or another MCP-compatible client to interact with Autonomi through structured tools.

The MCP server also talks to `antd`, but it presents Autonomi through an AI-tool interface rather than through language bindings.

Start with [Use MCP with AI Tools](mcp/use-mcp-with-ai-tools.md).

### CLI

Use the CLI when you want direct shell access for uploads, downloads, wallet checks, chunk operations, or node-management workflows.

Start with [Use the CLI](cli/use-the-cli.md).

### Developing in Rust

Build directly in Rust when you want in-process control over networking, uploads, and downloads without using `antd`.

Start with [Developing in Rust](rust/README.md).

## Build with an AI coding tool

If you are working in Claude Code or another AI coding tool, install the [Autonomi Developer Skill](developer-skill.md). It gives your tool a verified, focused guide to building on Autonomi, so it picks the right path, uses real APIs, and avoids common mistakes.

## Core concepts

- [Data Types](core-concepts/data-types.md)
- [Keys, Addresses, and DataMaps](core-concepts/keys-addresses-and-datamaps.md)
- [Self-Encryption](core-concepts/self-encryption.md)
- [Payment Model](core-concepts/payment-model.md)
- [Post-Quantum Cryptography](core-concepts/post-quantum-cryptography.md)

## Go deeper

- [System Overview](architecture/system-overview.md)
- [Source Repositories](reference/source-repositories.md)
