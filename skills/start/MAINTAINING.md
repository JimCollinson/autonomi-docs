# Maintaining the Autonomi Developer Skill

This skill lives in `skills/start/` (slash-invoked as `/developer:start` after install via the `withautonomi` marketplace) and follows the same source-of-truth model as the rest of the docs repo.

## Files that move together

Every release or re-verification pass updates these files together:

- `SKILL.md`
- `version.json`
- `CHANGELOG.md`

## Current scope

This skill is intentionally practical. It covers:

- SDK and daemon workflows
- CLI workflows
- Direct Rust with `ant-core`
- MCP setup rules
- read-only versus upload-enabled architecture
- local devnet testing
- wallet and payment basics needed to build safely

It does not try to teach the deeper routing, transport, or cryptography internals in detail. It only keeps the minimum protocol-adjacent guidance needed to stay safe around devnet manifests and prepare/finalize upload flows.

## Verification inputs

Use the same workflow the docs use:

1. Source audit
2. Draft
3. Verify

Read these repo files before changing the skill:

- `CLAUDE.md`
- `planning/verification-workflow.md`
- `repo-registry.yml`
- `component-registry.yml`

## Components that currently feed this skill

The skill is mapped through `feeds_skills:` in `component-registry.yml`.

Current component coverage:

- `antd`, `openapi`, `proto`, `ant-dev`, and `antd-mcp`
- the documented `antd-*` language bindings with standalone current-doc pages
- `ant-core`
- `ant-cli`
- `ant-node`
- `ant-devnet`
- `self_encryption`
- `evmlib`
- `ant-protocol`

Treat these repos as the skill's re-verification inputs today:

- `ant-sdk`
- `ant-client`
- `ant-node`
- `self_encryption`
- `evmlib`
- `ant-protocol`

## When to re-verify

Run a skill verification pass when:

- one of the mapped repos changes in a way that can affect the skill
- a docs page URL baked into `SKILL.md` changes
- a golden flow in the skill stops matching the current docs or source artifacts
- the skill adds or removes path coverage
- protocol-adjacent guidance in the skill changes, such as devnet-manifest behavior or prepare/finalize upload semantics

## What to verify

### SDK path

Check current daemon defaults and exact route names against the active `ant-sdk` source artifacts.

Use these artifacts first:

- `antd/openapi.yaml`
- `antd/proto/`
- `docs/sdk/reference/rest-api.md`
- `docs/sdk/reference/daemon-command-reference.md`

### CLI path

Check command names, global-flag placement, and quickstart flows against the active `ant-client` sources.

Use these artifacts first:

- `docs/cli/use-the-cli.md`
- `docs/cli/command-reference.md`
- current help output if you have the repo checked out locally

### Direct Rust path

Check named `ant-core` surfaces against the active `ant-client` sources.

Use these artifacts first:

- `docs/rust/build-directly-in-rust.md`
- `docs/rust/library-reference.md`
- upstream `ant-client` examples when signatures or helper names matter

### MCP path

Check MCP setup rules, tool names, and daemon discovery against the active `ant-sdk` sources.

Use these artifacts first:

- `docs/mcp/use-the-autonomi-mcp-server.md`
- `docs/mcp/mcp-server-reference.md`
- `antd-mcp/README.md` when the docs are being refreshed at the same time

### Concepts and safety rules

Check these against the relevant docs pages and source repos:

- public versus private data
- wallet key versus public address versus `DataMap`
- self-encryption behavior
- payment and wallet handling
- local devnet workflow
- protocol-adjacent operational details such as devnet-manifest handoff and prepare/finalize variants

## Update order

1. Update `SKILL.md`.
2. Update `version.json` with the same version, date, and verified commits.
3. Add a matching entry to `CHANGELOG.md`.

## Versioning

Use Semantic Versioning with these rules:

- major: breaking changes to skill loading or manifest shape
- minor: new paths, new verified examples, or new operational capabilities
- patch: wording fixes, pointer fixes, or re-verification-only updates

Keep the `-draft` suffix until the skill has gone through at least one deliberate re-verification pass after landing in the repo.

## Pre-merge checklist

- [ ] `SKILL.md`, `version.json`, and `CHANGELOG.md` agree on the version.
- [ ] `verified_date` and `published_date` match.
- [ ] every `verified_commits` entry is a real SHA.
- [ ] every live-docs URL in `SKILL.md` resolves.
- [ ] no hard-coded detail was added without a matching verification source.
- [ ] the skill still avoids guessed SDK methods, CLI flags, MCP tool names, and protocol payload shapes.
