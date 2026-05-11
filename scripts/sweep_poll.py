#!/usr/bin/env python3
"""Deterministic upstream-drift scanner for the daily sweep routine.

Walks every <!-- verification: ... --> block in docs/**/*.md, every entry in
the verified_commits map of skills/start/version.json, and every entry in the
verified_commits map of the YAML frontmatter of skills/start/SKILL.md.
Resolves each (repo, ref) pair against repo-registry.yml plus a GitHub API
HEAD lookup, and emits a per-record JSON drift report on stdout.

Read-only. Never modifies files. Exits 0 on success, 2 on fail-closed errors.
See planning/routines/upstream-sweep.md for the policy this implements.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "repo-registry.yml"
DOCS_DIR = REPO_ROOT / "docs"
VERSION_JSON_PATH = REPO_ROOT / "skills" / "start" / "version.json"
SKILL_MD_PATH = REPO_ROOT / "skills" / "start" / "SKILL.md"

VERIFICATION_BLOCK_RE = re.compile(
    r"<!--\s*verification:(.*?)-->",
    re.DOTALL,
)
KEY_VALUE_RE = re.compile(r"^\s*([a-z_]+)\s*:\s*(\S.*?)\s*$")
ALLOWED_MODES = {"current-merged-truth", "target-manifest"}
REQUIRED_DOC_KEYS = (
    "source_repo",
    "source_ref",
    "source_commit",
    "verification_mode",
)


class FailClosed(Exception):
    """Raised whenever the scanner cannot make a confident drift judgment.

    Carries one diagnostic dict to embed in the JSON output's `errors` array.
    """

    def __init__(self, diagnostic: dict[str, Any]):
        super().__init__(diagnostic.get("message", "fail-closed"))
        self.diagnostic = diagnostic


def _github_get(url: str, token: str | None) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "autonomi-developer-docs-sweep-poll",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def github_request(path: str, token: str | None = None) -> dict[str, Any]:
    # An authenticated 403 means the org refuses the token, not that the repo
    # is unreachable. Retry once without auth so public repos in orgs that
    # restrict fine-grained PATs still resolve.
    url = f"https://api.github.com{path}"
    try:
        return _github_get(url, token)
    except urllib.error.HTTPError as exc:
        if exc.code == 403 and token:
            try:
                return _github_get(url, None)
            except urllib.error.HTTPError as anon_exc:
                raise FailClosed(
                    {
                        "kind": "github_api_http_error",
                        "url": url,
                        "status": anon_exc.code,
                        "auth_status": exc.code,
                        "message": (
                            f"GitHub API returned {exc.code} authenticated "
                            f"and {anon_exc.code} anonymous for {path}"
                        ),
                    }
                ) from anon_exc
            except urllib.error.URLError as anon_exc:
                raise FailClosed(
                    {
                        "kind": "github_api_network_error",
                        "url": url,
                        "message": (
                            f"GitHub API network error on anonymous retry "
                            f"for {path}: {anon_exc.reason}"
                        ),
                    }
                ) from anon_exc
        raise FailClosed(
            {
                "kind": "github_api_http_error",
                "url": url,
                "status": exc.code,
                "message": f"GitHub API returned {exc.code} for {path}",
            }
        ) from exc
    except urllib.error.URLError as exc:
        raise FailClosed(
            {
                "kind": "github_api_network_error",
                "url": url,
                "message": f"GitHub API network error for {path}: {exc.reason}",
            }
        ) from exc


def parse_owner_repo(url: str) -> tuple[str, str]:
    parsed = urllib.parse.urlparse(url)
    parts = [p for p in parsed.path.strip("/").split("/") if p]
    if parsed.netloc != "github.com" or len(parts) < 2:
        raise FailClosed(
            {
                "kind": "registry_url_unparseable",
                "url": url,
                "message": f"cannot derive <owner>/<repo> from registry url: {url}",
            }
        )
    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[: -len(".git")]
    return owner, repo


def load_registry() -> dict[str, dict[str, Any]]:
    try:
        data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise FailClosed(
            {
                "kind": "registry_yaml_parse_error",
                "path": str(REGISTRY_PATH.relative_to(REPO_ROOT)),
                "message": f"YAML parse error in repo-registry.yml: {exc}",
            }
        ) from exc
    repos = (data or {}).get("repos") or {}
    if not isinstance(repos, dict):
        raise FailClosed(
            {
                "kind": "registry_shape_error",
                "path": str(REGISTRY_PATH.relative_to(REPO_ROOT)),
                "message": "repo-registry.yml: expected top-level 'repos' map",
            }
        )
    return repos


def parse_verification_block(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = KEY_VALUE_RE.match(line)
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def line_of_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def walk_docs(
    registry: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
    target_manifest_skipped: list[dict[str, Any]],
    pair_set: set[tuple[str, str]],
) -> None:
    if not DOCS_DIR.exists():
        return
    for path in sorted(DOCS_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        rel = str(path.relative_to(REPO_ROOT))
        for match in VERIFICATION_BLOCK_RE.finditer(text):
            block_line = line_of_offset(text, match.start())
            fields = parse_verification_block(match.group(1))
            missing = [k for k in REQUIRED_DOC_KEYS if k not in fields]
            if missing:
                raise FailClosed(
                    {
                        "kind": "doc_block_missing_required_keys",
                        "location": f"{rel}:{block_line}",
                        "missing": missing,
                        "message": (
                            f"verification block at {rel}:{block_line} "
                            f"missing required keys: {', '.join(missing)}"
                        ),
                    }
                )
            mode = fields["verification_mode"]
            if mode not in ALLOWED_MODES:
                raise FailClosed(
                    {
                        "kind": "doc_block_unknown_verification_mode",
                        "location": f"{rel}:{block_line}",
                        "verification_mode": mode,
                        "message": (
                            f"verification block at {rel}:{block_line} has "
                            f"unknown verification_mode: {mode!r}"
                        ),
                    }
                )
            repo_key = fields["source_repo"]
            if repo_key not in registry:
                raise FailClosed(
                    {
                        "kind": "doc_block_unknown_source_repo",
                        "location": f"{rel}:{block_line}",
                        "source_repo": repo_key,
                        "message": (
                            f"verification block at {rel}:{block_line} "
                            f"references repo not in repo-registry.yml: {repo_key}"
                        ),
                    }
                )
            ref = fields["source_ref"]
            recorded = fields["source_commit"]
            location = f"{rel}:{block_line}"
            if mode == "target-manifest":
                target_manifest_skipped.append(
                    {
                        "location": location,
                        "repo": repo_key,
                        "ref": ref,
                        "recorded_sha": recorded,
                    }
                )
                continue
            records.append(
                {
                    "location": location,
                    "scope": "docs",
                    "repo": repo_key,
                    "ref": ref,
                    "recorded_sha": recorded,
                    "head_sha": None,
                    "drifted": None,
                }
            )
            pair_set.add((repo_key, ref))


def resolve_skill_default_branch(
    repo_key: str,
    registry: dict[str, dict[str, Any]],
    token: str | None,
    cache: dict[str, str],
) -> str:
    if repo_key in cache:
        return cache[repo_key]
    if repo_key not in registry:
        raise FailClosed(
            {
                "kind": "skill_unknown_source_repo",
                "source_repo": repo_key,
                "message": (
                    f"skill verified_commits references repo not in "
                    f"repo-registry.yml: {repo_key}"
                ),
            }
        )
    owner, repo = parse_owner_repo(registry[repo_key]["url"])
    meta = github_request(f"/repos/{owner}/{repo}", token)
    branch = meta.get("default_branch")
    if not isinstance(branch, str) or not branch:
        raise FailClosed(
            {
                "kind": "github_default_branch_missing",
                "repo": repo_key,
                "message": (
                    f"GitHub /repos/{owner}/{repo} returned no default_branch"
                ),
            }
        )
    cache[repo_key] = branch
    return branch


def walk_version_json(
    registry: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
    target_manifest_skipped: list[dict[str, Any]],
    pair_set: set[tuple[str, str]],
    default_branch_cache: dict[str, str],
    token: str | None,
) -> None:
    if not VERSION_JSON_PATH.exists():
        return
    raw = VERSION_JSON_PATH.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FailClosed(
            {
                "kind": "version_json_parse_error",
                "path": str(VERSION_JSON_PATH.relative_to(REPO_ROOT)),
                "message": f"JSON parse error in version.json: {exc}",
            }
        ) from exc
    mode = data.get("verification_mode")
    if mode not in ALLOWED_MODES:
        raise FailClosed(
            {
                "kind": "version_json_unknown_verification_mode",
                "path": str(VERSION_JSON_PATH.relative_to(REPO_ROOT)),
                "verification_mode": mode,
                "message": (
                    f"version.json has missing or unknown verification_mode: "
                    f"{mode!r}"
                ),
            }
        )
    if "verified_commits" not in data:
        raise FailClosed(
            {
                "kind": "version_json_shape_error",
                "path": str(VERSION_JSON_PATH.relative_to(REPO_ROOT)),
                "message": "version.json: verified_commits is missing",
            }
        )
    commits = data["verified_commits"]
    if not isinstance(commits, dict):
        raise FailClosed(
            {
                "kind": "version_json_shape_error",
                "path": str(VERSION_JSON_PATH.relative_to(REPO_ROOT)),
                "message": "version.json: verified_commits must be an object",
            }
        )
    rel = str(VERSION_JSON_PATH.relative_to(REPO_ROOT))
    for repo_key, recorded in sorted(commits.items()):
        location = f"{rel}:verified_commits.{repo_key}"
        if not isinstance(recorded, str) or not recorded:
            raise FailClosed(
                {
                    "kind": "version_json_shape_error",
                    "path": rel,
                    "message": (
                        f"version.json: verified_commits.{repo_key} "
                        "is not a non-empty string"
                    ),
                }
            )
        if mode == "target-manifest":
            target_manifest_skipped.append(
                {
                    "location": location,
                    "repo": repo_key,
                    "ref": None,
                    "recorded_sha": recorded,
                }
            )
            continue
        ref = resolve_skill_default_branch(
            repo_key, registry, token, default_branch_cache
        )
        records.append(
            {
                "location": location,
                "scope": "skill_version_json",
                "repo": repo_key,
                "ref": ref,
                "recorded_sha": recorded,
                "head_sha": None,
                "drifted": None,
            }
        )
        pair_set.add((repo_key, ref))


def parse_skill_md_frontmatter() -> dict[str, Any] | None:
    """Return frontmatter as a dict, or None if SKILL.md does not exist.

    A present-but-empty or shape-invalid SKILL.md raises FailClosed; only a
    truly absent file is reported via the None sentinel so callers can
    distinguish that from an empty mapping.
    """
    if not SKILL_MD_PATH.exists():
        return None
    text = SKILL_MD_PATH.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise FailClosed(
            {
                "kind": "skill_md_missing_frontmatter",
                "path": str(SKILL_MD_PATH.relative_to(REPO_ROOT)),
                "message": "SKILL.md does not begin with YAML frontmatter",
            }
        )
    closing = text.find("\n---", 3)
    if closing < 0:
        raise FailClosed(
            {
                "kind": "skill_md_unterminated_frontmatter",
                "path": str(SKILL_MD_PATH.relative_to(REPO_ROOT)),
                "message": "SKILL.md frontmatter is not terminated by '---'",
            }
        )
    raw = text[3:closing]
    try:
        loaded = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise FailClosed(
            {
                "kind": "skill_md_yaml_parse_error",
                "path": str(SKILL_MD_PATH.relative_to(REPO_ROOT)),
                "message": f"YAML parse error in SKILL.md frontmatter: {exc}",
            }
        ) from exc
    if loaded is None:
        raise FailClosed(
            {
                "kind": "skill_md_frontmatter_empty",
                "path": str(SKILL_MD_PATH.relative_to(REPO_ROOT)),
                "message": (
                    "SKILL.md frontmatter is empty; verification metadata "
                    "is required"
                ),
            }
        )
    if not isinstance(loaded, dict):
        raise FailClosed(
            {
                "kind": "skill_md_frontmatter_shape_error",
                "path": str(SKILL_MD_PATH.relative_to(REPO_ROOT)),
                "message": "SKILL.md frontmatter must be a YAML mapping",
            }
        )
    return loaded


def walk_skill_md(
    registry: dict[str, dict[str, Any]],
    records: list[dict[str, Any]],
    target_manifest_skipped: list[dict[str, Any]],
    pair_set: set[tuple[str, str]],
    default_branch_cache: dict[str, str],
    token: str | None,
) -> None:
    fm = parse_skill_md_frontmatter()
    if fm is None:
        return
    mode = fm.get("verification_mode")
    if mode not in ALLOWED_MODES:
        raise FailClosed(
            {
                "kind": "skill_md_unknown_verification_mode",
                "path": str(SKILL_MD_PATH.relative_to(REPO_ROOT)),
                "verification_mode": mode,
                "message": (
                    f"SKILL.md frontmatter has missing or unknown "
                    f"verification_mode: {mode!r}"
                ),
            }
        )
    if "verified_commits" not in fm:
        raise FailClosed(
            {
                "kind": "skill_md_shape_error",
                "path": str(SKILL_MD_PATH.relative_to(REPO_ROOT)),
                "message": (
                    "SKILL.md frontmatter: verified_commits is missing"
                ),
            }
        )
    commits = fm["verified_commits"]
    if not isinstance(commits, dict):
        raise FailClosed(
            {
                "kind": "skill_md_shape_error",
                "path": str(SKILL_MD_PATH.relative_to(REPO_ROOT)),
                "message": (
                    "SKILL.md frontmatter: verified_commits must be a mapping"
                ),
            }
        )
    rel = str(SKILL_MD_PATH.relative_to(REPO_ROOT))
    for repo_key, recorded in sorted(commits.items()):
        location = f"{rel}:verified_commits.{repo_key}"
        if not isinstance(recorded, str) or not recorded:
            raise FailClosed(
                {
                    "kind": "skill_md_shape_error",
                    "path": rel,
                    "message": (
                        f"SKILL.md frontmatter: verified_commits.{repo_key} "
                        "is not a non-empty string"
                    ),
                }
            )
        if mode == "target-manifest":
            target_manifest_skipped.append(
                {
                    "location": location,
                    "repo": repo_key,
                    "ref": None,
                    "recorded_sha": recorded,
                }
            )
            continue
        ref = resolve_skill_default_branch(
            repo_key, registry, token, default_branch_cache
        )
        records.append(
            {
                "location": location,
                "scope": "skill_md",
                "repo": repo_key,
                "ref": ref,
                "recorded_sha": recorded,
                "head_sha": None,
                "drifted": None,
            }
        )
        pair_set.add((repo_key, ref))


def resolve_head_shas(
    pair_set: set[tuple[str, str]],
    registry: dict[str, dict[str, Any]],
    token: str | None,
) -> dict[tuple[str, str], str]:
    head_shas: dict[tuple[str, str], str] = {}
    for repo_key, ref in sorted(pair_set):
        owner, repo = parse_owner_repo(registry[repo_key]["url"])
        encoded_ref = urllib.parse.quote(ref, safe="")
        commit = github_request(
            f"/repos/{owner}/{repo}/commits/{encoded_ref}", token
        )
        sha = commit.get("sha")
        if not isinstance(sha, str) or not sha:
            raise FailClosed(
                {
                    "kind": "github_head_sha_missing",
                    "repo": repo_key,
                    "ref": ref,
                    "message": (
                        f"GitHub /repos/{owner}/{repo}/commits/{ref} returned "
                        f"no sha"
                    ),
                }
            )
        head_shas[(repo_key, ref)] = sha
    return head_shas


def attach_drift(
    records: list[dict[str, Any]],
    head_shas: dict[tuple[str, str], str],
) -> None:
    for record in records:
        head = head_shas[(record["repo"], record["ref"])]
        record["head_sha"] = head
        record["drifted"] = record["recorded_sha"] != head


def main() -> int:
    token_raw = os.environ.get("GITHUB_TOKEN", "").strip()
    token: str | None = token_raw or None
    notices: list[dict[str, Any]] = []
    if token is None:
        notices.append(
            {
                "kind": "unauthenticated_mode",
                "severity": "info",
                "message": (
                    "GITHUB_TOKEN not set; using anonymous GitHub API "
                    "requests (60 req/hour limit)."
                ),
            }
        )

    try:
        registry = load_registry()
        records: list[dict[str, Any]] = []
        target_manifest_skipped: list[dict[str, Any]] = []
        pair_set: set[tuple[str, str]] = set()
        default_branch_cache: dict[str, str] = {}

        walk_docs(registry, records, target_manifest_skipped, pair_set)
        walk_version_json(
            registry,
            records,
            target_manifest_skipped,
            pair_set,
            default_branch_cache,
            token,
        )
        walk_skill_md(
            registry,
            records,
            target_manifest_skipped,
            pair_set,
            default_branch_cache,
            token,
        )

        head_shas = resolve_head_shas(pair_set, registry, token)
        attach_drift(records, head_shas)

    except FailClosed as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                    "records": [],
                    "target_manifest_skipped": [],
                    "notices": notices,
                    "errors": [exc.diagnostic],
                },
                indent=2,
            )
        )
        return 2

    output = {
        "status": "ok",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "records": records,
        "target_manifest_skipped": target_manifest_skipped,
        "notices": notices,
        "errors": [],
    }
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
