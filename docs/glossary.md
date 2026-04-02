# Glossary

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
  source_repo: saorsa-pqc
  source_ref: main
  source_commit: 280e5478954abeedf1a8193c599c3c9676a032ee
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

Canonical terms used throughout this docs set.

## A

**ant-client** — Direct Rust and CLI interface to the network via `ant-core` and the `ant` binary.

**ant-core** — Headless Rust library used by `ant` for direct network operations and local devnet helpers.

**ant-keygen** — ML-DSA-65 release-signing utility.

**ant-sdk** — Daemon-based developer interface built around `antd`, REST/gRPC APIs, and language SDKs.

**antd** — Local daemon that exposes REST on `http://localhost:8082` and gRPC on `localhost:50051` by default.

**ANT token** — Token used for storage payments in the current wallet-backed upload flows.

**Arbitrum** — EVM network family referenced by the current payment tooling and CLI network selection.

**Autonomi** — The network these repos target for decentralized storage and retrieval.

**Autonomi Network** — The peer-to-peer network reached through `antd`, `ant-core`, `ant`, and `ant-node`.

## B

**BLAKE3** — Hash function used in current content-addressing and self-encryption flows.

## C

**ChaCha20-Poly1305** — Authenticated encryption primitive used in the current self-encryption crate.

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

**NAT traversal** — Techniques used by the current transport layer to help peers connect across NAT boundaries.

## P

**pay-once** — Current docs shorthand for wallet-backed upload payment rather than an ongoing subscription model.

**post-quantum cryptography** — Cryptographic approach centered here on `saorsa-pqc`, `saorsa-transport`, and `ant-keygen`.

## Q

**QUIC** — Transport protocol used by the current network transport layer.

## S

**self-encryption** — Client-side content processing that returns a `DataMap` plus encrypted chunks.

## X

**XOR distance** — Distance metric used for peer and data proximity in Kademlia-style routing.
