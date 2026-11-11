---
title: Make corrupt local transcripts degrade gracefully
id: make-corrupt-local-transcripts-degrade-gracefully
date: 2026-04-23
type: backlog
status: done
priority: high
tags: [backend, cache, reliability]
refs:
  part_of: [2026-04-23-hardening-and-multi-agent-expansion-plan]
  resolved_by: [harden-local-scan-resilience-and-project-browsing-completeness]
updated: 2026-04-23
---

# Make corrupt local transcripts degrade gracefully

## Objective

Ensure that malformed JSONL or JSON session files only affect the broken
session instead of taking down session browsing, project grouping, or usage
stats for the entire local history browser.

## Scope

- in scope
  - per-file exception isolation during archived JSONL scans
  - per-file exception isolation during legacy JSON scans
  - logging or counting skipped files so failures are visible but non-fatal
  - regression coverage for malformed local data
- out of scope
  - automatic repair of corrupt transcripts
  - broad parser redesign unrelated to graceful degradation

## Acceptance Criteria

- A malformed archived JSONL file does not prevent the session list from
  loading.
- A malformed legacy JSON file does not prevent project or stats views from
  loading.
- Broken files are skipped with enough logging or surfaced metadata to debug
  them later.
- Tests cover at least one malformed JSONL case and one malformed legacy JSON
  case.

## Dependencies

- none

## Implementation Notes

- Primary code areas: `server/fastapi-main.py` in `_load_archived_session_lines`
  and `_scan_local_codex_summaries`.
- Keep the fix local and surgical; this is a current-product reliability issue,
  not a reason to pause until broader provider planning is complete.
- If skipped-file counts are surfaced in API stats, make sure older sessions
  still degrade softly rather than rendering noisy placeholders.
