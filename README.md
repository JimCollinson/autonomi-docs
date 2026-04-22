# Autonomi Developer Docs

This repo is the curated developer documentation assembly for building on Autonomi and is intended to power what developers consume through `docs.autonomi.com/developers`.

The upstream repositories remain the implementation truth. This repo brings their merged surfaces together into one coherent developer experience so people do not have to jump between multiple repos and reconstruct how the network and tooling fit together.

It is designed to serve several purposes at once:

- a GitBook-driven, human-navigable documentation space alongside the rest of the Autonomi docs
- structured Markdown that remains useful for AI agents and LLM retrieval workflows
- AI-agent-friendly, parseable content designed for `llms.txt`-style consumption and GEO-aware discovery
- a verification layer that ties published claims back to specific upstream commits
- a future automation target that can detect upstream drift and keep the docs aligned

## What This Repo Covers

This repo currently focuses on the Autonomi developer documentation experience.

It documents four primary interfaces:

1. Build with the SDKs
2. Use MCP with AI tools
3. Use the `ant` CLI
4. Build directly in Rust

The documentation is written primarily for human developers encountering Autonomi for the first time, while also remaining parseable and useful for AI agents.

## What This Repo Is Not

- It is not the only source of truth for technical behavior. The upstream repos are.
- It is not a copy of every upstream README.
- It is not intended to describe unmerged branches or future-state product plans.

## Source Of Truth Model

The repo uses two source-of-truth modes:

1. `current-merged-truth`
2. `target-manifest`

### `current-merged-truth`

This is the default mode.

For each page, it means the latest merged commit on the default branch of each in-scope source repo at the time of audit.

### `target-manifest`

This is an explicit override for launch hardening or release verification.

When a `target-manifest.yml` exists and a pass explicitly uses it, docs are verified against the pinned refs in that manifest instead of moving default branches.

## Required Workflow

Every documentation task follows this workflow:

1. Source audit
2. Draft
3. Verify

That workflow is defined in:

- `CLAUDE.md`
- `planning/verification-workflow.md`

### Source audit

Determine:

- page type
- relevant source repos
- exact refs and SHAs
- canonical source artifacts

### Draft

Write only from audited evidence.

### Verify

Check every technical claim, endpoint, command, type, field, and example against the audited sources, then record real verification metadata in the page.

## Verification Metadata

Verified pages include HTML comment blocks like this:

```html
<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: 6c4df9b745f3adcb022ac82b6bbc485727297e3e
  verified_date: 2026-04-02
  verification_mode: current-merged-truth
-->
```

Rules:

- `source_commit` must be a real commit SHA
- multi-repo pages must use multiple verification blocks
- historical notes and prior synthesis docs are not authoritative

## Repository Structure

```text
repository-root/
├── .gitbook.yaml                # GitBook config; published content lives in docs/
├── CLAUDE.md                    # Repo rules for AI-assisted docs work
├── repo-registry.yml            # In-scope source repos and source-of-truth config
├── component-registry.yml       # Maps product components to docs pages
├── docs/                        # Published documentation content
├── planning/                    # Workflow docs, plans, and working process notes
└── reference/                   # Supporting reference material and research notes
```

Important:

- Only `docs/` is intended to be published via GitBook
- `planning/`, `reference/`, and `CLAUDE.md` are working materials, not published docs content
- GitBook should sync the repo root and use `.gitbook.yaml` to scope published content to `docs/`

## Review Model

This repo is intended to be reviewed in two places.

### Review in GitHub

Use GitHub review for:

- technical accuracy
- source alignment
- wording and structure
- verification metadata and SHAs
- repo/process changes

### Review in GitBook

Use GitBook review for:

- navigation
- page flow
- heading readability
- tabs, tables, and code block rendering
- overall user experience

## What Counts As Publishable

A page is publishable when:

1. it has been source-audited
2. it has been verified against real upstream SHAs
3. any required runnable workflow checks have passed
4. it renders cleanly in GitBook
5. it is ready for an external developer audience

## Automation Direction

This repo is designed to become progressively more automated.

The intended model is:

1. detect upstream merged changes
2. map changed components to affected docs pages
3. re-run source audit, draft, and verification
4. update verification SHAs only after re-verification succeeds

The files that support that model are:

- `repo-registry.yml`
- `component-registry.yml`
- `planning/verification-workflow.md`

At the moment, the repo is still in an agent-assisted hardening phase. Automation is being introduced deliberately rather than all at once.

## Publishing Model

Current working model:

- GitHub repo for content review and version control
- GitBook sync for unpublished preview and rendering review

Planned direction:

- finalize the verified baseline
- review with developers from GitHub and GitBook preview
- introduce upstream-triggered automation in this repo

## Working In This Repo

If you are editing or reviewing docs here:

1. read `CLAUDE.md`
2. use `planning/verification-workflow.md`
3. treat upstream merged code as the authority
4. keep internal provenance language out of rendered docs prose
5. favor developer-facing paths and tasks over repo-shaped framing

Key writing expectations include:

- explain what a tool is before telling the reader to install or run it
- prefer user outcomes and choices in titles
- avoid repo names as primary page titles unless the repo itself is the topic
- keep headings readable in GitBook
- use cURL, Python, Node.js / TypeScript, and Rust as the default featured SDK examples when supported and verified

## In-Scope Sources

See `repo-registry.yml` for the authoritative in-scope repo list.

See `component-registry.yml` for which components and repos inform each page.
