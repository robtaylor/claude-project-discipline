# Adopting this in a new project

Three steps. Five minutes if your project is fresh. Longer for an existing project, where you'll backfill a few decision records and write the first area docs.

## Step 1 — Drop in the templates

```sh
# from this repo's root
cp -r starter/docs/* /path/to/your-project/docs/
cp -n starter/CHANGELOG.md /path/to/your-project/   # skip if you already have one
```

That gives your project:

```
docs/
├── architecture/
│   ├── README.md              ← the map: area → reference doc → decisions
│   ├── _template.md           ← copy for each area doc
│   └── decisions/
│       ├── README.md          ← decision conventions + index
│       ├── 0000-template.md   ← copy for each new decision
│       ├── archive/           ← superseded and withdrawn decisions
│       └── spikes/
│           └── _template.md
├── plans/
│   ├── _template.md
│   └── archive/               ← finished plans
├── handoffs/
│   └── _template.md
├── scripts/
│   └── doctool.py             ← lint / archive / new
├── handoff-discipline.md      ← the migration rule, in full
├── prose-style.md             ← house writing style
└── release-process.md         ← optional companion
```

The empty directories signal intent. Even if they stay empty for a while, the structure is there.

## Step 2 — Append the CLAUDE.md snippet

```sh
cat starter/CLAUDE.md.snippet >> /path/to/your-project/CLAUDE.md
```

This adds a section to your project's `CLAUDE.md` that:

- Tells Claude where each kind of doc lives, and that the architecture map is the entry point.
- States the immutable-decision rule, so Claude edits area docs instead of rewriting decisions.
- Points Claude at `doctool.py` for linting, archiving, and creating docs.
- Overrides the default `thoughts/shared/handoffs/` location used by some Claude Code skill toolkits.

If your project doesn't have a `CLAUDE.md` yet, the snippet works as a complete starter.

## Step 3 — Backfill (existing projects only)

If you're adopting this on a project that already has months of decisions baked into the code:

1. **Pick the areas.** Three to eight parts of the system a contributor could own. Add a row per area to `docs/architecture/README.md`.
2. **Write one area doc first**, for the area people ask about most. Describe what the code does today, with file references. Check every sentence against the code.
3. **Skim recent commits and PRs** for "we decided to …" / "we chose …" rationales. Each one is a candidate decision record. Backfill only the decisions that are *currently* load-bearing: the ones a new contributor needs to know.
4. **Backdate the `Status:` line** when you backfill: `Accepted (2025-08-15, retroactive)`. Be honest about it being retroactive.
5. **Write the first plan doc** capturing what's actually in flight right now.

A reasonable backfill is **one or two area docs, 3–5 decisions, and 1 plan doc.** If you find yourself writing 30 decisions, you're treating them as documentation rather than load-bearing choices. That content probably belongs in an area doc.

## Migrating from the `docs/adr/` layout

Earlier versions of this discipline used `docs/adr/` and `docs/spikes/`, with records amended in place. To move a project onto the current layout:

1. **Move the files.** `git mv docs/adr/*.md docs/architecture/decisions/`, and `git mv docs/spikes/* docs/architecture/decisions/spikes/`. Keep the four-digit numbers; they're stable IDs. Superseded records go to `decisions/archive/`.
2. **Repoint every reference.** Resolve each link *relative to its source file*. Blind search-and-replace misses the subtle case: a file that moved deeper also needs its links to files that *didn't* move re-depthed (`../plans/` becomes `../../plans/`). For single files later on, `doctool.py archive` does this for you.
3. **Rename the term.** `ADR NNNN` becomes `Decision NNNN` across docs, `CLAUDE.md`, CI config, and source comments.
4. **Write the area docs.** Move each decision's present-tense *current state* claims into the area doc for its part of the system, and add a `**Current architecture:**` forward-link to every active decision. This is the bulk of the work.
5. **Leave old Amendment blocks alone** unless they actively mislead. Stripping them from cited records is risky for a modest gain once the area docs carry current state. New changes follow the immutable rule.
6. **Run `uv run docs/scripts/doctool.py lint`** until it's clean, and build the book if you render one.

## Optional — wire up a docs site

If you want the docs rendered as a navigable site (not just files in `docs/`), the simplest path is mdBook (matches how this very repo is built):

```sh
cd /path/to/your-project
cargo install mdbook              # or: brew install mdbook
mdbook init --title "<Project>"   # creates book.toml + src/
```

Point `book.toml`'s `src` at `docs/`, write a `SUMMARY.md`, and you're done. A good nav order puts Architecture first (Overview → area docs → Decisions → Archive → Spikes), then active plans, then a "Completed plans" part for `plans/archive/`. See this repo's [`book.toml`](https://github.com/robtaylor/claude-project-discipline/blob/main/book.toml) and [`src/SUMMARY.md`](https://github.com/robtaylor/claude-project-discipline/blob/main/src/SUMMARY.md) for a working example.

For projects that prefer Python-flavoured tooling, [MkDocs](https://www.mkdocs.org/) (with the Material theme) is an equally good choice and renders the same content with no changes.

## Optional — lint in CI

```yaml
- uses: astral-sh/setup-uv@v6
- run: uv run docs/scripts/doctool.py lint
```

Add `--strict` once the warnings are cleared, so they can't creep back.

## What "good adoption" looks like a month later

- `docs/architecture/README.md` maps every area, and each area doc's present-tense claims match the code.
- 2–8 decision records, each with a clear Status line and a forward-link. At least one superseded and moved to `archive/`.
- 1–3 active plan docs, updated in place. Finished ones in `plans/archive/`.
- A handful of resolved spikes, each Resolved with a one-line outcome.
- `docs/handoffs/` holds about one file per active thread, and never more than ~2× the people working.
- `git log -- docs/handoffs/` shows a clean rhythm of one-add-one-delete commits.
- `doctool.py lint` is clean.

## What "bad adoption" looks like

- `docs/handoffs/` has stacks of files with `STATUS: RESOLVED` banners. → The fold-then-delete rule isn't being followed.
- Every commit gets a new decision record. → Decisions are being written for trivial choices.
- Decision records describe what the code does today. → Current state belongs in the area doc.
- Plans are written once and never updated. → Plans are being treated as decisions.
- Decision records include "step 1: do X, step 2: do Y". → Decisions are being treated as plans.

If you see these patterns, re-read the [Overview](overview.md) and the migration table in [Handoff documents](handoffs.md). The kinds want to bleed into each other; the discipline is the dam.
