# Claude Project Discipline

A lightweight four-document discipline for software projects, designed to keep working memory, decisions, and forward-looking work tidy across long-running collaborations between humans and Claude Code.

📖 **Read the book:** <https://robtaylor.github.io/claude-project-discipline/>

## What this is

Four kinds of project memory, each with a clear home and a clear lifecycle:

| Doc kind | Lives in | Lifetime | Answers |
|---|---|---|---|
| **Architecture Decision Record (ADR)** | `docs/adr/NNNN-*.md` | Forever (amended in place; never deleted) | *Why* did we choose this? |
| **Plan** | `docs/plans/<topic>.md` | Long-lived; updated as work lands | *What's next, in what order?* |
| **Spike** | `docs/spikes/<topic>.md` | Forever, marked Resolved | *Did this idea work?* |
| **Handoff** | `docs/handoffs/<topic>-handoff.md` | Ephemeral — folded into the others, then deleted | *What's in flight right now?* |

"ADR" comes from [Michael Nygard's 2011 post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions); the format here is a lightly evolved descendant.

The discipline's load-bearing rule: **information has exactly one home, and the handoff is the only doc that gets deleted.** Everything that survives a session migrates from the handoff into an ADR / plan / spike / design doc / `CHANGELOG.md` *before* the handoff file is removed.

## Why this exists

Projects accumulate three kinds of rot when there's no discipline:

1. **Decision rationale lost in chat history.** "Why did we go with X?" gets answered by re-reading commits and old conversations.
2. **Forward-looking work scattered across stale TODO files, draft PRs, and "the latest handoff".** Nobody knows what's actually in flight.
3. **Handoff files that survive past their resolution.** "STATUS: RESOLVED" banners pile up; new contributors wade through history that no longer reflects reality.

Four-document discipline closes the gap by giving each kind of content a stable home and forcing handoffs to migrate-then-delete.

## Adopting this in a new project

```sh
# 1. Copy the starter templates into your project
cp -r starter/docs/* /path/to/your-project/docs/

# 2. Append the CLAUDE.md snippet to your project's CLAUDE.md
cat starter/CLAUDE.md.snippet >> /path/to/your-project/CLAUDE.md

# 3. Open your-project/CLAUDE.md and adjust the placeholders
```

That's it. The discipline doesn't require any tooling — it's prose, templates, and a habit. The skill activations (`create_handoff`, `resume_handoff`) from various Claude Code toolkits work *with* this convention if you point them at `docs/handoffs/`.

See [Adopting this](src/adopting.md) for a walk-through.

## Building the book locally

```sh
mdbook serve --open    # live preview at localhost:3000
mdbook build           # static site under book/
```

[`mdbook`](https://rust-lang.github.io/mdBook/) install: `cargo install mdbook` or `brew install mdbook`.

## Origin

Extracted from the conventions used in [Jacquard](https://github.com/ChipFlow/jacquard) (a GPU-accelerated RTL simulator). The discipline emerged organically across several months of human-and-Claude collaboration; this repo captures it as a reusable starting point.

## License

Apache-2.0. Templates and prose are MIT-spirit — copy, adapt, fork freely.
