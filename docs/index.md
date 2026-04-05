# Introduction

{% hint style="warning" %}
This is preview documentation for Autonomi 2.0 ahead of the planned network launch on 7 April 2026. Content is under active review and may change before launch.
{% endhint %}

Autonomi is a decentralized peer-to-peer network for permanent, immutable data storage. Data is encrypted before upload, stored using content-addressing, and paid for once at upload.\
\
These guides will help you get started building with the Autonomi Network!

## How to build on Autonomi

You can build on Autonomi in several ways, from SDKs in more than 15 languages through a local daemon that exposes REST and gRPC, to direct CLI access, to native Rust with `ant-core`.

### Build with the SDKs

Use the SDKs if you want the easiest starting point for application development in Python, Node.js / TypeScript, Go, Rust, Java, C#, Kotlin, Swift, Ruby, PHP, Dart, Zig, and other supported languages.

A daemon called `antd` running on the users machine, exposing REST and gRPC endpoints giving your application a stable REST and gRPC interface to the network.

Start with [Build with the SDKs](getting-started/install.md), then [Using the Autonomi Daemon](getting-started/using-the-autonomi-daemon.md), then [Your First Upload with the SDKs](getting-started/hello-world.md).

### Use the CLI

[Use the ant CLI ](getting-started/using-ant-client.md)when you want direct shell access for uploads, downloads, wallet checks, chunk operations, or node-management workflows.

### Build in directly in Rust

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
