# Autonomi 2.0 Developer Documentation — Information Architecture

**Document Status**: Information Architecture Design — structural guide only; page specifics must be re-audited against current merged truth
**Target Launch**: April 7, 2026
**Site Root**: docs.autonomi.com/developers
**Sync Source**: GitHub repo (GitBook auto-synced, llms.txt/llms-full.txt auto-generated)
**Estimated Page Count**: ~45 pages (includes 15 lightweight per-language binding pages)

**Operational note**: This file defines site structure and page intent. It is not a source-of-truth document. If any brief, example, or product-surface claim in this file conflicts with `CLAUDE.md` or `planning/verification-workflow.md`, the source-of-truth docs win.

**Route note**: The live docs tree later moved to the route-first layout under `docs/sdk/`, `docs/mcp/`, `docs/cli/`, `docs/rust/`, `docs/guides/`, and `docs/reference/`. Use `docs/SUMMARY.md`, `repo-registry.yml`, and `component-registry.yml` for the current path layout.

---

## REVISION NOTES

### v4 (April 2, 2026) — updated to match repo state

14. **data-model.md renamed to data-types.md** — Restructured from a network-internals framing ("Chunks and DataMaps") to a practical developer-first framing ("Data Types"). The rewritten page must describe the current developer-visible data types on merged refs. Chunks and content addressing stay as supporting context.
15. **Audience and objectives added to CLAUDE.md** — Explicit section defining primary audiences (human developers + AI agents), primary objectives (store, retrieve, build, integrate), and priority hierarchy (practical usage over network internals).
16. **Language binding pages finalised** — 14 per-language pages (Python, JavaScript, Rust, Go, TypeScript, Java, C#, Kotlin, Swift, Ruby, PHP, C++, Dart, Zig) plus a bindings overview. Replaces earlier cython.md and jvm.md with dart.md and zig.md.
17. **All 44 pages drafted** — Every page in the IA now has real content following CLAUDE.md templates and terminology lockfile. All pages verified against lockfile.

### v2/v3 (March 31, 2026) — changes from v1

1. **Archives removed** — Not shipping for April 7. Chunks/DataMaps covered in data model overview.
2. **Decentralisation/permanence** — Moved into Getting Started introduction, not a standalone core concept. Developers don't need to study this before building.
3. **Network topology, QUIC, Trust** — Moved out of Core Concepts into Architecture. These are implementation details, not prerequisites for development.
4. **FAQ removed** — No real developer questions to draw from yet. Will build post-launch from actual support/feedback.
5. **Troubleshooting removed** — No operational experience with v2. Risk of speculative content that doesn't reflect reality.
6. **Examples section removed** — Code examples embedded inline in how-to guides instead. No standalone gallery.
7. **Integration patterns removed** — Would need to be written from scratch. Parked for post-launch.
8. **ant-sdk is the primary interface** — ant-client treated as advanced/Rust-specific alternative, not an equal peer.
9. **Language bindings** — Binding coverage remains part of the IA, but each binding page must be verified individually against the current exported package surface. The REST API remains the primary shared reference where the bindings target the same daemon surface.
10. **Node operator guide** — Human "run a node" guide stays in existing Node section. Developer "embed a node programmatically" covered as a how-to guide here.
11. **Architecture** — Trimmed to a single system overview page for launch. Links to repo docs for deeper dives.
12. **Ed25519/TLS resolved** — saorsa-pqc v0.5.1 removed all classical crypto. PQC page can document pure ML-DSA-65/ML-KEM-768.
13. **Language bindings approach revised (v3)** — REST API with cURL examples remains the canonical shared reference. Per-language pages are lightweight (install + init + one example), but their constructors, types, transports, and packaging must be verified individually before publication.

---

## 1. DESIGN PRINCIPLES

### Audience & Use Cases
1. **Human developers** (sequential reading, learning flow)
   - New to decentralised storage, Autonomi-curious
   - Want to get from "Hello World" to production ready
   - Will read top-to-bottom, jump to API reference as needed

2. **AI agents** (semantic search + page-level fetch)
   - Will request specific pages via llms.txt index
   - Need self-contained pages (no "see previous chapter" dependencies)
   - Parse GEO-chunked Markdown with clear headers/sections
   - Extract code examples, architecture diagrams, verification targets

### Structure Strategy
- **Diátaxis framework** (proven pattern): Getting Started → Core Concepts → How-to Guides → Reference
- **One concept per page**: Allows clean LLM ingestion and hyperlink navigation
- **Hierarchical but flat**: Max 3 levels deep; each page is a distinct URL
- **ant-sdk first**: ant-sdk is the primary developer interface; ant-client is documented as advanced/Rust alternative
- **Verification trails**: Every page notes which repo/code it's verified against
- **Launch scope**: ~30 pages of verified, accurate content. Better to ship fewer pages that are correct than many that are speculative.

---

## 2. DIRECTORY STRUCTURE

```
docs/
├── index.md                                    # Landing page
├── getting-started/
│   ├── introduction.md                         # What is Autonomi + why decentralised/permanent
│   ├── install.md                              # Install ant-sdk (primary path)
│   ├── hello-world.md                          # First upload with ant-sdk
│   └── using-ant-client.md                     # Alternative: Rust/CLI path (brief)
├── core-concepts/
│   ├── overview.md                             # Conceptual landscape map
│   ├── data-types.md                            # Data types: public/private data, Pointers, Scratchpads, GraphEntries, Archives, Registers, Vaults
│   ├── self-encryption.md                      # ChaCha20-Poly1305 + BLAKE3
│   ├── post-quantum-cryptography.md            # ML-DSA-65, ML-KEM-768 (pure PQC, no classical)
│   ├── key-derivation.md                       # HKDF, master keys, child keys
│   └── payment-model.md                        # ANT token, pay-once, Merkle batch payments
├── how-to-guides/
│   ├── setup-local-network.md
│   ├── store-and-retrieve-data.md
│   ├── manage-keys.md
│   ├── handle-payments.md
│   ├── run-as-daemon.md
│   ├── use-external-signers.md
│   ├── test-your-application.md
│   ├── deploy-to-mainnet.md
│   └── embed-a-node.md                         # Programmatic node management for developers
├── sdk-reference/
│   ├── overview.md                             # ant-sdk architecture (daemon + REST/gRPC + thin clients)
│   ├── rest-api.md                             # REST endpoint reference (canonical, with cURL examples)
│   ├── grpc-services.md                        # gRPC service reference
│   ├── daemon-cli.md                           # antd command reference
│   └── language-bindings/
│       ├── overview.md                         # How bindings work (thin REST/gRPC clients, auto-discovery)
│       ├── python.md                           # Install + init + example (P0)
│       ├── javascript.md                       # Install + init + example (P0)
│       ├── rust.md                             # Install + init + example (P0 — uses ant-core, not REST)
│       ├── go.md                               # Install + init + example (P0)
│       ├── typescript.md                       # Install + init + example (P1)
│       ├── java.md                             # Install + init + example (P1)
│       ├── csharp.md                           # Install + init + example (P1)
│       ├── kotlin.md                           # Install + init + example (P2 — FFI, mobile)
│       ├── swift.md                            # Install + init + example (P2 — FFI, mobile)
│       ├── ruby.md                             # Install + init + example (P2)
│       ├── php.md                              # Install + init + example (P2)
│       ├── cpp.md                              # Install + init + example (P2)
│       ├── dart.md                              # Install + init + example (P2)
│       └── zig.md                              # Install + init + example (P2)
├── cli-reference/
│   ├── overview.md                             # ant-client overview (Rust/advanced)
│   ├── command-reference.md                    # ant CLI commands
│   └── ant-core-library.md                     # Rust library API
├── architecture/
│   └── system-overview.md                      # 10,000-foot view; links to repo docs
├── glossary.md
├── SUMMARY.md                                  # GitBook navigation file
└── .gitbook.yaml                               # GitBook sync config
```

---

## 3. SUMMARY.md (GitBook Navigation)

```markdown
# Summary

## Developer Documentation

- [Introduction](index.md)

## Getting Started

- [What is Autonomi?](getting-started/introduction.md)
- [Installing ant-sdk](getting-started/install.md)
- [Your First Upload](getting-started/hello-world.md)
- [Using ant-client (Rust / CLI)](getting-started/using-ant-client.md)

## Core Concepts

- [Overview](core-concepts/overview.md)
- [Data Types](core-concepts/data-types.md)
- [Self-Encryption](core-concepts/self-encryption.md)
- [Post-Quantum Cryptography](core-concepts/post-quantum-cryptography.md)
- [Key Derivation](core-concepts/key-derivation.md)
- [Payment Model](core-concepts/payment-model.md)

## How-To Guides

- [Set Up a Local Network](how-to-guides/setup-local-network.md)
- [Store and Retrieve Data](how-to-guides/store-and-retrieve-data.md)
- [Manage Keys and Wallets](how-to-guides/manage-keys.md)
- [Handle Payments](how-to-guides/handle-payments.md)
- [Run as a Daemon](how-to-guides/run-as-daemon.md)
- [Use External Signers](how-to-guides/use-external-signers.md)
- [Test Your Application](how-to-guides/test-your-application.md)
- [Deploy to Mainnet](how-to-guides/deploy-to-mainnet.md)
- [Embed a Node in Your Application](how-to-guides/embed-a-node.md)

## SDK Reference

- [ant-sdk Overview](sdk-reference/overview.md)
- [REST API](sdk-reference/rest-api.md)
- [gRPC Services](sdk-reference/grpc-services.md)
- [Daemon CLI: antd](sdk-reference/daemon-cli.md)
- **Language Bindings**
  - [How Bindings Work](sdk-reference/language-bindings/overview.md)
  - [Python](sdk-reference/language-bindings/python.md)
  - [JavaScript](sdk-reference/language-bindings/javascript.md)
  - [Rust](sdk-reference/language-bindings/rust.md)
  - [Go](sdk-reference/language-bindings/go.md)
  - [TypeScript](sdk-reference/language-bindings/typescript.md)
  - [Java](sdk-reference/language-bindings/java.md)
  - [C#](sdk-reference/language-bindings/csharp.md)
  - [Kotlin](sdk-reference/language-bindings/kotlin.md)
  - [Swift](sdk-reference/language-bindings/swift.md)
  - [Ruby](sdk-reference/language-bindings/ruby.md)
  - [PHP](sdk-reference/language-bindings/php.md)
  - [C++](sdk-reference/language-bindings/cpp.md)
  - [Dart](sdk-reference/language-bindings/dart.md)
  - [Zig](sdk-reference/language-bindings/zig.md)

## CLI Reference (ant-client)

- [ant-client Overview](cli-reference/overview.md)
- [Command Reference](cli-reference/command-reference.md)
- [ant-core Rust Library](cli-reference/ant-core-library.md)

## Architecture

- [System Overview](architecture/system-overview.md)

## Additional Resources

- [Glossary](glossary.md)
```

---

## 4. PER-PAGE BRIEFS

### SECTION: Getting Started

#### getting-started/introduction.md
**Title**: What is Autonomi?
**Purpose**: Answer "what is this system?" at a glance. Covers the decentralisation and permanence pitch here rather than as a separate concept page, since developers need context but not a deep study of decentralisation theory before they can start building.
**Covers**:
- One-sentence pitch: permanent, decentralised storage network
- Key properties: self-encryption, post-quantum ready, pay once retrieve free
- What "decentralised" means for a developer: no central server, data replicated across nodes, no single point of failure
- What "permanent" means: once stored, data persists as long as the network is live; immutable content addressing
- Primary interface: ant-sdk (daemon + REST/gRPC + language bindings)
- Alternative: ant-client (Rust CLI + library, for advanced/Rust developers)
- High-level flow: install → store → retrieve → pay
- Link to rest of docs

**Does NOT Cover**: Technical details of encryption, payment math, network topology (see Core Concepts and Architecture)

**Verification Against**: Autonomi conceptual guide (architecture overview section)

**LLM Note**: Short page (500–600 words); establishes vocabulary for downstream pages. Self-contained enough for an LLM to understand "what is Autonomi" from this page alone.

---

#### getting-started/install.md
**Title**: Installing ant-sdk
**Purpose**: Get ant-sdk running locally; minimal setup. This is the primary installation path.
**Covers**:
- Prerequisites: OS (Linux, macOS, Windows), required software
- Installation methods: Package manager (brew, apt, cargo), Docker, source build
- Verify installation: `antd --version`, daemon startup test
- Troubleshooting: Common issues (port conflict, daemon won't start)
- Next steps: "Run Your First Upload"

**Does NOT Cover**: ant-client installation (see Using ant-client page), advanced configuration

**Verification Against**: ant-sdk repo (install docs, CI/CD scripts)

**LLM Note**: Step-by-step; code examples for each OS.

---

#### getting-started/hello-world.md
**Title**: Your First Upload
**Purpose**: Working example in 5–10 minutes; builds confidence and validates setup. Uses ant-sdk as the default path.
**Covers**:
- Goal: Store a single text file, retrieve it, verify content
- Prerequisites: ant-sdk installed, daemon running
- Step-by-step:
  1. Start daemon
  2. Choose a language (Python example primary, others linked)
  3. Initialize client
  4. Upload text to network
  5. Retrieve by address
  6. Verify content integrity
- What happened: Brief explanation of self-encryption, chunking, network storage
- Next steps: Learn core concepts, try more operations, add payments

**Does NOT Cover**: Payment mechanics, key management, advanced features

**Verification Against**: ant-sdk examples, verified working code

**LLM Note**: Actual working code; verify it runs with each SDK release.

---

#### getting-started/using-ant-client.md
**Title**: Using ant-client (Rust / CLI)
**Purpose**: Brief introduction to the alternative interface for Rust developers or those wanting direct network access. Not a full getting-started flow — a concise "here's how this differs and when you'd use it" page with install + basic example.
**Covers**:
- When to use ant-client instead of ant-sdk: Rust project, direct network access, no daemon overhead, CLI scripting
- Install: `cargo install ant-client` or build from source
- Basic example: Store and retrieve via CLI
- Basic example: Same via ant-core Rust library
- Key differences from ant-sdk: No daemon, no REST/gRPC, Rust-only
- Link to CLI Reference for full command documentation

**Does NOT Cover**: Full CLI reference, Rust API deep dive (see CLI Reference section)

**Verification Against**: ant-client repo README, CLI help output

**LLM Note**: Keep brief — this is a secondary path. Most developers should use ant-sdk.

---

### SECTION: Core Concepts

#### core-concepts/overview.md
**Title**: Core Concepts Overview
**Purpose**: Map the conceptual landscape; help readers know what to study next.
**Covers**:
- Storage model: Permanent, content-addressed, encrypted at rest
- Cryptography: Self-encryption (ChaCha20-Poly1305), post-quantum (ML-DSA-65, ML-KEM-768), key derivation (HKDF)
- Data organization: Chunks (4MB max), DataMaps
- Payments: ANT token on Arbitrum, pay-once model, batch Merkle payments
- Developer interfaces: ant-sdk (primary) and ant-client (Rust/advanced)
- Reading guide: Suggested order based on use case

**Does NOT Cover**: Deep dives on any single topic (see linked pages)

**Verification Against**: Autonomi conceptual guide (full)

**LLM Note**: Index/navigation page; links to all core concept pages.

---

#### core-concepts/data-types.md
**Title**: Data Types
**Purpose**: Describe the data types developers can store on the network, from a practical "what can I do?" perspective. This is the primary reference for understanding Autonomi's data model as a developer.
**Covers**:
- Summary table: all data types at a glance (mutable?, max size, typical use)
- Public data: content-addressed, readable by anyone with the address
- Private data: chunks stored on network, DataMap held by client only
- Pointer: mutable reference to another address, stable URL-like indirection
- Scratchpad: mutable 4MB slot for single-owner data (profiles, state)
- GraphEntry: immutable 32-byte DAG node for linked data structures and append-only logs
- High-level types: Archive (directory/collection), Register (CRDT-like mutable via GraphEntry chain + Pointer), Vault (encrypted private data organizer)
- Under the hood: brief explanation of chunks, content addressing, DataMaps — supporting context, not primary framing
- API examples for each type

**Does NOT Cover**: Self-encryption pipeline details (see Self-Encryption), payment mechanics (see Payment Model), network topology (see Architecture)

**Verification Against**: ant-sdk and ant-client data type implementations, V1 data types documentation for continuity

**LLM Note**: Developer-first framing. A developer should be able to choose the right data type from this page alone. Network internals are "under the hood" context, not the lead.

---

#### core-concepts/self-encryption.md
**Title**: Self-Encryption
**Purpose**: Explain how data is encrypted client-side before network storage; privacy guarantee.
**Covers**:
- What is self-encryption: Encryption happens on client, keys never leave your device
- ChaCha20-Poly1305: Stream cipher for data, AEAD for authentication; why this choice
- BLAKE3: Cryptographic hash function; used for content addressing and key derivation
- The encryption pipeline: Raw data → chunked → hashed → encrypted → stored
- Key derivation: How per-chunk encryption keys are derived
- Verification: How the network can verify encrypted chunks without decryption
- No backdoors: Network operators cannot read your data

**Does NOT Cover**: Post-quantum cryptography (see PQC page), key management (see Key Derivation), payment verification

**Verification Against**: self_encryption crate (ChaCha20-Poly1305 + BLAKE3 confirmed by Mick van Dijke; crate README was outdated at time of audit)

**LLM Note**: Technical but accessible; include pseudocode for the pipeline.

---

#### core-concepts/post-quantum-cryptography.md
**Title**: Post-Quantum Cryptography
**Purpose**: Explain the quantum-resistant algorithms used; address long-term security.
**Covers**:
- Why post-quantum: Risk of quantum computers breaking elliptic curve cryptography
- ML-DSA-65: Digital signature algorithm; key sizes, signing/verification
- ML-KEM-768: Key encapsulation mechanism; for establishing shared secrets
- NIST Level 3: Security target and what it means
- Pure PQC: As of saorsa-pqc v0.5.1, no classical cryptographic fallback — all Ed25519/x25519 removed from TLS path
- Where used: Network identity, key exchange, TLS authentication
- Performance: No significant slowdown vs. classical crypto
- Standardization: NIST FIPS 203/204/205; not experimental
- FIPS caveats: Library uses FIPS-certified upstream crates but is not itself FIPS 140-3 module certified

**Does NOT Cover**: Quantum computing theory, algorithm proofs, implementation internals

**Verification Against**: saorsa-pqc v0.5.1 (all classical crypto removed, 360/360 tests passing), ant-quic (1998/1998 tests passing with saorsa-pqc 0.5)

**LLM Note**: Explain why without requiring quantum physics background.

---

#### core-concepts/key-derivation.md
**Title**: Key Derivation
**Purpose**: Explain how users generate unlimited keys from a single master key.
**Covers**:
- Master key: Derived from seed phrase; never used directly for encryption
- HKDF: HMAC-based Key Derivation Function; deterministic key generation
- Child keys: Unlimited derived keys from master; each can encrypt/sign independently
- Determinism: Same master key always produces same children in same order
- Key hierarchies: How to organize keys by purpose (payments, storage, signing)
- Index-based: `HKDF(master, "context", index)` → unique key for use case N
- Practical example: Generate keys for multiple storage locations from one seed phrase

**Does NOT Cover**: Password security, seed phrase generation, BLS threshold

**Verification Against**: ant-core (key derivation impl), HKDF RFC 5869

**LLM Note**: Include examples in pseudocode/Python showing determinism.

---

#### core-concepts/payment-model.md
**Title**: Payment Model
**Purpose**: Explain the economics; how storage is paid for and priced.
**Covers**:
- ANT token: ERC-20 on Arbitrum; used for all network payments
- Pay-once model: Single upfront payment for storage; no subscription or retrieval fees
- Pricing mechanism: Describe the pricing behavior that exists on merged refs at the time of audit
- Batch Merkle payments: Efficient multi-chunk payment verification
- Payment flow: User signs transaction → funds move to network → nodes earn rewards
- External signers: Use hardware wallets, multi-sig, or delegated signers
- Network economics: How nodes are incentivized to store data

**Does NOT Cover**: Detailed contract ABI, Arbitrum mechanics (external)

**Verification Against**: current merged pricing logic in the relevant source repos, payment contract

**LLM Note**: Include a worked example: cost to store 100MB.

---

### SECTION: How-To Guides

#### how-to-guides/setup-local-network.md
**Title**: Set Up a Local Network
**Purpose**: Get a testable environment without hitting mainnet.
**Covers**:
- Two options: ant-dev CLI (simple) or local nodes (advanced, realistic)
- ant-dev: `ant-dev network start`, single command, sandbox for testing
- Local nodes: Run multiple ant-node instances locally
- Configuration: Network parameters, payment token (testnet/local), ports
- Funding test accounts: Add ANT to test wallets
- Verification: Check nodes are communicating, store/retrieve a file
- Cleanup: Stop network, reset state

**Verification Against**: ant-dev CLI source, ant-node local network docs

**LLM Note**: Step-by-step with code blocks.

---

#### how-to-guides/store-and-retrieve-data.md
**Title**: Store and Retrieve Data
**Purpose**: Core operations — get data in and out of the network.
**Covers**:
- Storing: Upload file, get address, save address
- Retrieving: Fetch by address, decrypt, verify content hash
- Batch uploads: Multiple files, Merkle batch payments
- Streaming: For large files, avoid loading into memory
- Progress tracking: Monitor upload/download
- Error handling: Address not found, corrupted data, retries
- Tabbed code examples: cURL + Python + JavaScript + Rust using GitBook `{% tabs %}` blocks (same pattern as existing quick-start guide)

**Verification Against**: ant-sdk examples, ant-client CLI store/retrieve commands

**LLM Note**: Tabbed examples in the .md source are clean for agent consumption — `{% tab title="Python" %}` wrapping standard code fences. Agents can parse these directly.

---

#### how-to-guides/manage-keys.md
**Title**: Manage Keys and Wallets
**Purpose**: Secure key handling; backup, recovery, rotation.
**Covers**:
- Key generation: From seed phrase, from password
- Storage: Where to keep keys (environment variables, config files, vaults)
- Backup: Seed phrase backup, cold storage
- Recovery: Restore keys from seed, from backup
- Rotation: Change active keys without losing old data
- Hierarchies: Organize keys by purpose

**Verification Against**: ant-core key management, ant-client wallet commands

**LLM Note**: Emphasize security throughout.

---

#### how-to-guides/handle-payments.md
**Title**: Handle Payments
**Purpose**: Move ANT tokens, pay for storage, manage wallet balance.
**Covers**:
- ANT token basics: What it is, where to get it, check balance
- Estimating cost: Calculate storage cost using pricing formula
- Single payments: Pay for one upload, verify transaction
- Batch Merkle payments: Pay for multiple chunks efficiently
- Payment flow: Sign → broadcast → confirm → stored
- External signers: Use hardware wallet or signing service
- Payment status: Check transaction, retry on failure

**Verification Against**: ant-sdk payment examples, payment contract code

**LLM Note**: Include worked example: cost calculation, signing, verification.

---

#### how-to-guides/run-as-daemon.md
**Title**: Run as a Daemon
**Purpose**: Operate antd as a background service.
**Covers**:
- Starting daemon: `antd` command, systemd service, Docker container
- Configuration: antd.conf, key settings (REST port, data dir, cache size)
- Logging: Enable debug logging, log rotation
- Security: Restrict daemon access (localhost vs. network)
- Process management: systemd, launchd (macOS)
- Health checks: Readiness probes, liveness checks
- Graceful shutdown: Signal handling

**Verification Against**: ant-sdk daemon docs

**LLM Note**: Provide example systemd unit file.

---

#### how-to-guides/use-external-signers.md
**Title**: Use External Signers
**Purpose**: Sign transactions with hardware wallets or external services.
**Covers**:
- Why external signers: Keep private keys off internet-connected device
- Hardware wallets: Integration overview
- Signing services: Azure Key Vault, AWS KMS, custom signing API
- Flow: Request signature → embed in transaction
- Multi-sig: Multiple signers for sensitive operations

**Verification Against**: ant-sdk signer interface

**LLM Note**: Include step-by-step flow diagram.

---

#### how-to-guides/test-your-application.md
**Title**: Test Your Application
**Purpose**: Write tests without hitting mainnet.
**Covers**:
- Unit tests: Mock Autonomi client
- Integration tests: Real daemon on local network
- Test fixtures: Sample data, test addresses
- Payment simulation: Fake payment signing for tests
- CI/CD integration: Run tests in GitHub Actions, etc.

**Verification Against**: ant-sdk test examples, ant-client test suite

**LLM Note**: Provide test templates.

---

#### how-to-guides/deploy-to-mainnet.md
**Title**: Deploy to Mainnet
**Purpose**: Go live on the real Autonomi network; final checklist.
**Covers**:
- Pre-launch checklist: Security review, performance testing, error handling
- Configuration: Production daemon settings, logging, monitoring
- Key management: Secure key storage, backup strategy
- Payment setup: Real ANT on Arbitrum, wallet funding
- Monitoring: Set up dashboards, alerts
- Cost estimation: Estimate mainnet costs

**Verification Against**: Autonomi mainnet docs

**LLM Note**: Provide a pre-launch checklist template.

---

#### how-to-guides/embed-a-node.md
**Title**: Embed a Node in Your Application
**Purpose**: For developers who want to include a node as part of their application (not for humans who just want to run a node and earn rewards — that's covered in the existing Node section of docs.autonomi.com).
**Covers**:
- Use case: Application that provides storage capacity to the network as part of its operation
- Programmatic node management: Start/stop/configure a node via ant-core
- Resource allocation: CPU, memory, storage, bandwidth limits
- Rewards: How embedded nodes earn ANT
- Monitoring: Node health, storage metrics
- Considerations: Network requirements, uptime expectations

**Does NOT Cover**: Human node operation guide (see docs.autonomi.com/node), node installation for non-developers

**Verification Against**: ant-node programmatic API, ant-core node management

**LLM Note**: Distinguish clearly from the human-facing node guide.

---

### SECTION: SDK Reference

#### sdk-reference/overview.md
**Title**: ant-sdk Overview
**Purpose**: Architecture of ant-sdk; how the daemon, REST/gRPC API, and language bindings fit together.
**Covers**:
- ant-sdk definition: Daemon (antd) + REST/gRPC API + 15 language bindings
- Architecture: Daemon handles network I/O, encryption, payments. REST/gRPC API is the canonical interface. Language bindings are thin HTTP/gRPC clients with typed wrappers and daemon auto-discovery.
- Binding model: Most bindings are pre-built REST/gRPC clients (not FFI). Swift and Kotlin use FFI for mobile (embed the daemon). All bindings share the same API surface — learn one, know them all.
- REST API: HTTP endpoints; cURL as first-class citizen for both humans and agents
- gRPC: Alternative protocol for high-performance or streaming use cases
- Configuration: antd config file, ports, data directory
- Versioning: Semantic versioning, stable API

**Verification Against**: ant-sdk README, daemon source

**LLM Note**: Diagram: daemon in centre, REST/gRPC API layer, language clients around it. Emphasise that the REST API reference is the canonical source — all bindings call the same endpoints.

---

#### sdk-reference/rest-api.md
**Title**: REST API Reference
**Purpose**: Complete, canonical reference for all HTTP endpoints. This is the single source of truth that all language bindings wrap. cURL examples for every endpoint serve both humans and AI agents.
**Covers**:
- All REST endpoints with method, path, request/response schemas
- cURL example for every endpoint (first-class, not an afterthought)
- Authentication headers
- Error codes and responses with example error bodies
- Rate limiting (if applicable)
- Tabbed code examples for key operations (cURL + Python + JavaScript + Go) using GitBook tabs

**Verification Against**: ant-sdk REST handler source, OpenAPI spec if available

**LLM Note**: This is the most important page for agents. Structured for programmatic consumption; machine-parseable. An agent reading only this page should be able to use the full API in any language.

---

#### sdk-reference/grpc-services.md
**Title**: gRPC Services Reference
**Purpose**: Complete reference for gRPC service definitions.
**Covers**:
- Service definitions, RPCs, message types
- Proto file reference
- Connection setup
- Streaming RPCs (if applicable)

**Verification Against**: ant-sdk proto files

**LLM Note**: Include proto file contents or link to them.

---

#### sdk-reference/daemon-cli.md
**Title**: Daemon CLI: antd
**Purpose**: Command reference for the antd daemon process.
**Covers**:
- `antd` command-line flags and options
- Configuration file format
- Start, stop, status commands
- Log level control
- Port configuration

**Verification Against**: `antd --help` output, ant-sdk daemon source

---

#### sdk-reference/language-bindings/overview.md
**Title**: How Language Bindings Work
**Purpose**: Explain the binding architecture so developers understand what they're using and how each binding relates to the daemon and shared API surface.
**Covers**:
- Binding model: Describe the current transport model for each binding based on merged source artifacts.
- Shared API surface: Explain where bindings target the same daemon surface and where they differ.
- Packaging and discovery: Document how each verified binding is installed and how it finds the daemon.
- Type mappings: How Rust types map to each language (e.g., `Vec<u8>` → Python `bytes`, JS `Uint8Array`)
- When to use REST directly vs a binding: Bindings add types and error handling; cURL/raw HTTP is fine for scripting or unsupported languages

**Verification Against**: ant-sdk binding generation, REST client source

**LLM Note**: Key page for agents deciding which binding to use. The answer must be based on the verified exported surface of the language in question, not on an assumption of perfect parity.

---

#### sdk-reference/language-bindings/[python|javascript|go|etc].md
**Title**: [Language] SDK
**Purpose**: Per-language quickstart. Lightweight — install, init, one working example, language-specific notes. A shared structure is allowed, but each page must be verified against that binding's merged package surface.
**Covers per page** (~50-80 lines each):
- Install command (pip, npm, cargo, go get, etc.)
- Import and client initialization
- One complete working example: store and retrieve data
- Language-specific type mappings (how Autonomi types map to this language's idioms)
- Async patterns (if applicable — e.g., Python asyncio, JS promises, Go goroutines)
- Error handling idioms for this language
- Link back to REST API reference for full endpoint documentation

**Does NOT Cover**: Full API reference (that's the REST API page), advanced configuration, daemon management

**Template**: Pages can share a structure, but templates do not imply identical package names, constructors, response models, or transport behavior.

**Priority tiers**:
- P0 (launch day): Python, JavaScript, Rust, Go
- P1 (launch week): TypeScript, Java, C#
- P2 (post-launch or minimal stub): Kotlin, Swift (FFI/mobile — flag as beta), Ruby, PHP, C++, Dart, Zig

**Verification Against**: Each binding's install process and basic example tested end-to-end

---

### SECTION: CLI Reference (ant-client)

#### cli-reference/overview.md
**Title**: ant-client Overview
**Purpose**: Introduction to the Rust/CLI alternative interface.
**Covers**:
- What ant-client is: CLI tool (`ant`) + Rust library (`ant-core`)
- When to use: Rust projects, direct network access, scripting, advanced scenarios
- Relationship to ant-sdk: Alternative interface, same network
- Installation: cargo install, source build

**Verification Against**: ant-client README

---

#### cli-reference/command-reference.md
**Title**: Command Reference
**Purpose**: Complete CLI reference for the `ant` command.
**Covers**:
- All commands with flags, options, examples
- Grouped by function: storage, keys, wallet, network, node management

**Verification Against**: `ant --help` output, ant-client source

---

#### cli-reference/ant-core-library.md
**Title**: ant-core Rust Library
**Purpose**: API reference for the Rust library that powers ant-client.
**Covers**:
- Key types and traits
- Client initialization
- Storage operations
- Key management operations
- Payment operations
- Error types

**Verification Against**: ant-core rustdoc, source code

**LLM Note**: Link to docs.rs if published.

---

### SECTION: Architecture

#### architecture/system-overview.md
**Title**: System Overview
**Purpose**: 10,000-foot view of how the Autonomi network works. Single page for launch; deeper dives can be added post-launch.
**Covers**:
- High-level architecture diagram: Clients → QUIC → Nodes → DHT → Storage
- Network topology: Standard Kademlia DHT, XOR distance, close groups
- NAT traversal: Three-tier (direct, hole punching, MASQUE relay) via ant-quic and QUIC
- Trust and reputation: Local EMA trust scoring (not distributed EigenTrust)
- Data flow: Upload path (client → encrypt → chunk → pay → store) and retrieval path
- Replication: Close-group distribution, verified close-group membership
- Links to detailed repo documentation for each subsystem

**Does NOT Cover**: Deep algorithmic details (links to repo docs instead)

**Verification Against**: saorsa-core (standard Kademlia confirmed), ant-quic (NAT traversal), ant-node (trust scoring, replication)

**LLM Note**: This is the "how does it all fit together" page. Diagram-heavy.

---

### SECTION: Glossary

#### glossary.md
**Title**: Glossary
**Purpose**: Define Autonomi-specific terminology in one place. Essential for developers landing on any page mid-docs (via search or llms.txt) and for LLMs building vocabulary.
**Covers** (non-exhaustive, ~30-40 entries):
- ANT token, ant-sdk, ant-client, ant-core, antd
- Chunk, DataMap, content addressing
- Self-encryption, ChaCha20-Poly1305, BLAKE3
- ML-DSA-65, ML-KEM-768, post-quantum cryptography
- Kademlia DHT, close group, XOR distance
- QUIC, hole punching, MASQUE relay
- Arbitrum, ERC-20, Merkle batch payment
- HKDF, master key, child key
- Node, daemon, language binding
- (and other terms as they arise during writing)

**Verification Against**: All repo documentation, conceptual guide

**LLM Note**: Flat alphabetical list. Each entry: term, one-sentence definition, link to relevant page.

---

## 5. LAUNCH PRIORITIES

Given the April 7 deadline (one week), pages should be written in priority order:

### P0 — Must ship (core developer journey)
1. `getting-started/introduction.md`
2. `getting-started/install.md`
3. `getting-started/hello-world.md`
4. `core-concepts/data-types.md`
5. `core-concepts/self-encryption.md`
6. `core-concepts/payment-model.md`
7. `how-to-guides/store-and-retrieve-data.md`
8. `how-to-guides/handle-payments.md`
9. `sdk-reference/overview.md`
10. `sdk-reference/rest-api.md`
11. `glossary.md`
12. `index.md` (landing page)

### P1 — Should ship (complete the story)
13. `core-concepts/overview.md`
14. `core-concepts/post-quantum-cryptography.md`
15. `core-concepts/key-derivation.md`
16. `how-to-guides/setup-local-network.md`
17. `how-to-guides/manage-keys.md`
18. `how-to-guides/run-as-daemon.md`
19. `getting-started/using-ant-client.md`
20. `cli-reference/overview.md`
21. `cli-reference/command-reference.md`
22. `sdk-reference/daemon-cli.md`

### P2 — Nice to have (ship if time allows)
23. `sdk-reference/grpc-services.md`
24. `cli-reference/ant-core-library.md`
25. `how-to-guides/use-external-signers.md`
26. `how-to-guides/test-your-application.md`
27. `how-to-guides/deploy-to-mainnet.md`
28. `how-to-guides/embed-a-node.md`
29. `architecture/system-overview.md`
30. Language binding overview page
31. Per-language pages: Python, JavaScript, Rust, Go (P0), then TypeScript, Java, C# (P1), rest P2

---

## 6. OPEN QUESTIONS

1. ~~**Which language bindings are verified working?**~~ **RESOLVED**: Nic confirmed all 15 shipping for launch. Most are thin REST/gRPC clients; Swift and Kotlin use FFI for mobile (not fully tested). Documentation approach: REST API canonical + per-language lightweight pages.
2. **ant-sdk feature branch merge timeline**: The `feat/port-discovery` branch has all data/file/wallet operations; main only has chunks. Which branch will be merged by April 7?
3. **Pricing formula**: Confirmed quadratic `(record_count/6000)^2` will land by April 7 (currently logarithmic in code).
4. **Software attestation**: Confirmed out of scope (Mick). Not documented.
5. **Self-encryption crate README**: Outdated (says AES-256-CBC + SHA3-256). Actual implementation is ChaCha20-Poly1305 + BLAKE3. Mick confirmed. README should be updated by crate maintainers; docs will reflect reality.

---

## 7. POST-LAUNCH ROADMAP

Content to add after April 7 based on real developer feedback:
- FAQ (built from actual support questions)
- Troubleshooting guide (built from actual error reports)
- Integration patterns (built from real developer architectures)
- Example gallery (built from community contributions)
- Architecture deep dives (expand from single overview page)
- P2 language binding pages (Ruby, PHP, C++, Dart, Zig, Kotlin, Swift)
- Mobile development guide (Swift/Kotlin FFI bindings — once fully tested)
