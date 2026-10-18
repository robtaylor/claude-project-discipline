# Claude Project Discipline

A lightweight docs discipline for software projects. It keeps current state, decisions, and forward-looking work tidy across long-running collaborations between humans and Claude Code.

📖 **Read the book:** <https://robtaylor.github.io/claude-project-discipline/>

## What this is

Five kinds of document, each with a clear home and a clear lifecycle:

| Doc kind | Lives in | Lifetime | Answers |
|---|---|---|---|
| **Architecture reference** | `docs/architecture/<area>.md` | Living; edited in place as the code moves | *What* does the code do now? |
| **Decision** | `docs/architecture/decisions/NNNN-*.md` | Forever; immutable; superseded ones move to `archive/` | *Why* did we choose this? |
| **Spike** | `docs/architecture/decisions/spikes/<topic>.md` | Forever, marked Resolved | *Did this idea work?* |
| **Plan** | `docs/plans/<topic>.md` | Updated as work lands; finished ones move to `archive/` | *What's next, in what order?* |
| **Handoff** | `docs/handoffs/<topic>-handoff.md` | Ephemeral; one per active thread; folded into the others, then deleted | *What's in flight right now?* |

Decision records descend from the Architecture Decision Record (ADR) in [Michael Nygard's 2011 post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions), and keep his rule: a decision is a past-tense record of a choice, never rewritten. Current state lives in the architecture reference instead, which is what lets decisions stay immutable without going stale.

The discipline's load-bearing rule: **information has exactly one home, and the handoff is the only doc that gets deleted.** Everything that survives a session migrates from the handoff into an area doc / decision / spike / plan / `CHANGELOG.md` *before* the handoff file is removed.

## Why this exists

Projects accumulate four kinds of rot when there's no discipline:

1. **Decision rationale lost in chat history.** "Why did we go with X?" gets answered by re-reading commits and old conversations.
2. **Docs that describe a system that no longer exists.** Rationale and current state share a file, the code moves, and nobody can tell which sentences are still true.
3. **Forward-looking work scattered across stale TODO files, draft PRs, and "the latest handoff".** Nobody knows what's actually in flight.
4. **Handoff files that survive past their resolution.** "STATUS: RESOLVED" banners pile up; new contributors wade through history that no longer reflects reality.

The discipline closes the gap by giving each kind of content a stable home with its own tense and lifetime, and forcing handoffs to migrate-then-delete.

## Adopting this in a new project

```sh
# 1. Copy the starter templates into your project
cp -r starter/docs/* /path/to/your-project/docs/
cp -n starter/CHANGELOG.md /path/to/your-project/

# 2. Append the CLAUDE.md snippet to your project's CLAUDE.md
cat starter/CLAUDE.md.snippet >> /path/to/your-project/CLAUDE.md

# 3. Open your-project/CLAUDE.md and adjust the placeholders

# 4. Check the layout
cd /path/to/your-project && uv run docs/scripts/doctool.py lint
```

The discipline is prose, templates, and a habit. The one optional tool, `docs/scripts/doctool.py` (stdlib Python), lints the layout, archives finished plans and superseded decisions with every link repointed, and creates new docs from their templates. The skill activations (`create_handoff`, `resume_handoff`) from various Claude Code toolkits work *with* this convention if you point them at `docs/handoffs/`.

See [Adopting this](src/adopting.md) for a walk-through, including how to migrate a project from the older `docs/adr/` layout.

## Building the book locally

```sh
mdbook serve --open    # live preview at localhost:3000
mdbook build           # static site under book/
```

[`mdbook`](https://rust-lang.github.io/mdBook/) install: `cargo install mdbook` or `brew install mdbook`.

## Testing the tool

```sh
uv run --with pytest pytest tests/
```

## Origin

Extracted from the conventions used in [Jacquard](https://github.com/ChipFlow/jacquard) (a GPU-accelerated RTL simulator). The discipline emerged organically across several months of human-and-Claude collaboration; this repo captures it as a reusable starting point.

## License

Apache-2.0. Templates and prose are MIT-spirit — copy, adapt, fork freely.
