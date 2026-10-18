# Glossary

Terms and acronyms used throughout this book.

## Architecture reference / area doc

The current design of one part of the system, at `docs/architecture/<area>.md`. Present tense, kept in step with the code, no rationale and no dead history. Unbuilt work sits in its `## Implementation status` section. The map at `docs/architecture/README.md` lists every area.

See: [Architecture reference](architecture.md).

## Decision record

A short, numbered markdown file capturing a non-obvious choice and the rationale behind it, at `docs/architecture/decisions/NNNN-<short-name>.md` and cited as "Decision NNNN". Written in past tense and immutable once accepted: only its Status line and `**Current architecture:**` forward-link change. When a decision changes, a new record supersedes it and the old one moves to `archive/`.

See: [Decision records](decisions.md).

## ADR — Architecture Decision Record

The original name for a decision record, from [Michael Nygard's 2011 post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), which also gave the basic Context / Decision / Consequences structure. Earlier versions of this book used the term and the `docs/adr/` directory. See [Migrating from the `docs/adr/` layout](adopting.md#migrating-from-the-docsadr-layout).

## Plan doc

A scheduling document at `docs/plans/<topic>.md` that orders the work a decision (or set of decisions) has committed to. Organised into phases and workstreams with explicit entry/exit criteria. Updated in place as work lands, then moved to `docs/plans/archive/` when Implemented.

See: [Plan documents](plans.md).

## Spike

A time-boxed experiment, written up at `docs/architecture/decisions/spikes/<topic>.md`, that answers a single binary question — "did this approach work?" — before the project commits to it. The term comes from XP / agile usage. Resolved with a clear yes/no/partial outcome and kept forever as the historical answer.

See: [Spike documents](spikes.md).

## Handoff

An ephemeral working-memory document at `docs/handoffs/<topic>-handoff.md` that bridges a session boundary for one thread of work. **Folded into area docs / decisions / spikes / plans at resolution and then deleted in the same commit as the migration.** One per active thread; more than ~2× the people working is a WIP smell.

See: [Handoff documents](handoffs.md).

## Workstream (WS)

A unit of scoped work within a plan doc, typically named with a numeric or alphabetic suffix (`WS1`, `WS-P1.1`, `WS-RH.2`). Sized roughly so a contributor can pick it up cold and start within an hour. Each workstream has 1–3 deliverables and an exit criterion.

## Phase

A coarse-grained grouping of workstreams within a plan, with explicit entry and exit criteria. A plan typically has one or more phases; phases close when their exit criteria are met.

## Fold-then-delete

The migration rule for handoffs: every load-bearing piece of a handoff must be migrated to its proper home (area doc / decision / spike / plan / `CHANGELOG.md`) **before** the handoff file is `git rm`'d. The migration and deletion go in the same commit so the audit trail is intact.

## Archive

The `archive/` subdirectory under `docs/plans/` (finished plans) and `docs/architecture/decisions/` (superseded and withdrawn decisions). Archived docs stay in the repo and keep their names and numbers. Move files there with `doctool.py archive`, which repoints every reference.

## doctool.py

The stdlib-only helper at `docs/scripts/doctool.py`: `lint` checks the layout's rules, `archive` moves a finished doc and repoints links, `new` creates a doc from its template.

## Walk-back

A section in a decision record that names the conditions under which the decision should be revisited, and how to revisit it cheaply. Distinct from a spike: walk-backs are *predictions* about future re-evaluation; spikes are *experiments* run before committing.

## CI — Continuous Integration

The automated build/test pipeline that runs on every push or pull request. Used in the release process as a gating signal ("don't release if CI is red").

## PR — Pull Request

A proposed change to a repository, reviewed before merge. Used loosely throughout this book to mean "a unit of reviewed change," regardless of platform (GitHub PR, GitLab MR, Gerrit changeset, etc.).

## SemVer — Semantic Versioning

The [SemVer 2.0.0 spec](https://semver.org/) for `MAJOR.MINOR.PATCH` version numbers, where breaking changes bump `MAJOR`, additive changes bump `MINOR`, and bugfixes bump `PATCH`. Pre-1.0 (`0.x.y`) versions carry the standard caveat that minor bumps may include breaking changes.

## CLI — Command-Line Interface

The set of subcommands, flags, and arguments a binary exposes. Distinct from internal APIs: a project's CLI is a *user-facing* contract and gets versioned accordingly.

## Status (decision / spike / plan)

A line near the top of a decision, spike, or plan that names its lifecycle state. It's a claim about the code, so verify it before setting it. Decision statuses: `Proposed` → `Accepted (YYYY-MM-DD)` or `Accepted (partial) (YYYY-MM-DD)` → `Superseded by Decision NNNN (YYYY-MM-DD)` or `Withdrawn (YYYY-MM-DD)`. Plan statuses: `Proposed` → `Active` → `Implemented (YYYY-MM-DD)`, plus `Deferred` and `Withdrawn (YYYY-MM-DD)`. Spike statuses: `Open` → `Resolved (YYYY-MM-DD) — <one-line outcome>`.

## Migration table

The table inside [the handoff chapter](handoffs.md) (and in `docs/handoff-discipline.md` in adopting projects) mapping each kind of handoff content to its destination home. The single most important reference for resolving a handoff.
