# Introduction

This is a small, opinionated convention for how a software project keeps track of:

- **Why** non-obvious choices were made
- **What's next** and in what order
- **What's been tried** that didn't pan out
- **What's in flight right now** that someone else (or future-you) needs to pick up

Four document kinds, four homes, one inviolable rule: **every load-bearing piece of information has exactly one canonical home, and only one of the four — the handoff — gets deleted.**

## Who this is for

- **Solo developers using Claude Code** who want their project to stay coherent across many sessions, without context drift, without re-discovering decisions, and without scrolling back through transcripts.
- **Small teams** who want a low-overhead alternative to Notion / Confluence / Linear sprawl. Markdown in `docs/`, version-controlled, reviewable in PRs.
- **Maintainers of long-running projects** who've felt the pain of "what was the rationale for X?" being unanswerable.

## What this isn't

- **Not a project management framework.** No tickets, no statuses, no burn-downs.
- **Not a documentation site generator.** It is rendered as one (mdBook), but the discipline is fundamentally a habit, not a tool.
- **Not specific to Claude Code.** Claude Code happens to be where this discipline crystallised, and there are tooling integrations described later, but a human team using only `git` and `vim` could follow this verbatim.

## How to read this book

1. Read [Overview: four memory horizons](overview.md) first — it sketches the whole shape in one page.
2. Read [Handoff documents](handoffs.md) — this is the most distinctive part of the discipline and the most easily abused without it.
3. Skim the per-kind chapters ([ADRs](adr.md), [plans](plans.md), [spikes](spikes.md)) as you need them.
4. Use [Adopting this in a new project](adopting.md) as the actionable checklist.

## A note on style

These docs are short on purpose. Every word is load-bearing. If a sentence reads as filler, file an issue or a PR — it's a bug.
