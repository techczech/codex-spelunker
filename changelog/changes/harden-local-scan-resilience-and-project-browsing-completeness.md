---
title: Harden local scan resilience and project browsing completeness
id: harden-local-scan-resilience-and-project-browsing-completeness
date: 2026-04-23
type: change
status: shipped
tags: [backend, frontend, reliability]
refs:
  resolves: [accept-standard-openai-api-key-for-backend-translation, remove-silent-project-browser-truncation]
updated: 2026-04-23
---

# Harden local scan resilience and project browsing completeness

## Summary

Hardened the local Codex history browser against malformed local files,
aligned backend translation with the standard OpenAI API key environment
variable, and removed the silent 200-project cap in the project browser.

## What Changed

- In [server/fastapi-main.py](/Users/dominiklukes/gitrepos/14_apps-and-utilities/codex-spelunker/server/fastapi-main.py),
  malformed archived JSONL files and malformed legacy JSON files are now
  skipped with warnings instead of aborting the entire local scan.
- In [server/fastapi-main.py](/Users/dominiklukes/gitrepos/14_apps-and-utilities/codex-spelunker/server/fastapi-main.py),
  backend translation now prefers `OPENAI_API_KEY` and accepts
  `OPEN_AI_API_KEY` as a legacy fallback through a shared helper.
- In [src/components/app/app.ts](/Users/dominiklukes/gitrepos/14_apps-and-utilities/codex-spelunker/src/components/app/app.ts),
  project summaries are fetched page by page until the complete result set is
  loaded, removing the silent 200-item truncation.
- In [README.md](/Users/dominiklukes/gitrepos/14_apps-and-utilities/codex-spelunker/README.md),
  backend translation credential naming is now documented explicitly.
- Added backend regression coverage in
  [tests/test_fastapi_main.py](/Users/dominiklukes/gitrepos/14_apps-and-utilities/codex-spelunker/tests/test_fastapi_main.py)
  for malformed-file skipping and API key lookup behavior.

## Effect

- One broken local session file no longer takes down session browsing, project
  grouping, or usage stats for the rest of the history store.
- Backend translation works with the standard OpenAI environment variable on a
  normal machine setup.
- Large local histories no longer lose projects silently in the project view.
- No data migration is required. Existing users with `OPEN_AI_API_KEY` keep
  working, while `OPENAI_API_KEY` is now the preferred configuration.
