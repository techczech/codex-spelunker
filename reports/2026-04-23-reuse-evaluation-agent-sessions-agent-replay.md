# Reuse Evaluation: Agent Sessions and Agent Replay

Date: 2026-04-23

## Purpose

This report evaluates whether Codex Spelunker should reuse, interoperate with,
or intentionally avoid duplicating functionality from:

- [Agent Sessions](https://github.com/jazzyalex/agent-sessions)
- [Agent Replay](https://github.com/agentreplay/agentreplay)

The goal is not to pick a winner. The goal is to decide what Codex Spelunker
should build itself, what it should align with, and what it should not touch
without a stronger product reason.

## Executive Summary

Codex Spelunker should treat the two projects as complementary signals rather
than as direct implementation templates.

- Agent Sessions is the strongest product analogue for Codex Spelunker.
  It already solves multi-provider local session browsing, resume workflows,
  and local-first session search. Its MIT license makes code reuse possible in
  principle, but its native macOS Swift architecture means the highest-value
  reuse is likely at the level of provider coverage, transcript semantics,
  resume-command conventions, fixture design, and UX scope rather than direct
  code import.
- Agent Replay is strategically relevant for observability, tracing, memory,
  evaluations, and live telemetry ingestion, but it is not a close substitute
  for Codex Spelunker's current browse-first product. Its AGPL-3.0 core makes
  direct code reuse a licensing escalation, not a default move. Codex
  Spelunker should treat Agent Replay as an interoperability target and source
  of architectural ideas, not as a code donor.
- The near-term path for Codex Spelunker is still correct: harden the current
  Codex browser, then introduce a canonical multi-provider index with importers
  for transcript-centric tools first.
- The most promising reuse-first move is to align with the session and resume
  surfaces already exposed by Codex, Claude Code, Copilot CLI, and Gemini CLI,
  then leave live observability and memory-heavy workflows as optional
  integrations later.

## Recommendation By Capability Area

| Capability area | Agent Sessions | Agent Replay | Recommendation for Codex Spelunker |
|---|---|---|---|
| Local session browsing | Strong match | Weak match | Build natively in this repo; study Agent Sessions behavior and scope closely |
| Transcript search | Strong match | Partial | Keep local search/indexing here; borrow provider ideas, not UI |
| Resume workflows | Strong match | Not primary | Add a provider-level resume abstraction after importer work |
| Multi-provider ingestion | Strong match | Different model | Use Agent Sessions as product reference; build canonical adapters here |
| Live active-session monitoring | Partial/strong for terminal workflows | Strong | Defer until after canonical index; consider OTLP/event ingestion boundary |
| Persistent memory / evals | Not core | Core | Do not rebuild now; treat Agent Replay as future integration target |
| Direct code reuse | Possible in theory, architecture mismatch in practice | No by default due to AGPL core | Prefer concept, fixture, and compatibility reuse over code copying |

## Project Profiles

### Agent Sessions

Current public positioning:

- local-first macOS app for browsing and resuming AI coding sessions
- currently supports Codex CLI, Claude Code, Cursor CLI, Gemini CLI, GitHub
  Copilot CLI, OpenCode, OpenClaw, and legacy Droid imports
- emphasizes unified browsing, unified search, image browsing, resume commands,
  and local-only indexing
- adds an "Agent Cockpit" for live iTerm2 sessions

Evidence:

- [README on GitHub](https://github.com/jazzyalex/agent-sessions)
- supported paths listed in the README privacy/security section:
  `~/.codex/sessions`, `~/.claude/sessions`, `~/.gemini/tmp`,
  `~/.copilot/session-state`, `~/.cursor/projects`, `~/.cursor/chats`,
  `~/.factory/sessions`, and OpenCode local storage

Why it matters:

- It is already solving the "browse many local coding-agent sessions together"
  problem that Codex Spelunker wants to expand into.
- It proves that a transcript-centric, read-only, local-first multi-provider
  browser is product-valid.
- It exposes the likely first provider set Codex Spelunker should care about.

What is reusable:

- provider coverage priorities
- import assumptions about where session data lives
- normalized browse/search/resume product scope
- fixture/test strategy ideas for transcript-heavy providers
- compatibility targets for "resume this session" commands

What is not obviously reusable:

- native Swift/macOS UI code
- Agent Cockpit implementation details that depend on iTerm2 and a menu-bar app
- app-specific UX conventions that do not translate cleanly to a browser/server
  stack

### Agent Replay

Current public positioning:

- local-first desktop observability, memory, and eval platform
- traces agent activity via SDKs and OpenTelemetry
- includes persistent memory, semantic search, prompt versioning, evaluation
  runs, and a native desktop app
- positions itself as "full observability" rather than a session-history browser

Evidence:

- [GitHub repository](https://github.com/agentreplay/agentreplay)
- [product site](https://agentreplay.dev/)

Why it matters:

- It covers the observability and memory direction that Codex Spelunker could
  eventually grow into.
- It is a strong reference point for trace/event ingestion, causal graphs,
  cost/token analytics, and OTLP compatibility.

What is reusable:

- architectural ideas around traces, events, causal edges, and analytics
- OTLP or trace-style ingestion boundaries
- the idea that observability should support semantic search and analytics over
  local data

What is not reusable by default:

- AGPL-licensed core code
- SochDB- and Rust-specific storage implementation choices
- evaluation and prompt-registry systems that would significantly widen this
  repo's scope before the browse-first product is solid

## Licensing Assessment

### Agent Sessions

- Public repo states MIT license.
- That makes direct code reuse legally feasible.
- Practical constraint is architecture mismatch, not license.

Implication:

- Codex Spelunker may selectively reuse implementation ideas, tests, schemas,
  or narrow code fragments if they are genuinely helpful and technically
  portable.

### Agent Replay

- Public repo states AGPL-3.0 for the core.
- SDKs are described as Apache-2.0, but the main application/core remains AGPL.

Implication:

- Do not copy Agent Replay core code into this repository without an explicit
  licensing decision.
- Interoperability is fine.
- Studying its architecture and aligning with external interfaces is fine.
- Direct embedding, porting, or derivative implementation based on its core
  code is a legal/product escalation, not routine reuse.

## Relevance To Codex Spelunker's Current Direction

Codex Spelunker today is closer to Agent Sessions than to Agent Replay.

Current repo shape:

- local-first browser
- backend scanner + SQLite metadata cache
- transcript opening and local search
- project/session/time filters

That is a browse-first and history-first tool, not a trace-first
observability/evals platform.

Therefore:

- Agent Sessions should shape the next product boundary.
- Agent Replay should shape the eventual integration boundary.

## Provider Surfaces That Matter Most

The best reason not to overfit to either external project is that the primary
truth still lives in the provider tools themselves.

### Claude Code

Official docs confirm:

- sessions persist automatically on disk
- local transcripts live under `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`
- `resume` and `continue` are first-class
- hooks expose structured lifecycle events including session start/stop,
  subagent start/stop, task creation/completion, tool use, and transcript paths

Sources:

- [Claude session guide](https://code.claude.com/docs/en/agent-sdk/sessions)
- [Claude hooks reference](https://code.claude.com/docs/en/hooks)
- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)

Design implication:

- Claude should be treated as a first-class transcript provider now and a
  first-class event provider later.

### GitHub Copilot CLI

Official docs confirm:

- sessions are stored locally in `~/.copilot/session-state/`
- a complete session record exists as files
- a local SQLite session store powers `/chronicle`
- `/chronicle` provides standup/tips/improve flows derived from local history

Sources:

- [About Copilot CLI session data](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/chronicle)
- [Using Copilot CLI session data](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/copilot-cli/chronicle)

Design implication:

- Copilot CLI is a strong proof that a local file store plus derived SQLite
  index is the right pattern for browse-plus-insights products.
- Codex Spelunker should align with this idea for its own canonical index.

### Gemini CLI

Official docs confirm:

- sessions are stored in `~/.gemini/tmp/<project_hash>/chats/`
- history includes prompts, responses, tool executions, and token statistics
- resume/session browser flows are first-class
- checkpointing stores conversation history and tool calls locally
- telemetry can be emitted locally through OpenTelemetry-oriented logging

Sources:

- [Gemini session management](https://geminicli.com/docs/cli/session-management/)
- [Gemini manage sessions and history](https://geminicli.com/docs/cli/tutorials/session-management/)
- [Gemini checkpointing](https://geminicli.com/docs/cli/checkpointing)
- [Gemini telemetry](https://geminicli.com/docs/cli/telemetry)

Design implication:

- Gemini belongs in the first provider wave for transcript ingestion.
- Checkpoints and telemetry suggest a later branch into lineage and live-event
  support without needing to copy Agent Replay.

## What Codex Spelunker Should Reuse First

### 1. Product boundary from Agent Sessions

Adopt this framing:

- one local browser
- many transcript providers
- read-only by default
- strong local search
- explicit resume/reopen workflows
- large-history performance as a core requirement

This is the closest validated scope match.

### 2. Canonical index pattern from Copilot CLI and current Spelunker

Codex Spelunker should evolve toward:

- raw provider data remains in provider-native files or databases
- one derived local canonical index powers browsing, filters, stats, and search
- provider adapters populate that index

This preserves the repo's local-first nature and avoids forcing every feature
to parse raw provider history on demand.

### 3. Event/telemetry boundary from Agent Replay and Claude/Gemini docs

Do not build a full Agent Replay clone.
Do define a future-compatible event model:

- sessions
- turns/messages
- tool calls
- tool outputs
- checkpoints/restore points
- subagent/task lineage
- live events or trace spans

This lets the repo stay useful as a browser now while leaving a clean path to
live observability later.

## What Codex Spelunker Should Not Reuse First

### 1. Agent Replay core implementation

Reason:

- AGPL core
- much broader scope than this repo's current problem
- would drag the project into evals, prompt registries, and memory systems too
  early

### 2. Native app UI from Agent Sessions

Reason:

- architecture mismatch
- the reusable value is the provider and workflow model, not the macOS shell

### 3. Provider-specific live-monitoring assumptions

Agent Sessions' live cockpit is compelling, but it depends heavily on its app
shell and iTerm2 workflow. Codex Spelunker should first define a provider-agnostic
event ingestion model before adding cockpit-style features.

## Concrete Recommendations For Codex Spelunker

### Build now

1. Finish the three current hardening fixes.
2. Introduce a canonical `provider` dimension in the metadata cache and browse
   model.
3. Add transcript importers for:
   - Claude Code
   - Gemini CLI
   - GitHub Copilot CLI
4. Add provider-specific resume metadata and generated resume commands where
   the source tool supports it.

### Design next

1. Canonical schema for:
   - provider
   - session
   - event/message
   - artifact
   - checkpoint
   - resume handle
   - derived metrics
2. Import contracts:
   - transcript file adapter
   - provider database adapter
   - event/telemetry adapter
3. Search/index split:
   - exact/local filter index in SQLite/FTS
   - optional richer content index for semantic search

### Defer

1. Built-in prompt registry/versioning
2. Built-in evaluation framework
3. Full memory platform
4. Full live cockpit UI
5. Any AGPL-derived implementation reuse

## Suggested Architecture Direction

Codex Spelunker should become:

- a local session and artifact browser first
- a canonical multi-provider history index second
- an optional observability/event consumer third

Not:

- a full local evals/memory platform in the next step

The cleanest sequencing is:

1. harden Codex-only reliability
2. add provider abstraction
3. add transcript-centric providers
4. add resume compatibility
5. add optional live-event ingestion
6. decide later whether memory/evals should be native, integrated, or omitted

## Decision Summary

### Reuse from Agent Sessions

Yes, but mostly at the level of:

- provider priority
- workflow coverage
- normalization targets
- compatibility expectations
- fixture and browse semantics

### Reuse from Agent Replay

Yes, but only at the level of:

- architecture ideas
- interoperability targets
- trace/event vocabulary
- future integration possibilities

Not at the level of core-code adoption without a dedicated licensing decision.

## Immediate Next Steps

1. Keep the current hardening backlog items moving independently.
2. Turn `design-canonical-multi-provider-session-index` into the next concrete
   architecture task once this report is accepted.
3. Make Claude Code, Gemini CLI, and Copilot CLI the first explicit provider
   targets.
4. Treat Agent Replay integration as a future optional observability path, not
   as the mainline implementation plan.

## Sources

- [Agent Sessions README](https://github.com/jazzyalex/agent-sessions)
- [Agent Replay GitHub repository](https://github.com/agentreplay/agentreplay)
- [Agent Replay product site](https://agentreplay.dev/)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code sessions](https://code.claude.com/docs/en/agent-sdk/sessions)
- [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
- [About GitHub Copilot CLI session data](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/chronicle)
- [Using GitHub Copilot CLI session data](https://docs.github.com/en/enterprise-cloud@latest/copilot/how-tos/copilot-cli/chronicle)
- [Gemini session management](https://geminicli.com/docs/cli/session-management/)
- [Gemini manage sessions and history](https://geminicli.com/docs/cli/tutorials/session-management/)
- [Gemini checkpointing](https://geminicli.com/docs/cli/checkpointing)
- [Gemini telemetry](https://geminicli.com/docs/cli/telemetry)
