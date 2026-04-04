# What is Autonomi?

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
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Autonomi is a decentralized peer-to-peer network for permanent, immutable data storage. Data is encrypted client-side before upload, and the network's transport and security model uses post-quantum cryptography. You pay in Autonomi Network Token (ANT) when you upload data, and the storage model is designed around pay-once uploads rather than ongoing storage fees.

## What makes it different

At a high level, Autonomi gives you:

- immutable data storage: changing the content produces a new address instead of mutating the old one
- client-side encryption through self-encryption before chunks are stored on the network
- public and private retrieval paths through addresses and DataMaps
- pay-once storage: you pay when you upload, and downloads are free

## Three ways to build on Autonomi

### 1. Build an app with the SDKs

This is the easiest starting point for most developers.

- `antd` runs as a local daemon on your machine
- it exposes REST and gRPC endpoints
- language SDKs talk to that daemon for you

Choose the SDKs if you want to build in Python, Node.js / TypeScript, Go, Rust, Java, C#, Kotlin, Swift, Ruby, PHP, Dart, Zig, or another supported SDK language.

### 2. Use the ant CLI

The CLI gives you direct command-line access to uploads, downloads, chunk operations, wallet inspection, and node-management workflows.

Choose it when you want shell access, automation scripts, or a daemon-free operational workflow.

### 3. Build in Rust with ant-core

This route uses `ant-core` instead of going through the daemon.

Choose it when you want native Rust control over networking, payment flows, and upload logic.

## What matters first as a developer

Start with these concepts:

- [Data Types](../core-concepts/data-types.md)
- [Self-Encryption](../core-concepts/self-encryption.md)
- [Payment Model](../core-concepts/payment-model.md)

You do not need to understand every network detail before storing and retrieving data, but you do need to understand that uploads are content-addressed, immutable, and paid for at write time.

## Next steps

- [Build with the SDKs](install.md)
- [Use the ant CLI](using-ant-client.md)
- [Build in Rust with ant-core](build-directly-in-rust.md)
