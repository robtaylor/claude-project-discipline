# Introduction

This is a small, opinionated convention for how a software project keeps track of:

- **What** the code does today, area by area
- **Why** non-obvious choices were made
- **What's next** and in what order
- **What's been tried** that didn't pan out
- **What's in flight right now** that someone else (or future-you) needs to pick up

Five document kinds, five homes, one inviolable rule: **every load-bearing piece of information has exactly one canonical home, and only the handoff gets deleted.** Finished plans and superseded decisions move to an `archive/` directory. Nothing else leaves the repo.

## Who this is for

- **Solo developers using Claude Code** who want their project to stay coherent across many sessions, without context drift, without re-discovering decisions, and without scrolling back through transcripts.
- **Small teams** who want a low-overhead alternative to Notion / Confluence / Linear sprawl. Markdown in `docs/`, version-controlled, reviewable in PRs.
- **Maintainers of long-running projects** who've felt the pain of "what was the rationale for X?" being unanswerable.

## What this isn't

- **Not a project management framework.** No tickets, no statuses, no burn-downs.
- **Not a documentation site generator.** It is rendered as one (mdBook), but the discipline is fundamentally a habit, not a tool.
- **Not specific to Claude Code.** Claude Code happens to be where this discipline crystallised, and there are tooling integrations described later, but a human team using only `git` and `vim` could follow this verbatim.

## How to read this book

1. Read [Overview: five kinds of document](overview.md) first. It sketches the whole shape in one page.
2. Read [Architecture reference](architecture.md) and [Decision records](decisions.md) together. The split between *what the code does now* and *why it got that way* is the spine of the discipline.
3. Read [Handoff documents](handoffs.md). It's the most distinctive part of the discipline and the most easily abused.
4. Skim [spikes](spikes.md) and [plans](plans.md) as you need them.
5. Use [Adopting this in a new project](adopting.md) as the actionable checklist.

## A note on style

These docs are short on purpose. Every word is load-bearing. If a sentence reads as filler, file an issue or a PR — it's a bug.
