# CLAUDE.md — Autonomi Developer Documentation

This file controls how AI agents (Claude Code, Greptile, automation) behave when writing, updating, or reviewing documentation in this repository.

## Repository purpose

This repo is the source of truth for docs.autonomi.com/developers. It is synced to GitBook via Git Sync. All content is Markdown. The site follows the Diátaxis framework: Getting Started → Core Concepts → How-to Guides → Reference.

## Scope

This repo documents the Autonomi 2.0 network. See `repo-registry.yml` for which upstream repos are in scope and how to treat each one. See `component-registry.yml` for which components map to which pages.

**Do not** reference or verify against:
- Autonomi 1.0 (MaidSafe org)
- ant-quic (excluded — older ancestor/fork; use saorsa-transport instead)
- Any repo not listed in the repo registry

## Audience and objectives

### Who these docs are for

- **Human developers** building applications and services on Autonomi — from indie hackers to enterprise teams
- **AI agents** consuming documentation via llms.txt to interact with the network programmatically
- Assume the reader is a competent developer who is new to Autonomi, not new to programming

### What these docs must enable

The primary use cases, in priority order:

1. **Storing data** on the Autonomi Network
2. **Retrieving data** from the Autonomi Network
3. **Building applications** that use Autonomi as their storage layer
4. **Creating services** that integrate with the network

### Priority hierarchy

**Practical usage ("what can I do?") always takes priority over network internals ("how does it work?").**

When deciding what to foreground on a page, ask: "Does a developer need this to store data, retrieve data, or build an application?" If yes, it is first-class content. If no, it is supporting context.

Network internals (chunks, DataMaps, content addressing, Kademlia routing) are valuable context and belong in the docs, but they are secondary to practical guidance. A developer should be able to use every data type without understanding the internal storage mechanics. Internals should appear in dedicated concept pages or as brief "under the hood" sections — never as the primary framing of a page that teaches developers how to do something.

## Source of truth

The repo has two verification modes: `current-merged-truth` and `target-manifest`.

### `current-merged-truth`

This is the default mode. For each page, it means the latest merged commit on the default branch of each in-scope source repo at the time of the source audit.

Rules:
- Do not document unmerged feature branches, PR branches, or expected future behavior.
- If a capability exists only on a branch or is "expected by launch", it is out of scope until it merges.
- Installation, download, package, and version pages must point to artifacts that users can actually install now, even if merged code is newer.

### `target-manifest`

This is an explicit override for launch hardening or release verification. A `target-manifest.yml` pins the exact refs the docs must match.

Rules:
- Use this mode only when a `target-manifest.yml` exists and the task explicitly says to verify against it.
- Verify against the pinned refs in the manifest, not the moving default branches.
- Record `verification_mode: target-manifest` in the verification block for pages checked this way.
- When no target manifest is active, fall back to `current-merged-truth`.

### Required workflow

All documentation work follows `source audit -> draft -> verify`. Follow the detailed procedure in `planning/verification-workflow.md`.

- **Source audit**: determine page type and source repos, resolve the active refs and exact SHAs, and collect canonical source artifacts before writing.
- **Draft**: write only from audited evidence. If evidence is missing, stop and defer, stub, or reframe the page.
- **Verify**: check every endpoint, command, type, field, code sample, and technical claim against the audited sources, then add verification block(s) with real SHAs.

### Refusal rules

- Do not use `source_commit: TBD` on a page presented as verified.
- Do not mark a page as verified without real commit SHAs.
- Do not infer endpoints, commands, package names, constructors, types, or product surfaces that are not present in the active source of truth.
- Historical notes, research memos, and prior synthesis documents are not authoritative. They may help you locate likely source files, but they cannot justify a technical claim.
- For pages verified against multiple repos, include multiple verification blocks.

---

## Style guide

### Voice and tone

- Write in **second person** ("you"), **present tense**, **active voice**
- Be direct and precise. Respect the developer's time.
- Explain the "why" before the "how" — one sentence of context, then the steps
- Lead with the product, user task, or developer path, not with internal repo or implementation names, unless the tool name itself is the topic of the page
- Do not surface provenance language such as `current-merged-truth`, "current merged", refs, audits, or verification modes in rendered prose. Keep that information in verification comments and workflow docs only.
- Do not use repo names as primary page titles, nav labels, or opening framing unless the repo itself is the topic.
- Avoid time-relative or changelog-style wording in rendered docs unless the page is explicitly comparing versions. Prefer direct statements of fact over words like `current`, `now`, `currently`, or phrases such as `in the current implementation`.
- Use `path` language only on pages where the reader is explicitly choosing between routes. In normal prose, prefer phrases like "using the SDKs", "using the CLI", or "building in Rust with ant-core".
- Prefer system behavior and user-facing tool names over repo names in ordinary explanatory prose.
- Avoid provenance terms such as `upstream` and `downstream` in rendered prose unless the page is explicitly about source repositories, contribution workflow, or source verification.
- Do not narrate the evidence in rendered prose. Avoid phrases like `the README says`, `the README notes`, `the README documents`, `the documentation describes`, `the relevant repos`, or `the sources covered here`. State the system, tool, or workflow directly and confidently. If a claim is not strong enough to state directly, re-audit it or remove it.
- Expand important acronyms on first use when that helps a first-time reader.
- See [Audience and objectives](#audience-and-objectives) for reader assumptions

### Prohibited words and phrases

Never use:
- "simply", "just", "easy", "easily", "obviously", "of course"
- "we" (Autonomi is a decentralised network, not a company speaking)
- "please" (documentation is not a request)
- "leverage" (use "use")
- "utilize" (use "use")
- "in order to" (use "to")
- "it should be noted that" (just state it)

### Terminology

All technical terms must match the terminology lockfile below exactly. Using the wrong form is a linting error.

On first mention in rendered prose, expand important acronyms when that helps a first-time reader. For example, use `Autonomi Network Token (ANT)` on first mention, then `ANT` afterward.

### Code examples

- Must be **complete and runnable**. Never snippets that require imagination.
- Always include imports, error handling, and expected output
- Use `{% tabs %}` / `{% tab title="Language" %}` blocks for multi-language examples (GitBook syntax)
- cURL is always the first tab (canonical)
- For major SDK guides, the default featured tab order is cURL, Python, Node.js / TypeScript, and Rust when those examples are supported and verified
- When a page shows only a subset of supported SDK languages, say that other SDK languages are available and link to the language-specific references
- Every code example must specify the language in the code fence (```python, ```bash, etc.)

### Page structure

- Every page must be **self-contained**. No "as we discussed in the previous section" or "see above."
- An agent reading any single page via llms.txt should understand the topic without needing other pages.
- Link to related pages at the end, not inline as prerequisites.
- When you mention another supported tool, route, or approach that is not explained on the current page, add an inline link to the relevant page if one exists.
- Getting Started and How-to pages must explain what tool or route they cover, why you would choose it, and where the alternatives live when multiple supported routes exist.
- Explain a tool or interface before telling the reader to install, run, or configure it.
- Titles should describe user outcomes or choices, not internal mechanisms, unless the mechanism name itself is the thing the page teaches.
- Do not use inline code spans in headings. For commands, endpoints, and signatures, use a readable heading and put the exact literal syntax on the next line.
- Glossary entries should be short, timeless definitions. Avoid changelog phrasing, repo framing, and unnecessary implementation qualifiers.
- Do not inline-link repo names throughout normal prose by default. When useful, add a short `Upstream sources` section near the end of overview, concept, or reference pages instead.

### Formatting

- Use ATX-style headers (`#`, `##`, `###`). Maximum depth: `###`.
- One blank line before and after headers, code blocks, and lists
- No trailing whitespace
- No HTML in Markdown (GitBook handles rendering)
- No emojis unless explicitly requested

---

## Page templates

Each page type has a required structure. Follow the template for the page type determined by its directory location.

### Getting Started pages

```
# [Title]

<!-- verification:
  source_repo: [repo]
  source_ref: [branch/tag]
  source_commit: [sha]
  verified_date: [YYYY-MM-DD]
  verification_mode: current-merged-truth
-->

[One-paragraph summary: what this page helps you do]

## Prerequisites

[Bulleted list of what you need before starting]

## Steps

### 1. [First step]
[Instructions + code]

### 2. [Second step]
[Instructions + code]

[Continue numbered steps...]

## What happened

[Brief explanation of what the steps above actually did under the hood. 2-3 sentences max.]

## Next steps

[Links to logical next pages]
```

### Core Concept pages

```
# [Title]

<!-- verification:
  source_repo: [repo]
  source_ref: [branch/tag]
  source_commit: [sha]
  verified_date: [YYYY-MM-DD]
  verification_mode: current-merged-truth
-->

[One-sentence definition of the concept]

## Why it matters

[1-2 paragraphs: why a developer building on Autonomi needs to understand this]

## How it works

[Technical explanation with diagrams or pseudocode where helpful]

## Practical example

[Concrete example showing the concept in action]

## Related pages

[Links to related concepts and how-to guides]
```

### How-to Guide pages

```
# [Title]

<!-- verification:
  source_repo: [repo]
  source_ref: [branch/tag]
  source_commit: [sha]
  verified_date: [YYYY-MM-DD]
  verification_mode: current-merged-truth
-->

[One-sentence summary: what you will accomplish]

## Prerequisites

[What you need before starting]

## Steps

### 1. [First step]

{% tabs %}
{% tab title="cURL" %}
```bash
[cURL example]
```
{% endtab %}
{% tab title="Python" %}
```python
[Python example]
```
{% endtab %}
{% tab title="JavaScript" %}
```javascript
[JavaScript example]
```
{% endtab %}
{% endtabs %}

[Continue steps with tabbed examples...]

## Verify it worked

[How to confirm the operation succeeded]

## Common errors

[2-3 common errors and their solutions]

## Next steps

[Links to related guides]
```

### Reference pages

```
# [Title]

<!-- verification:
  source_repo: [repo]
  source_ref: [branch/tag]
  source_commit: [sha]
  verified_date: [YYYY-MM-DD]
  verification_mode: current-merged-truth
-->

[One-paragraph overview of what this reference covers]

## [Endpoint/Command/Type group]

### `[METHOD /path]` or `[command]`

[Description]

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| ... | ... | ... | ... |

**Response:**
```json
[Example response]
```

**Example:**
```bash
[cURL example]
```

[Continue for each endpoint/command/type...]

## Error codes

| Code | Meaning | Resolution |
|------|---------|------------|
| ... | ... | ... |
```

### Language Binding pages

```
# [Language] SDK

<!-- verification:
  source_repo: ant-sdk
  source_ref: [branch/tag]
  source_commit: [sha]
  verified_date: [YYYY-MM-DD]
  verification_mode: current-merged-truth
-->

The [Language] SDK is a thin REST/gRPC client for the antd daemon.

## Install

```[language]
[install command]
```

## Connect to the daemon

```[language]
[import + client init]
```

## Store and retrieve data

```[language]
[complete working example: store a string, get address, retrieve, verify]
```

## Type mappings

| Autonomi type | [Language] type |
|---------------|----------------|
| ... | ... |

## Error handling

```[language]
[idiomatic error handling example]
```

## Full API reference

For all available endpoints, see the [REST API Reference](../rest-api.md).
```

---

## Verification rules

Every page must include a verification comment in its frontmatter (see templates above).

A page is not verified unless every verification block contains a real `source_commit` SHA from the active source-of-truth mode.

### What "verified" means

- **Reference pages**: Every endpoint, function, type, and field mentioned exists in the current codebase at the specified commit. Machine-verifiable.
- **Concept pages**: Every technical claim can be traced to the active source repos at the specified commit. Human-checkable.
- **How-to guides**: Every code example runs successfully against the current SDK version. Machine-verifiable.
- **Getting-started pages**: The full flow works end-to-end. Manually verified before each release.

### Verification metadata format

```html
<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: abc1234def5678
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
```

Never use `source_commit: TBD` on a page presented as verified.

For pages verified against multiple repos, include multiple verification blocks.

---

## Terminology lockfile

Canonical terms and their prohibited alternatives. Used by both agents (when writing) and CI (when linting).

```
# Format: canonical_term | prohibited_alternatives | definition

# Network and system
Autonomi | autonomi, AUTONOMI, Autonomy | Autonomi is a decentralised data storage network
Autonomi Network | Autonomi network, the network | The peer-to-peer network of Autonomi nodes
decentralized | decentralised | (Use American English spelling throughout)

# Data model
self-encryption | self encryption, Self-Encryption, Self Encryption | Client-side encryption using content-derived keys
chunk | Chunk | A unit of encrypted data (max 4MB) stored on the network
DataMap | data map, Data Map, datamap, Datamap | Mapping from a file to its chunks and network addresses
content addressing | content-addressing, Content Addressing | Deriving a data address from its cryptographic hash

# Cryptography
ChaCha20-Poly1305 | chacha20, Chacha20, CHACHA20 | Stream cipher used for self-encryption
BLAKE3 | blake3, Blake3 | Cryptographic hash function used for content addressing
ML-DSA-65 | MLDSA65, ML-DSA65, Dilithium | NIST FIPS 204 digital signature algorithm
ML-KEM-768 | MLKEM768, ML-KEM768, Kyber | NIST FIPS 203 key encapsulation mechanism
post-quantum cryptography | PQC, post quantum | Cryptographic algorithms resistant to quantum attacks
HKDF | hkdf | HMAC-based Key Derivation Function

# Software components
antd | the daemon, ant daemon, Ant Daemon, ANT daemon | The ant-sdk daemon process
ant-sdk | Ant SDK, ANT SDK, ant sdk | SDK for building on Autonomi (daemon + REST/gRPC + bindings)
ant-client | Ant Client, ANT Client | Rust CLI and library for direct network access
ant-core | Ant Core, ANT Core | Rust library powering ant-client
ant-keygen | Ant Keygen | ML-DSA-65 key management utility

# Network concepts
Kademlia DHT | Kademlia distributed hash table, kademlia | Standard Kademlia distributed hash table for peer routing
close group | Close Group, close-group | The set of nodes closest to a data address in XOR space
XOR distance | xor distance, Xor distance | Metric used by Kademlia to determine node proximity
NAT traversal | NAT Traversal, nat traversal | Techniques for connecting peers behind NAT devices
QUIC | quic | UDP-based transport protocol

# Payments
Autonomi Network Token (ANT) | ANT token, Ant token, ant token | ERC-20 token on Arbitrum used for network payments
Arbitrum | arbitrum | Layer 2 Ethereum network where Autonomi Network Token (ANT) operates
pay-once | pay once, Pay Once | Storage payment model: single upfront payment, no ongoing fees
Merkle batch payment | merkle batch payment, Merkle Batch Payment | Efficient multi-chunk payment verification using Merkle trees

# Trust and security
local trust scoring | Local Trust Scoring, EigenTrust | Node reputation system based on local EMA observations
```

---

## Drafting rules for agents

### When writing a new page

1. Determine the active verification mode: `current-merged-truth` by default, `target-manifest` only when explicitly active
2. Run the source audit described in `planning/verification-workflow.md`
3. Identify the page type from its directory location
4. Follow the template for that page type (see above)
5. Identify the user path when relevant (for example: SDKs and daemon, CLI, or direct Rust) and make sure the page is explicit about which path it covers
6. Start from **broad source repos** (ant-sdk, ant-client, ant-node)
7. Add **targeted foundational repos** only when the page topic requires them (check component-registry.yml)
8. Use only terms from the terminology lockfile
9. Keep provenance and verification language out of the rendered body text
10. Verify the page against the audited evidence, then add the verification metadata comment with the repo, ref, and commit you verified against
11. Every code example must be complete and runnable

### When updating an existing page

1. Read the current page content first
2. Determine the active verification mode and re-run the relevant source audit from `planning/verification-workflow.md`
3. Make the minimum change required to address the drift
4. Preserve the existing structure, tone, and formatting
5. Update the verification metadata to reflect the new source commit
6. Do not rewrite sections that are still accurate

### When reviewing a page (Greptile / PR review)

Check for:
- Terminology violations (compare against lockfile)
- Code examples that reference non-existent APIs
- Structural deviations from page templates
- Cross-page contradictions
- Missing or stale verification metadata
- Prohibited words or phrases
