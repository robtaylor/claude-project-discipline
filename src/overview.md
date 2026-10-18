# Overview: five kinds of document

A project carries five kinds of document. Each has a different lifetime, a different tense, and a different failure mode if it ends up in the wrong place.

| Kind | Answers | Lifetime | Lives in | Failure mode if mis-stored |
|---|---|---|---|---|
| **Architecture reference** | "What does the code do now?" | Living; edited in place as the code moves | `docs/architecture/<area>.md` | Current state scattered across decision records; readers build on stale claims |
| **Decision** | "Why did we choose X?" | Forever; immutable; archived when superseded | `docs/architecture/decisions/NNNN-*.md` | Buried in commit messages or chat history; future contributors re-litigate |
| **Spike** | "Did this idea work?" | Forever, marked Resolved | `docs/architecture/decisions/spikes/<topic>.md` | Quietly forgotten; ideas re-attempted years later |
| **Plan** | "What's next, in what order?" | Long-lived; updated in place; archived when finished | `docs/plans/<topic>.md` | Scattered across TODOs, draft Pull Requests (PRs), the latest handoff; nobody knows the truth |
| **Handoff** | "What's in flight right now?" | Ephemeral; folded, then deleted | `docs/handoffs/<topic>-handoff.md` | Survives past resolution; "STATUS: RESOLVED" piles up; new contributors mistake it for current |

Spikes sit under `decisions/` because a spike is the evidence a decision rested on. A decision cites its spike; the spike is a dated record that doesn't get rewritten.

Two supporting homes already exist in most projects:

| Kind | Lives in |
|---|---|
| **What shipped, when** | `CHANGELOG.md` + git tags |
| **How-to guides and user docs** | Free-form `docs/<topic>.md` |

## The migration pattern

The discipline lives or dies by one rule:

> Every load-bearing piece of a handoff migrates into its proper home (area doc / decision / spike / plan / `CHANGELOG`) **before** the handoff file is deleted.

This forces every handoff to ask "where does this *actually* belong?" at resolution time. The answer is almost always one of the other kinds. The handoff was just the temporary workspace.

## Why the strict separation

**Decisions never go stale, because they're history. The reference goes stale whenever the code moves, so it's kept current. Plans go stale fast. Handoffs go stale instantly.** Mixing them creates a class of bug where a doc says one thing and the code says another, and the only way to know which is current is by reading commit dates.

By giving each kind its own directory and lifetime rule, you can answer "is this still true?" by looking at the *kind*, not by reading the contents.

| You're asking… | Look at… | Why you can trust it |
|---|---|---|
| "How does X work today?" | The area doc in `docs/architecture/` | It's edited whenever the code moves |
| "Why does X work this way?" | The decision it links to | It's a record of the choice, and records don't change |
| "Did anyone try Y already?" | `docs/architecture/decisions/spikes/` | Spikes are kept forever and marked Resolved |
| "What's the project doing this quarter?" | The active plans in `docs/plans/` | Plans are kept current; finished ones move to `archive/` |
| "What's the next concrete action on thread Z?" | `docs/handoffs/z-handoff.md` | One live handoff per thread, deleted when resolved |

If `docs/handoffs/` holds more than about **2× as many files as there are people actively working**, the team is running more threads than it can hold context on. That's the smell test.

## Concrete shape on disk

```
your-project/
├── CLAUDE.md                          ← project conventions, points at this discipline
├── CHANGELOG.md
├── docs/
│   ├── architecture/
│   │   ├── README.md                  ← the map: area → reference doc → decisions
│   │   ├── <area>.md                  ← one per area, present tense
│   │   └── decisions/
│   │       ├── README.md              ← decision conventions + index
│   │       ├── 0001-some-decision.md
│   │       ├── 0002-another-decision.md
│   │       ├── archive/               ← superseded and withdrawn decisions
│   │       └── spikes/
│   │           └── <topic>.md
│   ├── plans/
│   │   ├── <active-plan>.md
│   │   └── archive/                   ← finished plans
│   ├── handoffs/
│   │   └── <topic>-handoff.md         ← one per active thread of work
│   ├── scripts/
│   │   └── doctool.py                 ← archive / lint / new: keeps the layout honest
│   ├── handoff-discipline.md          ← the migration rule, in full
│   ├── prose-style.md                 ← optional: house writing style
│   ├── release-process.md             ← optional: how releases get cut
│   └── <guides>.md                    ← how-tos, user docs
└── ...
```

The next chapters cover each kind in detail.
