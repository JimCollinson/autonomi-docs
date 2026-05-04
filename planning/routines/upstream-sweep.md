# Upstream sweep routine

## Purpose

Implements the `source audit -> draft -> verify` workflow defined in `planning/verification-workflow.md` on a daily cadence. Every weekday (and weekend) the routine checks every recorded `source_commit` in the docs and the developer skill against the corresponding upstream HEAD, audits any drifted page against the exact pinned SHA the routine intends to stamp, and opens PRs or issues per the topology below.

The routine is the hosted-scheduled equivalent of Tier 1 + Tier 2 from `planning/implementation-plan.md` Section 8. It does not replace the eventual `repository_dispatch`-driven path; it sits alongside as an interim path that works without `notify-docs.yml` being installed in any upstream repo.

## Trigger shape

- Execution venue: Claude Desktop → Routines → New routine → Remote.
- Schedule: daily at 09:00 UTC. Comfortably above the documented one-hour minimum interval for Remote-routine schedules.
- Routine model: Opus 4.7 end-to-end. No subagent layer.
- Prompt: the committed prompt at `planning/routines/upstream-sweep-prompt.md`.
- Body: the prompt invokes `scripts/sweep_poll.py` for deterministic detection, then runs the audit-draft-verify workflow against pinned upstream checkouts and opens PRs/issues per the topology.
- Webhook arm (`repository_dispatch` or per-event collation) is explicitly deferred to v2 of the trigger shape.

## Routine flow

1. Bootstrap the rolling status thread (label + issue, see `## Rolling status issue`).
2. Run the open-PR collision check. If a prior `claude/sweep-*` or `claude/prose-*` PR is still open, post a collision notice to the rolling issue and exit without opening anything.
3. Run `scripts/sweep_poll.py`. If the JSON status is `error`, post the diagnostics to the rolling issue and exit.
4. If `records` is empty or every record has `drifted: false`, post a no-drift summary to the rolling issue and exit.
5. For each drifted record, group by `(repo, head_sha)` and check out the pinned SHA in a fresh tmp dir (see `## Source checkout for audit`). Audit each affected docs page against the pinned tree per `planning/verification-workflow.md`. Classify per-page outcome into one of three batches:
   - **sweep batch** — audit confirms metadata-only refresh suffices.
   - **prose batch** — audit identifies prose impact; the page needs human-reviewed edits alongside its SHA stamp refresh.
   - **issue batch** — audit cannot make a confident judgment (ambiguous evidence, removed surface, deleted file). Page does not enter any PR.
6. Open at most two PRs (one sweep, one prose draft) plus zero or more `manual review needed` issues per the topology in `## PR body format`. Post a run summary with PR/issue links to the rolling issue.

## Branch convention

All routine-opened branches use the `claude/` namespace.

- Metadata-only stamp refreshes: `claude/sweep-<YYYY-MM-DD>`.
- Prose-impact PRs: `claude/prose-<YYYY-MM-DD>-<slug>`. Opened as **draft** PRs so the human reviewer promotes them to ready-for-review only after the prose has been read.

## Rolling status issue

The routine maintains a single open GitHub issue labelled `upstream-sweep-status` as the chronological log of its behavior.

Bootstrap, run by every execution before any other GitHub work:

1. Ensure the `upstream-sweep-status` label exists. Idempotent: list the label, create it if missing (`gh label list` → `gh label create` with `-f` for re-runs). `gh issue create --label X` fails when the label is missing, so this step must precede any issue creation.
2. Ensure an open issue with that label exists. Idempotent: list open issues with the label sorted by issue number ascending.
   - Zero results: create the issue.
   - Exactly one result: use it.
   - More than one result: pick the lowest-numbered issue deterministically and post a one-time warning to that thread asking a human to close the duplicates. The run continues against the chosen issue rather than failing the cadence.

Every status post (collision skip, error diagnostics, no-drift summaries, run summaries with PR/issue links, target-manifest skip notices) targets the chosen issue.

## Open-PR collision handling

Before opening any new PR, list open PRs and filter `headRefName` by prefix client-side:

```bash
gh pr list --state open --json number,headRefName \
  --jq '.[] | select(.headRefName | startswith("claude/sweep-") or startswith("claude/prose-"))'
```

GitHub's `--search` syntax does not reliably match branch prefixes, so the JSON list with a client-side prefix filter is the trustworthy form.

If any results come back regardless of date, the routine skips the run, posts a "skipping; prior PR(s) #X #Y still open" comment to the rolling status issue, and exits. Drift is re-detected on the next run after the prior PR(s) merge or close. This forces a clean serial cadence and prevents PR accumulation.

## Source checkout for audit

For each unique `(repo, head_sha)` across drifted records, the routine creates a fresh tmp dir and runs:

```bash
git init
git remote add origin <url>
git fetch --depth 1 origin <head_sha>
git checkout --detach <head_sha>
```

Fetching the exact SHA matches the pinned-audit principle: the SHA being stamped is the SHA being audited, independent of any subsequent ref movement.

If the SHA fetch fails (GitHub does not allow reachable-SHA fetches for that repo, the SHA has been garbage-collected, etc.), the routine fails closed: post error diagnostics to the rolling status issue and exit without opening any PR. Audit never runs against a moving `main`.

`git clone --depth N` is rejected because an arbitrary `N` may not contain the target SHA. `git fetch <ref>` is rejected because the ref may have moved between the scanner run and the audit run.

The routine cleans up tmp dirs after each run.

## Credentials and access

The routine needs:

- read access to all in-scope upstream repos for GitHub API HEAD lookups and the shallow clones,
- write access to `withautonomi/autonomi-developer-docs` for branch push, PR creation, and comment/issue creation.

Recommended: a dedicated GitHub App installation token (refreshed per run by Claude Desktop) with `contents: write`, `pull-requests: write`, `issues: write` on the docs repo and `contents: read` on the in-scope upstream repos.

Acceptable v1 alternative: a fine-grained personal access token with the same scopes, stored as a Claude Desktop routine secret.

The token is exposed as `GITHUB_TOKEN` in the routine environment. The script and any `gh` calls read from there. The repo file does not contain the secret value, only the policy.

## PR body format

Both sweep and prose PRs open with the same three-part body:

1. Per-page audit note. One or two sentences per affected page citing the pinned `head_sha` the audit consulted.
2. Summary table:

   | Page | Repo | Recorded SHA | HEAD SHA |
   | --- | --- | --- | --- |
   | docs/sdk/install.md | ant-sdk | `abc1234` | `def5678` |

3. Link to the run summary on the rolling status issue.

Sweep PRs add: "metadata-only envelope; the structural guard runs and must be green."

Prose PRs add a list of pages with prose changes versus pages whose only change in this PR is a metadata bump, so the reviewer knows where to focus.

## Metadata-only allowlist

Verbatim envelope for `claude/sweep-` PRs:

- verification-block lines (`source_commit:`, `verified_date:`) in `docs/**/*.md`,
- the `verified_commits` map in `skills/start/version.json`,
- the `verified_commits` map and the `verified_date:` line in the YAML frontmatter of `skills/start/SKILL.md`,
- one new `planning/sweeps/<YYYY-MM-DD>.md`.

Forbidden on `claude/sweep-` PRs:

- `version` and `published_date` keys in `version.json`,
- the YAML-frontmatter `version:` line in `SKILL.md`,
- any change to `skills/start/CHANGELOG.md`,
- any rendered prose change in `docs/`.

`claude/prose-` PRs allow rendered prose changes in `docs/`. The `version` / `published_date` / CHANGELOG / frontmatter-`version` forbidding still applies because version bumps are not the routine's job: a release happens on a separate, manual concept-edit PR.

## Audit gating

SHAs are bumped only after the per-page audit step succeeds against the pinned upstream checkout. If audit fails for a page (ambiguous evidence, removed surface, deleted file, etc.), the page does not enter any PR — it is surfaced as a `manual review needed` issue. The scanner's drift report is a candidate list, not a directive.

## Fail-closed semantics

The scanner exits non-zero on any of:

- GitHub API auth failure or 4xx/5xx on a HEAD or repo metadata lookup,
- network timeout,
- malformed `<!-- verification:` block (missing `source_repo`, `source_ref`, `source_commit`, or `verification_mode`),
- unparseable `repo-registry.yml`,
- unparseable `version.json` or `SKILL.md` frontmatter,
- unknown `source_repo` not in the registry,
- `verification_mode` set to a value other than `current-merged-truth` or `target-manifest`.

The routine treats any non-zero scanner exit as an error condition, posts the JSON diagnostics to the rolling status issue, and exits without opening any PR.

`target-manifest` blocks are deliberately skipped by the scanner and listed in a separate `target_manifest_skipped` array in the JSON output. The routine surfaces those entries in the run summary as "pinned by target-manifest, not bumped" so a human can confirm those pins remain intentional. v1 must never bump a `target-manifest` block against a moving HEAD; doing so would silently overwrite a launch-hardening pin.

## No-drift status report

Comment to the rolling status issue. Format: a short markdown table with one row per record (location / recorded SHA / HEAD SHA / drifted?), grouped by repo for readability.

## Failure modes

- GitHub API rate-limit during the daily poll. Handled by the scanner's fail-closed semantics; the routine posts the error and waits for the next run.
- Deleted or renamed source repo. Same handling.
- Force-push that invalidates a recorded SHA. Caught by the SHA-reachability required check on the resulting PR.
- Routine missing the 09:00 UTC slot. Recovery: next-day run picks up the drift; latency at most 24h.
- Claude Desktop routine credential or token expiry. Routine fails closed; user refreshes the secret.
- Daily routine-start cap exhausted on Max plan. Same recovery as missed slot.
- Collision skip when a prior PR is left open for many days. Recovery: user merges or closes the prior PR; the next-day run resumes.

## Alignment with implementation-plan.md Section 8

The routine is a hosted-scheduled, polling-based equivalent of Tier 1 + Tier 2 of Section 8.

Differences from the per-event arm:

- pull-shaped from a scheduler instead of `repository_dispatch`-driven,
- narrower envelope (metadata-only sweep PR plus optional prose draft PR),
- no per-event collation in v1.

Forward compatibility: when `notify-docs.yml` rolls out in upstream repos, the same routine can grow a webhook-receiver arm without invalidating the daily-poll v1.

## Required-check setup (one-time, after merge)

1. Add `sweep-guard` and `sweep-sha-reachability` (the exact workflow `name:` strings) as required checks on `main` in repo settings → Branch protection.
2. Confirm the routine's bot identity has push access. If branch protection requires reviewers, ensure the bot is granted bypass or has CODEOWNERS coverage on `planning/sweeps/*` and the metadata-only paths, or accept that the user reviews each sweep PR by hand.
3. Provision the `GITHUB_TOKEN` secret in the Claude Desktop routine config per the credentials section above.

## Out of scope

- Claude Desktop Remote routine config (model = Opus 4.7, schedule, secret value of `GITHUB_TOKEN`) — lives in Claude Desktop, not in this repo. The behaviour (the prompt) is committed at `planning/routines/upstream-sweep-prompt.md`.
- `notify-docs.yml` installation in any upstream repo — tracked under `planning/implementation-plan.md` Section 8.2.
- Per-event sweep PRs — deferred to v2 of the trigger shape.
- Auto-merge — deferred to v1.5. The label-driven `sweep-auto-merge` workflow ships once both required checks have run cleanly for several weeks.
- Terminology lint, Greptile reviewer setup, and broader v2 verification-staleness checks beyond the sweep envelope.
