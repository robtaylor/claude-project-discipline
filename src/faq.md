# FAQ

## Why four kinds of doc? Isn't that a lot?

The four kinds correspond to four genuinely different lifetimes:

- **Forever, immortal** (Architecture Decision Record, ADR)
- **Long-lived, kept current** (plan)
- **Forever, marked Resolved** (spike)
- **Ephemeral, deleted at resolution** (handoff)

Collapsing any pair leads to a class of bug. ADR + plan collapsed → "decisions" that get rewritten as scope changes. Plan + handoff collapsed → can't tell what's currently committed vs. what was just last week's brainstorm. Handoff + ADR collapsed → handoffs survive forever and pile up.

The cost of four kinds is low (each has a clear template). The cost of fewer kinds is high (the ones that remain become overloaded).

## Why mdBook over MkDocs / Docusaurus / VitePress?

No strong reason. mdBook is what this repo uses because (a) it's Rust-native and matches the Jacquard project the discipline was extracted from, (b) it has zero JavaScript and a fast build, and (c) the default theme is good enough out of the box. MkDocs (especially with the Material theme) is an equally fine choice and the underlying Markdown content needs no changes.

The discipline itself doesn't care. Plain `docs/` files in your repo, viewed on GitHub, work fine.

## What if my project genuinely doesn't have any non-obvious decisions yet?

Then don't write any ADRs yet. The discipline doesn't require backfilling decisions that aren't there.

That said, "we deliberately chose *not* to use X" is itself an ADR-worthy decision. If your project's shape was influenced by an explicit choice — even a "we'll keep it simple and not bring in framework Y" — write that down.

## How do I handle a decision that was made before this discipline was adopted?

Backfill an ADR with `Status: Accepted (YYYY-MM-DD, retroactive)`. Be honest about the retroactive nature. Don't invent commitments that weren't actually made; just record what's currently true.

## Can a handoff reference a previous handoff?

Yes, in the `## References` section. But it's a smell — handoffs aren't supposed to chain. If you find yourself referencing a previous handoff, ask whether the previous one's content should have been folded into a plan or ADR instead of carried forward.

## What if the next session needs context from three previous handoffs?

That context belongs in the plan doc, not in a chain of handoffs. Migrate it.

## Do I need a `release-process.md`?

Only if your project produces releases (libraries, binaries, services with versions consumers can pin against). For internal services with continuous deployment, you probably don't.

## Does the same person who creates a handoff have to resolve it?

No. The whole point of the handoff template is that it captures enough context for someone else (Claude, a colleague, future-you) to pick up cold. The verification command at the top is the safety net — it confirms the handoff's claimed state matches reality before the new session starts work.

## Does this work for non-software projects?

Probably. The four memory horizons (decision, plan, spike, handoff) are general enough. The templates would need light adjustment (verification commands wouldn't be `cargo test`). If you try it for, say, a writing project or a research project, file an issue with what worked and what didn't.

## What's the relationship between this and the [arc42](https://arc42.org/) / [diátaxis](https://diataxis.fr/) / [C4](https://c4model.com/) / RFC frameworks?

Adjacent but different scopes:

- **arc42** is a software architecture *documentation* template. It would fit alongside this as the structure of your `docs/<subsystem>.md` design docs. It doesn't address the lifecycle question.
- **Diátaxis** classifies user-facing documentation (tutorials, how-tos, references, explanations). This discipline is about *internal* project memory (decisions, plans, spikes, handoffs); the two are complementary.
- **C4 model** describes diagram conventions for software architecture. Orthogonal — use C4 inside your design docs if you want.
- **IETF RFCs** are similar in spirit to ADRs but for cross-team standards. ADRs are RFCs scoped to a single project.

Nothing here conflicts with any of those; they fill in different parts of the documentation surface area.

## Is this proprietary to Claude Code?

No. The discipline is plain-Markdown, plain-`git`, and tool-agnostic. The `CLAUDE.md` snippet is Claude-specific because Claude Code happens to read that file by convention; an analogous snippet for any other AI coding assistant (or none at all) would work equally well. The core convention is older than AI coding assistants.
