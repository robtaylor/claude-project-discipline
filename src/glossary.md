# Glossary

Terms and acronyms used throughout this book.

## ADR — Architecture Decision Record

A short, numbered markdown file capturing a non-obvious design choice and the rationale behind it. Lives at `docs/adr/NNNN-<short-name>.md`. Never deleted; amended in place when scope expands; superseded (with the old one preserved) when replaced.

The term and the basic three-section structure (Context / Decision / Consequences) come from [Michael Nygard's 2011 post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions). The discipline in this book extends that with an explicit Status lifecycle and amendment rules.

See: [Architecture Decision Records](adr.md).

## Plan doc

A scheduling document at `docs/plans/<topic>.md` that orders the work an ADR (or set of ADRs) has committed to. Organised into phases and workstreams with explicit entry/exit criteria. Updated in place as work lands.

See: [Plan documents](plans.md).

## Spike

A time-boxed experiment, written up at `docs/spikes/<topic>.md`, that answers a single binary question — "did this approach work?" — before the project commits to it. The term comes from XP / agile usage. Resolved with a clear yes/no/partial outcome and kept forever as the historical answer.

See: [Spike documents](spikes.md).

## Handoff

An ephemeral working-memory document at `docs/handoffs/<topic>-handoff.md` that bridges a single session boundary. **Folded into ADRs / plans / spikes / design docs at resolution and then deleted in the same commit as the migration.** Exactly one handoff exists at a time.

See: [Handoff documents](handoffs.md).

## Workstream (WS)

A unit of scoped work within a plan doc, typically named with a numeric or alphabetic suffix (`WS1`, `WS-P1.1`, `WS-RH.2`). Sized roughly so a contributor can pick it up cold and start within an hour. Each workstream has 1–3 deliverables and an exit criterion.

## Phase

A coarse-grained grouping of workstreams within a plan, with explicit entry and exit criteria. A plan typically has one or more phases; phases close when their exit criteria are met.

## Fold-then-delete

The migration rule for handoffs: every load-bearing piece of a handoff must be migrated to its proper home (ADR / plan / spike / design doc / `CHANGELOG.md`) **before** the handoff file is `git rm`'d. The migration and deletion go in the same commit so the audit trail is intact.

## Walk-back

A section in an ADR that names the conditions under which the decision should be revisited, and how to revisit it cheaply. Distinct from a spike: walk-backs are *predictions* about future re-evaluation; spikes are *experiments* run before committing.

## CI — Continuous Integration

The automated build/test pipeline that runs on every push or pull request. Used in the release process as a gating signal ("don't release if CI is red").

## PR — Pull Request

A proposed change to a repository, reviewed before merge. Used loosely throughout this book to mean "a unit of reviewed change," regardless of platform (GitHub PR, GitLab MR, Gerrit changeset, etc.).

## SemVer — Semantic Versioning

The [SemVer 2.0.0 spec](https://semver.org/) for `MAJOR.MINOR.PATCH` version numbers, where breaking changes bump `MAJOR`, additive changes bump `MINOR`, and bugfixes bump `PATCH`. Pre-1.0 (`0.x.y`) versions carry the standard caveat that minor bumps may include breaking changes.

## CLI — Command-Line Interface

The set of subcommands, flags, and arguments a binary exposes. Distinct from internal APIs: a project's CLI is a *user-facing* contract and gets versioned accordingly.

## Status (ADR / spike)

A line near the top of an ADR or spike file that names its lifecycle state. ADR statuses: `Proposed` → `Accepted (YYYY-MM-DD)` → `Superseded by ADR NNNN (YYYY-MM-DD)` or `Withdrawn (YYYY-MM-DD)`. Spike statuses: `Open` → `Resolved (YYYY-MM-DD) — <one-line outcome>`.

## Migration table

The table inside [the handoff chapter](handoffs.md) (and in `docs/handoff-discipline.md` in adopting projects) mapping each kind of handoff content to its destination home. The single most important reference for resolving a handoff.
