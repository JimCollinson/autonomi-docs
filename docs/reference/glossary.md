# Glossary

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: bf541ccd4ae1fd3e174fb7b5bb21deef38d999ce
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 0b104d1e8e5a8dab08a24eeb8c81b25702548c96
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 5a5d7d4fed766cd56d0f97f337fcd5ff049bea6a
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-core
  source_ref: main
  source_commit: 50734d0416dce646da74f4477c9d4f46fa0cb969
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-transport
  source_ref: main
  source_commit: c34424efba78546ca08a4bf69382a7fc04aa2789
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-pqc
  source_ref: main
  source_commit: 1619cb2231db942cd65ab954ca0e0304dd6bc220
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-keygen
  source_ref: main
  source_commit: 3a2953f384a3b16391968de451b703843b98ed86
  verified_date: 2026-04-21
  verification_mode: current-merged-truth
-->

Canonical terms used throughout this docs set.

## A

**ant-client** — Direct Rust and CLI interface to the network via `ant-core` and the `ant` binary.

**ant-core** — Headless Rust library used by `ant` for direct network operations and local devnet helpers.

**ant-keygen** — ML-DSA-65 release-signing utility.

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

**NAT traversal** — Peer-observed address discovery, coordinator hints, hole punching, and optional UPnP-assisted address mapping used to keep peers reachable across NAT boundaries. Relay fallback may still be needed for some CGNAT cases.

## P

**pay-once** — Storage payment model where you pay when you upload and do not pay ongoing storage fees.

**post-quantum cryptography** — Cryptographic approach centered here on `saorsa-pqc`, `saorsa-transport`, and `ant-keygen`.

## Q

**QUIC** — UDP-based transport protocol used for peer connections, NAT traversal coordination, and relay-assisted fallback.

## S

**self-encryption** — Client-side content processing that returns a `DataMap` plus encrypted chunks.

## X

**XOR distance** — Distance metric used for peer and data proximity in Kademlia-style routing.
