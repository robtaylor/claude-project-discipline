# Overview: four memory horizons

A project carries four kinds of memory. Each has a different lifetime, a different audience, and a different failure mode if it ends up in the wrong place.

| Memory kind | Lifetime | Lives in | Failure mode if mis-stored |
|---|---|---|---|
| **Decision** ("why we chose X") | Forever | `docs/adr/NNNN-*.md` (Architecture Decision Records, ADRs) | Buried in commit messages or chat history; future contributors re-litigate |
| **Plan** ("what's next, in what order") | Long-lived; updated in place | `docs/plans/<topic>.md` | Scattered across TODOs, draft Pull Requests (PRs), latest handoff — nobody knows the truth |
| **Spike** ("did this idea work?") | Forever, marked Resolved | `docs/spikes/<topic>.md` | Quietly forgotten; ideas re-attempted years later |
| **Handoff** ("what's in flight RIGHT NOW") | Ephemeral — folded then deleted | `docs/handoffs/<topic>-handoff.md` | Survives past resolution; "STATUS: RESOLVED" piles up; new contributors mistake it for current |

The term **Architecture Decision Record (ADR)** comes from [Michael Nygard's 2011 post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions); the format used in this discipline is a lightly evolved descendant. Used throughout this book, "ADR" always refers to a numbered file in `docs/adr/`.

Plus three supporting kinds that already have well-established homes:

| Memory kind | Lives in |
|---|---|
| **How something works** ("design") | Free-form `docs/<topic>.md` |
| **What shipped, when** | `CHANGELOG.md` + git tags |
| **Working source of truth on code shape** | The code itself |

## The migration pattern

The discipline lives or dies by one rule:

> Every load-bearing piece of a handoff migrates into its proper home (ADR / plan / spike / design doc / `CHANGELOG`) **before** the handoff file is deleted.

This forces every handoff to ask the question "where does this *actually* belong?" at resolution time. The answer is almost always one of the other four kinds. The handoff was just the temporary workspace.

## Why the strict separation

**Decisions go stale slowly; plans go stale fast; handoffs go stale instantly.** Mixing them creates a class of bug where a doc says one thing and the code says another, and the only way to know which is current is by reading commit dates.

By giving each kind its own directory and lifetime rule, you can answer "is this still true?" by looking at the *kind*, not by reading the contents.

| You're asking… | Look at… | Confidence in currency |
|---|---|---|
| "Why does the system work this way?" | The relevant ADR | High — ADRs are amended in place |
| "What's the project doing this quarter?" | The active plan doc | High — plans are kept current |
| "Did anyone try X already?" | `docs/spikes/` | High — spikes are immortal but resolved |
| "What's the next concrete action?" | The single live handoff in `docs/handoffs/` | High — there's only ever one |

If `docs/handoffs/` has more than one file, the discipline has been broken. That's the smell test.

## Concrete shape on disk

```
your-project/
├── CLAUDE.md                          ← project conventions, points at this discipline
├── CHANGELOG.md
├── docs/
│   ├── adr/
│   │   ├── README.md                  ← ADR conventions
│   │   ├── 0001-some-decision.md
│   │   ├── 0002-another-decision.md
│   │   └── ...
│   ├── plans/
│   │   ├── phase-0-foo.md
│   │   ├── phase-1-bar-roadmap.md
│   │   └── ...
│   ├── spikes/
│   │   ├── opentimer-sky130.md
│   │   └── ...
│   ├── handoffs/
│   │   └── current-work-handoff.md    ← exactly zero or one file at a time
│   ├── handoff-discipline.md          ← copy of the migration rule
│   ├── release-process.md             ← optional: how releases get cut
│   └── <design docs>.md               ← architecture, subsystem walkthroughs, etc.
└── ...
```

The next chapters cover each kind in detail.
