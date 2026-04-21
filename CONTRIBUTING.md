# Contributing

Thanks for helping improve the Autonomi developer docs.

## Before You Start

- Read `README.md` for the repo scope, structure, and publishing model.
- Read `CLAUDE.md` for terminology, style, and verification rules.
- Use `planning/verification-workflow.md` for the required `source audit -> draft -> verify` workflow.

## Working Model

- Open a pull request for changes to `main`.
- Keep each change focused and as small as possible.
- Treat merged upstream code as the technical source of truth.
- Do not document unmerged branches or future behavior as if it is current.
- Keep provenance and evidence narration out of rendered docs prose.

## Updating Docs

- Identify the page type and relevant source repos before editing.
- Use `current-merged-truth` unless a task explicitly activates `target-manifest`.
- Update verification blocks when you change a verified page.
- Use terminology from `CLAUDE.md` exactly.
- Keep code examples complete, runnable, and explicit about which developer interface they cover.
- Use the four primary interface labels consistently in navigation and overview pages: SDK, MCP, CLI, and Direct Rust.
- Keep Core Concepts tool-neutral and use `How-To Guides` for shared or cross-interface task pages.
- Keep pages interface-pure unless they are explicitly comparison or chooser pages.
- Use tabs for languages or equivalent interfaces within one interface, not for switching between interfaces.
- In user-facing prose, name the specific tool or interface rather than using abstract words like `route` or `path`.
- Inside each interface section in `SUMMARY.md`, use a landing page first and nest child pages beneath it. Add landing pages for How-To Guides or Reference when a section has enough pages to benefit from that extra layer, and omit empty groups.

## Pull Requests

- Explain what changed and why.
- Call out any upstream repo, ref, or commit drift the change resolves.
- Note any verification work or GitBook rendering checks you performed.

## Related Files

- `README.md`
- `CLAUDE.md`
- `planning/verification-workflow.md`
- `repo-registry.yml`
- `component-registry.yml`
