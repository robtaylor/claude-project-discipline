# FAQ

## Why five kinds of doc? Isn't that a lot?

The five kinds correspond to genuinely different lifetimes:

- **Living, rewritten as the code moves** (architecture reference)
- **Forever, immutable** (decision)
- **Forever, marked Resolved** (spike)
- **Long-lived, kept current, archived when done** (plan)
- **Ephemeral, deleted at resolution** (handoff)

Collapsing any pair leads to a class of bug. Reference + decision collapsed → records that mix *why* with *what the code does now*, and go stale the moment the code moves. Decision + plan collapsed → "decisions" that get rewritten as scope changes. Plan + handoff collapsed → can't tell what's committed from last week's brainstorm. Handoff + decision collapsed → handoffs survive forever and pile up.

The cost of five kinds is low, because each has a clear template and `doctool.py` checks the layout. The cost of fewer kinds is high: the ones that remain get overloaded.

## Why drop the term "ADR"?

"Architecture Decision Record" doesn't tell a newcomer what's inside, and enough people bounce off the acronym that it costs more than it buys. "Decision" says what the record is. The format is still Nygard's, and the numbers carry over unchanged.

## Why did decisions stop being amended in place?

Because amending was a workaround. When the decision record was the only doc, it had to carry current state, so it had to be edited whenever the code moved. The result mixed three tenses in one file. With an architecture reference to hold current state, the decision record can go back to being a plain record of a choice. See [Why not amend in place?](decisions.md#why-not-amend-in-place).

## Why mdBook over MkDocs / Docusaurus / VitePress?

No strong reason. mdBook is what this repo uses because (a) it's Rust-native and matches the Jacquard project the discipline was extracted from, (b) it has zero JavaScript and a fast build, and (c) the default theme is good enough out of the box. MkDocs (especially with the Material theme) is an equally fine choice and the underlying Markdown content needs no changes.

The discipline itself doesn't care. Plain `docs/` files in your repo, viewed on GitHub, work fine.

## What if my project genuinely doesn't have any non-obvious decisions yet?

Then don't write any decision records yet. The discipline doesn't require backfilling decisions that aren't there.

That said, "we deliberately chose *not* to use X" is itself worth a decision record. If your project's shape was influenced by an explicit choice — even a "we'll keep it simple and not bring in framework Y" — write that down.

## How do I handle a decision that was made before this discipline was adopted?

Backfill a decision record with `Status: Accepted (YYYY-MM-DD, retroactive)`. Be honest about the retroactive nature. Don't invent commitments that weren't actually made; just record what's currently true.

## Can a handoff reference a previous handoff?

Yes, in the `## References` section. But it's a smell — handoffs aren't supposed to chain. If you find yourself referencing a previous handoff, ask whether the previous one's content should have been folded into a plan or decision instead of carried forward.

## What if the next session needs context from three previous handoffs?

That context belongs in the plan doc, not in a chain of handoffs. Migrate it.

## How many handoffs is too many?

One per active thread is normal. Past roughly twice the number of people actively working, you have more threads open than anyone can hold context on. `doctool.py lint --people N` warns at that point. Resolve or drop threads rather than opening more.

## Do I need a `release-process.md`?

Only if your project produces releases (libraries, binaries, services with versions consumers can pin against). For internal services with continuous deployment, you probably don't.

## Does the same person who creates a handoff have to resolve it?

No. The whole point of the handoff template is that it captures enough context for someone else (Claude, a colleague, future-you) to pick up cold. The verification command at the top is the safety net — it confirms the handoff's claimed state matches reality before the new session starts work.

## Does this work for non-software projects?

Probably. The five kinds (reference, decision, spike, plan, handoff) are general enough. The templates would need light adjustment (verification commands wouldn't be `cargo test`). If you try it for, say, a writing project or a research project, file an issue with what worked and what didn't.

## What's the relationship between this and the [arc42](https://arc42.org/) / [diátaxis](https://diataxis.fr/) / [C4](https://c4model.com/) / RFC frameworks?

Adjacent but different scopes:

- **arc42** is a software architecture *documentation* template. It would fit inside this as the structure of your area docs. It doesn't address the lifecycle question.
- **Diátaxis** classifies documentation into tutorials, how-tos, references, and explanations. This discipline borrows its reference/explanation split directly: the architecture reference is Diátaxis *reference*, and the decision log is *explanation*. Tutorials and how-tos sit alongside as ordinary guides.
- **C4 model** describes diagram conventions for software architecture. Orthogonal; use C4 inside your area docs if you want.
- **IETF RFCs** are similar in spirit to decision records but for cross-team standards. A decision record is an RFC scoped to a single project.

Nothing here conflicts with any of those; they fill in different parts of the documentation surface area.

## Is this proprietary to Claude Code?

No. The discipline is plain-Markdown, plain-`git`, and tool-agnostic. The `CLAUDE.md` snippet is Claude-specific because Claude Code happens to read that file by convention; an analogous snippet for any other AI coding assistant (or none at all) would work equally well. The core convention is older than AI coding assistants.
