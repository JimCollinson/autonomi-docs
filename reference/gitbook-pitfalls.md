## Common Pitfalls & Mitigations

| Pitfall | Why it happens | Mitigation |
| --- | --- | --- |
| Editing README/SUMMARY in GitBook UI while Git Sync is enabled | GitBook will regenerate those files in the repo, potentially overwriting upstream edits or creating duplicates.[^1][^2] | Lock down README/SUMMARY editing to GitHub PRs only; educate writers that UI edits in those files are off-limits. |
| Losing advanced block formatting in Git diffs | Blocks like tabs are serialized into `{% tabs %}` macros; manual edits that remove tags will break rendering.[^3] | Document custom syntax in CONTRIBUTING.md and add lint rules to ensure `{% tab %}` blocks stay balanced. |
| PR previews unavailable | GitBook only generates previews if the docs space is published and not behind authenticated access; forks are disabled by default for security.[^4] | Keep at least a staging site publicly available for previewing; avoid strict auth on preview environments. |
| Assuming `llms.txt`/`llms-full.txt` are optional | GitBook now auto-publishes them; if they leak drafts, crawlers/LLMs will ingest them.[^5] | Treat LLM endpoints as part of release gating—publish only when ready, and verify content via the `.md`/`llms` URLs before launch. |
| Over-reliance on GitBook Agent | The agent excels at focused edits but still requires precise prompts and human review to avoid hallucinations.[^6] | Keep manual reviewers in the loop; script lint/tests in GitHub Actions before merging AI-authored docs. |
| Cross-repo workflow flakiness | `repository_dispatch` requires PAT/App credentials with `contents:write`; missing permissions silently drop events.[^7][^8] | Centralize dispatching in an automation repo with a dedicated GitHub App; log 204 responses and queue retries. |
| Secrets missing in forked PR workflows | GitHub withholds secrets (other than a read-only `GITHUB_TOKEN`) for forked PRs.[^9] | Run drift/validation jobs on base repos only, or require contributors to open PRs from branches within the org. |
| Copying monorepo patterns without branching discipline | Projects like Kubernetes rely on strict branch naming for releases/localization.[^10] | Adopt explicit release branches (`dev-<version>`) and localization conventions from day one to avoid backport chaos. |

[^1]: GitBook, "Content configuration." https://gitbook.com/docs/getting-started/git-sync/content-configuration
[^2]: GitBook, "Troubleshooting Git Sync." https://gitbook.com/docs/getting-started/git-sync/troubleshooting
[^3]: GitBook, "Tabs block." https://gitbook.com/docs/creating-content/blocks/tabs
[^4]: GitBook, "GitHub pull request preview." https://gitbook.com/docs/getting-started/git-sync/github-pull-request-preview
[^5]: GitBook, "LLM-ready docs." https://gitbook.com/docs/publishing-documentation/llm-ready-docs
[^6]: GitBook, "Writing with GitBook Agent." https://gitbook.com/docs/gitbook-agent/write-and-edit-with-ai
[^7]: GitHub Docs, "Create a repository dispatch event." https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event
[^8]: GitHub Docs, "repository_dispatch webhook." https://docs.github.com/en/webhooks-and-events/webhooks/webhook-events-and-payloads#repository_dispatch
[^9]: GitHub Docs, "Events that trigger workflows (fork limitations)." https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows
[^10]: Kubernetes.io, "Contributing new content." https://kubernetes.io/docs/contribute/new-content/overview/
