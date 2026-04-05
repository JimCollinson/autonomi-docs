# Build a Read-Only Application

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-05
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 796d0df75d748419a004aec6f5e288b41d8b496e
  verified_date: 2026-04-05
  verification_mode: current-merged-truth
-->

Build a read-only Autonomi application when you only need to retrieve data that has already been stored and paid for.

## Why this matters

Read-only systems are simpler than upload-enabled systems.

If your application only reads public data:

- you do not need ANT
- you do not need gas
- you do not need a wallet
- you do not need upload permissions

That can make retrieval-only tools, dashboards, or content browsers much easier to build and operate.

## Prerequisites

- A known public address to retrieve
- One of these routes:
  - SDKs through `antd`
  - the `ant` CLI
  - native Rust with `ant-core`

## Steps

### 1. Choose the route you want to use

For SDKs and the local daemon:

- [Build with the SDKs](../getting-started/install.md)
- [Using the Autonomi Daemon](../getting-started/using-the-autonomi-daemon.md)

For the CLI:

- [Use the ant CLI](../getting-started/using-ant-client.md)

For native Rust:

- [Build in Rust with ant-core](../getting-started/build-directly-in-rust.md)

### 2. Retrieve public data

For the SDK route:

```bash
curl http://localhost:8082/v1/data/public/<address>
```

For the CLI route:

```bash
ant --bootstrap 1.2.3.4:12000 chunk get <address>
```

For native Rust, use the retrieval APIs in `ant-core` after connecting to the network client.

### 3. Keep wallet setup out of your architecture unless you also upload

If your application only reads public data, it does not need:

- `AUTONOMI_WALLET_KEY`
- `SECRET_KEY`
- token approvals
- upload payment flows

That means you can keep the architecture focused on retrieval and content handling instead of wallet management.

## Verify it worked

Your read-only application is configured correctly when it can retrieve the expected content from a known address without any wallet setup.

## Common errors

**404 Not Found**: Check the address.

**Trying to use private retrieval without a DataMap**: Private content still requires the retrieval metadata even though the content has already been paid for.

**Adding wallet complexity unnecessarily**: Public retrieval alone does not require wallet configuration.

## Next steps

- [Store and Retrieve Data with the SDKs](store-and-retrieve-data.md)
- [Payment Model](../core-concepts/payment-model.md)
- [Use the ant CLI](../getting-started/using-ant-client.md)
