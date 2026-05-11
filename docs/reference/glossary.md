# Glossary

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 529280c32c024c92b68436abb6ace956c8da66ba
  verified_date: 2026-05-11
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-client
  source_ref: main
  source_commit: 6cada1d6b318a93e52ea6c34aa4b68fc2782c946
  verified_date: 2026-05-11
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 0c2f2c97aa0b7a2f1000aaa4a3a2a2d629da4e5d
  verified_date: 2026-05-11
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-protocol
  source_ref: main
  source_commit: 8955144bd2473d1bb5f3b6753061eb104b552070
  verified_date: 2026-05-11
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-core
  source_ref: main
  source_commit: db94fe0e7d0209b619caab576d747288ac0cc935
  verified_date: 2026-05-11
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-transport
  source_ref: main
  source_commit: 5d2408e1fd394570f993529a610cb8c76f493952
  verified_date: 2026-05-11
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-pqc
  source_ref: main
  source_commit: 2ab931e2533f1df6aa446636fbcf6e95b5bf5a21
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: self_encryption
  source_ref: master
  source_commit: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-keygen
  source_ref: main
  source_commit: 3a2953f384a3b16391968de451b703843b98ed86
  verified_date: 2026-05-02
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

**BLAKE3** — Cryptographic hash used for content addresses and for self-encryption chunk hashing.

## C

**ChaCha20-Poly1305** — Authenticated encryption primitive used in self-encryption.

**chunk** — Low-level stored unit of encrypted content.

**close group** — The set of nodes closest to a target address in XOR space.

**content addressing** — Deriving an address from content rather than from a mutable location.

## D

**DataMap** — Retrieval metadata that ties uploaded content back to its encrypted chunks.

## E

**external signer** — Wallet or signing flow that submits upload-payment transactions without giving `antd` or `ant-core` direct custody of the private key.

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

**NAT traversal** — Peer-observed address discovery, coordinator hints, hole punching, and optional UPnP-assisted address mapping used to keep peers reachable across NAT boundaries. Relay-assisted fallback handles cases where direct traversal still fails.

## P

**pay-once** — Storage payment model where you pay when you upload and do not pay ongoing storage fees.

**post-quantum cryptography** — Cryptographic approach used here for transport key exchange, transport identity, and release signing. Content self-encryption remains a separate BLAKE3 plus ChaCha20-Poly1305 layer.

## Q

**QUIC** — UDP-based transport protocol used for peer connections, NAT traversal coordination, and relay-assisted fallback.

## S

**self-encryption** — Client-side content processing that returns a `DataMap` plus encrypted chunks.

## X

**XOR distance** — Distance metric used for peer and data proximity in Kademlia-style routing.
