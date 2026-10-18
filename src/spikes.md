# Spike documents

A **spike** is a **time-boxed experiment with a binary outcome** ("did this idea work?"). It's written down before it's answered, resolved with a clear yes/no, and kept forever as the historical answer. The term comes from XP / agile usage and just means a short, sharp investigation. Here it's formalised into its own document kind so the question and the answer are findable later.

Spikes live at `docs/architecture/decisions/spikes/<topic>.md`, under the decision log, because a spike is the *evidence* a decision rested on. It's neither a *what* nor a *why*. It's the experiment.

Spikes pair naturally with [decision records](decisions.md). A Proposed decision names a direction, a spike tests the foundational assumption, and the outcome decides whether the decision is accepted as written or replaced by a new one. The decision cites the spike in its Links; the spike is never rewritten.

## When to write one

Write a spike when you're about to invest non-trivial effort in validating an assumption that the project's direction depends on. Examples:

- "Will library X parse our actual production inputs without re-engineering?"
- "Can we hit the throughput target on the available hardware?"
- "Does the proposed schema handle the edge cases we know about?"

The signal: **the answer determines whether a decision proceeds, gets superseded, or pivots.** If there's no decision (or Proposed decision) the spike informs, you might be doing exploratory research instead. That's fine, but it doesn't need a spike doc.

## Anatomy

```markdown
# Spike — <One-line question this spike answers>

**Status:** <Open | Resolved (YYYY-MM-DD) — <one-line outcome>>

**Time-box:** <e.g. "≤ 3 days; abort if Q1 hasn't passed by EOD day 1">

## Question

The single binary question this spike answers. If you find yourself
writing two questions, that's two spikes.

## Why this is in question

What we don't know, that we'd need to know to accept Decision NNNN
(or to replace it with a different decision).

## Approach

The plan for the time-box. Be specific:
- Q1 (sub-question 1, the cheapest first):
  - Step 1: <thing>
  - Step 2: <thing>
- Q2 (only attempted if Q1 passes):
  - ...

## Decision matrix

What we'll do under each outcome:

| Outcome | Means | Action |
|---|---|---|
| Q1 fails | Approach unworkable on our inputs | Spike resolves NO; Decision NNNN superseded and archived |
| Q1 passes, Q2 fails | Partially viable, but blocking gap | Spike resolves PARTIAL; new narrower decision supersedes NNNN |
| Both pass | Fully viable | Spike resolves YES; Decision NNNN accepted as written |

## Findings

(Filled in as the spike runs. Written terse — these are evidence, not narrative.)

## Outcome

(Single short paragraph at resolution. The conclusion sentence
becomes the Status line.)
```

## Time-boxing

A spike that runs longer than its box has lost the discipline. When the box expires:

- If the answer is clear → resolve.
- If the answer needs another N days → write that down, extend the box once, and proceed. Don't extend twice. If it needs that much investigation, it's no longer a spike. It's a research thread that probably needs its own plan.
- If you've gotten side-tracked → resolve as inconclusive, capture the side-track as a follow-up.

## Resolving a spike

A resolved spike is **never deleted** and doesn't move to an archive. The Status line gets updated and the Outcome section is filled in. The decision that follows from it (accepting the Proposed one, or a new one that supersedes it) cites the spike.

```markdown
**Status:** Resolved (2026-05-01) — Q2 fail; Decision 0003 superseded by 0004.
```

The spike file becomes a permanent part of the repo's "we tried this" record. Future contributors who find an archived decision follow its link to the spike to understand *why* it was dropped.

## Spike vs. walk-back

These look similar but serve different purposes:

- A decision's **walk-back** section is a *prediction*: "if X happens, we'd revisit." Written before the fact.
- A **spike** is an *experiment*: "we don't yet know if X works; here's how we'll find out." Written before the fact, *resolved* after.

A spike is cheap insurance against accepting a decision whose foundational assumption hasn't been tested.

## Template

A copy-paste-ready template lives at [`starter/docs/architecture/decisions/spikes/_template.md`](https://github.com/robtaylor/claude-project-discipline/blob/main/starter/docs/architecture/decisions/spikes/_template.md).
