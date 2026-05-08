# Upstream sweep — routine prompt

This is the prompt the Claude Desktop Remote routine executes once per day. The behaviour lives in version control so it is reviewable, diffable, and rollback-able. The Claude Desktop routine config references this file by URL or paste-in. Schedule, model selection, and the `GITHUB_TOKEN` secret value live in Claude Desktop, not in this repo.

## Goal

Perform the daily upstream-drift sweep per `planning/routines/upstream-sweep.md`. Read that policy doc and `planning/verification-workflow.md` first; they govern this run.

## Model requirement

This prompt requires **Opus 4.7 or higher**. The audit/write/verify loop in step 4 assumes the model can:

- inspect upstream diffs and source at pinned SHAs,
- compare those source changes against affected docs pages and `skills/start/SKILL.md`,
- write actual prose into a draft PR (not suggestions in the PR body),
- run practical verification on the prepared branch (linters, syntax checks, re-runs of the scanner) before opening the PR.

Do not run this prompt under a smaller model.

## Inputs available

- The `Bash` tool, with the docs repo cloned at the working directory.
- The `gh` CLI for all GitHub operations (PR list/create, issue list/create, comment).
- `GITHUB_TOKEN` in the environment, with read access to in-scope upstream repos and write access to `withautonomi/autonomi-developer-docs`.
- `python3` plus the PyYAML pin from `scripts/requirements.txt`.

Use `gh` consistently for GitHub work. Do not call the GitHub MCP server.

## Reference rules

Apply verbatim:

- `CLAUDE.md` — voice, terminology lockfile, page templates, refusal rules.
- `planning/verification-workflow.md` — source audit -> draft -> verify procedure.
- `planning/routines/upstream-sweep.md` — sweep policy (branch convention, collision handling, named envelopes, fail-closed semantics, Opus audit/write/verify loop, page batching rule, PR body format, audit-diff fetch rule).
- `repo-registry.yml` — `url:` and `topics:` per repo; `topics:` focuses source-artifact selection in step 4.
- `component-registry.yml` — component-to-page map; same role.

## Steps

### 0. Bootstrap the rolling status thread

POSIX shell only. No `mapfile`, no Bash arrays, no bash-only parameter expansions, no `gh issue create --json/--jq` (`gh issue create` does not support those flags). Capture-then-decide is the key invariant: any `gh` failure (auth, network, API) must abort the bootstrap immediately rather than be silently coerced into "label missing" or "no open issue".

```sh
set -eu

# (a) label — capture gh output before deciding so auth/API failure is fatal,
# not silently coerced into "label missing".
labels=$(gh label list --json name --jq '.[].name')
if ! printf '%s\n' "$labels" | grep -qx upstream-sweep-status; then
  gh label create upstream-sweep-status \
    --description "Rolling status thread for the daily upstream-sweep routine"
fi

# (b) issue — same capture-then-decide pattern. gh issue create has no
# --json/--jq, so parse the URL it writes to stdout.
first_issue=$(gh issue list --state open --label upstream-sweep-status \
  --json number --jq 'sort_by(.number) | .[0].number // empty')
if [ -z "$first_issue" ]; then
  url=$(gh issue create --title "Upstream sweep status" \
    --label upstream-sweep-status \
    --body "Rolling status thread for the daily upstream-sweep routine.")
  STATUS_ISSUE="${url##*/}"
else
  STATUS_ISSUE="$first_issue"
  count=$(gh issue list --state open --label upstream-sweep-status \
    --json number --jq 'length')
  if [ "$count" -gt 1 ]; then
    others=$(gh issue list --state open --label upstream-sweep-status \
      --json number --jq '[.[].number | tostring] | join(", ")')
    gh issue comment "$STATUS_ISSUE" --body \
      "Multiple open issues carry the upstream-sweep-status label: $others. Continuing against #$STATUS_ISSUE (lowest number). Please close the duplicates."
  fi
fi
```

`gh issue create --label X` fails when the label is missing, so the label step must precede issue creation. Capture `$STATUS_ISSUE` for every status post in later steps.

### 1. Open-PR collision check

```sh
OPEN_CLAUDE_PRS=$(
  gh pr list --state open --limit 1000 --json number,headRefName \
    --jq '.[] | select(.headRefName | startswith("claude/sweep-") or startswith("claude/prose-")) | .number'
)
```

If `OPEN_CLAUDE_PRS` is non-empty, post a collision comment to `$STATUS_ISSUE` listing the open PR numbers, and exit without opening anything. Drift is re-detected on the next run.

`--limit 1000` defeats `gh`'s default 30-row cap so a busy repo cannot hide a still-open prior sweep/prose PR behind pagination. GitHub's `--search` syntax does not reliably match branch prefixes; the JSON list with a client-side prefix filter is the trustworthy form.

### 2. Run the deterministic scanner

```sh
python3 scripts/sweep_poll.py > sweep_report.json
```

Read `sweep_report.json`. If `status` is `"error"`, post the JSON diagnostics to `$STATUS_ISSUE` and exit. The scanner's fail-closed semantics are documented in `planning/routines/upstream-sweep.md` and in `scripts/sweep_poll.py`.

If `target_manifest_skipped` is non-empty, include those entries in the run summary at step 6 as "pinned by target-manifest, not bumped" so a human can confirm those pins remain intentional. Never modify `target-manifest` records.

### 3. Short-circuit on no drift

If `records` is empty or every record has `drifted: false`, post a no-drift summary table to `$STATUS_ISSUE` (one row per record: location / recorded / HEAD / drifted?) and exit.

### 4. Opus audit/write/verify loop

For each drifted record, run the loop below. Treat the deterministic scanner's drift list as a candidate set, not a directive: SHAs are bumped only after this loop confirms the audit succeeds.

#### 4.1 Fetch both SHAs

Audit must compare the upstream tree at `head_sha` against the diff from `recorded_sha` to `head_sha`. Both SHAs are required.

```sh
TMP=$(mktemp -d)
cd "$TMP"
git init -q
git remote add origin "<upstream-url-from-repo-registry.yml>"
git fetch --depth 1 origin "<recorded_sha>"
git fetch --depth 1 origin "<head_sha>"
git checkout --detach "<head_sha>"
```

If either `git fetch` fails (reachable-SHA fetches disabled by the repo, SHA garbage-collected, network failure), fall back to the GitHub compare API:

```sh
gh api "repos/<owner>/<repo>/compare/<recorded_sha>...<head_sha>" > compare.json
```

Inspect `compare.json` for `commits[]`, `files[]`, and the `status` field.

If both the local fetch and the compare API fail for a record, **fail closed for that record's page**: open a `manual review needed` issue per step 5 and skip the page from both PRs. Never compare against a moving branch name like `main`.

#### 4.2 Compute the upstream diff

```sh
git log --oneline "<recorded_sha>..<head_sha>"
git diff --stat "<recorded_sha>..<head_sha>"
git diff "<recorded_sha>..<head_sha>" -- <focused-paths>
```

Or read `compare.json` `commits[]` and `files[]` when running via the compare-API fallback.

#### 4.3 Inspect upstream source artifacts at `head_sha`

Focus on the artifacts the affected docs page or skill cites. Use `repo-registry.yml`'s `topics:` and `component-registry.yml`'s component map to pick artifacts deterministically.

Common artifacts to read:

- OpenAPI specs (`antd/openapi.yaml`),
- gRPC `.proto` files (`antd/proto/`),
- CLI source and `--help` output for command-name and flag changes,
- public Rust modules cited by the Direct Rust pages,
- README and docs in the upstream repo when the page references them.

#### 4.4 Compare against the affected docs pages and `SKILL.md`

For `scope: "docs"` records, read the page at the recorded `location` path. For `scope: "skill_version_json"` and `scope: "skill_md"` records, read `skills/start/SKILL.md`.

Identify any rendered claim, code sample, command, endpoint, type, field, or live-reference URL that no longer matches the pinned source.

#### 4.5 Classify the record

Pick exactly one:

- **metadata-only** — internal refactor, test-only changes, dependency bumps, code style. No developer-facing impact. Stamp refresh suffices.
- **prose** — a documented surface changed (new flow, renamed command, removed step, changed payload shape, new error variant that surfaces to users, a moved live-reference URL). Prose changes are required.
- **ambiguous** — evidence is unclear, the page or skill cites something the routine cannot reliably re-derive, or the audit hits a known edge case (deleted file the page referenced, removed surface still mentioned in prose). Defer to a manual-review issue rather than guess.

#### 4.6 Apply the page batching rule (after all records are classified)

Apply the five-case rule per page:

1. **No ambiguous + any prose** → prose PR. All audited non-ambiguous records on the page (prose-impacting **and** metadata-only) are stamped in the same PR.
2. **No ambiguous + all metadata-only** → sweep PR.
3. **Ambiguous + no prose** → manual-review issue, no PR for the page. Metadata-only records on the same page are deferred alongside the ambiguity.
4. **Ambiguous overlapping prose, or unproven independence** → manual-review issue, no PR for the page. Two records overlap when they share any of: claim, page section, code sample, command, endpoint, source artifact, or `<!-- verification: -->` block.
5. **Ambiguous + prose with proven independence** → prose PR for the prose-affected records and any metadata-only records on the same page that are independent of every deferred ambiguity (same overlap dimensions). Ambiguous records and any metadata-only records that overlap a deferred ambiguity stay unstamped: the entire `<!-- verification: ... -->` block is left byte-identical to base. One manual-review issue per deferred record.

The two PRs never touch the same page. A prose PR may touch a page with deferred ambiguous records, but must not edit any byte inside those records' verification blocks.

#### 4.7 Write prose changes directly into the prose PR

When the page is in the prose batch, write the actual prose edits into the draft `claude/prose-*` PR. Apply `CLAUDE.md`'s voice, terminology lockfile, page templates, and refusal rules. Do not stop at "suggestions in the PR body" — the PR diff must contain the prose edit.

#### 4.8 Skill-aware prose

If the audit finds skill impact, include both the human-facing docs change and the `SKILL.md` change in the same prose PR. If the `SKILL.md` body changes, also include the linked patch release set in the same PR:

- `skills/start/version.json: version` bumped to a new patch version (`MAJOR.MINOR.(PATCH+1)`),
- `skills/start/version.json: published_date` updated,
- `skills/start/SKILL.md` frontmatter `version:` matching the new `version.json: version`,
- `skills/start/SKILL.md` frontmatter `verified_date:` updated,
- `skills/start/CHANGELOG.md` adding one new entry whose header matches the new `version`.

If the `SKILL.md` body does not change, none of those release fields may change. `prose-guard` enforces both directions.

#### 4.9 Deferred-record self-check (case 5 only)

When the page batching rule emits a prose PR with proven-independent ambiguous records held back, confirm — for **every** deferred record on every prose-PR page — that the entire `<!-- verification: ... -->` block on the prose-PR branch is **byte-identical to base**. Every byte from the opening `<!-- verification:` to the closing `-->` is checked: `source_repo:`, `source_ref:`, `source_commit:`, `verified_date:`, `verification_mode:`, comments, and any other line. Checking only `source_commit:` and `verified_date:` is too narrow; the audit/write step can edit `source_ref:`, change `verification_mode:`, or rewrite a comment inside the block without realising it crossed the deferred-record boundary.

Confirm the prose PR body contains a `Deferred ambiguous records:` section that links each open `upstream-sweep-manual-review` issue by number for those records.

The guards cannot enforce this — they have no way to know which records were classified ambiguous — so this self-check is the only thing that catches an accidental edit. **Fail closed on mismatch: do not open the prose PR. Open a manual-review issue describing the slip and continue with the rest of the run.**

#### 4.10 Practical verification before opening the PR

Run the checks below on the prepared branch where the toolchain is available. If a check cannot be run (tool missing, environment limit), state that explicitly in the PR body. Never silently skip.

- repo lint/format checks (`markdownlint`, link checkers — gracefully skip if not configured),
- re-run `python3 scripts/sweep_poll.py` on the prepared branch and confirm `status: "ok"` with no malformed-block errors,
- parse `SKILL.md` frontmatter and `version.json` to confirm the linked-release rule holds when the body changed,
- for changed code samples: language-appropriate syntax check (`python -m py_compile` for Python, `python -m json.tool` for JSON, `node --check` for JavaScript, OpenAPI re-parse as YAML, cURL command shape sanity), each gracefully skipped when the toolchain is unavailable,
- for endpoint/type claims: targeted re-grep against the pinned upstream checkout to confirm the cited endpoint or type still exists.

Clean up tmp dirs after the loop completes.

### 5. Open issues, then PRs, then post backlinks

The opening order is fixed to break the body↔issue mutual-reference cycle.

**5.1 Manual-review issues first**, before any PR is opened. For each deferred record (case 5) and each whole-page deferral (cases 3 and 4), compute the fingerprint defined in `planning/routines/upstream-sweep.md` `## Manual-review issue format`. Then list open manual-review issues:

```sh
gh issue list --state open --label upstream-sweep-manual-review \
  --limit 1000 --json number,title,body
```

Walk each candidate issue's `body` field client-side and look for a line that, after stripping leading and trailing whitespace, equals the fingerprint string verbatim. Do **not** use `gh issue list --search` — GitHub issue search tokenization does not reliably match a pipe-heavy fingerprint embedded in the body. `--limit 1000` defeats `gh`'s default 30-row cap.

- On a fingerprint match: reuse the existing issue. Skip `gh issue create` and capture the existing number for the PR body. Do not edit the issue body — reused issues will accumulate a chronological comment trail in step 5.3.
- No fingerprint match: `gh issue create --label upstream-sweep-manual-review` with the body specified in `## Manual-review issue format`. The body **must** contain the fingerprint on its own line, surrounded by blank lines, so the next run's client-side match is unambiguous. Capture the new issue's number from the URL `gh issue create` writes to stdout (`number=${url##*/}`).

Do **not** include a PR backlink in any issue body at this stage — the PR URL does not exist yet.

**5.2 Open the draft PR(s)** next. The PR body's `Deferred ambiguous records:` section embeds the manual-review issue numbers captured in 5.1 (a mix of newly-created and reused). Capture each PR URL from `gh pr create` stdout. Sweep PRs are opened ready-for-review; prose PRs are opened as draft.

**Sweep PR** (only if at least one page has all records classified `metadata-only`, case 2):

- Branch: `claude/sweep-<YYYY-MM-DD>` from `main`.
- Diff envelope (verbatim from `planning/routines/upstream-sweep.md` `## Sweep PR envelope`):
  - update `source_commit:` and `verified_date:` lines inside `<!-- verification: -->` blocks of the affected docs pages,
  - update entries in the `verified_commits` map of `skills/start/version.json` for the corresponding repos (key set unchanged),
  - update entries in the `verified_commits` map of `skills/start/SKILL.md` frontmatter and refresh the `verified_date:` line (key set unchanged),
  - add one new `planning/sweeps/<YYYY-MM-DD>.md` summary file.
- Forbidden: any change to `version`, `published_date`, `skills/start/CHANGELOG.md`, the YAML-frontmatter `version:` line, any rendered prose in `docs/`, any file under `scripts/`, `.github/`, `repo-registry.yml`, or `component-registry.yml`, and any byte inside a `verification_mode: target-manifest` block (sweep PRs must never edit target-manifest pins).
- PR body: see `## PR body format` below.

**Prose PR** (cases 1 and 5):

- Branch: `claude/prose-<YYYY-MM-DD>-<slug>` from `main`. Open as **draft**.
- Includes the prose edits plus the corresponding `source_commit:` / `verified_date:` refreshes for those same pages.
- For case 5, every deferred record's `<!-- verification: ... -->` block is byte-identical to base (deferred-record self-check from step 4.9).
- If the audit found skill impact, include the `SKILL.md` body edit and the linked patch release set per step 4.8.
- The two PRs never touch the same page.
- PR body: see `## PR body format` below; include a "Why prose changed" section, and (for case 5) a "Deferred ambiguous records" section with the issue numbers captured in 5.1.

**5.3 Post backlinks last**. For each manual-review issue captured in 5.1 (newly-created **and** reused), comment with the matching prose-PR URL:

```sh
gh issue comment "$ISSUE_NUMBER" \
  --body "Tracked in $PR_URL. (Run date $(date -u +%Y-%m-%d).)"
```

Use a comment, not a body edit, so the original issue body remains an authoritative record of what was deferred and why, and reused issues accumulate a chronological trail of every run that re-encountered them.

If any of 5.1 / 5.2 / 5.3 errors, post the partial state to `$STATUS_ISSUE` and exit the routine without retrying.

### 6. Run summary

Post a single comment to `$STATUS_ISSUE` summarising the run:

- counts of records scanned, drifted, swept, prose-flagged, manual-review-flagged, and target-manifest-skipped,
- links to the sweep PR, prose PR, and any new issues,
- one-line "no drift" or "skipping; prior PRs open" if those short-circuits fired.

Link to the prose PR's body for audit detail rather than duplicating it in this comment.

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

## Behaviour rules

- Use only `gh` for GitHub operations. Do not invoke the GitHub MCP server.
- Bump the skill's `version`, `published_date`, frontmatter `version:`, and `CHANGELOG.md` only when the prose PR's `SKILL.md` body change requires the linked patch release per step 4.8. On `claude/sweep-*` PRs these fields never move.
- Do not modify `target-manifest` verification blocks. They are pinned for launch hardening.
- If a step fails, post the error to `$STATUS_ISSUE` and exit. Do not open partial PRs.
- For per-record fail-closed (e.g., both SHA fetch and compare API failing for one record), open a `manual review needed` issue for that page and continue with the rest of the run.
- Apply the terminology lockfile in `CLAUDE.md` to any prose written in the prose PR or in issue bodies.
- Cite the pinned `head_sha` in audit notes so a reviewer can reproduce the exact tree the audit consulted.
