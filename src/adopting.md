# Adopting this in a new project

Three steps. Five minutes if your project is fresh; longer for an existing project where you'll need to backfill a few Architecture Decision Records (ADRs).

## Step 1 — Drop in the templates

```sh
# from this repo's root
cp -r starter/docs/* /path/to/your-project/docs/
```

That gives your project:

```
docs/
├── adr/
│   ├── README.md          ← ADR conventions + index
│   └── 0000-template.md   ← copy this for each new ADR
├── plans/
│   └── _template.md
├── spikes/
│   └── _template.md
├── handoffs/
│   └── _template.md
├── handoff-discipline.md  ← the migration rule, in full
└── release-process.md     ← optional companion
```

The empty directories (`adr/`, `plans/`, `spikes/`, `handoffs/`) signal intent. Even if they're empty for a while, the structure is there.

## Step 2 — Append the CLAUDE.md snippet

```sh
cat starter/CLAUDE.md.snippet >> /path/to/your-project/CLAUDE.md
```

This adds a section to your project's `CLAUDE.md` that:

- Points Claude at `docs/handoff-discipline.md` for the migration rule.
- Overrides the default `thoughts/shared/handoffs/` location used by some Claude Code skill toolkits.
- Lists the three "where does X go?" rules so Claude doesn't have to re-derive them.

If your project doesn't have a `CLAUDE.md` yet, the snippet works as a complete starter.

## Step 3 — Backfill (existing projects only)

If you're adopting this on a project that already has months of decisions baked into the code:

1. **Skim recent commits and PRs** for "we decided to …" / "we chose …" rationales. Each becomes a candidate ADR.
2. **Don't try to backfill everything.** Backfill only the decisions that are *currently* load-bearing — the ones a new contributor needs to know.
3. **Backdate the `Status:` line** when you do backfill: `Accepted (2025-08-15, retroactive)`. Be honest about the retro nature.
4. **Write the first plan doc** capturing what's actually in flight right now. Often this is just promoting the team's existing tracking into a doc.

A reasonable backfill is **3–5 ADRs and 1 plan doc.** If you find yourself writing 30 ADRs, you're treating ADRs as documentation rather than load-bearing decisions.

## Optional — wire up a docs site

If you want the docs rendered as a navigable site (not just files in `docs/`), the simplest path is mdBook (matches how this very repo is built):

```sh
cd /path/to/your-project
cargo install mdbook              # or: brew install mdbook
mdbook init --title "<Project>"   # creates book.toml + src/
```

Then move (or symlink) `docs/` content under mdBook's `src/`, write a `SUMMARY.md`, and you're done. See this repo's [`book.toml`](https://github.com/robtaylor/claude-project-discipline/blob/main/book.toml) and [`src/SUMMARY.md`](https://github.com/robtaylor/claude-project-discipline/blob/main/src/SUMMARY.md) for a working example.

For projects that prefer Python-flavoured tooling, [MkDocs](https://www.mkdocs.org/) (with the Material theme) is an equally good choice and renders the same content with no changes.

## What "good adoption" looks like a month later

- 2–8 ADRs in `docs/adr/`, each with a clear Status line. At least one Superseded by a later ADR or by a spike.
- 1–3 plan docs in `docs/plans/`. The active one updated in place; older ones with `Status: Closed`.
- A handful of resolved spikes in `docs/spikes/`. Each Resolved with a one-line outcome.
- `docs/handoffs/` has either zero files (clean stopping point) or one file (work in flight).
- `git log -- docs/handoffs/` shows a clean rhythm of one-add-one-delete commits.

## What "bad adoption" looks like

- `docs/handoffs/` has 4+ files, each with `STATUS: RESOLVED` banners. → The fold-then-delete rule isn't being followed.
- Every commit gets a new ADR. → ADRs are being written for trivial decisions.
- Plans are written once and never updated. → Plans are being treated as ADRs.
- ADRs include "step 1: do X, step 2: do Y" implementation steps. → ADRs are being treated as plans.

If you see these patterns, re-read the [Overview](overview.md) and the migration table in [Handoff documents](handoffs.md). The four kinds want to bleed into each other; the discipline is the dam.
