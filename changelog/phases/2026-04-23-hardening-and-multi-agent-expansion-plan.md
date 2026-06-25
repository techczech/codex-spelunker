---
title: Hardening and multi-agent expansion plan
id: 2026-04-23-hardening-and-multi-agent-expansion-plan
date: 2026-04-23
type: phase
status: active
tags: [hardening, planning, multi-agent]
refs: {}
updated: 2026-04-23
---

# Hardening and multi-agent expansion plan

## Objective

Harden the current Codex Spelunker implementation against the three review
findings while creating a reuse-driven path for broader multi-agent session
support. The phase exists to avoid mixing quick correctness fixes with a blind
greenfield expansion into Claude Code, Gemini CLI, Copilot CLI, Antigravity,
and similar tools.

## Scope

- in scope:
  - graceful handling of corrupt local session files
  - backend support for the standard `OPENAI_API_KEY`
  - removal of silent project-browser truncation
  - a reuse and licensing spike against Agent Sessions and Agent Replay
  - a follow-on design for a canonical multi-provider session index
- out of scope:
  - immediate implementation of all non-Codex providers
  - large UI rewrites copied wholesale from other tools
  - any AGPL-derived code adoption without an explicit licensing decision

## Entries In This Phase

- `evaluate-reuse-boundaries-with-agent-sessions-and-agent-replay`
- `make-corrupt-local-transcripts-degrade-gracefully`
- `accept-standard-openai-api-key-for-backend-translation`
- `remove-silent-project-browser-truncation`
- `design-canonical-multi-provider-session-index`
