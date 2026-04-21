# What is Autonomi?

Autonomi is a decentralized peer-to-peer network for permanent, immutable data storage. Data is encrypted before upload, stored using content-addressing, and paid for once when you write it to the network.

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

## Core concepts

- [Data Types](core-concepts/data-types.md)
- [Keys, Addresses, and DataMaps](core-concepts/keys-addresses-and-datamaps.md)
- [Self-Encryption](core-concepts/self-encryption.md)
- [Payment Model](core-concepts/payment-model.md)
- [Post-Quantum Cryptography](core-concepts/post-quantum-cryptography.md)

## Go deeper

- [System Overview](architecture/system-overview.md)
- [Source Repositories](reference/source-repositories.md)
