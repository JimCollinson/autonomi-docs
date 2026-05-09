# Upstream sweep routine

## Purpose

Implements the `source audit -> draft -> verify` workflow defined in `planning/verification-workflow.md` on a daily cadence. Every weekday (and weekend) the routine checks every recorded `source_commit` in the docs and the developer skill against the corresponding upstream HEAD, audits any drifted page against the exact pinned SHAs the routine intends to stamp, and opens PRs or issues per the topology below.

The routine is the hosted-scheduled equivalent of Tier 1 + Tier 2 from `planning/implementation-plan.md` Section 8. It does not replace the eventual `repository_dispatch`-driven path; it sits alongside as an interim path that works without `notify-docs.yml` being installed in any upstream repo.

## Trigger shape

- Execution venue: Claude Desktop → Routines → New routine → Remote.
- Schedule: daily at 09:00 UTC. Comfortably above the documented one-hour minimum interval for Remote-routine schedules.
- Routine model: **Opus 4.7 or higher** end-to-end. The audit/write/verify loop in `## Opus audit/write/verify loop` requires the model to inspect upstream diffs and source at pinned SHAs, compare against docs and `SKILL.md`, write actual prose into draft PRs, and run practical verification. No subagent layer.
- Prompt: the committed prompt at `planning/routines/upstream-sweep-prompt.md`.
- Body: the prompt invokes `scripts/sweep_poll.py` for deterministic detection, then runs the audit/write/verify loop against pinned upstream checkouts and opens PRs/issues per the topology.
- Webhook arm (`repository_dispatch` or per-event collation) is explicitly deferred to v2 of the trigger shape.

## Routine flow

1. Bootstrap the rolling status thread (label + issue, see `## Rolling status issue`).
2. Run the open-PR collision check. If a prior `claude/sweep-*` or `claude/prose-*` PR is still open, post a collision notice to the rolling issue and exit without opening anything.
3. Run `scripts/sweep_poll.py`. If the JSON status is `error`, post the diagnostics to the rolling issue and exit.
4. If `records` is empty or every record has `drifted: false`, post a no-drift summary to the rolling issue and exit.
5. For each drifted record, run the `## Opus audit/write/verify loop` (fetch both SHAs, compute the upstream diff, inspect source artifacts, compare against docs and skill, classify the record, apply the page batching rule, write prose where required, run the deferred-record self-check, run practical verification).
6. Open at most two PRs (one sweep, one prose draft) plus zero or more `upstream-sweep-manual-review`-labelled issues per the topology in `## Page batching rule`, `## Manual-review issue format`, `## Manual-review issue de-duplication`, and `## PR body format`. Manual-review issues are opened **before** PRs so PR bodies can reference issue numbers; a `Tracked in <PR URL>.` comment is posted on each issue once the corresponding PR exists. Post a run summary with PR/issue links to the rolling issue.

## Branch convention

All routine-opened branches use the `claude/` namespace.

- Metadata-only stamp refreshes: `claude/sweep-<YYYY-MM-DD>` or `claude/sweep-<YYYY-MM-DD>-<slug>` (the slug is optional for production runs and required for synthetic test PRs that exercise individual envelope rules).
- Prose-impact PRs: `claude/prose-<YYYY-MM-DD>-<slug>`. Opened as **draft** PRs so the human reviewer promotes them to ready-for-review only after the prose has been read.

## Rolling status issue

The routine maintains a single open GitHub issue labelled `upstream-sweep-status` as the chronological log of its behavior.

Bootstrap, run by every execution before any other GitHub work, in POSIX shell only (no `mapfile`, no Bash arrays, no `gh issue create --json/--jq`). Capture-then-decide is the key invariant: any `gh` failure (auth, network, API) must abort the bootstrap immediately rather than be silently coerced into "label missing" or "no open issue". See `planning/routines/upstream-sweep-prompt.md` Step 0 for the exact script.

1. Ensure the `upstream-sweep-status` and `upstream-sweep-manual-review` labels both exist. Idempotent: list labels with `--limit 1000`, create either label if missing. Both labels are bootstrapped here because step 5 opens manual-review issues with `--label upstream-sweep-manual-review`, and `gh issue create --label X` fails when the label is missing, so this step must precede any issue creation.
2. Ensure an open issue with that label exists. Idempotent: list open issues with the label sorted by issue number ascending.
   - Zero results: create the issue. `gh issue create` has no `--json/--jq` flags, so parse the URL it writes to stdout and take the trailing path component as the issue number.
   - Exactly one result: use it.
   - More than one result: pick the lowest-numbered issue deterministically and post a one-time warning to that thread asking a human to close the duplicates. The run continues against the chosen issue rather than failing the cadence.

Every status post (collision skip, error diagnostics, no-drift summaries, run summaries with PR/issue links, target-manifest skip notices) targets the chosen issue.

## Open-PR collision handling

Before opening any new PR, list open PRs and filter `headRefName` by prefix client-side:

```bash
gh pr list --state open --limit 1000 --json number,headRefName \
  --jq '.[] | select(.headRefName | startswith("claude/sweep-") or startswith("claude/prose-"))'
```

`--limit 1000` defeats `gh`'s default 30-row cap so a busy repo cannot hide a still-open prior sweep/prose PR behind pagination — without it the routine would see "no results" and open a colliding PR. GitHub's `--search` syntax does not reliably match branch prefixes, so the JSON list with a client-side prefix filter is the trustworthy form.

If any results come back regardless of date, the routine skips the run, posts a "skipping; prior PR(s) #X #Y still open" comment to the rolling status issue, and exits. Drift is re-detected on the next run after the prior PR(s) merge or close. This forces a clean serial cadence and prevents PR accumulation.

## Audit-diff fetch rule

For each drifted record, the routine must inspect the diff between `recorded_sha` and `head_sha` against the upstream tree at `head_sha`. **Both SHAs are required.**

Default path: fetch both exact SHAs into a fresh tmp dir.

```bash
git init -q
git remote add origin <url>
git fetch --depth 1 origin <recorded_sha>
git fetch --depth 1 origin <head_sha>
git checkout --detach <head_sha>
```

Then `git log <recorded_sha>..<head_sha>` and `git diff <recorded_sha>..<head_sha>` work locally.

Fallback path: if either `git fetch` fails (reachable-SHA fetches disabled by the repo, SHA garbage-collected, network failure), use the GitHub compare API:

```bash
gh api "repos/<owner>/<repo>/compare/<recorded_sha>...<head_sha>"
```

Read `commits[]`, `files[]`, and the `status` field from the response.

Per-record fail-closed: if **both** the local fetch and the compare API fail for a record, open a `manual review needed` issue for that page and skip the page from both PRs. Continue with the rest of the run.

**Never compare against a moving branch name** (`main`, `master`, etc.). The audit must reference the exact pinned SHAs the routine plans to stamp. `git clone --depth N` is rejected because an arbitrary `N` may not contain the target SHA. `git fetch <ref>` is rejected because the ref may have moved between the scanner run and the audit run.

The routine cleans up tmp dirs after each run.

## Page batching rule

After every record on every drifted page is classified by the audit loop, apply the five-case rule per page:

1. **No ambiguous + any prose** → prose PR. All audited non-ambiguous records on that page (prose-impacting **and** metadata-only) are stamped in the same PR. The page never appears on the sweep PR.
2. **No ambiguous + all metadata-only** → sweep PR.
3. **Ambiguous + no prose** → manual-review issue, no PR for that page. Metadata-only records on the same page are deferred alongside the ambiguity rather than spun off into a sweep PR.
4. **Ambiguous overlapping prose, or unproven independence** → manual-review issue, no PR for that page. Two records overlap when they share any of: claim, page section, code sample, command, endpoint, source artifact, or `<!-- verification: -->` block.
5. **Ambiguous + prose with proven independence** → prose PR for the prose-affected records and any metadata-only records on the same page that are also independent of every deferred ambiguity (same overlap dimensions). Ambiguous records and any metadata-only records that share an overlap dimension with a deferred ambiguity stay unstamped: every byte inside the deferred record's `<!-- verification: ... -->` block (including `source_repo:`, `source_ref:`, `source_commit:`, `verified_date:`, `verification_mode:`, comments, and any other field) stays byte-identical to base. One manual-review issue per deferred record tracks the unresolved evidence.

The two PRs never touch the same page. A prose PR may touch a page with deferred ambiguous records but must not edit any byte inside those records' verification blocks. The deferred-record self-check at PR-open time confirms the entire block is byte-identical to base; the routine fails closed on mismatch and does not open the prose PR.

## Manual-review issue format

Every manual-review issue carries the `upstream-sweep-manual-review` label, distinct from `upstream-sweep-status`.

- Title for cases 3 and 4: `manual review needed for <page>`.
- Title for case 5 (deferred record from a prose PR with proven independent ambiguity): `manual review needed for deferred record in <page>`.
- Body includes:
  - exact record location (`file:line` and the verification block content),
  - upstream SHA range (`recorded_sha..head_sha`),
  - the ambiguity reason,
  - the independence rationale (case 5 only),
  - a deterministic `Fingerprint:` line on its own line, surrounded by blank lines, of the form:
    - docs records: `Fingerprint: <repo_path>:<line>|<source_repo>|<recorded_sha>..<head_sha>`,
    - skill `version.json` records: `Fingerprint: skill_version_json|<repo_key>|<recorded_sha>..<head_sha>`,
    - skill `SKILL.md` records: `Fingerprint: skill_md|<repo_key>|<recorded_sha>..<head_sha>`.

The fingerprint includes the SHA range so a record whose `head_sha` advanced since the previous run is treated as a new event with a new issue, while a record that has not moved reuses the existing issue.

## Manual-review issue de-duplication

Deferred records are not stamped, so the next run will rediscover them and would otherwise re-open a duplicate issue every day. Before creating a new manual-review issue, the routine lists open manual-review issues and matches the fingerprint client-side as an exact-line match:

```bash
gh issue list --state open --label upstream-sweep-manual-review \
  --limit 1000 --json number,title,body
```

`gh issue search` is not used: GitHub issue search tokenization does not reliably match a pipe-heavy fingerprint embedded in the body. The match is performed by walking each candidate issue's `body` field and looking for a line that, after stripping leading and trailing whitespace, equals the fingerprint string verbatim — not a substring match.

On a fingerprint match, the routine reuses the existing issue: it skips `gh issue create`, captures the existing issue's number for the prose PR body, and posts a `Tracked in <PR URL>. (Run date <today>.)` comment on the issue once the PR exists. The original issue body is not edited, so reused issues accumulate a chronological trail of every run that re-encountered them. With no fingerprint match, a new issue is created with the fingerprint embedded in the body.

## Sweep PR envelope (claude/sweep-*)

`claude/sweep-*` PRs are metadata-only.

Allowed:

- verification-block lines (`source_commit:`, `verified_date:`) in `docs/**/*.md`,
- the `verified_commits` map in `skills/start/version.json` (key set unchanged),
- the `verified_commits` map and the `verified_date:` line in `skills/start/SKILL.md`'s YAML frontmatter (key set unchanged),
- one new `planning/sweeps/<YYYY-MM-DD>.md` whose date suffix matches the head-branch date suffix.

Forbidden:

- any change to docs prose (`docs/**/*.md` outside an `<!-- verification: -->` block),
- any change to `skills/start/SKILL.md` body (anything outside the YAML frontmatter),
- any change to the `version:` line in `SKILL.md` frontmatter,
- any change to `version` or `published_date` in `version.json`,
- any change to `skills/start/CHANGELOG.md`,
- any change to `scripts/**`, `.github/**`, `repo-registry.yml`, `component-registry.yml`,
- any add or remove of a key in the `verified_commits` map of `version.json` or `SKILL.md` frontmatter (key sets locked; values may refresh).

`sweep-guard` enforces this envelope. It runs on `claude/sweep-*` only and green-skips on every other branch.

## Prose PR envelope (claude/prose-*)

`claude/prose-*` PRs allow rendered prose changes plus the linked skill patch release when the audit found skill impact.

Allowed:

- `docs/**/*.md` — any change.
- `skills/start/SKILL.md` — frontmatter and/or body may change. If body changes, the linked-release rule below applies in full.
- `skills/start/version.json` — `verified_commits` value updates always (key set unchanged); `version` and `published_date` only as part of a linked release.
- `skills/start/CHANGELOG.md` — only as part of a linked release.
- `planning/sweeps/<branch-date>.md` — optional add; date suffix matches `claude/prose-<YYYY-MM-DD>-<slug>`.

Forbidden:

- any change to `scripts/**`, `.github/**`, `repo-registry.yml`, `component-registry.yml` (byte-identical to base),
- any add or remove of a key in the `verified_commits` map of `version.json` or `SKILL.md` frontmatter,
- any change to `version`, `published_date`, frontmatter `version:`, or `CHANGELOG.md` **when the `SKILL.md` body is byte-identical to base** (release metadata may only move with a body change),
- any of the linked-release fields missing **when the `SKILL.md` body has changed**.

Linked-release rule (both directions):

If `skills/start/SKILL.md` body bytes differ between base and head, the same PR must include all of:

- `skills/start/version.json: version` bumped to a new patch version (`MAJOR.MINOR.(PATCH+1)`),
- `skills/start/version.json: published_date` updated,
- `skills/start/SKILL.md` frontmatter `version:` matching the new `version.json: version`,
- `skills/start/SKILL.md` frontmatter `verified_date:` updated,
- `skills/start/CHANGELOG.md` adding one new entry whose header matches the new `version`.

If the `SKILL.md` body is byte-identical between base and head, **none** of `version`, `published_date`, frontmatter `version:`, or `CHANGELOG.md` may change.

`prose-guard` enforces this envelope. It runs on `claude/prose-*` only and green-skips on every other branch.

## Opus audit/write/verify loop

Required model: **Opus 4.7 or higher**. The deterministic scanner is only the drift detector; audit, prose-writing, and verification are first-class duties of the routine.

For each drifted record:

1. **Fetch both SHAs** per `## Audit-diff fetch rule`. If both fetch and compare API fail, fail closed for the page → manual-review issue.
2. **Compute the upstream diff**: `git log --oneline <recorded>..<head>`, `git diff --stat <recorded>..<head>`, targeted `git diff <recorded>..<head> -- <path>`. Or read the compare API response when running via fallback.
3. **Inspect upstream source artifacts** at `head_sha` (OpenAPI specs, `.proto` files, CLI source and `--help` output, public Rust modules, README/docs). Use `repo-registry.yml`'s `topics:` and `component-registry.yml`'s component map to focus on artifacts the affected page actually depends on.
4. **Compare against the affected docs pages** and `skills/start/SKILL.md`. Identify any rendered claim, code sample, command, endpoint, type, field, or live-reference URL that no longer matches the pinned source.
5. **Classify the record** as `metadata-only`, `prose`, or `ambiguous` (see prompt step 4.5 for criteria).
6. **Apply the page batching rule** once every record is classified.
7. **Write prose changes directly into the draft `claude/prose-*` PR** when the page is in the prose batch. Apply `CLAUDE.md`'s voice, terminology lockfile, page templates, and refusal rules. The PR diff must contain the prose edit, not merely a suggestion in the PR body.
8. **Skill-aware prose**: if the audit finds skill impact, include both the docs change and the `SKILL.md` change in the same prose PR. If `SKILL.md` body changes, the same PR must include the linked patch release set per `## Prose PR envelope`.
9. **Deferred-record self-check** (case 5 only — prose PR opened with proven-independent ambiguous records held back). For every deferred record, the routine confirms the entire `<!-- verification: ... -->` block on the prose-PR branch is byte-identical to base. Every byte from the opening `<!-- verification:` to the closing `-->` is checked, including `source_repo:`, `source_ref:`, `source_commit:`, `verified_date:`, `verification_mode:`, comments, and any other line. Checking only `source_commit:` and `verified_date:` is too narrow: the loop can edit `source_ref:`, change `verification_mode:`, or rewrite a comment inside the block without realising it crossed the deferred-record boundary. The routine also confirms the prose PR body contains a `Deferred ambiguous records:` section that links each open `upstream-sweep-manual-review` issue by number for those records. The guards cannot enforce this — they have no way to know which records were classified ambiguous — so the routine is the only thing that catches an accidental edit. **Fail closed on mismatch: do not open the prose PR.**

10. **Practical verification before opening a prose PR**, where available: lint/format checks; re-run `scripts/sweep_poll.py` and confirm `status: "ok"`; parse `SKILL.md` frontmatter and `version.json` to confirm the linked-release rule holds when the body changed; language-appropriate syntax checks for changed code samples; targeted re-grep against the pinned upstream checkout for endpoint/type claims. If a check cannot be run, state that explicitly in the PR body — never silently skip.

## PR body format

Both sweep and prose PR bodies must include:

- **Upstream**: repo name and SHA range checked, e.g. `ant-sdk: 1cbfb3e → d7652ec`.
- **Source artifacts inspected**: short list, e.g. `antd/openapi.yaml`, `docs/sdk/reference/rest-api.md` upstream.
- **Developer-facing change**: one or two sentences describing what changed for users of the documented surface, or "internal refactor; no developer-facing impact".
- **Files changed in this PR**: bulleted list of docs pages and skill files.
- **Why prose changed** (prose PR only): one or two sentences per page explaining the rendered-text edit and which upstream artifact it tracks.
- **Verification run**: bulleted list of which practical checks ran and their result, or "skipped — <reason>" per check.
- **Uncertainties**: one or two sentences calling out any judgment calls or partial evidence the human reviewer should re-check, or "none".

The body is intentionally concise — no full audit transcript — but every claim is traceable to the pinned `head_sha`. The reviewer should be able to skim the body in under a minute and know exactly what to spot-check.

## Credentials and access

The routine needs:

- read access to all in-scope upstream repos for GitHub API HEAD lookups and the shallow clones,
- write access to `withautonomi/autonomi-developer-docs` for branch push, PR creation, and comment/issue creation.

Recommended: a dedicated GitHub App installation token (refreshed per run by Claude Desktop) with `contents: write`, `pull-requests: write`, `issues: write` on the docs repo and `contents: read` on the in-scope upstream repos.

Acceptable alternative: a fine-grained personal access token with the same scopes, stored as a Claude Desktop routine secret.

The token is exposed as `GITHUB_TOKEN` in the routine environment. The script and any `gh` calls read from there. The repo file does not contain the secret value, only the policy.

## Audit gating

SHAs are bumped only after the per-page audit step succeeds against the pinned upstream checkout. If audit fails for a page (ambiguous evidence, removed surface, deleted file, both SHA-fetch paths failing), the page does not enter any PR — it is surfaced as a `manual review needed` issue. The scanner's drift report is a candidate list, not a directive.

## Fail-closed semantics

Scanner fail-closed (whole run aborts):

- GitHub API auth failure or 4xx/5xx on a HEAD or repo metadata lookup,
- network timeout,
- malformed `<!-- verification:` block (missing `source_repo`, `source_ref`, `source_commit`, or `verification_mode`),
- missing or unknown file-level `verification_mode` on `version.json` or `SKILL.md` frontmatter,
- unparseable `repo-registry.yml`,
- unparseable `version.json` or `SKILL.md` frontmatter,
- unknown `source_repo` not in the registry,
- `verification_mode` set to a value other than `current-merged-truth` or `target-manifest`.

The routine treats any non-zero scanner exit as an error condition, posts the JSON diagnostics to the rolling status issue, and exits without opening any PR.

Per-record fail-closed (one page deferred, rest of run continues):

- both `git fetch <recorded_sha>` and `git fetch <head_sha>` fail and the compare API also fails for the same record.

That page is held back as a `manual review needed` issue.

`target-manifest` blocks are deliberately skipped by the scanner and listed in a separate `target_manifest_skipped` array in the JSON output. The routine surfaces those entries in the run summary as "pinned by target-manifest, not bumped" so a human can confirm those pins remain intentional. The routine must never bump a `target-manifest` block against a moving HEAD; doing so would silently overwrite a launch-hardening pin.

## No-drift status report

Comment to the rolling status issue. Format: a short markdown table with one row per record (location / recorded SHA / HEAD SHA / drifted?), grouped by repo for readability.

## Failure modes

- GitHub API rate-limit during the daily poll. Handled by the scanner's fail-closed semantics; the routine posts the error and waits for the next run.
- Deleted or renamed source repo. Same handling.
- Force-push that invalidates a recorded SHA. Caught by the `sweep-sha-reachability` required check on the resulting PR.
- Routine missing the 09:00 UTC slot. Recovery: next-day run picks up the drift; latency at most 24h.
- Claude Desktop routine credential or token expiry. Routine fails closed; user refreshes the secret.
- Daily routine-start cap exhausted on Max plan. Same recovery as missed slot.
- Collision skip when a prior PR is left open for many days. Recovery: user merges or closes the prior PR; the next-day run resumes.
- SHA-fetch failure for a single record (both fetch paths). Recovery: page deferred to a manual-review issue; the rest of the run proceeds.

## Alignment with implementation-plan.md Section 8

The routine is a hosted-scheduled, polling-based equivalent of Tier 1 + Tier 2 of Section 8.

Differences from the per-event arm:

- pull-shaped from a scheduler instead of `repository_dispatch`-driven,
- narrower envelope (metadata-only sweep PR plus optional prose draft PR),
- no per-event collation in v1.

Forward compatibility: when `notify-docs.yml` rolls out in upstream repos, the same routine can grow a webhook-receiver arm without invalidating the daily-poll v1.

## Required-check setup (one-time, after the synthetic verification cases pass)

1. Add `sweep-guard`, `prose-guard`, and `sweep-sha-reachability` (the exact workflow `name:` strings) as required checks on `main` in repo settings → Branch protection.
2. Confirm the routine's bot identity has push access. If branch protection requires reviewers, ensure the bot is granted bypass or has CODEOWNERS coverage on `planning/sweeps/*` and the metadata-only paths, or accept that the user reviews each PR by hand.
3. Provision the `GITHUB_TOKEN` secret in the Claude Desktop routine config per the credentials section above.

## Out of scope

- Claude Desktop Remote routine config (model = Opus 4.7 or higher, schedule, secret value of `GITHUB_TOKEN`) — lives in Claude Desktop, not in this repo. The behaviour (the prompt) is committed at `planning/routines/upstream-sweep-prompt.md`.
- `notify-docs.yml` installation in any upstream repo — tracked under `planning/implementation-plan.md` Section 8.2.
- Per-event sweep PRs — deferred to v2 of the trigger shape.
- Auto-merge — deferred to v1.5. The label-driven `sweep-auto-merge` workflow ships once all three required checks have run cleanly for several weeks.
- Terminology lint, Greptile reviewer setup, and broader v2 verification-staleness checks beyond the sweep envelope.
