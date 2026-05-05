# Architecture Decision Records (ADRs)

An **Architecture Decision Record** ("ADR") is a short, numbered markdown file capturing **the *why* behind a non-obvious choice** so future contributors don't re-litigate it. The term and the basic structure (Context / Decision / Consequences) come from [Michael Nygard's 2011 post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions); the discipline here adds an explicit Status lifecycle, in-place amendments, and the rule that ADRs are never deleted.

## When to write one

Write an ADR whenever you make a non-trivial choice that future-you (or a future contributor, or a future Claude session) would want to understand the reasoning behind. Examples that qualify:

- Picking one tool / library / format over another
- Choosing a particular architectural boundary
- Adopting a multi-piece convention that spans several files
- Deciding *not* to do something obvious-looking

**Skip ADRs for:**

- Mechanical changes (renames, typo fixes, dependency bumps)
- Choices the code itself makes self-evident (a small refactor, a chosen variable name)
- Things adequately captured by a commit message

A useful test: *if someone asked "why is it like this?" six months from now, would the answer be in the code, the commit, or this ADR?* If the answer is "this ADR", write it.

## Format

Numbered (`0001-...md`, `0002-...md`), structured as:

```markdown
# ADR NNNN — Short title

**Status:** Accepted (YYYY-MM-DD).

## Context

What was the situation? What constraints forced a decision?
Be concrete — name the systems, the data formats, the friction.

## Decision

What we chose, with enough specificity to act on.
Numbered sub-points if multiple commitments.

## Consequences

What this buys us, what it costs us, and what would trigger a walk-back.
Be honest about the costs.

## Walk-back options

(Optional, but strongly encouraged.) Conditions under which this
decision should be revisited, and how to revisit it cheaply.

## Links

Cross-references to related files, design docs, related ADRs.
```

## Status lifecycle

ADRs go through these states:

- **Proposed** — written, under review.
- **Accepted (YYYY-MM-DD)** — agreed upon. The date matters.
- **Superseded by ADR NNNN (YYYY-MM-DD)** — replaced. The old ADR stays in place; the new one references it.
- **Withdrawn (YYYY-MM-DD)** — abandoned without replacement (rare).

When scope expands, **amend the `Status:` line in place** rather than silently rewriting the body:

```markdown
**Status:** Accepted (2026-05-05). Scope expanded 2026-09-01 — see Decision §3 below.
```

The amendment goes inline as a clearly-marked section near the top:

```markdown
## Amendment (2026-09-01)

The original Decision <X> turned out to be too restrictive given <Y>.
This amendment relaxes it as follows: ...

The original Context, Decision, and Walk-back sections below are
retained for historical record. Where they conflict with this
amendment, this amendment wins.
```

This pattern preserves the historical reasoning while making the current bright lines easy to find.

## Numbering and the index

Use sequential zero-padded numbers: `0001-foo.md`, `0002-bar.md`. Don't reuse numbers, don't renumber.

Maintain `docs/adr/README.md` as the index:

```markdown
| ADR  | Title                | Status                |
| ---- | -------------------- | --------------------- |
| 0001 | [OpenSTA as oracle](0001-opensta-as-oracle.md) | Accepted 2026-04-15 |
| 0002 | [Timing IR](0002-timing-ir.md) | Accepted 2026-04-20 |
| 0003 | [OpenTimer primary STA](0003-opentimer-primary-sta.md) | **Superseded** by spike (2026-05-01) |
```

## Never delete an ADR

If superseded, add a new ADR that references the old one and update the old one's `Status:` to `Superseded by ADR NNNN (YYYY-MM-DD)`. The old ADR stays in the repo. Future readers tracing the history of a decision need both.

This is uncomfortable when the old ADR is wrong; *that's the point*. Wrong-ADR-with-Superseded-marker is more useful than a clean repo with no record of the wrong turn.

## A worked example

The cleanest ADR sequence is one where ADR `M` proposes a path, a spike investigates, the spike fails, ADR `N` supersedes ADR `M`, and the supersession is recorded inline:

- ADR 0001: "Use external tool X as our oracle." Accepted.
- ADR 0003: "Add tool Y as our in-process reference." Accepted (proposed).
- Spike: time-boxed validation of Y on real workloads. **Resolved — Y unfit for our inputs.**
- ADR 0003 Status updated to: `Superseded by spike outcome (2026-05-01).`
- ADR 0001 amended: scope expanded — X is now both oracle *and* sole STA path. Inline `## Amendment` block records the rationale.

A reader chasing "why are we using X out of process?" reads ADR 0001's amendment and the spike, and gets the full story.

## Template

A copy-paste-ready template lives at [`starter/docs/adr/0000-template.md`](https://github.com/robtaylor/claude-project-discipline/blob/main/starter/docs/adr/0000-template.md) in this repo. Drop it into your project's `docs/adr/` and rename to the next available number.
