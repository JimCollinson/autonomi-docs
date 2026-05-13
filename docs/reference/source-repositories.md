# Source Repositories

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
  source_commit: 91d5f18e3fbf5125fc6b5bbc46bb0a1fe6356ae8
  verified_date: 2026-05-13
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-node
  source_ref: main
  source_commit: 8b68b2d7f4662faf67ed7812dc6cb37de0c74a8b
  verified_date: 2026-05-13
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-protocol
  source_ref: main
  source_commit: 93e63b8a41a97c37c24d1164a3ee5525e002ddcd
  verified_date: 2026-05-13
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-core
  source_ref: main
  source_commit: 5f482af334b4703a78f9a051b38fd79d5478c607
  verified_date: 2026-05-13
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: saorsa-transport
  source_ref: main
  source_commit: 7d02af138f4b9ea77239a908837ad3cc56366d73
  verified_date: 2026-05-13
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
  source_repo: evmlib
  source_ref: main
  source_commit: 225acbb1af613193bcc8264b6ede4d7e4a7ac607
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->
<!-- verification:
  source_repo: ant-merkle
  source_ref: master
  source_commit: 80af80a5df1e26e3b6fb386d041178889c4ed993
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

This docs set is assembled from the active source repositories below. If you want to inspect the implementation directly, start with these repos.

## WithAutonomi

- [`WithAutonomi`](https://github.com/WithAutonomi) — Main GitHub organization for the current Autonomi developer-facing repos
- [`ant-sdk`](https://github.com/WithAutonomi/ant-sdk) — `antd`, language SDKs, local dev tooling, and `antd-mcp`
- [`ant-client`](https://github.com/WithAutonomi/ant-client) — Direct CLI and native Rust path: `ant`, `ant-core`, and local devnet tooling
- [`ant-node`](https://github.com/WithAutonomi/ant-node) — Node runtime, chunk storage, payment verification, and replication behavior
- [`ant-protocol`](https://github.com/WithAutonomi/ant-protocol) — Shared wire protocol crate for chunk messages, payment proofs, and devnet manifests
- [`self_encryption`](https://github.com/WithAutonomi/self_encryption) — Client-side self-encryption crate used for content processing before network storage
- [`evmlib`](https://github.com/WithAutonomi/evmlib) — EVM payment helpers used by the daemon, CLI, and direct Rust flows
- [`ant-merkle`](https://github.com/WithAutonomi/ant-merkle) — Merkle batch payment contracts and proof structures used by larger upload batches
- [`ant-keygen`](https://github.com/WithAutonomi/ant-keygen) — ML-DSA-65 release-signing utility

## saorsa-labs

- [`saorsa-labs`](https://github.com/saorsa-labs) — Supporting transport, networking, and cryptography repos used by the current Autonomi stack
- [`saorsa-core`](https://github.com/saorsa-labs/saorsa-core) — Core peer-to-peer node, DHT, routing, and trust system
- [`saorsa-transport`](https://github.com/saorsa-labs/saorsa-transport) — QUIC transport, NAT traversal, relay-assisted connectivity, and post-quantum transport layer
- [`saorsa-pqc`](https://github.com/saorsa-labs/saorsa-pqc) — Post-quantum cryptography library used by the broader stack

## How to use these links

Use these repos when you want to:

- inspect the implementation behind a documented interface
- follow a tool or crate in more detail
- review upstream changes alongside the docs
- understand how the different parts of the Autonomi stack fit together

For a docs-first view of how the stack fits together, start with [System Overview](../architecture/system-overview.md).
