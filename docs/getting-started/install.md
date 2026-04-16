# Build with the SDKs

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-04
  verification_mode: current-merged-truth
-->

Use the SDKs when you want the easiest starting point for application development on Autonomi.

This route is built around:

- a local daemon called `antd`
- REST and gRPC interfaces exposed by that daemon
- language SDKs in Python, Node.js / TypeScript, Go, Rust, Java, C#, Kotlin, Swift, Ruby, PHP, Dart, Zig, and other supported languages

## Why use the SDKs

Choose the SDKs if you want:

- the easiest path into building an application on Autonomi
- a stable local API instead of direct peer-to-peer networking in your app
- one local daemon process that multiple apps, scripts, or tools can share
- SDK support in the language you already work in

## How this route works

`antd` runs on your machine and talks to the network for you. The SDKs, REST API, gRPC clients, and MCP server all build on that same local daemon.

If you would rather work directly from the terminal, use [the ant CLI](using-ant-client.md). If you want daemon-free Rust access, build in Rust with `ant-core` instead.

## What to do next

### 1. Using the Autonomi Daemon

Start with [Using the Autonomi Daemon](using-the-autonomi-daemon.md) to learn what `antd` is, how to install it, and how to verify that it is running.

### 2. Your first upload

Once the daemon is running, continue to [Your First Upload with the SDKs](hello-world.md).

### 3. Language-specific references

If you already know your target language, use the [Language Bindings](../sdk-reference/language-bindings/overview.md) section for setup and API details.

## Related pages

- [Using the Autonomi Daemon](using-the-autonomi-daemon.md)
- [Your First Upload with the SDKs](hello-world.md)
- [SDK Overview](../sdk-reference/overview.md)
