# Build with the SDKs

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-17
  verification_mode: current-merged-truth
-->

Use the SDKs when you want a simpler application integration model on Autonomi.

This approach combines:

- a local daemon called `antd`
- REST and gRPC interfaces exposed by that daemon
- language SDKs in Python, Node.js / TypeScript, Go, Rust, Java, C#, Kotlin, Swift, Ruby, PHP, Dart, Zig, and other supported languages

## Why use the SDKs

Choose the SDKs if you want:

- a local API between your application and the network
- a stable local API instead of direct peer-to-peer networking in your app
- one local daemon process that multiple apps, scripts, or tools can share
- SDK support in the language you already work in

## How the SDKs work

`antd` runs on your machine and talks to the network for you. The SDKs, REST API, gRPC clients, and MCP server all build on that same local daemon.

Your application code can still be Python, Node.js / TypeScript, Go, Rust, or another supported language. The supported `antd` install method in these docs is to build the daemon from the `ant-sdk` repo, then connect to it from the SDK language you choose.

If you would rather work directly from the terminal, use [the CLI](../cli/use-the-cli.md). If you want daemon-free Rust access, see [Build Directly in Rust](../rust/build-directly-in-rust.md).

## What to do next

### 1. Start the local daemon

Start with [Start the Local Daemon](start-the-local-daemon.md) to build `antd` from source, run it in read-only mode, and verify that it is healthy.

### 2. Retrieve data from the network

If you only need read-only features, continue to [Retrieve Data from the Network](retrieve-data-from-the-network.md).

### 3. Choose how you want to handle writes

If you need uploads after the read-only flow, choose one of these next steps:

- [Prepare a Wallet for Uploads](../guides/prepare-a-wallet-for-uploads.md) for daemon-signed writes on the default network
- [Use External Signers for Upload Payments](how-to-guides/use-external-signers-for-upload-payments.md) when your app should keep the signing key outside `antd`
- [Set Up a Local Network](../guides/set-up-a-local-network.md) if you want local services and test funds provisioned for you

### 4. Store data on the network

Once the daemon is running and you have set up writes, continue to [Store Data on the Network](store-data-on-the-network.md).

### 5. Language-specific references

If you already know your target language, use the [Language Bindings](../sdk/reference/language-bindings/overview.md) section for setup and API details.

## Related pages

- [Start the Local Daemon](start-the-local-daemon.md)
- [Retrieve Data from the Network](retrieve-data-from-the-network.md)
- [Prepare a Wallet for Uploads](../guides/prepare-a-wallet-for-uploads.md)
- [Use External Signers for Upload Payments](how-to-guides/use-external-signers-for-upload-payments.md)
- [Store Data on the Network](store-data-on-the-network.md)
- [SDK Overview](../sdk/reference/overview.md)
