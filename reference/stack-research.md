## Recommended Stack Components

### Documentation authoring & hosting

- **GitBook Spaces with Git Sync** — Use GitHub or GitLab repositories as the canonical source, configure `.gitbook.yaml` for each space to point at the docs root, and keep `README.md`/`SUMMARY.md` under version control to drive the nav structure.[^1]
- **GitBook Content Blocks** — Leverage tabs, hints, cards, etc., but remember that Git Sync serializes them into Liquid-style tags that the repository must preserve when reviewing Markdown diffs.[^2]
- **skill.md metadata** — Provide per-repo context for AI tooling when editing locally via Git Sync, aligning with GitBook's recommendation to guide assistants.[^1]

### AI assistance & LLM readiness

- **GitBook Agent** — Scope prompts per page or block, tag @gitbook in comments for targeted edits, and keep the "Improve" menu for standardized actions (summaries, SEO cleanup). Treat outputs as drafts requiring review.[^3]
- **LLM exports** — Publish `.md` endpoints, auto-generated `llms.txt`, `llms-full.txt`, and MCP endpoints provided by GitBook to feed Retrieval-Augmented Generation workflows without custom crawlers.[^4]

### Automation & release tooling

- **GitHub Actions reusable workflows** — Model shared validation and drift checks as reusable workflows invoked via `workflow_call`, so secrets/inputs stay typed and auditable across repos.[^5]
- **Repository dispatch (selective use)** — Trigger cross-repo workflows only when necessary, authenticating via PAT or GitHub App tokens with `contents:write` per GitHub's API requirements; model the payload schema up front (`event_type`, `client_payload`, branch).[^
- **Branching/versioning** — Mirror mature doc sets (Kubernetes, Rust book) by keeping release-specific branches (`dev-<version>`), plus language folders (e.g., `/content/en/docs/`).[^

### Governance & review

- **Human-in-the-loop reviews** — Because GitBook Agent is optimized for focused tasks, keep change requests and reviewer ownership in GitHub; use PR previews for GitHub-originated work (note: previews require published docs and do not work behind GitBook's authenticated access).[^

[^1]: GitBook, "Git Sync: Content configuration." https://gitbook.com/docs/getting-started/git-sync/content-configuration
[^2]: GitBook, "Tabs block." https://gitbook.com/docs/creating-content/blocks/tabs
[^3]: GitBook, "Writing with GitBook Agent." https://gitbook.com/docs/gitbook-agent/write-and-edit-with-ai
[^4]: GitBook, "LLM-ready docs." https://gitbook.com/docs/publishing-documentation/llm-ready-docs
[^5]: GitHub Docs, "Reuse workflows." https://docs.github.com/en/actions/using-workflows/reusing-workflows
[^6]: GitHub Docs, "Create a repository dispatch event." https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event
[^7]: GitHub Docs, "repository_dispatch webhook." https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#repository_dispatch
[^8]: Kubernetes.io, "Contributing new content." https://kubernetes.io/docs/contribute/new-content/overview/
[^9]: rust-lang/book README. https://raw.githubusercontent.com/rust-lang/book/main/README.md
[^10]: GitBook, "GitHub pull request preview." https://gitbook.com/docs/getting-started/git-sync/github-pull-request-preview
