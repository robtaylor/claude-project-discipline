# Plan documents

Plan documents schedule the work an Architecture Decision Record (ADR) or a set of ADRs has committed to. They answer the question "*what's next, in what order?*" — and they answer it durably, in a place that doesn't rot the way a `TODO` list or a draft Pull Request (PR) description does.

## What a plan is

A plan doc is a **scheduling doc**, not a design doc. The design lives in ADRs and in free-form `docs/<subsystem>.md` design docs. The plan organises the implementation of those decisions into:

- **Phases** with entry and exit criteria
- **Workstreams** (often abbreviated *WS* with a numeric or alphabetic suffix, e.g. `WS1`, `WS-P1.1`) that can sometimes run in parallel
- A **status section** that's updated in place as work lands

The shape varies. A small project might have a single `docs/plans/roadmap.md`. A larger one accumulates per-phase plans and a top-level roadmap that orders them.

## What a plan is *not*

- **Not an ADR.** "We chose X over Y because Z" → an ADR. The plan *consumes* that decision and slices it into work.
- **Not a handoff.** "What needs to happen tomorrow morning, with verification commands" → a handoff. The plan is the *persistent* layer the handoff folds into at resolution.
- **Not a design doc.** "How the X subsystem works internally" → a design doc. The plan refers to the design doc; it doesn't reproduce it.

## Anatomy of a good plan

Plans tend to settle into this shape:

```markdown
# Plan — <Phase / topic>: <one-line goal>

**Status:** <Proposed | Active | Closed>. <Latest dated update.>

## Goal

What this phase / topic delivers, in 1–3 sentences.

## Prerequisites

What must be true / accepted / merged before this can start. ADRs
that need to be Accepted, fixtures that need to be in place.

## Where things stand (YYYY-MM-DD)

The single most-recent status snapshot. Updated in place.
Past states are in `git log`, not stacked here.

## Workstreams

### WS1 — <Name>

**Status:** <In flight | Shipped commit `abc1234` | Blocked on X>

<Concrete scope. Reference ADRs and design docs; don't duplicate them.>

**Deliverables:**
- Specific artefacts: a binary, a schema, a CI gate, a test fixture.

**Exit criteria:**
- Verifiable conditions for declaring this workstream done.

### WS2 — <Name>

...

## Phase exit criteria

A short checklist of bullets. When all are true, the phase closes.
```

## Why entry/exit criteria matter

Plans without exit criteria become *forever* documents. Someone always thinks of one more thing to add. The exit criteria are the contract: when these are met, the phase closes and a new plan (or follow-up roadmap) takes over.

A useful pattern: the *next* plan's prerequisites and the *current* plan's exit criteria mirror each other. That makes the handoff between phases explicit.

## Workstream sizing

The right workstream size is **"a contributor can pick this up cold and start within an hour."** Anything larger and it's really a phase. Anything smaller and it's really a task that belongs in a handoff.

A workstream typically has:

- A short name (`WS-P1.1`, `WS2.4`, `WS-RH.1` — whatever scheme fits)
- 1–3 deliverables
- An exit criterion you can test for
- An effort estimate ("~2 days", "~1 week")

## Updating a plan

Plans are updated **in place** as work lands. A common pattern:

```markdown
### WS-P1.1 — Structured timing output

- **WS-P1.1.a — Symbolic violation messages.** **Shipped 2026-05-02 in commit `0432d9a`.** New `WordSymbolMap` ...
- **WS-P1.1.b — `--timing-report <path.json>`.** **Shipped 2026-05-02 in commit `58a7a04`.** ...
- **WS-P1.1.c — `--timing-summary` text output.** **Shipped 2026-05-02 in commit `44e70a0`.** ...
- **WS-P1.1.d — Per-DFF worst-slack ranking.** Partially shipped in `58a7a04`. Remaining: ...
```

The pattern: bold the status, name the commit, say what shipped. The plan becomes a readable history once enough of it is filled in.

## Scheduling vs. design split

A subtle but load-bearing rule: **plans schedule; ADRs decide.**

When you find yourself writing "we chose X over Y because Z" inside a plan, that paragraph belongs in an ADR. When you find yourself writing "the system works by …" inside a plan, that belongs in a design doc.

The plan should reference both — *"per ADR 0007, Pillar B Stage 3 lands only if measurement justifies it"* — without reproducing them.

## Multiple plans, one roadmap

Once a project has more than two or three active plans, add a `roadmap.md` that orders them. The roadmap doesn't replace the per-phase plans; it sequences them. See [Jacquard's `post-phase-0-roadmap.md`](https://github.com/ChipFlow/jacquard/blob/main/docs/plans/post-phase-0-roadmap.md) as a real example.

## Template

A copy-paste-ready plan template lives at [`starter/docs/plans/_template.md`](https://github.com/robtaylor/claude-project-discipline/blob/main/starter/docs/plans/_template.md).
