---
name: start
description: |
  Build applications, automations, and AI workflows on the Autonomi Network.
  Use this skill when the user wants to store or retrieve data, add Autonomi
  storage to an application, build read-only or upload-enabled features, use
  the `antd` daemon and SDK bindings, work from the `ant` CLI, build directly
  in Rust with `ant-core`, or expose Autonomi through an MCP-compatible client.
  Do not use for Autonomi 1.0, the MaidSafe-era network, `ant-quic`, or
  general EVM work that is not part of building on Autonomi.
version: 0.1.3-draft
license: MIT
repository: https://github.com/WithAutonomi/autonomi-developer-docs
homepage: https://docs.autonomi.com/developers
author: Autonomi Developer Documentation
keywords:
  - autonomi
  - ant-sdk
  - antd
  - ant-client
  - ant-core
  - ant
  - ant-protocol
  - mcp
  - devnet
  - datamap
  - self-encryption
  - uploads
  - read-only

# Verification block. Re-verify before changing stable claims or examples.
verified_date: 2026-05-02
verification_mode: current-merged-truth
verified_commits:
  ant-sdk: d7652ec3da82dfbe2107778e5223dc413d95815b
  ant-client: 71ad53b047f7fc6b55e73ce6008d0a834feebbd6
  ant-node: 23aee15cae33a17257ba833b2b98ed8a7a12e684
  ant-protocol: 65651f3a3243af8299a3e8d63385cba846ef88a4
  self_encryption: 5f9d1646231da7ca2ce60e84d010acfb6d9c29d0
  evmlib: 225acbb1af613193bcc8264b6ede4d7e4a7ac607

version_manifest_url: https://raw.githubusercontent.com/WithAutonomi/autonomi-developer-docs/main/skills/start/version.json
canonical_docs_url: https://docs.autonomi.com/developers
---

# Autonomi Developer

This skill makes you effective at building on the Autonomi Network without making the user read the full docs set first. Treat it as an operational guide: pick the correct Autonomi path, fetch one live reference when exact interface details matter, and do not invent Autonomi-specific APIs.

## Scope

Use this skill when the task is about:

- storing or retrieving data on Autonomi
- adding Autonomi storage to an application
- building read-only or upload-enabled features
- using `antd` and the SDK bindings
- using the `ant` CLI
- building directly in Rust with `ant-core`
- exposing Autonomi through an MCP-compatible client
- testing with a local devnet before public-network deployment

Do not use this skill for:

- Autonomi 1.0 or anything under the MaidSafe org unless the user explicitly wants historical context
- `ant-quic` or older transport docs
- general EVM, Arbitrum, IPFS, or Filecoin work unrelated to building on Autonomi

## Operating Rules

1. Check whether a newer verified version of this skill exists:

```bash
curl -fsSL https://raw.githubusercontent.com/WithAutonomi/autonomi-developer-docs/main/skills/start/version.json
```

If the published `version` is newer, tell the user this copy may be stale and offer to reload it. If the fetch fails, continue silently. For an unpublished draft, that usually means the skill is not on `main` yet.

2. Pick one path before you start coding: SDK, CLI, Direct Rust, or MCP.

3. Fetch one live reference page once per task when you need volatile details such as install steps, exact REST or gRPC schemas, binding-specific helpers, CLI flags, MCP tool names, devnet-manifest fields, or prepare/finalize payload shapes.

4. Do not invent Autonomi-specific details. If this skill does not name a route, flag, method, env var, or tool and you have not fetched the live reference, do not guess it.

5. For anything that uploads data, start on a local devnet first unless the user explicitly wants public-network work.

6. Ask before installing software, configuring wallets, or touching real ANT on a public network.

## Path Selector

| Path | Choose it when the user wants to... | Fetch first when details matter |
|------|-------------------------------------|---------------------------------|
| SDK | Build an application in Python, JavaScript, TypeScript, Rust, Go, Java, C#, Kotlin, Swift, Ruby, PHP, C++, Dart, or Zig through a local daemon | language page plus REST or gRPC reference |
| CLI | Work from the shell, script uploads or downloads, inspect wallets, or do operational workflows | CLI command reference |
| Direct Rust | Build daemon-free Rust with direct network control or local devnet helpers | Rust getting-started page plus library reference |
| MCP | Let an MCP-compatible client talk to Autonomi through `antd` | MCP setup page plus MCP server reference |

If the user has not chosen a path, recommend SDK first. It is the best fit for most application work.

## Fast Lookup Discipline

Use this workflow to stay fast without guessing:

1. Decide whether the feature is read-only or upload-enabled.
2. Pick a path.
3. Check the local prerequisite for that path.
4. Fetch one live page for the path-specific details.
5. Reuse that page for the rest of the task instead of re-fetching several pages.

For SDK and MCP work, the fastest first check is usually:

```bash
curl http://localhost:8082/health
```

Expected shape:

```json
{
  "status": "ok",
  "network": "default"
}
```

Treat `network` as environment-dependent. On a local devnet, it is typically `local` instead of `default`.

If the user is on a non-default host or port, ask for the base URL instead of assuming `localhost:8082`.

## Path Playbooks

### SDK

Choose SDK when the user wants normal application development in a supported language. This path goes through `antd`.

Current daemon defaults:

- REST: `http://localhost:8082`
- gRPC: `localhost:50051`
- several SDKs expose helpers that read the `daemon.port` file written by `antd`

Current shared daemon surfaces you can rely on at this commit:

- `GET /health`
- `POST /v1/data/public`
- `GET /v1/data/public/{addr}`
- `POST /v1/data/private`
- `GET /v1/data/private`
- `POST /v1/data/cost`
- `POST /v1/files/cost`
- `GET /v1/wallet/address`
- `GET /v1/wallet/balance`
- `POST /v1/wallet/approve`
- `POST /v1/data/prepare`
- `POST /v1/upload/prepare`
- `POST /v1/upload/finalize`

Golden public-data round trip:

```bash
DATA_B64=$(printf 'Hello, Autonomi!' | base64)

curl -X POST http://localhost:8082/v1/data/public \
  -H "Content-Type: application/json" \
  -d "{\"data\":\"$DATA_B64\"}"

curl http://localhost:8082/v1/data/public/<address>
```

Keep these rules straight:

- REST binary payloads are base64 inside JSON.
- `POST /v1/data/public` returns a public address.
- `POST /v1/data/private` returns a serialized `DataMap`.
- `GET /v1/data/private` needs the `data_map` query parameter.
- read-only daemon work does not require `AUTONOMI_WALLET_KEY`

Current documented binding entry points:

- Python: `AntdClient()` or `AsyncAntdClient()`
- JavaScript and TypeScript: `createClient()`
- Go: `NewClient(...)`
- Rust SDK: `Client::new(...)`

Standalone binding pages also exist for Java, C#, Kotlin, Swift, Ruby, PHP, C++, Dart, and Zig. Fetch the language-specific page when the user is working in one of those SDKs.

The bindings overview is not exhaustive for every standalone binding page. Use the direct language page when one exists instead of assuming the overview lists everything.

Before writing SDK code beyond health checks and the public-data round trip, fetch the binding page for the user's language.

### CLI

Choose CLI when the user wants direct shell workflows, scripts, CI automation, wallet inspection, or quick operational tasks without `antd` in the data path.

Current CLI rules that matter in practice:

- data commands do not require the daemon
- root flags such as `--bootstrap`, `--devnet-manifest`, `--allow-loopback`, and `--evm-network` come before the subcommand
- the direct-network `ant` CLI's main top-level groups are `file`, `chunk`, `wallet`, `node`, and `update`
- uploads and wallet commands require `SECRET_KEY`

Golden public-file flow on a local devnet:

```bash
SECRET_KEY=0x... ant \
  --devnet-manifest /tmp/devnet.json \
  --allow-loopback \
  --evm-network local \
  file upload photo.jpg --public

ant \
  --devnet-manifest /tmp/devnet.json \
  --allow-loopback \
  --evm-network local \
  file download <address> -o photo_copy.jpg
```

Keep these rules straight:

- private file uploads save a local `.datamap` file instead of returning a public address
- private file downloads use `--datamap <PATH>`
- public downloads do not need a wallet

For anything beyond these patterns, fetch the CLI command reference first.

### Direct Rust

Choose Direct Rust when the user wants daemon-free Rust, native Rust types, direct client control, or built-in local devnet helpers.

Current `ant-core` surfaces you can name safely:

- `Client::connect(...)`
- `with_wallet(...)`
- `data_upload(...)`
- `data_download(...)`
- `file_upload_with_mode(...)`
- `file_download(...)`
- `data_map_store(...)`
- `data_map_fetch(...)`
- `LocalDevnet::start_minimal()`
- `LocalDevnet::create_funded_client(...)`

Use Direct Rust when the user needs those native surfaces. Do not infer full method signatures or argument shapes from memory; fetch the Rust getting-started page and the library reference before writing the code.

### MCP

Choose MCP when an MCP-compatible client should use Autonomi through structured tools instead of raw HTTP.

Current MCP setup facts:

- server command: `antd-mcp`
- install pattern:

```bash
pip install "antd[rest]"
pip install -e antd-mcp/
```

Run the editable install from an `ant-sdk` checkout root.

- stdio mode: `antd-mcp`
- SSE mode: `antd-mcp --sse`
- daemon discovery still attempts this order:
  - `ANTD_BASE_URL`
  - `daemon.port`
  - `http://127.0.0.1:8082`

`ANTD_BASE_URL` is the reliable MCP setup path because `antd` writes `ant/sdk/daemon.port` while `antd-mcp` reads `ant/daemon.port`.

Do not memorize MCP tool names or schemas in this skill. Fetch the MCP server reference when the task is MCP-specific.

## Concepts That Affect Implementation

### Public vs private data

Autonomi has one underlying storage primitive: encrypted chunks. Public and private data differ mainly in where the `DataMap` lives.

- public data returns an address that can be shared and fetched later
- private data returns a `DataMap` that the caller must keep
- if private retrieval is failing, check for a missing or wrong `DataMap` before anything else

### Wallet keys vs retrieval material

These are different things:

- `AUTONOMI_WALLET_KEY` pays for uploads through `antd`
- `SECRET_KEY` pays for uploads and wallet commands through `ant`
- an attached `Wallet` pays for uploads through `ant-core`
- a public address retrieves public data
- a `DataMap` retrieves private data

Do not collapse those concepts into one key-handling model.

### Read-only vs upload-enabled features

This is the first architectural split to make.

If the feature is read-only:

- no ANT is required
- no gas is required
- no wallet is required
- the daemon can run without `AUTONOMI_WALLET_KEY`

If the feature uploads data:

- local devnet gives you funded local test wallets
- public networks need ANT plus gas on the selected EVM network
- wallet setup becomes part of the feature, not an afterthought

### Local devnet first

For upload-enabled work, the shortest safe loop is:

```bash
ant dev start --ant-node-dir ../ant-node
ant dev status
ant dev wallet show
curl http://localhost:8082/health
```

The local environment gives you a running devnet, `antd --network local`, and a funded local wallet. Stop it with:

```bash
ant dev stop
```

These `ant dev` commands come from the `ant-dev` package in `ant-sdk`, not from the direct-network `ant` CLI in `ant-client`.

The devnet-manifest handoff is shared across client and node code. Treat its exact field shape as volatile and fetch the live reference before automating around it.

### Payment modes and external signing

Current upload payment modes are:

- `auto`
- `merkle`
- `single`

Use `auto` unless the user has a reason to force the behavior. If the user wants explicit cost estimation before an upload, use the current cost endpoints or the path-specific reference page.

The prepare/finalize flows are also shared across multiple layers now. Treat exact prepare payload fields, finalize variants, and Merkle versus wave-batch response shapes as volatile and fetch the live reference before writing code around them.

## Common Failures

### Daemon health check fails

The daemon is not running, it is on a different port, or the task should be using CLI or Direct Rust instead of SDK or MCP.

### `503` on daemon write routes

`antd` is reachable but wallet configuration is missing. Check `AUTONOMI_WALLET_KEY` or switch to an external-signer flow.

### `insufficient funds`

Distinguish between missing ANT and missing gas. Do not tell the user to fund the wallet without identifying which balance is missing.

### Private retrieval fails

Check the `DataMap` first. Private content still needs the retrieval metadata even after the content has already been paid for.

### CLI command shape looks wrong

Check whether the root flags were placed after the subcommand. In `ant`, global flags belong before `file`, `chunk`, `wallet`, `node`, or `update`.

### Tests fail against the daemon surface

Check whether the test expects raw bytes over REST. Current REST binary payloads are JSON with base64 in the `data` field.

## Hard Constraints

- Do not reference Autonomi 1.0 as if it were current.
- Do not reference `ant-quic` in Autonomi 2.0 work.
- Do not guess endpoints, flags, method names, or contract details.
- Do not put real wallet keys into committed code.
- Do not walk a user into public-network uploads without checking that they understand the money and irreversibility involved.
- Stay on one Autonomi path unless the user explicitly asks for a comparison.

## Live References

Use these pages as the first lookup for current details:

| Need | Live page |
|------|-----------|
| Overview | `https://docs.autonomi.com/developers` |
| SDK entry point | `https://docs.autonomi.com/developers/sdk/install` |
| SDK first upload | `https://docs.autonomi.com/developers/sdk/install/store-data-on-the-network` |
| SDK first retrieval | `https://docs.autonomi.com/developers/sdk/install/retrieve-data-from-the-network` |
| SDK store and retrieve guide | `https://docs.autonomi.com/developers/sdk/install/how-to-guides/store-and-retrieve-data` |
| SDK daemon as service | `https://docs.autonomi.com/developers/sdk/install/how-to-guides/use-the-daemon-as-a-local-service` |
| REST API | `https://docs.autonomi.com/developers/sdk/install/reference/rest-api` |
| gRPC services | `https://docs.autonomi.com/developers/sdk/install/reference/grpc-services` |
| Daemon command reference | `https://docs.autonomi.com/developers/sdk/install/reference/daemon-command-reference` |
| Language bindings overview | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/overview` |
| Python SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/python` |
| JavaScript SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/javascript` |
| TypeScript SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/typescript` |
| Rust SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/rust` |
| Go SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/go` |
| Java SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/java` |
| C# SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/csharp` |
| Kotlin SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/kotlin` |
| Swift SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/swift` |
| Ruby SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/ruby` |
| PHP SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/php` |
| C++ SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/cpp` |
| Dart SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/dart` |
| Zig SDK | `https://docs.autonomi.com/developers/sdk/install/reference/language-bindings/zig` |
| CLI quickstart | `https://docs.autonomi.com/developers/cli/use-the-cli` |
| CLI command reference | `https://docs.autonomi.com/developers/cli/command-reference` |
| Direct Rust quickstart | `https://docs.autonomi.com/developers/developing-in-rust/build-directly-in-rust` |
| Rust library reference | `https://docs.autonomi.com/developers/developing-in-rust/library-reference` |
| MCP setup | `https://docs.autonomi.com/developers/mcp/use-the-autonomi-mcp-server` |
| MCP reference | `https://docs.autonomi.com/developers/mcp/mcp-server-reference` |
| Local devnet | `https://docs.autonomi.com/developers/guides/set-up-a-local-network` |
| Prepare a wallet | `https://docs.autonomi.com/developers/guides/prepare-a-wallet-for-uploads` |
| Payments and cost estimation | `https://docs.autonomi.com/developers/guides/estimate-costs-and-handle-upload-payments` |
| Read-only features | `https://docs.autonomi.com/developers/guides/build-read-only-features` |
| Testing | `https://docs.autonomi.com/developers/guides/test-your-application` |
| Deploy to mainnet | `https://docs.autonomi.com/developers/guides/deploy-to-mainnet` |
| Data types | `https://docs.autonomi.com/developers/core-concepts/data-types` |
| Keys, addresses, and DataMaps | `https://docs.autonomi.com/developers/core-concepts/keys-addresses-and-datamaps` |
| Self-encryption | `https://docs.autonomi.com/developers/core-concepts/self-encryption` |
| Payment model | `https://docs.autonomi.com/developers/core-concepts/payment-model` |
| System overview | `https://docs.autonomi.com/developers/architecture/system-overview` |
| Glossary | `https://docs.autonomi.com/developers/reference-extras/glossary` |
| Source repositories | `https://docs.autonomi.com/developers/reference-extras/source-repositories` |

## If Something Conflicts

Trust the live docs over stale memory. If the live docs and this skill disagree, tell the user the skill may be stale, use the live docs for the task in front of you, and update the skill package in this repo afterward.
