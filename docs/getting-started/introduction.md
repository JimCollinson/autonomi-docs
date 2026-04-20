# What is Autonomi?

Autonomi is a decentralized peer-to-peer network for permanent, immutable data storage. Data is encrypted before upload, stored using content-addressing, and paid for once when you write it to the network.

## What makes Autonomi different

At a high level, Autonomi gives you:

* immutable storage, where changing the content produces a new address instead of mutating the old one
* client-side encryption through self-encryption before chunks are stored on the network
* public and private retrieval paths through addresses and DataMaps
* pay-once storage, where you pay in Autonomi Network Token (ANT) when you upload and downloads are free
* post-quantum cryptography in the transport and security model

## Choose how you want to build

You can build on Autonomi through four main interfaces. Choose the one that matches how you want to work, then stay with that interface until you need something more advanced.

### SDK

This is the simplest integration model for most application developers.

`antd` runs as a local daemon on your machine. It exposes REST and gRPC endpoints, and SDKs are available in more than 15 languages.

Use the SDK if you want to build with Python, Node.js / TypeScript, Go, Rust, Java, C#, Kotlin, Swift, Ruby, PHP, Dart, Zig, or another supported SDK language.

### MCP

This is the best fit when you want AI tools to interact with Autonomi through structured tool calls.

The MCP server talks to `antd` for you, so your AI client can use the daemon without calling it directly.

Use MCP when you want AI-assisted storage and retrieval rather than a traditional application or shell workflow.

### CLI

The CLI gives you direct command-line access to uploads, downloads, chunk operations, wallet inspection, and node-management workflows.

Choose it when you want shell access, scripts, or a daemon-free operational workflow.

### Direct Rust

Direct Rust uses the native Rust library instead of the daemon.

Choose it when you want direct Rust control over networking, payment flows, and upload logic in your application.

## What to understand first

Start with these core concepts:

* [Data Types](../core-concepts/data-types.md)
* [Keys, Addresses, and DataMaps](../core-concepts/keys-addresses-and-datamaps.md)
* [Self-Encryption](../core-concepts/self-encryption.md)
* [Payment Model](../core-concepts/payment-model.md)
* [Post-Quantum Cryptography](../core-concepts/post-quantum-cryptography.md)

You do not need to understand every network detail before you store and retrieve data, but it helps to understand that uploads are content-addressed, immutable, and paid for at write time.

## Next steps

* [Build with the SDKs](install.md)
* [Use MCP with AI Tools](use-mcp-with-ai-tools.md)
* [Use the CLI](using-ant-client.md)
* [Build Directly in Rust](build-directly-in-rust.md)
* [GitHub](../github.md)
