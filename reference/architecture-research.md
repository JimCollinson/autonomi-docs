## System Structure

1. **Repository layer**
   - Maintain one GitHub repo per product vertical, each containing `/docs` (or equivalent) plus `.gitbook.yaml`, `README.md`, `SUMMARY.md`, and static assets. The file defines the root and TOC GitBook will ingest, enabling multi-space or monorepo syncing.[^1]
   - Enforce branching similar to Kubernetes (`main` for current English, `dev-<version>` for release branches, language-specific folders) to simplify release gating and localization backports.[^2]

2. **GitBook integration layer**
   - Configure Git Sync per space; point at the repo subfolder via "Project directory" and `.gitbook.yaml root`. Avoid authoring README/summary files in the UI to prevent divergence during sync.[^1][^3]
   - Enable PR previews through the GitBook GitHub App so each docs PR shows a rendered preview; remember previews require the docs site to be published and will not render for private/authenticated-only sites.[^4]
   - Use GitBook Agent for scoped edits by tagging @gitbook inside change requests or the "Improve" menu, but keep final approval in GitHub/GitBook review queues.[^5]

3. **AI/LLM distribution layer**
   - Rely on GitBook's automatic `.md` endpoints, `llms.txt`, `llms-full.txt`, and `/~gitbook/mcp` server for LLM ingestion, eliminating the need for custom site crawlers. Cache-bust or snapshot `llms-full.txt` before launch day to ensure RAG pipelines index the intended content.[^6]

4. **Automation layer**
   - **Reusable validation workflow**: Build a central workflow (e.g., `.github/workflows/docs-validate.yml`) triggered via `workflow_call` that runs Markdown linting, link checking, and optionally diff-checks against GitBook exports. Each repo references it via `jobs.<id>.uses`, passing `with` inputs such as doc root path and optionally inheriting secrets.[^7]
   - **Drift detection**: If cross-repo comparisons are essential (e.g., platform repo vs. shared reference), emit a lightweight `repository_dispatch` from the authoritative repo whenever docs change, with a GUID in `client_payload`. A separate "control" repo listens for `repository_dispatch` with a PAT/GitHub App that has access to both repos, runs deeper comparisons, and files issues/PRs.[^8][^9]
   - **Security controls**: Because secrets don't cross forks and `GITHUB_TOKEN` is read-only there, run drift workflows only on trusted branches or via GitHub Apps installed on all repos. Store PATs/App credentials in organization secrets and scope them to the automation repo.[^10]

5. **Publishing & delivery**
   - Use GitBook's built-in static hosting and custom domains for public docs; keep authenticated spaces separate if PR previews are required (previews can't render when spaces are private/authenticated-only).[^
   - Provide `llms.txt`/`llms-full.txt` URLs to internal AI consumers and third-party assistant integrations.

[^1]: GitBook, "Content configuration." https://gitbook.com/docs/getting-started/git-sync/content-configuration
[^2]: Kubernetes.io, "Contributing new content." https://kubernetes.io/docs/contribute/new-content/overview/
[^3]: GitBook, "Troubleshooting Git Sync." https://gitbook.com/docs/getting-started/git-sync/troubleshooting
[^4]: GitBook, "GitHub pull request preview." https://gitbook.com/docs/getting-started/git-sync/github-pull-request-preview
[^5]: GitBook, "Writing with GitBook Agent." https://gitbook.com/docs/gitbook-agent/write-and-edit-with-ai
[^6]: GitBook, "LLM-ready docs." https://gitbook.com/docs/publishing-documentation/llm-ready-docs
[^7]: GitHub Docs, "Reuse workflows." https://docs.github.com/en/actions/using-workflows/reusing-workflows
[^8]: GitHub Docs, "Create a repository dispatch event." https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event
[^9]: GitHub Docs, "repository_dispatch webhook." https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#repository_dispatch
[^10]: GitHub Docs, "Events that trigger workflows (fork limitations)." https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows
