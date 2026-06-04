# Handoff documents

A **handoff** is an ephemeral working-memory document that bridges a single session boundary — when you stop working and someone else (Claude or human) picks up — and is deleted once the work it describes is resolved. The name is literal: it's what you hand to the next session.

This is the most distinctive part of the discipline, and the one most easily abused without it.

## Why this discipline exists

Decision rationale, technical context, and project state all already have natural homes:

- **Architecture Decision Records (ADRs)** capture architectural decisions and their *why*.
- **Design docs** capture *how* things work.
- **Plan docs** capture *what's left* and the next workstream slices.

When that content lives in a handoff instead, two things go wrong:

1. **It's not where contributors look.** A new contributor reading the README → ADR chain shouldn't have to dig through a stack of resolved handoff docs to find load-bearing decisions.
2. **It rots out of sync with reality.** Handoffs are point-in-time snapshots. A "STATUS: RESOLVED" banner doesn't help when the thing referenced has moved or changed; the canonical doc is what should hold the current truth.

The discipline closes this gap by **forcing migration before deletion**. Every load-bearing piece of a handoff lands in its proper home (ADR / plan / spike / design doc / `CHANGELOG`) before the handoff file is removed.

## What a handoff IS

A single markdown file at `docs/handoffs/<topic>-handoff.md` containing exactly what the next session needs to pick up where you left off:

- **Goal & next-up** — what this session was trying to do, and what the *very next* concrete action is.
- **Done this session** — commits landed, with one-line summaries.
- **Open follow-ups** — the work that wasn't done, with enough scope detail to start cold.
- **Critical context** — gotchas, surprising findings, environment specifics that aren't obvious from the code or docs *yet*.
- **Verification** — the command(s) the next session runs to confirm the work is in the state you say it is.

**Exactly one handoff exists at a time.** There's no chain of resolved predecessors to wade through. If you find yourself with two, that's the smell test failing.

## What a handoff IS NOT

- **Not a decision log.** Decisions go in ADRs. If you find yourself writing "we chose X over Y because Z" in a handoff, that paragraph belongs in an ADR (or an existing ADR's Consequences / Walk-back section).
- **Not a design doc.** "How subsystem A works" is a design topic; it lives in a free-form `docs/<topic>.md`, not in a handoff's "Critical context" section.
- **Not a status dashboard for the project.** Workstream status lives in plan docs. A handoff *cites* a plan; it doesn't reproduce one.
- **Not a historical record.** `git log` is the historical record. Handoffs that survive past their resolution turn into noise that misleads new contributors.

## When to write one

Write a handoff at the end of any session that:

1. **Leaves work in a partial state** that someone else might pick up cold.
2. **Captures non-obvious context** the next session needs (e.g. "the `find_timing` proc rejects `-full_update`; use `::sta::find_timing_cmd 1` directly").
3. **Documents the next concrete step** with enough scope to start without re-discovering it.

If the session ended at a clean stopping point (everything merged, all decisions documented in ADRs/plans, nothing surprising), **don't write a handoff.** The plan doc already says what's next.

## Before you hand off: sweep for undocumented decisions

A handoff is written at the moment your session context is richest and about to evaporate. That makes it the right checkpoint for one deliberate question:

> **Did I make any architectural decision this session that isn't yet captured in an ADR?**

Run the sweep *before* writing the handoff, not after. Walk the session's diffs and discussion for choices that pass the ADR test — *"if someone asked 'why is it like this?' six months from now, would the answer be in the code, the commit, or an ADR?"* For each one whose answer is "an ADR":

- **No ADR fits** → write a new one now, while the rationale and the alternatives you weighed are still in working memory.
- **An existing ADR covers the area but its scope grew** → amend it in place (Status-line note plus an inline `## Amendment` block).

Only *then* write the handoff. This keeps the decision out of the handoff's "Critical context" (where it doesn't belong) and puts it in its permanent home at the moment you can write it best.

Why at handoff time? Two failure modes this closes:

1. **Decisions captured nowhere.** Without the sweep, a choice made mid-session lives only in the chat transcript and the diff. The transcript is gone next session; the diff shows *what* changed, never *why this and not that*.
2. **Decisions smuggled into the handoff.** The tempting shortcut is to jot "we went with X because Y" into the handoff and move on. But the handoff is deleted at resolution — if the fold-and-delete step misses that paragraph, the rationale dies with the file. Writing the ADR up front means there's nothing to migrate later.

The sweep is cheap when decisions are fresh and expensive to reconstruct later. Treat "I'm about to open a handoff" as the trigger to do it.

## Resolution: fold, then delete

The two-location split is deliberate: handoffs *live* at `docs/handoffs/<topic>-handoff.md` while in flight; their *content* migrates into the persistent docs (`docs/adr/`, `docs/plans/`, design docs under `docs/`) at resolution. The handoff file then gets removed; nothing about the work is lost because everything load-bearing has a permanent home elsewhere.

When a handoff's work is done — whether in the next session or several sessions later — every load-bearing piece of it must be migrated **before the handoff file is deleted**:

| If the handoff says... | It belongs in... |
|---|---|
| "We chose approach X over Y because Z" | The relevant ADR's Decision/Consequences section, or a new ADR if no fit exists |
| "Future scope for WS-N: do A then B then C" | The plan doc's WS-N section |
| "Gotcha: tool Z's API X behaves Y" | A code comment near the call site, or a design doc if the gotcha cuts across files |
| "Build dep Z is required on Linux" | The build script's apt-suggestion / Brewfile / README install section |
| "Subsystem A doesn't yet do B" | Plan doc as a new open item, or an ADR-tracked walk-back if it's a deferred design choice |
| "Run `cargo test --feature foo` to verify" | The verification block in the relevant plan doc, or a test-running section in `CLAUDE.md` |

After migration, the handoff file is removed in the same commit as the migration:

```sh
git rm docs/handoffs/<topic>-handoff.md
git add <files-receiving-the-migrated-content>
git commit -m "docs: resolve <topic> handoff — fold into <where-it-went>"
```

The commit message records what migrated where — that's the audit trail. `git log -- docs/handoffs/` then shows the project's handoff history (one add, one delete per session) without needing the files themselves to live forever.

## Template

When you do need to write one, use this skeleton. Replace placeholders inline; delete sections that don't apply (better to omit a section than fill it with "N/A").

```markdown
# Handoff — <Topic> (one-line summary of what this session left open)

**Created:** YYYY-MM-DD
**Working tree:** clean | <state if not clean>
**Branch:** main | <branch>

## Goal & next-up

**Goal of this session:** <what you were trying to do, in 1–3 sentences>

**Next session should pick up:** <the very next concrete action, by name. Reference the plan doc section if applicable.>

**Verification command:**
\`\`\`sh
<commands the next session runs to confirm this handoff's claimed state>
# Expect: <what success looks like>
\`\`\`

## Done this session

| Commit | Subject | Notes |
|---|---|---|
| `<sha>` | <subject> | <one-line note> |

## Open follow-ups (priority-ordered)

### 1. <Item name> (<rough size>)

<Concrete scope. Enough detail to start cold. Link to existing plan/ADR/design-doc sections rather than reproducing them.>

### 2. ...

## Critical context

<Things the next session needs to know that aren't yet in the code/docs.
Be honest about what's truly load-bearing — anything obvious from
`git log` or a quick `grep` doesn't belong here.>

## References

- [`<predecessor-handoff if any>`](<path>) — predecessor (if relevant)
- [`<plan doc>`](<path>) — current workstream state
- [`<ADR>`](<path>) — relevant decision

## Migration note

<When this resolves, what migrates where. Helps the next session
do the fold-and-delete cleanly.>
```

## Tooling

The `create_handoff` and `resume_handoff` skills (from various Claude Code orchestration toolkits) generate and consume handoffs. They're optional — the discipline above is the load-bearing artefact. A handoff written by hand following the template is just as valid.

If you use one of those skills, expect it to default to YAML format under `thoughts/shared/handoffs/` with database indexing. **That doesn't apply here.** Override it: produce markdown at `docs/handoffs/<topic>-handoff.md` and skip the database step. The skill activation is informational; the project's convention takes precedence.

The CLAUDE.md snippet in this repo's `starter/CLAUDE.md.snippet` includes the override note so Claude Code picks it up automatically.

## A worked example

A real handoff resolution from Jacquard:

1. **Session 1**: deep-investigation work on a vendored dependency revealed a license-tagging bug upstream. The session ended with the bug filed but not yet fixed, plus a list of follow-ups blocked on different self-hosted runners coming back online. A handoff `pre-release-runners-handoff.md` was written.
2. **Session 2** (days later): one of the open follow-ups was unblocked. The fix was implemented, and the *Critical context* gotcha (an OpenSTA Tcl quirk) was migrated into a code comment near the Tcl call site. The HIP/CUDA routing notes from the handoff's open follow-ups migrated into the plan doc as a new "WS-RH.2" workstream.
3. **At resolution**: `git rm docs/handoffs/pre-release-runners-handoff.md` in the same commit as the plan-doc edit. The commit message: *"docs: resolve pre-release-runners handoff — fold HIP/CUDA routing into post-phase-0-roadmap WS-RH.2."*

`git log -- docs/handoffs/` now shows: one add, one delete. The audit trail is intact; the handoff itself is gone.
