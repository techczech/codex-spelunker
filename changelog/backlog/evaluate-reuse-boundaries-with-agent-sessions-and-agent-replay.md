---
title: Evaluate reuse boundaries with Agent Sessions and Agent Replay
id: evaluate-reuse-boundaries-with-agent-sessions-and-agent-replay
date: 2026-04-23
type: backlog
status: in-progress
priority: critical
artifacts: ["https://github.com/jazzyalex/agent-sessions", "https://github.com/agentreplay/agentreplay", "../reports/2026-04-23-reuse-evaluation-agent-sessions-agent-replay.md"]
tags: [architecture, research, reuse]
refs:
  part_of: [2026-04-23-hardening-and-multi-agent-expansion-plan]
updated: 2026-04-23
---

# Evaluate reuse boundaries with Agent Sessions and Agent Replay

## Objective

Establish where Codex Spelunker should reuse, interoperate with, or explicitly
avoid duplicating capabilities that already exist in Agent Sessions and Agent
Replay before broadening this repo into a multi-agent history platform.

## Scope

- in scope
  - compare provider coverage, storage models, search/index approaches,
    analytics surfaces, resume workflows, and live-session observability
  - identify which capabilities are worth reusing as concepts, formats, or
    import/export boundaries
  - document licensing constraints, especially MIT versus AGPL implications
  - recommend where Codex Spelunker should stay focused versus where it should
    integrate or remain compatible
- out of scope
  - copying code into this repo
  - shipping multi-provider support in the same change as the evaluation
  - pixel-level UI parity with either project

## Acceptance Criteria

- Produce a written comparison matrix covering Agent Sessions and Agent Replay
  against Codex Spelunker's current and planned capabilities.
- Record an explicit recommendation for each major capability area:
  parser/import, canonical index, resume workflows, live monitoring, analytics,
  and UI.
- Record license implications and a clear no-go or escalation rule for AGPL
  code reuse.
- Identify concrete next steps for Codex Spelunker that follow from the
  evaluation rather than from generic competitor research.

## Dependencies

- none

## Implementation Notes

- This repo does not currently have local clones of either project, so the
  first pass can rely on public repo/docs inspection before deciding whether a
  local checkout is necessary.
- The evaluation should focus on reuse boundaries, not on proving that this
  repo must become a clone of either product.
- If a reusable boundary is found, prefer import/export compatibility or a
  provider adapter contract over shared UI assumptions.
- First report written in `reports/2026-04-23-reuse-evaluation-agent-sessions-agent-replay.md`.
