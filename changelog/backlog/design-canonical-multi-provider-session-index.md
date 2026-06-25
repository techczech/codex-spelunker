---
title: Design canonical multi-provider session index
id: design-canonical-multi-provider-session-index
date: 2026-04-23
type: backlog
status: proposed
priority: high
depends_on: [evaluate-reuse-boundaries-with-agent-sessions-and-agent-replay]
artifacts: ["https://github.com/jazzyalex/agent-sessions", "https://github.com/agentreplay/agentreplay", "https://code.claude.com/docs/en/claude-directory", "https://docs.github.com/en/copilot/concepts/agents/copilot-cli/chronicle", "https://geminicli.com/docs/cli/telemetry/"]
tags: [architecture, providers, indexing]
refs:
  part_of: [2026-04-23-hardening-and-multi-agent-expansion-plan]
updated: 2026-04-23
---

# Design canonical multi-provider session index

## Objective

Define the canonical provider and index model that would let Codex Spelunker
support Claude Code, Gemini CLI, Copilot CLI, Antigravity-style artifact
inputs, and future agents without hardcoding Codex-specific assumptions into
every browse, search, and analytics path.

## Scope

- in scope
  - canonical schema for providers, sessions, events, artifacts, checkpoints,
    metrics, and resume handles
  - compatibility plan for current Codex SQLite metadata cache
  - provider adapter boundaries for transcript files, local databases,
    checkpoints, and telemetry streams
  - rules for when a provider gets full transcript support versus artifact-only
    support
- out of scope
  - implementing every provider
  - direct code adoption before the reuse spike is complete
  - immediate UI parity with tools that already ship live cockpit features

## Acceptance Criteria

- Produce a concrete schema and adapter plan that can map Codex, Claude Code,
  Copilot CLI, and Gemini CLI inputs into one local index.
- Define which provider capabilities are first-class on day one versus deferred
  or artifact-only.
- Define the migration path from the current Codex-only cache to the canonical
  multi-provider model.
- Record how the reuse-evaluation outcome changes or constrains this design.

## Dependencies

- `evaluate-reuse-boundaries-with-agent-sessions-and-agent-replay`

## Implementation Notes

- This item should start only after the reuse and licensing evaluation has a
  clear recommendation.
- Antigravity should be treated cautiously until there is a stable official
  local session-format surface; artifact and verification inputs may be the
  right first boundary.
- Primary current code area is `server/fastapi-main.py`, where Codex metadata
  scanning, caching, and qmd document generation are tightly coupled.
