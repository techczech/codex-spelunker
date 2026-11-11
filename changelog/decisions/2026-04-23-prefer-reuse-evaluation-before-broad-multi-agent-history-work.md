---
title: Prefer reuse evaluation before broad multi-agent history work
id: 2026-04-23-prefer-reuse-evaluation-before-broad-multi-agent-history-work
date: 2026-04-23
type: decision
status: accepted
tags: [architecture, planning, reuse]
refs: {}
updated: 2026-04-23
---

# Prefer reuse evaluation before broad multi-agent history work

## Context

Codex Spelunker is moving from a Codex-only session browser toward a broader
local observability tool for coding agents. That direction overlaps with
existing projects such as Agent Sessions and Agent Replay, both of which
already cover significant parts of the target surface: multi-provider session
browsing, resume workflows, analytics, and live activity views.

The repo also has immediate correctness work to do on the current Codex path:

- malformed local transcript handling should degrade gracefully
- backend translation should accept the standard `OPENAI_API_KEY`
- the project browser should not silently truncate large histories

The user explicitly requested that broad follow-on work should consider reuse
from Agent Sessions and Agent Replay so this repo does not replicate large
blocks of already-solved functionality. Licensing is also material here:
Agent Sessions is MIT, while Agent Replay is AGPL-3.0, so direct code reuse
has different implications depending on the source.

## Decision

Before any broad multi-agent history or observability expansion, the project
must complete a reuse evaluation against Agent Sessions and Agent Replay and
prefer composition, interoperability, narrow importers, or upstream
contribution over greenfield duplication.

Small correctness and reliability fixes inside the current Codex-only
implementation do not need to wait for that evaluation and may land directly.

Direct code adoption from AGPL components is out of scope unless a follow-up
decision explicitly accepts the licensing consequences.

## Consequences

- The current hardening fixes can proceed immediately without being blocked by
  the larger architecture spike.
- Multi-provider work now has a concrete prerequisite: compare reuse options
  before adding new providers or large new observability surfaces.
- The project should bias toward adapter boundaries and canonical import
  contracts rather than cloning whole UI or backend stacks.
- AGPL code cannot be copied casually into this repository; any such move
  requires an explicit licensing decision.
- Planning artefacts for this work should live in `backlog/` and `phases/`
  and stay tied to the reuse-evaluation milestone.

## Alternatives Considered

- Build Codex Spelunker's multi-agent support entirely in-house now —
  rejected because it risks duplicating mature functionality that already
  exists elsewhere.
- Block even the small correctness fixes until the broader evaluation is done —
  rejected because the current findings are local reliability issues and can be
  fixed safely inside the existing architecture.
- Copy functionality ad hoc from whichever project looks closest —
  rejected because license, architecture, and product-boundary differences need
  deliberate evaluation first.
