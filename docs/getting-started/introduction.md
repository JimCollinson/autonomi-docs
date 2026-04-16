# What is Autonomi?

Autonomi is a decentralized peer-to-peer network for permanent, immutable data storage. Data is encrypted before upload, stored using content-addressing, and paid for once when you write it to the network.

## What makes Autonomi different

At a high level, Autonomi gives you:

* immutable storage, where changing the content produces a new address instead of mutating the old one
* client-side encryption through self-encryption before chunks are stored on the network
* public and private retrieval paths through addresses and DataMaps
* pay-once storage, where you pay in Autonomi Network Token (ANT) when you upload and downloads are free
* post-quantum cryptography in the transport and security model

## Ways to build on Autonomi

You can build on Autonomi in several ways.

### Build an app with the SDKs

This is the easiest starting point for most developers.

`antd` runs as a local daemon on your machine. It exposes REST and gRPC endpoints, and SDKs are available in more than 15 languages.

Choose this route if you want to build with Python, Node.js / TypeScript, Go, Rust, Java, C#, Kotlin, Swift, Ruby, PHP, Dart, Zig, or another supported SDK language.

### Use the ant CLI

The CLI gives you direct command-line access to uploads, downloads, chunk operations, wallet inspection, and node-management workflows.

Choose it when you want shell access, scripts, or a daemon-free operational workflow.

### Build in Rust with ant-core

This route uses the native Rust library instead of the daemon.

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
* [Using the Autonomi Daemon](using-the-autonomi-daemon.md)
* [Use the ant CLI](using-ant-client.md)
* [Build in Rust with ant-core](build-directly-in-rust.md)
* [GitHub](../github.md)
