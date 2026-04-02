# System Overview

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
  source_commit: 727a75c46bebc6d5948ea7754debd4220ead9400
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 8e9541b5bd5ae9791a1b9d037c62c76ff8a7d0c8
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-core
  source_ref: main
  source_commit: 6c5fb3cd67f621b4faeb9f6520a1498d3064b1d0
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-transport
  source_ref: main
  source_commit: a81dbb5bc3c7929537873c90e7a10678993d415e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-pqc
  source_ref: main
  source_commit: 280e5478954abeedf1a8193c599c3c9676a032ee
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->

This page gives a high-level view of how the main developer-facing and network-facing repos fit together.

## High-level architecture

```text
Application
  |                         Rust / CLI
  | REST or gRPC                |
  v                             v
 antd                      ant-core / ant
  |                             |
  +-------------+---------------+
                |
                v
             ant-node
                |
                v
            saorsa-core
                |
                v
         saorsa-transport
                |
                v
            Autonomi peers
```

## Developer interfaces

The main developer entry points are:

- `ant-sdk`, centered on the `antd` daemon plus language SDKs
- `ant-client`, centered on `ant-core` and the `ant` CLI

These interfaces target the same network, but one uses a local daemon and the other connects directly from Rust or CLI code.

## Network and node layer

The current `ant-node` crate is a thin wrapper around `saorsa-core::P2PNode`. It adds configuration, chunk storage, payment verification, upgrade handling, and node runtime management on top of the core P2P layer.

In the repos used for this page, `ant-node` documents chunk storage as its active network data type.

## Routing and transport

`saorsa-core` provides the P2P node, DHT, bootstrap handling, and trust system. `saorsa-transport` provides QUIC transport, NAT traversal, and the documented pure post-quantum transport layer centered on ML-KEM-768 and ML-DSA-65.

## Data path

On the client side, `self_encryption` turns uploaded content into a `DataMap` plus encrypted chunks. Higher-level tools then store or retrieve those chunks through `antd`, `ant-core`, or `ant-node` depending on which layer you are working in.

## Related pages

- [Core Concepts Overview](../core-concepts/overview.md)
- [SDK Overview](../sdk-reference/overview.md)
- [CLI Overview](../cli-reference/overview.md)
- [Developing in Rust](../rust-reference/overview.md)
