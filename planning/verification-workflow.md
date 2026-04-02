# Verification Workflow

This document defines the repeatable workflow for writing, updating, and re-verifying documentation in this repo.

## Purpose

The repo follows a strict source-of-truth model. Pages must describe the active source of truth for the repos they depend on, not the expected future product shape.

Use this workflow for:
- new pages
- rewrites of inaccurate pages
- updates after upstream merges
- launch-hardening passes

## Active mode

The repo has two operating modes.

### `current-merged-truth`

This is the default mode.

Meaning:
- for each in-scope repo, use the latest merged commit on the default branch at the time of the source audit
- ignore unmerged branches, PR branches, and expected future behavior

Use this mode unless a `target-manifest.yml` is explicitly active.

### `target-manifest`

This is the launch-hardening or release-verification mode.

Meaning:
- use the refs pinned in `target-manifest.yml`
- do not follow moving default branches for pages verified in this mode

Use this mode only when the manifest exists and the task explicitly says to use it.

## Required workflow

Every documentation task follows these stages:

1. Source audit
2. Draft
3. Verify

Do not skip or reorder these stages.

## 1. Source audit

Before writing or editing a page:

1. Identify the page type.
2. Identify the source repos for the page.
3. Determine the active mode: `current-merged-truth` or `target-manifest`.
4. Resolve the exact refs and commit SHAs for each source repo.
5. Collect the canonical source artifacts for the page.
6. Extract the facts, commands, types, and examples the page is allowed to describe.

### Source repo selection

Use these repo files to determine scope:
- `repo-registry.yml`
- `component-registry.yml`

Start with the broad product repos:
- `ant-sdk`
- `ant-client`
- `ant-node`

Add foundational repos only when the topic requires them.

### Canonical source artifacts by page type

#### Reference pages

Use the canonical interface artifacts first:
- OpenAPI specs
- gRPC proto files
- CLI `--help` output
- exported request/response models
- package metadata and published install instructions

If the interface is not present in these artifacts on the active source of truth, do not document it as current.

#### Getting Started and How-to pages

Use:
- runnable examples from the active source repos
- actual daemon defaults and current commands
- published install or download paths

These pages must reflect what a developer can do now.

#### Language binding pages

Use:
- package metadata
- exported constructors and models
- upstream README examples
- transport/discovery defaults from the binding source

Do not assume every binding shares the same shape unless the source artifacts show that it does.

#### Concept pages

Use:
- code-backed facts from the active source repos

Concept pages can explain the system, but they still must reflect the active source of truth.

Historical notes, research memos, and prior synthesis documents are not authoritative. They may help you locate likely code paths, but every technical claim must still be grounded in the active source repos.

## 2. Draft

Write only from the audited evidence.

Rules:
- Keep the existing information architecture unless the content itself is wrong for the current source of truth.
- Prefer the smallest correct rewrite.
- Preserve structure that is still accurate.
- Use the page template that matches the page type.
- Use only terminology allowed by `CLAUDE.md`.

If evidence is missing:
- do not infer the missing details
- do not write a future-state page as if it were current
- either defer the page, leave a thin placeholder, or reframe it conceptually

## 3. Verify

After drafting, verify the page against the audited sources.

### Verification checklist

#### Reference pages

Verify that every:
- endpoint
- method
- command
- flag
- type
- field
- example payload

exists in the active source of truth at the recorded commit.

#### Getting Started and How-to pages

Verify that every:
- install instruction
- command
- code example
- default port or URL
- expected response

matches the active source of truth and is runnable in principle.

#### Concept pages

Verify that every technical claim can be traced to:
- code in the active source repos, or
- a confirmed technical decision

### Verification metadata

Only after verification is complete:

1. Add a verification block for each source repo used.
2. Record the repo, ref, exact commit SHA, verified date, and verification mode.
3. Use multiple verification blocks for multi-repo pages.

Never use `source_commit: TBD` on a page presented as verified.

## Page states

Pages move through these states:

1. `source-audited`
2. `drafted`
3. `verified`
4. `publishable`

Meaning:
- `source-audited`: source repos, refs, SHAs, and canonical artifacts identified
- `drafted`: content written from audited evidence
- `verified`: claims checked and verification metadata populated with real SHAs
- `publishable`: verified and ready to push once repo publishing is set up

## Special rules

### Installation and downloads

Pages about installation, binaries, packages, and versions must point to artifacts users can actually download or install now. These pages are not allowed to get ahead of published artifacts.

### Unmerged branches

Unmerged branches are not part of the source of truth in `current-merged-truth` mode. If a feature exists only on a branch, it stays out of the docs until it merges.

### Launch hardening

When a launch-ready state is declared, create `target-manifest.yml` and re-verify the launch-critical pages against the pinned refs. This is a focused override, not the default day-to-day mode.

## Automation

Automation must follow the same workflow:

1. detect upstream merged changes
2. map changed components to affected pages
3. mark those pages stale
4. re-run source audit -> draft -> verify
5. update verification SHAs only after re-verification succeeds

Automation does not change the source-of-truth rules. It applies them.
