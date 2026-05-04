# Use the Autonomi Developer Skill

<!-- verification:
  source_repo: ant-sdk
  source_ref: main
  source_commit: d7652ec3da82dfbe2107778e5223dc413d95815b
  verified_date: 2026-05-02
  verification_mode: current-merged-truth
-->

The Autonomi Developer Skill is a verified knowledge package for AI coding tools such as Claude Code. It is a companion to these docs, not a replacement, and gives your AI coding tool the operational expertise it needs to help you build, integrate, and deploy applications on the Autonomi Network.

**Preview release.** The skill is currently in a draft state. Install names and identifiers may shift before the first non-draft version.

## What it gives your AI

- **Autonomi development expertise**, including how to choose the right path for your project across the SDK, CLI, Direct Rust, and MCP.
- **Access to verified API surfaces, golden flows, and common-failure recipes**, so your AI works from real endpoints, real CLI commands, and real method names instead of guessing.
- **Safety rules around wallets, keys, uploads, and public-network work**, so it defaults to a local devnet first and asks before touching real Autonomi Network Token (ANT).

## Install it

### In Claude Code

Run these commands inside Claude Code to add the Autonomi marketplace and install the skill:

```text
/plugin marketplace add WithAutonomi/autonomi-developer-docs
/plugin install developer@withautonomi
/reload-plugins
```

The skill is now available across all your Claude Code sessions. Claude uses it automatically when you work on Autonomi tasks. To invoke it explicitly, type `/developer:start`.

### In other AI tools

Any tool that loads Claude-style skill files can read it directly from the canonical URL:

```text
https://raw.githubusercontent.com/WithAutonomi/autonomi-developer-docs/main/skills/start/SKILL.md
```

Follow your tool's instructions for installing a Markdown skill file.

### Manual install

To install the skill by hand into Claude Code, drop the file into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/autonomi-developer
curl -fsSL https://raw.githubusercontent.com/WithAutonomi/autonomi-developer-docs/main/skills/start/SKILL.md \
  -o ~/.claude/skills/autonomi-developer/SKILL.md
```

## Staying current

The skill checks for newer published versions on each use and tells you when one is available so you can refresh your local copy. The verified upstream commits are recorded in the skill's metadata, so you can always see exactly which versions of the Autonomi source repos a given copy of the skill was verified against.

## Related pages

- [What is Autonomi?](index.md)
- [Build with the SDKs](sdk/install.md)
- [Use the CLI](cli/use-the-cli.md)
- [Developing in Rust](rust/README.md)
- [Use MCP with AI Tools](mcp/use-mcp-with-ai-tools.md)
