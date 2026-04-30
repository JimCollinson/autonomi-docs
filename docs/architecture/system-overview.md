# System Overview

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 8b2c9c606a1223f105fed9aa2b56310b6a6763da
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 23aee15cae33a17257ba833b2b98ed8a7a12e684
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-protocol
  source_ref: main
  source_commit: 65651f3a3243af8299a3e8d63385cba846ef88a4
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-core
  source_ref: main
  source_commit: a3fd6eaedb8a7d6a8e4bbeeeebe07426bb9f6bc6
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-transport
  source_ref: main
  source_commit: 9808c2782a5605a7cf728a4e2c756c4bf24eef40
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-pqc
  source_ref: main
  source_commit: 2ab931e2533f1df6aa446636fbcf6e95b5bf5a21
  verified_date: 2026-04-30
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  verified_date: 2026-04-30
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

The `ant-node` crate builds on `saorsa-core::P2PNode`. It adds configuration, chunk storage, payment verification, replication, upgrade handling, and node runtime management on top of the core P2P layer.

`ant-core` and `ant-node` also share wire-message types, payment-proof types, and devnet manifest types through `ant-protocol`.

In the repos used for this page, `ant-node` documents chunk storage as its active network data type.

## Routing and transport

`saorsa-core` provides the P2P node, DHT, bootstrap handling, trust system, and routing-table logic around typed addresses and peer identity. It is also responsible for publishing dialable self-addresses and coordinator hints into DHT records. `saorsa-transport` provides QUIC transport, NAT traversal, address discovery, and relay fallback where direct hole punching is not enough.

The transport story includes:

- observed-address discovery and address propagation across the network
- reachability tracking by scope: loopback, local-network, or global
- best-effort UPnP port mapping as an extra public candidate on compatible routers
- peer-ID-based hole-punch coordination, with coordinator hints and coordinator rotation when one path cannot help
- relay fallback for some CGNAT cases
- QUIC-based post-quantum transport security centered on ML-KEM-768 and ML-DSA-65

That post-quantum framing applies to transport identity and session establishment. Content self-encryption remains a separate client-side layer built around BLAKE3 and ChaCha20-Poly1305.

## Data path

On the client side, `self_encryption` turns uploaded content into a `DataMap` plus encrypted chunks. Developer-facing clients such as `antd` and `ant-core` prepare and retrieve that content, while `ant-node` stores and serves chunk data across the network.

## Upstream sources

- [ant-sdk](https://github.com/WithAutonomi/ant-sdk)
- [ant-client](https://github.com/WithAutonomi/ant-client)
- [ant-node](https://github.com/WithAutonomi/ant-node)
- [ant-protocol](https://github.com/WithAutonomi/ant-protocol)
- [self_encryption](https://github.com/WithAutonomi/self_encryption)
- [saorsa-core](https://github.com/saorsa-labs/saorsa-core)
- [saorsa-transport](https://github.com/saorsa-labs/saorsa-transport)
- [saorsa-pqc](https://github.com/saorsa-labs/saorsa-pqc)

## Related pages

- [Core Concepts Overview](../core-concepts/overview.md)
- [SDK Overview](../sdk/reference/overview.md)
- [Using the Autonomi CLI](../cli/use-the-cli.md)
- [Developing in Rust](../rust/README.md)
