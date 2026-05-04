# Changelog - Autonomi Developer Skill

All notable changes to this skill are recorded here.

## [Unreleased]

## [0.1.3-draft] - 2026-05-02

### Changed
- Re-verified the skill against current upstream source heads. No prose changes.
- Refreshed the pinned `ant-client` commit to track an internal payment-quote BLAKE3 peer-ID binding fix in `ant-core/src/data/client/quote.rs` (and a new typed `Error::BadQuoteBinding` variant). The fallback `Err(error) => ...` arm in the Direct Rust error-handling example still covers it.

### Verified Against
- ant-sdk: d7652ec3da82dfbe2107778e5223dc413d95815b
- ant-client: 71ad53b047f7fc6b55e73ce6008d0a834feebbd6
- ant-node: 23aee15cae33a17257ba833b2b98ed8a7a12e684
- ant-protocol: 65651f3a3243af8299a3e8d63385cba846ef88a4
- self_encryption: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
- evmlib: 225acbb1af613193bcc8264b6ede4d7e4a7ac607

## [0.1.2-draft] - 2026-04-30

### Changed
- Reverified the skill against the current docs layout and current upstream source heads.
- Added `ant-protocol` to the skill's verification scope for protocol-adjacent operational guidance.
- Refreshed SDK guidance to point at the current file-cost endpoint and current shared prepare/finalize semantics.
- Updated the maintenance guide to match the current component mapping and re-verification triggers.
- Refreshed the pinned `ant-client` and `ant-protocol` verification commits and clarified `LocalDevnet::create_funded_client(...)` in the Direct Rust playbook.

### Verified Against
- ant-sdk: d7652ec3da82dfbe2107778e5223dc413d95815b
- ant-client: 8b2c9c606a1223f105fed9aa2b56310b6a6763da
- ant-node: 23aee15cae33a17257ba833b2b98ed8a7a12e684
- ant-protocol: 65651f3a3243af8299a3e8d63385cba846ef88a4
- self_encryption: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
- evmlib: 225acbb1af613193bcc8264b6ede4d7e4a7ac607

## [0.1.1-draft] - 2026-04-30

### Changed
- Moved the skill from `skills/autonomi-developer/` to `skills/start/` so the namespaced slash form is `/developer:start` instead of `/autonomi-developer:autonomi-developer`. Plugin identifier is now `developer` and the marketplace identifier is `withautonomi`. Internal `name:` and `skill:` fields and canonical URLs updated to match.

## [0.1.0-draft] - 2026-04-22

### Added
- Initial in-repo `autonomi-developer` skill package.
- Operational path selector for SDK, CLI, Direct Rust, and MCP work.
- Exact golden flows for daemon health, SDK public data round-trip, CLI public file round-trip, and local devnet startup checks.
- Live reference table for the current docs site.
- Skill version manifest and maintenance guide.

### Changed
- Rebuilt the skill around the current docs and current upstream source artifacts instead of the earlier standalone draft.
- Reduced deep network internals so the skill stays focused on building and shipping applications.

### Verified Against
- ant-sdk: 2ed9b14bda42fbdc604a173cc1af27be0964908f
- ant-client: b0c501a163c1a95bdbfc703892b88a8a91f7e482
- ant-node: 5a5d7d4fed766cd56d0f97f337fcd5ff049bea6a
- self_encryption: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
- evmlib: 82f2fccff243b48de0e04ceb71ccb2aa17d810af
