## Key Findings

- GitBook's Git Sync treats GitHub as the canonical source: you must keep `.gitbook.yaml`, `README.md`, and `SUMMARY.md` in the repository, define the docs root/structure there, and avoid editing README files in the GitBook UI to prevent duplicate files or sync conflicts.[^1][^2]
- Tabbed and other advanced content blocks exist in the GitBook editor, but when syncing via Markdown they are serialized into Liquid-style tags (for example `{% tabs %}`), so upstream repositories must preserve that syntax for parity.[^3]
- GitBook now auto-publishes `.md` endpoints, `llms.txt`, `llms-full.txt`, and an MCP server for every public space, confirming that LLM-focused exports are a first-class, current feature rather than an undocumented hack.[^4]
- GitBook Agent accelerates authoring and reviews, but it works best with small, specific prompts; teams still need to plan review workflows and guardrails for AI-generated content.[^5]
- GitHub cross-repo orchestration typically relies on the `repository_dispatch` API/event, which demands a token or GitHub App with `contents:write` access; without that, remote workflows will never start.[^6][^7]
- Workflows triggered from forks or external repos don't receive shared secrets (only a read-only `GITHUB_TOKEN`), so any drift-detection workflow that needs repo-to-repo comparisons must run from a trusted repo with explicit PAT/GitHub App credentials.[^8]
- Reusable workflows invoked via `workflow_call` are GitHub's supported alternative to bespoke dispatch networks and keep secret passing, inputs, and outputs well-defined across repos.[^9]
- Mature multi-repo or multi-source doc stacks (Rust book, Kubernetes website) centralize shared tooling in a single repo, enforce strict branching/versioning rules, and rely on static site generators (mdBook, Hugo) with language/version folders, suggesting a similar structure for this effort.[^10][^11]

## Implications for the proposed docs system

1. **GitHub must stay the source of truth.** Enable Git Sync per space and keep repo layouts consistent with GitBook's expectations to avoid accidental UI edits overwriting Markdown.
2. **AI outputs need review.** GitBook Agent can draft content quickly but still requires scoped prompts, human review, and possibly linting/CI to prevent hallucinations from landing in Git.
3. **Cross-repo drift detection requires privileged automation.** Choose between PATs or GitHub Apps with dispatch events, or refactor into reusable workflows so secrets don't cross trust boundaries.
4. **Launch scope should prioritize the baseline Git Sync + `llms.txt` delivery.** Advanced workflow automation (multi-repo diffing, AI auto-writers) can iterate after the site is reliably syncing.

[^1]: GitBook, "Content configuration." https://gitbook.com/docs/getting-started/git-sync/content-configuration
[^2]: GitBook, "Troubleshooting Git Sync." https://gitbook.com/docs/getting-started/git-sync/troubleshooting
[^3]: GitBook, "Tabs block." https://gitbook.com/docs/creating-content/blocks/tabs
[^4]: GitBook, "LLM-ready docs." https://gitbook.com/docs/publishing-documentation/llm-ready-docs
[^5]: GitBook, "Writing with GitBook Agent." https://gitbook.com/docs/gitbook-agent/write-and-edit-with-ai
[^6]: GitHub Docs, "Create a repository dispatch event." https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event
[^7]: GitHub Docs, "Webhook events: repository_dispatch." https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#repository_dispatch
[^8]: GitHub Docs, "Events that trigger workflows (fork limitations)." https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows
[^9]: GitHub Docs, "Reuse workflows." https://docs.github.com/en/actions/using-workflows/reusing-workflows
[^10]: Kubernetes.io, "Contributing new content." https://kubernetes.io/docs/contribute/new-content/overview/
[^11]: rust-lang/book README. https://raw.githubusercontent.com/rust-lang/book/main/README.md
