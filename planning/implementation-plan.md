# Autonomi 2.0 Developer Documentation — Implementation Plan

**Status**: Active — all 44 pages drafted, under review
**Owner**: Jim Collinson
**Launch date**: April 7, 2026
**Last updated**: April 2, 2026

**Route note**: This plan predates the later route-first file reorganization. For the current live docs tree and page paths, use `docs/SUMMARY.md`, `repo-registry.yml`, and `component-registry.yml`.

---

## 1. STRATEGIC OVERVIEW

### What we're building

A centralised developer documentation site at docs.autonomi.com/developers for the Autonomi 2.0 network launch. The site will be the single authoritative source of developer-facing information about Autonomi, spanning the specific upstream repos that comprise the Autonomi 2.0 network stack, organised into repo classes with a component registry that maps code to documentation pages (see Section 1, Scope).

### Scope

The docs system distinguishes between two levels of scope:

1. **Repo scope** — the outer automation boundary. Repos drive GitHub events, source-of-truth tracking, and automation triggers.
2. **Component scope** — the inner documentation boundary. Components drive which pages are written, re-verified, or ignored when a change happens. A component can be a Rust crate, a binary/CLI, an OpenAPI spec, a gRPC proto surface, or a language SDK package.

Both are recorded in machine-readable registries (see Section 1.4).

#### 1.1 Repo classes

Each repo is assigned a class that determines how agents and automation treat it:

| Class | Meaning | Agent behaviour |
|-------|---------|----------------|
| **Broad source** | Main developer-facing surfaces | Watched broadly, used by default for drafting, broad re-verification on change |
| **Targeted foundational** | Authoritative for specific technical topics | Watched narrowly, pulled in only when a page/topic requires them |
| **Specialist** | Only relevant for certain docs areas | Used only for explicitly related pages |
| **Watchlist** | Transitional or legacy-adjacent | Not used as source-of-truth for new docs; only issue/flag if still referenced |
| **Excluded** | Not part of active docs source-of-truth | Ignored unless explicitly brought back into scope |

#### 1.2 Repo registry

**Broad source repos** (main developer-facing surfaces, default starting point for writing and auditing):

| Repo | Org | Topics |
|------|-----|--------|
| ant-sdk | WithAutonomi | getting-started, sdk-reference, bindings, how-to-guides |
| ant-client | WithAutonomi | cli-reference, rust-usage, local-devnet, data-flows |
| ant-node | WithAutonomi | node-behaviour, local-network, architecture, payment-model |

**Targeted foundational repos** (authoritative for specific technical topics, used when a page depends on those topics):

| Repo | Org | Topics |
|------|-----|--------|
| saorsa-core | saorsa-labs | DHT, routing, trust, architecture |
| saorsa-transport | saorsa-labs | transport, NAT traversal, connectivity |
| saorsa-pqc | saorsa-labs | PQC, signatures, key derivation |
| self_encryption | WithAutonomi | self-encryption, DataMaps, file internals |
| evmlib | WithAutonomi | EVM payments, wallet integration |
| ant-merkle | MaidSafe (moving to WithAutonomi) | batch payments, gas optimisation, Merkle payment flows |

**Specialist repos** (used only when those specific docs exist):

| Repo | Org | Topics |
|------|-----|--------|
| ant-keygen | WithAutonomi | release-signing, key management |

**Watchlist repos** (not source-of-truth for new docs; flag if still referenced):

| Repo | Org | Notes |
|------|-----|-------|
| ant-evm | WithAutonomi | Collapsed into evmlib. Watch until all references disappear from merged code. |

**Excluded repos** (ignored by default):

| Repo | Org | Reason |
|------|-----|--------|
| ant-quic | saorsa-labs | Confirmed by Mick van Dijke as older ancestor/fork. Docs focus on saorsa-transport instead. |
| ant-ui | WithAutonomi | Vue UI client, separate product |
| indelible | WithAutonomi | Private, Go, not part of network |
| Autonomi 1.0 | MaidSafe | Previous version, different codebase |
| Non-network saorsa-labs repos | saorsa-labs | communitas, fae, saorsa-gossip, saorsa-mls, saorsa-tui, saorsa-cli, saorsa-canvas, saorsa-robotics, saorsa-multiapp, saorsa-webrtc, saorsa-testnet, saorsa-seal, saorsa-logic, saorsa-rsps, saorsa-fec, saorsa-attestation-guest, saorsa-vdf-guest, saorsa-disk, rq |

**Tangentially in scope** (not part of core network, but must be accurate when referenced):

| Repo | Org | Policy |
|------|-----|--------|
| x0x | saorsa-labs | Features and behaviour should be accurate when mentioned in docs |

#### 1.3 Component registry

Repo scope alone is not enough — agents need to know which components within each repo map to which documentation pages.

**ant-sdk components:**

| Component | Kind | Path | Topics | Pages |
|-----------|------|------|--------|-------|
| antd | rust-binary | `antd/` | daemon, REST API, gRPC, install | getting-started/install.md, sdk-reference/overview.md, sdk-reference/rest-api.md |
| openapi | api-spec | `antd/openapi.yaml` | REST API | sdk-reference/rest-api.md |
| proto | grpc-spec | `antd/proto/` | gRPC | sdk-reference/grpc-services.md |
| antd-rust | rust-crate | `antd-rust/` | Rust binding | sdk-reference/language-bindings/rust.md |
| antd-py | python-package | `antd-py/` | Python binding | sdk-reference/language-bindings/python.md |
| antd-js | js-package | `antd-js/` | JavaScript binding | sdk-reference/language-bindings/javascript.md |
| antd-go | go-module | `antd-go/` | Go binding | sdk-reference/language-bindings/go.md |
| (other bindings) | per-language | `antd-*/` | per-language binding | sdk-reference/language-bindings/*.md |

**ant-client components:**

| Component | Kind | Path | Topics | Pages |
|-----------|------|------|--------|-------|
| ant-core | rust-crate | `ant-core/` | data model, files, payments, devnet | core-concepts/data-types.md, how-to-guides/store-and-retrieve-data.md, how-to-guides/handle-payments.md |
| ant-cli | rust-binary | `ant-cli/` | CLI, node management | cli-reference/overview.md, cli-reference/command-reference.md |

**ant-node components:**

| Component | Kind | Path | Topics | Pages |
|-----------|------|------|--------|-------|
| ant-node | rust-binary | `src/` | node, local network, payment model | core-concepts/payment-model.md, how-to-guides/setup-local-network.md |
| ant-devnet | rust-binary | `src/bin/ant-devnet/` | devnet launcher | how-to-guides/setup-local-network.md |

**Foundational single-crate repos:**

| Component | Repo | Topics | Pages |
|-----------|------|--------|-------|
| saorsa-core | saorsa-core | DHT, routing, trust, architecture | core-concepts/overview.md, architecture/system-overview.md |
| saorsa-transport | saorsa-transport | transport, NAT traversal | architecture/system-overview.md |
| saorsa-pqc | saorsa-pqc | PQC, key derivation | core-concepts/post-quantum-cryptography.md, core-concepts/key-derivation.md |
| self_encryption | self_encryption | self-encryption, DataMaps | core-concepts/self-encryption.md, core-concepts/data-types.md |
| evmlib | evmlib | payments | core-concepts/payment-model.md, how-to-guides/handle-payments.md |
| ant-merkle | ant-merkle | batch payments, gas optimisation | how-to-guides/handle-payments.md |

**Specialist:**

| Component | Repo | Topics | Pages |
|-----------|------|--------|-------|
| ant-keygen | ant-keygen | release-signing, key management | (only if key management docs exist) |

#### 1.4 Machine-readable registries

These registries live in the docs repo and are read by both agents and automation. Full YAML definitions are maintained as operational config files — see `repo-registry.yml` and `component-registry.yml` in the docs repo root.

The **repo registry** records: repo name, class, watch mode, default-for-drafting flag, topic ownership, and on-change behaviour.

The **component registry** maps each component to: repo, path, kind, topics, and the specific pages it feeds.

The **target manifest** (Section 5) is kept separate — it only answers "which refs should the docs match right now?" and does not encode repo class, topic ownership, drafting rules, or watch behaviour.

#### 1.5 Dependency tree (confirmed from Cargo.toml, April 1 2026)

```
ant-node (WithAutonomi)
├── saorsa-core 0.21.0 (saorsa-labs)
│   ├── saorsa-pqc 0.5 (saorsa-labs) ← leaf
│   └── saorsa-transport 0.30.1 (saorsa-labs)
│       └── saorsa-pqc 0.4 (saorsa-labs)
├── saorsa-pqc 0.5 (saorsa-labs)
├── evmlib 0.5.0 (WithAutonomi)
│   └── ant-merkle 1.5.1 (MaidSafe → moving to WithAutonomi)
├── self_encryption 0.35.0 (WithAutonomi)
└── xor_name 5 (crates.io)

ant-client (WithAutonomi) — workspace
└── ant-core
    ├── ant-node 0.9.0 (WithAutonomi) ← pulls in everything above
    ├── saorsa-pqc 0.5 (saorsa-labs)
    ├── evmlib 0.5.0 (WithAutonomi)
    ├── self_encryption 0.35.0 (WithAutonomi)
    └── xor_name 5 (crates.io)

ant-sdk (WithAutonomi) — monorepo, 16 language SDKs
├── antd-rust: pure REST/gRPC client (reqwest, tonic) — no Autonomi deps
├── antd-py: httpx + grpcio — no Autonomi deps
└── [all other bindings]: thin REST/gRPC clients, no Autonomi deps
```

#### 1.6 SDK binding count

The ant-sdk monorepo contains **16** language directories: Python, Rust, Go, Java, C++, C#, Dart, Elixir, JavaScript, Kotlin, Lua, MCP (server binding), PHP, Ruby, Swift, Zig. The docs repo covers **14 per-language pages** (Python, JavaScript, Rust, Go, TypeScript, Java, C#, Kotlin, Swift, Ruby, PHP, C++, Dart, Zig) plus a bindings overview page. TypeScript has its own page separate from JavaScript. Elixir, Lua, and MCP are not documented as separate binding pages for launch.

### Why centralised documentation

1. **Cross-repo coherence**: Documentation for Autonomi spans six repositories. No single repo is the right home for content like "how self-encryption and payment work together" or a developer getting-started flow. The docs repo is the join table.
2. **GEO and AI discoverability**: Scattered READMEs across GitHub repos are invisible to foundation model training pipelines and agent crawlers. A well-structured site with `llms.txt`, `llms-full.txt`, and clean markdown provides a single, authoritative surface for agents to consume. This directly affects Autonomi's visibility and adoption.
3. **Developer experience**: Developers learn Autonomi by following a guided path (concepts → quickstart → how-to → reference), not by reading six separate READMEs in the right order.
4. **Automated consistency**: A docs repo with CI automation can detect when upstream code changes make documentation stale — something that's invisible when docs live inside individual repos.

### Design principles

- **AI-generated, progressively automated**: No documentation is hand-crafted. For launch, content is AI-generated from codebase analysis and human-reviewed. Over time, automated checks reduce the amount of human review required, with humans focusing on conceptual accuracy, editorial quality, and low-confidence changes.
- **Accuracy over speed**: Every page is verified against the actual codebase, not written speculatively.
- **Diátaxis framework**: Getting Started → Core Concepts → How-to Guides → Reference.
- **ant-sdk first**: ant-sdk is the primary developer interface; ant-client is the Rust/advanced alternative.
- **REST API canonical**: The REST API (with cURL examples) is the single source of truth. All 15 language bindings wrap the same endpoints.
- **No speculative branch synthesis**: Unmerged feature branches are not documented as authoritative. The docs system does not attempt to infer final behaviour from multiple branches that have not yet landed. When branches merge, automation detects the change and updates the docs.
- **Launch-scoped**: ~30 substantive pages + 15 lightweight binding templates. Better to ship fewer accurate pages than many speculative ones.

---

## 2. REPO STRATEGY

### Phase 1: POC under jimcollinson (now → pre-launch)

- Create the initial personal docs repo on GitHub
- Scaffold directory structure, SUMMARY.md, .gitbook.yaml
- Connect GitBook Git Sync to verify the pipeline
- Write and verify all P0 pages
- Iterate freely without organisational overhead

### Phase 2: Move to WithAutonomi (post-launch or when David is bought in)

- Transfer and rename repo to `WithAutonomi/autonomi-developer-docs`
- Update GitBook Git Sync URL (5-minute change)
- Present as a working, battle-tested system — not a proposal
- Add team write access, branch protection rules

### Rationale

Starting under personal GitHub avoids the "why is this empty?" conversation before there's something to show. Moving later is trivial (change the remote URL). David will be more receptive to a working system than a pitch deck.

---

## 3. PLATFORM: GITBOOK

### Why GitBook

- Already in use at docs.autonomi.com — no migration cost
- Git Sync: GitHub repo is the source of truth, not GitBook's editor
- Auto-generates `llms.txt` and `llms-full.txt` manifests
- Auto-generates clean `.md` versions of all pages (verified: agent-consumable)
- Supports `{% tabs %}` / `{% tab %}` blocks for multi-language code examples
- Has an MCP server for programmatic access
- Good SEO/GEO out of the box
- Content team already knows it

### GitBook configuration

```yaml
# .gitbook.yaml
root: ./docs/
structure:
  readme: index.md
  summary: SUMMARY.md
```

---

## 4. CONTENT GENERATION APPROACH

### Principle: AI-generated, human-reviewed

Jim has been clear: no hand-crafting documentation, even for April 7. The codebase is moving too fast. Everything is AI-generated and human-audited.

### How pages are generated

Each documentation page follows this pipeline:

1. **Source identification**: Determine which repos, files, and code paths are the authoritative source for the page's content.
2. **Codebase audit**: AI reads the actual source code, tests, examples, existing documentation, and interface artifacts in the source repos.
3. **Claim extraction**: AI extracts the facts, commands, interfaces, and examples that can be supported directly by the audited source artifacts.
4. **Draft generation**: AI generates or rewrites the page content from the audited evidence, following the per-page brief from the IA document.
5. **Verification**: AI verifies the page against the audited sources before it is treated as finished.
6. **Verification metadata**: Each verified page includes a comment noting which repo, branch or tag, commit SHA, and verification mode it was checked against.
7. **Human review**: Jim reviews and approves. For technical accuracy, may send to relevant dev (Mick, Nic, David) for confirmation.

### Verification against codebase

Every page carries a machine-readable verification trail (see Section 5 for the full metadata format). This allows the automation to detect when the verified commit is no longer HEAD and flag the page for re-verification.

---

## 5. SOURCE-OF-TRUTH MODEL

### Definitions

**Current merged truth**: The latest merged commit on the default branch of each relevant Autonomi 2.0 repository at the time of the source audit. This is the default source for documentation generation and verification before a launch target is explicitly declared.

**Target manifest**: A fixed per-repo list of refs that the docs should match for a launch-hardening or release-verification pass. Each entry can be a tag, release, branch head, or commit SHA. It does not require every repo to have a formal GitHub release.

**Active mode**: The source-of-truth mode currently in force for a page. By default this is `current-merged-truth`. It changes to `target-manifest` only when a `target-manifest.yml` exists and the pass explicitly uses it.

**Required workflow**: `source audit -> draft -> verify`. The detailed operational procedure lives in `planning/verification-workflow.md`.

### Pre-launch policy (now → launch hardening)

These docs describe the current merged Autonomi 2.0 codebase and are being hardened toward the April 6 internal docs target ahead of the April 7 network launch.

Before a final release candidate or launch target is explicit, docs are generated and verified against the **current merged truth** of the relevant Autonomi 2.0 repos — usually the default branch.

This means:
- The docs describe how Autonomi 2.0 works based on merged code now
- The system does not try to predict the final shape of multiple unmerged branches
- Feature branches (e.g., `feat/port-discovery`) are ignored by default until they merge
- Pages are written only after a source audit resolves the exact upstream SHAs in scope
- Historical notes and prior synthesis documents are not part of the evidentiary chain
- Pages are not treated as verified until every verification block contains a real commit SHA
- When changes merge, automation detects drift and updates or flags the affected documentation

This is a more realistic and defensible pre-launch promise than trying to coordinate unmerged branches across many repos.

### Launch-hardening policy

When the team declares a launch-ready state, a target manifest is created:

```yaml
# target-manifest.yml
# Refs the docs should match for launch verification
refs:
  ant-sdk: "v2.0.0-rc1"           # tag
  ant-client: "v2.0.0-rc1"        # tag
  ant-node: "main@abc1234"         # pinned commit on main
  saorsa-core: "v0.6.0"           # release
  saorsa-pqc: "v0.5.1"            # release
  saorsa-transport: "v0.30.1"      # release
```

P0 and P1 pages are then re-verified against these specific refs. This is a focused hardening pass, not the day-to-day operating mode.

### Post-launch policy

After launch, docs return to tracking current merged truth. The target manifest pattern is reused for future release-specific hardening passes.

### Install/download rule

Pages about installation, binaries, packages, and version numbers are treated separately from technical content. These pages must point to versions that users can actually download or install at that moment. They are updated when new binaries or packages are published, not when code merges.

### Verification metadata format

Every page carries a machine-readable verification comment:

```markdown
<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: abc1234def5678
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
```

Fields:
- `source_repo`: Which repo this page's content was verified against
- `source_ref`: Branch, tag, or release name
- `source_commit`: Specific commit SHA
- `verified_date`: When the verification was performed
- `verification_mode`: Either `current-merged-truth` or `target-manifest`

`source_commit: TBD` is not valid on a page presented as verified.

For pages verified against multiple repos (e.g., the architecture overview), multiple verification blocks are included.

---

## 6. INFORMATION ARCHITECTURE (SUMMARY)

Full IA is in `docs-v2-information-architecture.md` (v3). Key structure:

```
docs/
├── index.md
├── getting-started/          (4 pages)
├── core-concepts/            (6 pages)
├── how-to-guides/            (9 pages)
├── sdk-reference/
│   ├── overview, rest-api, grpc-services, daemon-cli
│   └── language-bindings/    (overview + 14 per-language pages)
├── cli-reference/            (3 pages)
├── architecture/             (1 page)
└── glossary.md
```

~45 pages total: 30 substantive + 15 lightweight binding templates.

---

## 7. EXECUTION PLAN (CURRENT PASS)

### Priority tiers

**P0 — Must ship** (12 pages: core developer journey):

| # | Page | Source repos | Notes |
|---|------|-------------|-------|
| 1 | `index.md` | — | Landing page |
| 2 | `getting-started/introduction.md` | Conceptual guide | What is Autonomi |
| 3 | `getting-started/install.md` | ant-sdk | Install antd + verify |
| 4 | `getting-started/hello-world.md` | ant-sdk examples | First upload, working code |
| 5 | `core-concepts/data-types.md` | ant-sdk, ant-client, self_encryption | Current developer-visible data types and storage outputs on merged refs |
| 6 | `core-concepts/self-encryption.md` | self_encryption crate | ChaCha20 + BLAKE3 |
| 7 | `core-concepts/payment-model.md` | ant-node pricing | Current payment flow and pricing behavior on merged refs |
| 8 | `how-to-guides/store-and-retrieve-data.md` | ant-sdk, ant-client | Core CRUD operations |
| 9 | `how-to-guides/handle-payments.md` | ant-sdk payment | Payment flow |
| 10 | `sdk-reference/overview.md` | ant-sdk | Daemon + REST/gRPC + bindings architecture |
| 11 | `sdk-reference/rest-api.md` | ant-sdk REST handlers | Canonical API reference |
| 12 | `glossary.md` | All repos | ~30-40 terms |

Plus **P0 binding pages** (4 pages): Python, JavaScript, Rust, Go — each ~50-80 lines from a shared template.

**P1 — Should ship** (10 pages): core-concepts/overview, PQC, key-derivation, setup-local-network, manage-keys, run-as-daemon, using-ant-client, cli-reference/overview, command-reference, daemon-cli.

**P2 — Ship if time allows**: gRPC reference, ant-core library, external signers, test-your-application, deploy-to-mainnet, embed-a-node, architecture overview, remaining binding pages.

### Internal target

- External launch constraint: April 7.
- Internal docs hardening target: April 6.
- Current objective: get the baseline docs accurate against current merged truth as soon as possible, ideally today.

### Required execution order

1. Tighten the process docs and rules.
2. Rewrite the docs page by page against `current-merged-truth`.
3. Verify rewritten pages with real SHAs.
4. Create the GitHub repo and push the verified baseline.
5. Connect GitBook sync and test the baseline.
6. Turn on the ongoing automation/drift workflow.

### Page states

Pages move through these states:

1. `source-audited`
2. `drafted`
3. `verified`
4. `publishable`

Meaning:
- `source-audited`: source repos, refs, SHAs, and canonical artifacts identified
- `drafted`: content written from audited evidence
- `verified`: technical claims and examples checked; verification metadata populated with real SHAs
- `publishable`: verified and ready to publish once repo sync is set up

### Current pass rules

1. Unmerged branches are not dependencies for this pass.
2. If a surface is only present on a branch or is merely expected by launch, it is out of scope until merged.
3. Installation and version pages describe what users can actually install now.
4. The information architecture stays in place unless a page's framing itself is wrong for the current merged truth.
5. The same `source audit -> draft -> verify` workflow is used before launch, at launch hardening, and after launch.

---

## 8. AUTOMATION ARCHITECTURE

### 8.1 Overview

Event-driven CI automation that detects when upstream code changes make documentation stale, and in many cases fixes the drift automatically. Not a batch job — triggers on every push to source repos. Built on Claude Code GitHub Actions and Greptile, both of which are already running on the saorsa and labs repos.

The automation follows the declared source of truth (see Section 5) and does not try to infer intent from unmerged branches.

**Two operating modes**:

1. **Current-merged-truth mode** (default, day-to-day): Automation watches default branches of the relevant Autonomi 2.0 repos. Detects drift between docs and current merged state. Auto-updates or flags mechanical changes. Ignores unmerged feature branches entirely.

2. **Target-manifest mode** (launch hardening, release verification): Automation reads `target-manifest.yml` as input. Verifies launch-critical pages (P0/P1) against the specific refs in that manifest. Distinguishes between pages tracking current merged truth and pages pinned for launch verification. Used for final pre-launch passes and future release hardening.

### 8.2 Direction: Push from source repos

Each source repo (ant-sdk, ant-node, saorsa-core, etc.) has a lightweight GitHub Action that fires on push to main (or on release/tag). It sends a `repository_dispatch` event to the docs repo. The docs repo receives that event and runs verification.

**Why push, not pull**: If the docs repo polled source repos, it would need to know what to look for, how often to check, and it breaks silently when someone adds a new repo. Push from the source means the intelligence lives in the docs repo's receiving workflow — one place to maintain.

**Setup per source repo**: ~10-line workflow file:

```yaml
# .github/workflows/notify-docs.yml
name: Notify docs repo
on:
  push:
    branches: [main]
  release:
    types: [published]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - uses: peter-evans/repository-dispatch@v3
        with:
          token: ${{ secrets.DOCS_REPO_TOKEN }}
          repository: WithAutonomi/autonomi-developer-docs
          event-type: upstream-change
          client-payload: '{"repo": "${{ github.repository }}", "ref": "${{ github.ref }}", "sha": "${{ github.sha }}"}'
```

### 8.3 Tiered response model

The automation does NOT create a bottleneck. Responses are tiered by confidence:

#### Tier 1 — Auto-merge (no human needed)

Mechanical, programmatically verifiable changes:

- OpenAPI spec changed → REST API reference page updated to match new endpoint signatures
- Function renamed → reference page updated with new name
- Config field added → reference page updated with new field
- CLI help text changed → command reference updated

These changes are generated by the automation, pass CI checks (build, lint, internal link validation), and merge automatically. No human gate.

**How this works**: The docs repo CI workflow:
1. Receives the `repository_dispatch` event with repo name and commit SHA
2. Clones the source repo at that SHA
3. Extracts structured data (OpenAPI spec, CLI help output, public API surface)
4. Compares against the docs repo's current reference pages
5. If mechanical differences found: Claude Code is invoked with a scoped prompt to update the specific pages
6. PR passes CI + Greptile review → auto-merges

#### Tier 2 — Flagged for review (human needed, low urgency)

Cases where the automation detects drift but can't fix it automatically:

- New module appeared in SDK with no corresponding docs page
- How-to guide references an API pattern that no longer exists
- An endpoint was removed
- A page's verification commit is more than N commits behind HEAD

These open **issues** (not PRs) with:
- Which doc page is affected
- What changed in the source repo
- The specific diff that triggered the flag
- Suggested action

Jim batches these and reviews periodically — they're informational, not blocking.

#### Tier 3 — Release-gated (human writes, automation verifies)

Substantive new content requiring human authoring:

- New feature needs a how-to guide
- New concept needs an explanation page
- Getting-started flow changes significantly

The automation can't write these, but it can:
- Detect they're needed (new public API surface with no corresponding docs)
- Notify Jim with context
- Once written, verify the new pages are consistent with the codebase

### 8.4 What the automation checks

The docs repo's CI verification workflow checks:

1. **API surface drift**: Do the docs site's endpoint references match the source repo's actual endpoints? (Source: OpenAPI spec, route handlers, proto files)
2. **CLI drift**: Does the command reference match `ant --help` / `antd --help` output? (Source: CLI binary or clap/structopt definitions)
3. **Type drift**: Do documented type names, field names, and signatures match the public API? (Source: Rust public API surface)
4. **Link validity**: Do all internal links resolve? Do external links to repo files still exist?
5. **Verification staleness**: For each page, is the verified-against commit still reasonably close to HEAD?
6. **Example validity**: Do code examples still compile/run against the current SDK version?

### 8.5 What the automation does NOT do

- It does not generate conceptual explanations from code
- It does not write how-to guides from scratch
- It does not make editorial decisions about content structure
- It does not replace human judgment about what developers need to know

### 8.6 Automation behaviour by repo class

The automation follows the repo registry (Section 1.2) to determine how to respond to changes in each repo:

| Repo class | On change | Agent behaviour |
|------------|-----------|----------------|
| **Broad source** | Broad re-verification of all mapped pages. Tier 1 changes auto-updated, Tier 2 flagged as issues. | Start from these repos when writing new pages. |
| **Targeted foundational** | Re-verify only the pages linked to affected components (via component registry). | Pull in only when a page's topic requires it. |
| **Specialist** | Review only if those specific docs exist. | Use only when explicitly writing those pages. |
| **Watchlist** | Do not auto-rewrite docs. Open an issue only if pages still reference the watchlist repo. | Do not use as source-of-truth for new content. |
| **Excluded** | Ignore entirely. | Do not read, reference, or verify against. |

**First-time writing workflow:**
1. Start from broad source repos (ant-sdk, ant-client, ant-node)
2. Add targeted foundational repos only when the page topic requires them
3. Ignore watchlist and excluded repos by default
4. Use specialist repos only when explicitly writing those docs

**Automated auditing workflow:**
1. Change in broad source repo → broad re-verification of its mapped pages
2. Change in targeted foundational repo → re-verify only pages linked to affected components
3. Change in specialist repo → only matters if those docs exist
4. Change in watchlist repo → open issue if pages still reference it
5. Change in excluded repo → ignore

### 8.7 Relationship between repo docs and docs site

Both should be accurate. They serve different purposes:

- **Repo-level docs** (READMEs, doc comments, inline examples): Implementation-accurate layer. Close to the code, updated by the people changing the code.
- **Docs site**: Developer-experience layer. Curated, ordered, cross-referenced, tells a coherent story across the whole project.

The automation keeps them consistent: when a repo's README says one thing and the docs site says another, that's a bug and the automation flags it.

**Practical rule**: A developer reading only the docs site should never be given incorrect information. A developer reading only a repo README should never be given incorrect information. The README may give less context, but never wrong context.

---

## 9. AI TOOLING AND QUALITY CONTROLS

### 9.1 AI tools used

Two AI tools, both already running on the saorsa and labs repos. No new tooling to introduce.

#### Claude Code (GitHub Actions) — the writer and updater

Claude Code is the AI that reads source code and writes/updates documentation pages. It runs as a GitHub Action in the docs repo, invoked when the automation detects drift or when Jim triggers a manual documentation update.

**For the initial documentation pass (launch sprint)**: Claude works in Cowork / Claude Code locally, reading the codebase audits and generating pages against the IA briefs. Jim reviews the output. This is a one-time sprint using existing tooling.

**For ongoing maintenance**: Claude Code runs in GitHub Actions in the docs repo. When the deterministic checks (Section 8.4) find drift, Claude Code is invoked with a focused, scoped prompt. It receives the specific change that triggered the drift (e.g., "endpoint `/v1/data/store` response schema changed from X to Y"), reads the docs repo's `CLAUDE.md` for style/tone/structure rules, and makes a bounded edit to the affected page(s). It does not re-read the entire codebase on every invocation — it gets a precise, bounded task.

**Key point**: Claude Code's token costs scale with the size of the change, not the size of the codebase. A renamed function costs a few hundred tokens. A new feature page costs more, but those are infrequent and human-triggered.

#### Greptile — the reviewer

Greptile reviews all PRs to the docs repo, exactly as it does on the other repos. This includes PRs opened by Claude Code (Tier 1 auto-updates) and PRs opened by humans (new content, Tier 3 work).

Greptile catches:
- Terminology inconsistencies (does this PR use "the daemon" where the glossary says "antd"?)
- Code examples referencing APIs that don't exist in the current SDK version
- Structural deviations from the page templates
- Cross-page contradictions (does the new payment guide claim something different from the payment model concept page?)

**The combination**: Claude Code writes, Greptile reviews, deterministic CI validates the build and links. Three layers, each catching different classes of error.

### 9.2 The docs repo's CLAUDE.md — editorial quality control

The docs repo's `CLAUDE.md` is the single file that controls Claude Code's behaviour when writing or updating documentation. It serves as the editorial style guide, structural template library, and verification checklist — all in one version-controlled, reviewable file.

The `CLAUDE.md` contains four sections:

#### Section 1: Style guide (tone, language, consistency)

Concrete, enforceable rules that Claude Code follows on every invocation:

- **Voice**: Second person ("you"), present tense, active voice
- **Prohibited words**: Never use "simply", "just", "easy", "obviously". Never use "we" (Autonomi is a network, not a company speaking)
- **Technical terminology**: Must match the glossary exactly. "self-encryption" not "self encryption" or "Self-Encryption". "antd" not "the daemon" or "ant daemon". "Kademlia DHT" not "Kademlia distributed hash table" in running text
- **Code examples**: Must be complete and runnable. Never snippets that require imagination. Always include imports, error handling, and expected output
- **Page self-containment**: No "as we discussed in the previous section" or "see above." Every page must make sense if read in isolation (critical for LLM ingestion via llms.txt)
- **Verification trail**: Every page must include a comment noting which repo, branch, and commit it was verified against (format: `<!-- Verified against: repo@branch (commit abc1234), YYYY-MM-DD -->`)

#### Section 2: Page templates (structural consistency)

Each page type has a defined template that Claude Code must follow:

- **Getting-started pages**: Title → Prerequisites → Steps (numbered) → What happened (brief explanation) → Next steps
- **Core concept pages**: Title → One-sentence definition → Why it matters → How it works (with diagram/pseudocode) → Practical example → Links to related pages
- **How-to guide pages**: Title → Goal → Prerequisites → Steps (numbered, with tabbed code examples) → Verification (how to confirm it worked) → Troubleshooting (common errors) → Next steps
- **Reference pages**: Title → Overview → Endpoint/command listing (method, path, parameters, response, example) → Error codes → Notes
- **Language binding pages**: Title → Install → Import and init → One complete example → Type mappings → Async patterns → Error handling → Link to REST API reference

When Claude Code generates or updates a page, it identifies the page type from the directory location and applies the corresponding template.

#### Section 3: Verification rules

What "verified" means, per page type:

- **Reference pages**: Every endpoint, function, type, and field mentioned exists in the current codebase at the specified commit. Machine-verifiable.
- **Concept pages**: Every technical claim can be traced to the active source repos at the specified commit. Human-checkable.
- **How-to guides**: Every code example runs successfully against the current SDK version. Machine-verifiable (CI can run examples).
- **Getting-started pages**: The full flow (install → first upload → verify) works end-to-end on a clean machine. Manually verified before each release.

#### Section 4: Terminology lockfile

A machine-readable glossary section mapping canonical terms to prohibited alternatives:

```
# Terminology lockfile — CLAUDE.md
# Format: canonical_term | prohibited_alternatives | definition
self-encryption | self encryption, Self-Encryption, Self Encryption | Client-side encryption using ChaCha20-Poly1305 + BLAKE3
antd | the daemon, ant daemon, Ant Daemon | The ant-sdk daemon process
Kademlia DHT | Kademlia distributed hash table, kademlia | Standard Kademlia distributed hash table
ANT token | ANT, Ant token, ant token | ERC-20 token on Arbitrum used for network payments
DataMap | data map, Data Map, datamap | Mapping from file to chunks to network addresses
```

This file serves double duty: Claude Code reads it when writing (avoids inconsistencies at generation time), and CI can lint all pages against it (catches inconsistencies at review time).

### 9.3 Deterministic CI checks (no AI tokens)

Several checks consume zero AI tokens and run on every PR:

- **Link validation**: All internal links resolve. External links to repo files still exist. (Tool: markdown-link-check or similar)
- **Terminology lint**: All pages conform to the terminology lockfile. (Tool: custom script or Vale with Autonomi-specific rules)
- **Template conformance**: Each page has the required sections for its type. (Tool: custom script checking for expected headings)
- **GitBook build**: `SUMMARY.md` is valid, `.gitbook.yaml` is correct, build succeeds. (Tool: GitBook CLI or equivalent)
- **Verification staleness**: Flag pages whose verified-against commit is more than N commits behind the source repo's HEAD. (Tool: custom script comparing git SHAs)

These run before Claude Code or Greptile are invoked. If deterministic checks pass and no drift is detected, no AI tokens are spent at all.

### 9.4 Concrete workflow: upstream change arrives

Here is the end-to-end flow when a source repo changes:

```
1. Developer pushes to ant-sdk main
   └── ant-sdk's notify-docs.yml fires repository_dispatch to docs repo

2. Docs repo receives event, CI workflow starts
   ├── Clone ant-sdk at the new commit SHA
   ├── Extract structured data:
   │   ├── OpenAPI spec (if available) or route handler signatures
   │   ├── `antd --help` output (build and run)
   │   ├── Public Rust API surface (cargo doc --document-private-items=false)
   │   └── README.md content
   └── Run deterministic diff against current docs pages

3. Deterministic checks classify the drift:
   ├── No drift detected → STOP. No AI tokens spent. Log "docs current."
   │
   ├── Tier 1 drift (mechanical, high confidence):
   │   ├── Invoke Claude Code with scoped prompt:
   │   │   "The response schema for POST /v1/data/store changed.
   │   │    Old: { address: string }
   │   │    New: { address: string, size: number }
   │   │    Update sdk-reference/rest-api.md. Follow CLAUDE.md style guide."
   │   ├── Claude Code edits the page, updates verification comment
   │   ├── Opens PR
   │   ├── Deterministic CI runs (links, terminology, template, build)
   │   ├── Greptile reviews the PR
   │   └── If all green → auto-merge. If issues → flag for human review.
   │
   ├── Tier 2 drift (needs human decision):
   │   └── Open GitHub issue with:
   │       - Which doc page(s) affected
   │       - What changed in the source repo (with diff)
   │       - Suggested action
   │       - Label: `docs-drift`, priority based on page tier (P0/P1/P2)
   │
   └── Tier 3 drift (new feature, no existing page):
       └── Open GitHub issue with:
           - What new public API surface was detected
           - Suggested page location in the IA
           - Label: `new-content-needed`
           - Jim or Claude Code (with Jim's approval) writes the new page
```

### 9.5 Concrete workflow: Jim triggers a documentation update

For cases where Jim wants to add or rewrite a page (not triggered by upstream change):

```
1. Jim opens a GitHub issue or works locally in Claude Code
   └── Describes what needs writing or updating

2. Claude Code generates the page:
   ├── Reads CLAUDE.md (style guide, templates, terminology)
   ├── Reads the relevant source repos at HEAD
   ├── Extracts only the claims supported by current merged source artifacts
   ├── Generates the page following the appropriate template
   └── Adds verification comment with repo + commit SHA

3. Jim reviews the output:
   ├── Technical accuracy check
   ├── May send specific claims to relevant dev for confirmation
   └── Opens PR when satisfied

4. PR goes through the standard pipeline:
   ├── Deterministic CI (links, terminology, template, build)
   ├── Greptile review
   └── Jim merges
```

### 9.6 Cost model

#### Claude Code (GitHub Actions)

Already budgeted and running on the saorsa/labs repos. The docs repo adds incremental cost, not a new cost line.

**Token cost drivers**:
- **Deterministic checks find no drift**: Zero AI tokens. Only GitHub Actions compute minutes (minimal).
- **Tier 1 mechanical update**: Small prompt (the diff) + small edit (a few lines in a reference page). Estimated ~1K-5K tokens per invocation. These are the most frequent but cheapest.
- **Tier 2 issue creation**: Minimal tokens — just formatting the issue body. Could be done without AI entirely.
- **Tier 3 new page**: Larger — Claude Code reads source repos + CLAUDE.md + audit notes, generates a full page. Estimated ~10K-50K tokens per page. Infrequent (only on significant feature launches).

**During launch sprint (April 1-7)**: Higher usage as all P0 pages are generated. This is a one-time cost.

**Post-launch steady state**: Most pushes to source repos won't affect the docs at all (internal refactors, test changes, etc.). When they do, it's typically Tier 1 (cheap). Estimate: a few dollars per week in token costs, well within existing Claude Code budget.

#### Greptile

Already running on the other repos. Adding one more repo to Greptile's scope is covered by the existing plan/pricing. No new cost.

#### GitHub Actions compute

Standard GitHub Actions minutes. The deterministic checks are fast (seconds). Claude Code invocations are the longer steps but still typically under a minute. Well within free tier for public repos or within existing org allocation for private repos.

### 9.7 Administration and maintenance

**What needs ongoing human attention**:

- **CLAUDE.md updates**: When the team agrees on a style change, terminology addition, or template modification, update `CLAUDE.md`. This is version-controlled and reviewable like any other code change. Expect quarterly updates, not daily.
- **Terminology lockfile**: Add new terms as they're introduced. Remove deprecated terms. This grows slowly.
- **Tier 2 issue triage**: Jim reviews flagged drift issues periodically. During active development, maybe daily. Post-stabilisation, weekly.
- **Source repo workflow files**: The ~10-line `notify-docs.yml` needs adding to each new source repo. One-time setup per repo.
- **GitHub token management**: The `DOCS_REPO_TOKEN` secret needs maintaining in each source repo. Standard secret rotation practices.

**What runs unattended**:

- Deterministic CI checks on every PR
- Tier 1 auto-updates (Claude Code write → Greptile review → auto-merge)
- Link validation, terminology linting, build checks
- Verification staleness flagging

---

## 10. RESPONDING TO DAVID'S ANTICIPATED PUSHBACK

David Irvine will likely raise these objections. Prepared responses:

### "Why a separate dependency for documentation?"

Because documentation spans six repos. No single repo is the right home for cross-cutting content like "how self-encryption and payment work together." The docs repo is the join table — the same pattern used by Rust (rust-lang/book), Kubernetes (website), and every project that outgrew a single README.

### "Why does it lag?"

It doesn't. Event-driven automation triggers on every push to source repos. Tier 1 changes (mechanical reference updates) auto-merge with no human gate. The current approach — scattered READMEs with no cross-repo consistency checking — actually lags worse because nobody notices when README in repo A contradicts README in repo B.

### "Why can't it happen from within the GitHub repos?"

It partly does. Each repo keeps good READMEs, doc comments, and working examples. The docs site synthesises these into a coherent developer journey. Both are accurate; they serve different audiences.

### "Why GitBook?"

We already have it. docs.autonomi.com runs on GitBook. The content team knows it. It supports Git Sync (so GitHub is the source of truth), auto-generates llms.txt/llms-full.txt for AI discoverability, and has decent SEO. Moving to something else costs time we don't have for zero user-facing benefit.

### The GEO argument (lead with this)

Scattered READMEs across GitHub are invisible to foundation model training and agent crawlers. A well-structured docs site with `llms.txt`, `llms-full.txt`, and clean markdown gives Autonomi a single, authoritative surface that AI systems can consume and understand as a coherent project. This directly affects Autonomi's discoverability, visibility in AI-generated responses, and developer adoption. GitHub repos are optimised for developers who already know what they're looking for — not for discovery.

---

## 11. TOOLING SUMMARY

| Tool | Role | Already in use? | Cost |
|------|------|----------------|------|
| Claude Code (GitHub Actions) | Writes and updates documentation pages | Yes (saorsa/labs repos) | Incremental token cost within existing budget |
| Greptile | Reviews all PRs to the docs repo | Yes (saorsa/labs repos) | Covered by existing plan |
| Deterministic CI scripts | Link validation, terminology lint, template check, build | New (docs repo specific) | Zero AI cost; standard GH Actions minutes |
| GitBook Git Sync | Auto-deploys docs on merge to main | Yes (docs.autonomi.com) | Existing GitBook plan |
| CLAUDE.md | Editorial style guide + templates + terminology lockfile | Convention already used | N/A (it's a file) |

See Section 8 for automation architecture and Section 9 for detailed AI tooling, quality controls, workflows, and cost model.

---

## 12. OPEN QUESTIONS

1. **Launch-critical page scope**: Which binding pages beyond Python, JavaScript, Rust, and Go are required in the initial verified set before repo setup and GitBook sync?
2. **OpenAPI spec availability**: Does antd expose an OpenAPI/Swagger spec? This determines how automated the REST API reference generation can be.
3. **Conceptual guide v2**: Awaiting dev approval on 9 surgical changes (archives removed, EigenTrust → local trust, software attestation removed). **Reminder for Jim**: Chase this if not yet confirmed.
4. **CI secrets and cross-repo dispatch**: Will need a GitHub token with appropriate permissions for the repository_dispatch events between source repos and the docs repo.
5. **Automation implementation timeline**: Tier 1/2 automation is post-launch hardening, but the verification metadata format should be used from day one so pages are ready for it.
6. **Target manifest timing**: When does the team declare a launch-ready state for April 7? At that point, a target manifest is created and P0/P1 pages are re-verified against pinned refs.
7. ~~**ant-quic vs saorsa-transport**~~: **RESOLVED**. Mick confirmed ant-quic is an older ancestor/fork. saorsa-transport is the current transport layer. ant-quic is excluded from docs scope.
8. **SDK binding count**: ant-sdk monorepo has 16 language directories (not 15). Adds Dart, Elixir, Lua, Zig, MCP; no separate TypeScript, Cython, or JVM. Need to confirm with Nic which are shipping for launch and update IA accordingly.
9. **ant-keygen dependencies**: Couldn't fetch Cargo.toml. Almost certainly depends on saorsa-pqc given its ML-DSA-65 description. Confirm and add to dependency tree.
10. ~~**Repo and component registry files**~~: **RESOLVED**. `repo-registry.yml` and `component-registry.yml` exist in the repo and are now part of the source-audit workflow.

---

## 13. DECISION LOG

| Date | Decision | Rationale | Who |
|------|----------|-----------|-----|
| Mar 31 | Diátaxis framework for IA | Proven pattern, good for both humans and AI | Jim + Claude |
| Mar 31 | ant-sdk as primary interface | Nic confirmed REST/gRPC architecture as the primary SDK direction | Jim |
| Mar 31 | Archives removed from v2 scope | Not shipping for April 7 | Jim |
| Mar 31 | EigenTrust → local trust scoring | Mick confirmed local EMA likely sufficient | Mick |
| Mar 31 | Software attestation out of scope | Mick confirmed | Mick |
| Mar 31 | GitBook as platform | Already in use, Git Sync, llms.txt auto-generation | Jim |
| Apr 1 | REST API as canonical reference | Most bindings target the same daemon surface, so the REST API remains the primary shared reference | Jim + Nic |
| Apr 1 | Tabbed code examples via GitBook tabs | Clean .md output verified for agent consumption | Jim + Claude |
| Apr 1 | POC under jimcollinson, move to WithAutonomi later | Iterate freely, present working system to David | Jim |
| Apr 1 | Push-based automation (source repos → docs repo) | Intelligence centralised in docs repo, not spread across six repos | Jim + Claude |
| Apr 1 | Tiered automation response | Tier 1 auto-merges, Tier 2 flags, Tier 3 human-authored. Avoids bottleneck | Jim + Claude |
| Apr 1 | AI-generated, progressively automated | Launch: AI-generated + human-reviewed. Long-term: automated checks reduce human review to conceptual accuracy and low-confidence changes | Jim |
| Apr 2 | `current-merged-truth` is the default operating mode | The docs describe merged code now; `target-manifest` is only an explicit launch-hardening override | Jim + OpenCode |
| Apr 2 | Required workflow is `source audit -> draft -> verify` | Draft-first created speculative pages and invalid verification metadata; evidence-first is now mandatory | Jim + OpenCode |
| Apr 2 | Pages are not verified without real SHAs | `source_commit: TBD` is not valid on a page presented as verified | Jim + OpenCode |
| Apr 2 | Binding pages must be verified individually against current exports | Shared templates are allowed, but only after each binding's package surface, constructors, and models are checked on merged refs | Jim + OpenCode |
| Apr 1 | Claude Code (GH Actions) for doc writing | Already running on saorsa/labs repos. Same integration, known cost model | Jim + Claude |
| Apr 1 | Greptile for PR review on docs repo | Already running on other repos. Catches terminology, consistency, API validity | Jim + Claude |
| Apr 1 | CLAUDE.md as editorial style guide | Version-controlled quality controls: tone, terminology, templates, verification rules | Jim + Claude |
| Apr 1 | Deterministic checks before AI invocation | Link validation, terminology lint, template conformance — zero AI tokens when no drift detected | Jim + Claude |
| Apr 1 | Current-merged-truth as default source of truth | Docs track merged default branches; no speculative branch synthesis | Jim + Claude |
| Apr 1 | Target manifest for launch hardening | Pinned per-repo refs for final verification pass; does not require every repo to have a release | Jim + Claude |
| Apr 1 | Install pages track downloadable versions | Install/download pages must point to versions users can actually get, not just merged code | Jim + Claude |
| Apr 1 | Scope: specific Autonomi 2.0 network repos only | Not all repos in WithAutonomi/saorsa-labs — only network stack repos, plus any explicitly added | Jim + Claude |
| Apr 1 | Dependency-verified scope (11 repos) | Cargo.toml crawl confirms: ant-node, ant-client, ant-sdk, ant-keygen, evmlib, self_encryption, saorsa-core, saorsa-pqc, saorsa-transport, ant-merkle (+ x0x tangential) | Jim + Claude |
| Apr 1 | ant-evm collapsed into evmlib | Devs confirmed ant-evm absorbed into evmlib; ant-evm is out of scope | Jim (from devs) |
| Apr 1 | ant-merkle moving to WithAutonomi | Currently under MaidSafe org; will move to WithAutonomi | Jim (from devs) |
| Apr 1 | Repo class model for scope | Broad source / targeted foundational / specialist / watchlist / excluded. Drives agent and automation behaviour. | Jim + Claude |
| Apr 1 | Component registry maps code to pages | Components (crates, binaries, specs) within repos mapped to specific doc pages. Enables precise re-verification. | Jim + Claude |
| Apr 1 | ant-quic excluded | Mick confirmed as older ancestor/fork. saorsa-transport is the current transport layer. | Mick |
| Apr 1 | ant-evm on watchlist (not fully excluded) | Collapsed into evmlib but worth watching until all references disappear from merged code | Jim + Claude |
| Apr 1 | saorsa-transport is the transport source of truth | Not ant-quic. QUIC/NAT traversal docs verified against saorsa-transport. | Mick + Claude |

---

## 14. NEXT STEPS (IMMEDIATE)

1. **Transfer and rename the docs repo** to `WithAutonomi/autonomi-developer-docs`
2. **Reconnect and verify GitBook Git Sync** after transfer and rename
3. **Confirm maintainer and contributor PR flow** under `WithAutonomi`
4. **Verify Claude reviews and secrets** under the organisation setup
5. **Add repo governance basics**: branch protection, CODEOWNERS, contribution guidance
6. **Introduce upstream-triggered review automation** once the org setup is stable
