# Build Read-Only Features

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-17
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: d46a73d38731a31fbd9815394fe8a2943eb38246
  verified_date: 2026-04-17
  verification_mode: current-merged-truth
-->

Build read-only Autonomi features when you only need to retrieve data that has already been stored and paid for.

This guide compares the SDK, CLI, and direct Rust ways to build read-only retrieval features so you can choose the right read-only architecture for your application.

## Why this matters

Read-only features are simpler than upload-enabled ones.

If your application only reads data that has already been written to the network:

- you do not need ANT
- you do not need gas
- you do not need a wallet
- you do not need upload permissions

That can make retrieval-only tools, dashboards, content browsers, and other read-heavy features much easier to build and operate.

## Prerequisites

- A known public address to retrieve, or a `DataMap` for private data
- One of these routes:
  - SDKs through `antd`
  - the `ant` CLI
  - native Rust with `ant-core`

If you do not already have an address or `DataMap`, create one first by following [Store and Retrieve Data with the SDKs](../sdk/how-to-guides/store-and-retrieve-data.md) or by storing data through the CLI or direct Rust.

## Steps

### 1. Choose the interface you want to use

With the SDK:

- [Build with the SDKs](../sdk/install.md)
- [Start the Local Daemon](../sdk/start-the-local-daemon.md)
- [Retrieve Data from the Network](../sdk/retrieve-data-from-the-network.md)

With the CLI:

- [Use the CLI](../cli/use-the-cli.md)

With Direct Rust:

- [Build Directly in Rust](../rust/build-directly-in-rust.md)

### 2. Retrieve public or private data

For public data, you need a public address.

For private data, you need the `DataMap` or equivalent private retrieval material.

With the SDK, `antd` can run without `AUTONOMI_WALLET_KEY` when you only need retrieval.

Public retrieval through the daemon:

```bash
curl http://localhost:8082/v1/data/public/<address>
```

Private retrieval through the daemon:

```bash
curl "http://localhost:8082/v1/data/private?data_map=<hex_encoded_datamap>"
```

The private retrieval response is JSON with the content returned as base64 in the `data` field.

With the CLI, public and private file retrieval use `ant file download` with either a public address or a local `.datamap` file:

```bash
ant file download <public_address> -o downloaded.bin --bootstrap 1.2.3.4:12000
ant file download --datamap my_data.bin.datamap -o downloaded.bin --bootstrap 1.2.3.4:12000
```

For native Rust, use the retrieval APIs in `ant-core` after connecting to the network client.

### 3. Keep wallet setup out of your architecture unless you also upload

If your application only reads data that has already been stored, it does not need:

- `AUTONOMI_WALLET_KEY`
- `SECRET_KEY`
- token approvals
- upload payment flows

That means you can keep the architecture focused on retrieval and content handling instead of wallet management.

## Verify it worked

Your read-only feature is configured correctly when it can retrieve the expected content from a known public address or private `DataMap` without any wallet setup.

## Common errors

**404 Not Found**: Check the address.

**Trying to use private retrieval without a DataMap**: Private content still requires the retrieval metadata even though the content has already been paid for.

## Next steps

- [Store and Retrieve Data with the SDKs](../sdk/how-to-guides/store-and-retrieve-data.md)
- [Payment Model](../core-concepts/payment-model.md)
- [Use the CLI](../cli/use-the-cli.md)
