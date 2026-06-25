---
title: Accept standard OPENAI_API_KEY for backend translation
id: accept-standard-openai-api-key-for-backend-translation
date: 2026-04-23
type: backlog
status: done
priority: medium
tags: [backend, configuration]
refs:
  part_of: [2026-04-23-hardening-and-multi-agent-expansion-plan]
  resolved_by: [harden-local-scan-resilience-and-project-browsing-completeness]
updated: 2026-04-23
---

# Accept standard OPENAI_API_KEY for backend translation

## Objective

Make backend translation work with the standard OpenAI environment variable so
users do not need a repo-specific credential name for a normal local setup.

## Scope

- in scope
  - prefer `OPENAI_API_KEY` for backend translation
  - keep `OPEN_AI_API_KEY` as a backward-compatible fallback if needed
  - align client initialization and runtime validation on the same helper
  - update repo docs if they mention translation credentials
- out of scope
  - translation prompt redesign
  - frontend-only translation flow changes

## Acceptance Criteria

- Backend translation succeeds when only `OPENAI_API_KEY` is configured.
- Existing setups using `OPEN_AI_API_KEY` continue to work unless deliberately
  removed in a later breaking change.
- The backend no longer has mismatched credential checks between client
  initialization and request-time validation.
- Documentation names the preferred environment variable explicitly.

## Dependencies

- none

## Implementation Notes

- Primary code areas: module-level OpenAI client initialization and
  `_call_openai_translate` in `server/fastapi-main.py`.
- Use one helper or constant for env lookup so the import-time client setup and
  runtime guard cannot diverge again.
- This is intentionally a small hardening change and should not be bundled with
  broader multi-provider work.
