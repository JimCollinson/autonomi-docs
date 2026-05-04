# Upstream sweep — routine prompt

This is the prompt the Claude Desktop Remote routine executes once per day. The behaviour lives in version control so it is reviewable, diffable, and rollback-able. The Claude Desktop routine config references this file by URL or paste-in. Schedule, model selection, and the `GITHUB_TOKEN` secret value live in Claude Desktop, not in this repo.

## Goal

Perform the daily upstream-drift sweep per `planning/routines/upstream-sweep.md`. Read that policy doc and `planning/verification-workflow.md` first; they govern this run.

## Inputs available

- The `Bash` tool, with the docs repo cloned at the working directory.
- The `gh` CLI for all GitHub operations (PR list/create, issue list/create, comment).
- `GITHUB_TOKEN` in the environment, with read access to in-scope upstream repos and write access to `withautonomi/autonomi-developer-docs`.
- `python3` plus `scripts/requirements.txt` (PyYAML).

Use `gh` consistently for GitHub work. Do not call the GitHub MCP server.

## Reference rules

Apply verbatim:

- `CLAUDE.md` — voice, terminology lockfile, page templates, refusal rules.
- `planning/verification-workflow.md` — source audit -> draft -> verify procedure.
- `planning/routines/upstream-sweep.md` — sweep policy (branch convention, collision handling, allowlist, fail-closed semantics, PR body format, audit gating).

## Steps

### 0. Bootstrap the rolling status thread

Ensure the `upstream-sweep-status` label exists, then ensure exactly one open issue carries it. Both steps are idempotent.

```bash
# (a) label
if [ -z "$(gh label list --json name --jq '.[] | select(.name=="upstream-sweep-status") | .name')" ]; then
  gh label create upstream-sweep-status \
    --description "Rolling status thread for the daily upstream-sweep routine"
fi

# (b) issue
mapfile -t open_issues < <(
  gh issue list --state open --label upstream-sweep-status \
    --json number --jq 'sort_by(.number) | .[].number'
)
case "${#open_issues[@]}" in
  0) STATUS_ISSUE=$(gh issue create \
       --title "Upstream sweep status" \
       --label upstream-sweep-status \
       --body "Rolling status thread for the daily upstream-sweep routine." \
       --json number --jq '.number') ;;
  1) STATUS_ISSUE="${open_issues[0]}" ;;
  *) STATUS_ISSUE="${open_issues[0]}"
     # Warn once: more than one open status issue, asking a human to close the duplicates.
     gh issue comment "$STATUS_ISSUE" --body \
       "Multiple open issues carry the upstream-sweep-status label: ${open_issues[*]}. Continuing against #${STATUS_ISSUE} (lowest number). Please close the duplicates." ;;
esac
```

`gh issue create --label X` fails if the label is missing, so the label step must precede issue creation.

Capture `$STATUS_ISSUE` for every status post in later steps.

### 1. Open-PR collision check

```bash
OPEN_CLAUDE_PRS=$(
  gh pr list --state open --json number,headRefName \
    --jq '.[] | select(.headRefName | startswith("claude/sweep-") or startswith("claude/prose-")) | .number'
)
```

If `OPEN_CLAUDE_PRS` is non-empty, post a collision comment to `$STATUS_ISSUE` listing the open PR numbers, and exit without opening anything. Drift will be re-detected on the next run.

GitHub's `--search` syntax does not reliably match branch prefixes; the JSON list with a client-side prefix filter is the trustworthy form.

### 2. Run the deterministic scanner

```bash
python3 scripts/sweep_poll.py > sweep_report.json
```

Read `sweep_report.json`. If `status` is `"error"`, post the JSON diagnostics to `$STATUS_ISSUE` and exit. The scanner's fail-closed semantics are documented in `planning/routines/upstream-sweep.md` and in `scripts/sweep_poll.py`.

If `target_manifest_skipped` is non-empty, include those entries in the run summary at step 6 as "pinned by target-manifest, not bumped" so a human can confirm those pins remain intentional. Never modify `target-manifest` records.

### 3. Short-circuit on no drift

If `records` is empty or every record has `drifted: false`, post a no-drift summary table to `$STATUS_ISSUE` (one row per record: location / recorded / HEAD / drifted?) and exit.

### 4. Per-page audit against the pinned upstream SHA

Group the drifted records by `(repo, head_sha)`. For each unique `(repo, head_sha)`:

```bash
TMP=$(mktemp -d)
cd "$TMP"
git init
git remote add origin "<upstream-url-from-repo-registry.yml>"
git fetch --depth 1 origin "<head_sha>"
git checkout --detach "<head_sha>"
```

If the SHA fetch fails (reachable-SHA fetches disabled, SHA garbage-collected, network failure), fail closed: post the error to `$STATUS_ISSUE` and exit. Audit must never run against a moving `main`.

Audit each affected docs page against the pinned tree per `planning/verification-workflow.md`:

- For `scope: "docs"` records, the affected page is at the recorded `location` path.
- For `scope: "skill_version_json"` and `scope: "skill_md"` records, the affected page is the relevant skill file.

Classify per-page outcome into one of three batches:

- **sweep batch** — audit confirms the page's claims still hold at `head_sha`; only the metadata stamp needs to move.
- **prose batch** — audit identifies prose impact; the page needs human-reviewed prose edits alongside its SHA stamp refresh.
- **issue batch** — audit cannot make a confident judgment (ambiguous evidence, removed surface, deleted file, etc.). The page does not enter any PR.

Clean up tmp dirs after this step.

### 5. Open PRs and issues per topology

At most one sweep PR and one prose draft PR per run, and zero or more `manual review needed` issues.

**Sweep PR** (if the sweep batch is non-empty):

- Branch: `claude/sweep-<YYYY-MM-DD>` from `main`.
- Diff envelope (verbatim allowlist from `planning/routines/upstream-sweep.md`):
  - update `source_commit:` and `verified_date:` lines inside `<!-- verification: -->` blocks of the affected docs pages,
  - update entries in the `verified_commits` map of `skills/start/version.json` for the corresponding repos,
  - update entries in the `verified_commits` map of `skills/start/SKILL.md`'s YAML frontmatter and refresh its `verified_date:` line,
  - add one new `planning/sweeps/<YYYY-MM-DD>.md` summary file.
- Forbidden in this PR: any change to `version`, `published_date`, `skills/start/CHANGELOG.md`, the YAML-frontmatter `version:` line, or rendered prose in `docs/`.
- PR body uses the format in `planning/routines/upstream-sweep.md` `## PR body format`.

**Prose PR** (if the prose batch is non-empty):

- Branch: `claude/prose-<YYYY-MM-DD>-<slug>` from `main`. Open as **draft**.
- Includes the prose changes plus the corresponding `source_commit:` / `verified_date:` refreshes for those same pages. The two PRs never touch the same page.
- The same `version` / `published_date` / CHANGELOG / frontmatter-`version` forbidding still applies; version bumps are not the routine's job.
- PR body lists which pages have prose changes versus which pages on this PR are metadata-only-on-this-PR so the reviewer knows where to focus.

**Issues** (one per page in the issue batch):

- Title: `Upstream sweep: manual review needed for <page>`.
- Body: the page path, the recorded SHA, the upstream HEAD SHA, the audit failure mode (ambiguous evidence, removed surface, deleted file, etc.), and a snippet of the relevant upstream diff.

### 6. Run summary

Post a single comment to `$STATUS_ISSUE` summarising the run:

- counts of records scanned, drifted, swept, prose-flagged, issue-flagged, and target-manifest-skipped,
- links to the sweep PR, prose PR, and any new issues,
- one-line "no drift" or "skipping; prior PRs open" if those short-circuits fired.

## Behaviour rules

- Use only `gh` for GitHub operations. Do not invoke the GitHub MCP server.
- Do not bump the skill's `version`, `published_date`, or `CHANGELOG.md`. Stamp refreshes are not releases (per `skills/start/MAINTAINING.md`).
- Do not modify `target-manifest` verification blocks. They are pinned for launch hardening.
- If a step fails, post the error to `$STATUS_ISSUE` and exit. Do not open partial PRs.
- Apply the terminology lockfile in `CLAUDE.md` to any prose written in the prose PR or in issue bodies.
- Cite the pinned `head_sha` in audit notes so a reviewer can reproduce the exact tree the audit consulted.
