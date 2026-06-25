---
title: Remove silent project browser truncation
id: remove-silent-project-browser-truncation
date: 2026-04-23
type: backlog
status: done
priority: high
tags: [frontend, browsing, scale]
refs:
  part_of: [2026-04-23-hardening-and-multi-agent-expansion-plan]
  resolved_by: [harden-local-scan-resilience-and-project-browsing-completeness]
updated: 2026-04-23
---

# Remove silent project browser truncation

## Objective

Ensure the project browser remains complete and trustworthy for large local
histories instead of silently hiding projects after the first 200 entries.

## Scope

- in scope
  - remove the hardcoded 200-project ceiling in the frontend flow
  - fetch all projects or introduce explicit pagination with visible controls
  - ensure the UI communicates when additional results exist
- out of scope
  - redesigning the full project card UI
  - unrelated session-list filtering work

## Acceptance Criteria

- No project is silently omitted because of a frontend fetch cap.
- If pagination remains, the UI exposes it explicitly and makes the limit
  visible to the user.
- If the project list is fetched exhaustively, the implementation handles large
  histories deterministically rather than depending on a magic constant.
- The backlog item references the affected code path so future regressions are
  easy to trace.

## Dependencies

- none

## Implementation Notes

- Primary code area: `refreshLocalProjectSummaries()` in
  `src/components/app/app.ts`.
- The backend already paginates by `offset` and `limit`, so the fix can either
  loop until complete or expose project pagination as a first-class UI concern.
- Prefer a fix that preserves the repo's goal of reliable local browsing over a
  prematurely optimized shortcut.
