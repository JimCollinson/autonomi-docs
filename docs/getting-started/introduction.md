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
  source_commit: 1fb95f03f8010db60e4b1e9a26957b3bb2acd8bc
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d164c895f8609754c6ff2a8faf99375695276
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

Autonomi is the network these repos target for storing, retrieving, and managing data through either a local daemon (`antd`) or direct Rust/CLI access (`ant-core` and `ant`).

## How it works at a high level

When you use the current merged developer interfaces, the flow looks like this:

1. Your application or CLI submits data through `antd` or directly through `ant-core`
2. The content is self-encrypted into a `DataMap` plus encrypted chunks
3. Write operations use wallet-backed payment flows
4. The resulting address or DataMap is used later for retrieval

## The two current developer paths

### `ant-sdk`

`ant-sdk` is the daemon-based path.

- `antd` exposes REST on `http://localhost:8082`
- `antd` exposes gRPC on `localhost:50051`
- language SDKs wrap that daemon surface

This is the easiest starting point for most application development.

### `ant-client`

`ant-client` is the direct Rust and CLI path.

- `ant-core` connects to the network directly
- `ant` exposes file, chunk, wallet, and node-management commands

This path is useful when you want direct Rust control or CLI-based workflows.

## What matters first as a developer

The current docs set is organized around the concepts that show up in the merged toolchain today:

- [Data Types](../core-concepts/data-types.md)
- [Self-Encryption](../core-concepts/self-encryption.md)
- [Payment Model](../core-concepts/payment-model.md)

You do not need to understand every network detail before storing and retrieving data, but you do need to understand which surface you are using and how it handles addresses, DataMaps, and payments.

## Next steps

- [Install antd](install.md)
- [Your First Upload](hello-world.md)
- [Using ant-client](using-ant-client.md)
