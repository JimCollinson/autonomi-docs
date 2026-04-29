# Glossary

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 71f9e0fbdc6189e8fa0dc12887339ac52769b1ee
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 97587c248ce6410edc1c6ee28846216ef82145eb
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 23aee15cae33a17257ba833b2b98ed8a7a12e684
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-protocol
  source_ref: main
  source_commit: 87071931a982e8a90494353007a3f4e6ebb3de3c
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-core
  source_ref: main
  source_commit: ae3c607fec0882b80e37837143382e9c9687c316
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-transport
  source_ref: main
  source_commit: 9808c2782a5605a7cf728a4e2c756c4bf24eef40
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-pqc
  source_ref: main
  source_commit: 2ab931e2533f1df6aa446636fbcf6e95b5bf5a21
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-keygen
  source_ref: main
  source_commit: 3a2953f384a3b16391968de451b703843b98ed86
  verified_date: 2026-04-29
  verification_mode: current-merged-truth
-->

Canonical terms used throughout this docs set.

## A

**ant-client** — Direct Rust and CLI interface to the network via `ant-core` and the `ant` binary.

**ant-core** — Headless Rust library used by `ant` for direct network operations and local devnet helpers.

**ant-keygen** — ML-DSA-65 release-signing utility.

**ant-protocol** — Shared wire protocol crate used by `ant-core` and `ant-node` for chunk messages, payment proofs, and devnet manifests.

**ant-sdk** — Daemon-based developer interface built around `antd`, REST/gRPC APIs, and language SDKs.

**antd** — Local daemon that exposes REST on `http://localhost:8082` and gRPC on `localhost:50051` by default.

**Autonomi Network Token (ANT)** — Token used for storage payments.

**Arbitrum** — EVM network family used by payment tooling and CLI network selection.

**Autonomi** — The network these repos target for decentralized storage and retrieval.

**Autonomi Network** — The peer-to-peer network reached through `antd`, `ant-core`, `ant`, and `ant-node`.

## B

**BLAKE3** — Hash function used in content addressing and self-encryption flows.

## C

**ChaCha20-Poly1305** — Authenticated encryption primitive used in self-encryption.

**chunk** — Low-level stored unit of encrypted content.

**close group** — The set of nodes closest to a target address in XOR space.

**content addressing** — Deriving an address from content rather than from a mutable location.

## D

**DataMap** — Retrieval metadata that ties uploaded content back to its encrypted chunks.

## H

**HKDF** — Key-derivation primitive exposed by `saorsa-pqc`.

## K

**Kademlia DHT** — The distributed-hash-table model used for routing and lookup.

## L

**local trust scoring** — Local trust and response-rate style scoring rather than a network-wide shared reputation feed.

## M

**Merkle batch payment** — Batch-payment mode used for larger chunk sets.

**ML-DSA-65** — Post-quantum signature algorithm highlighted by the current transport and signing repos.

**ML-KEM-768** — Post-quantum key-encapsulation algorithm highlighted by the current transport docs.

## N

**NAT traversal** — Observed-address discovery and hole punching used to keep peers reachable across NAT boundaries. Relay fallback may be needed for some CGNAT cases.

## P

**pay-once** — Storage payment model where you pay when you upload and do not pay ongoing storage fees.

**post-quantum cryptography** — Cryptographic approach centered here on `saorsa-pqc`, `saorsa-transport`, and `ant-keygen`.

## Q

**QUIC** — UDP-based transport protocol used for peer connections and NAT traversal coordination.

## S

**self-encryption** — Client-side content processing that returns a `DataMap` plus encrypted chunks.

## X

**XOR distance** — Distance metric used for peer and data proximity in Kademlia-style routing.
