# Decision records

A **decision record** is a short, numbered markdown file that captures **the *why* behind a non-obvious choice**, so future contributors don't re-litigate it. Records live at `docs/architecture/decisions/NNNN-<short-name>.md` and are cited as "Decision NNNN".

The format descends from the Architecture Decision Record (ADR) in [Michael Nygard's 2011 post](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions). This book used the term "ADR" in earlier versions and dropped it. The phrase doesn't tell a newcomer what's inside, and enough people bounce off it that "decision" works better. The Nygard rule survives intact: **a decision record is immutable and written in past tense.** It records a choice at the moment it was made. It doesn't describe the system now. That's the [architecture reference](architecture.md)'s job.

## When to write one

Write a decision record whenever you make a non-trivial choice that future-you (or a future contributor, or a future Claude session) would want to understand the reasoning behind. Examples that qualify:

- Picking one tool / library / format over another
- Choosing a particular architectural boundary
- Adopting a multi-piece convention that spans several files
- Deciding *not* to do something obvious-looking

**Skip them for:**

- Mechanical changes (renames, typo fixes, dependency bumps)
- Choices the code itself makes self-evident (a small refactor, a chosen variable name)
- Things adequately captured by a commit message

A useful test: *if someone asked "why is it like this?" six months from now, would the answer be in the code, the commit, or a decision record?* If the answer is "a decision record", write it.

## Three kinds of claim, aged differently

A decision is usually written against a codebase it's about to change, often *because* of the decision. Three kinds of claim end up near each other, and they age at different rates:

1. **Why the decision was made.** The rationale, and the problem that prompted it. This is the record's lasting value. The code and `git log` show the *what*; only the record holds the *why*. It's written as the state at decision time, in past tense, and never rewritten when the code moves. The problem is worth keeping even after it's solved.
2. **What the current architecture is.** What the code does today. This is a verifiable present-tense claim that has to be kept in step with the code. It's what goes stale, so it lives in the [architecture reference](architecture.md), not in the decision record. Each *what* links back to the *why* that produced it.
3. **What's decided but not built yet.** The gap between a decision and the code. It lives in the area doc's `## Implementation status` section, with a plan or issue so the unbuilt half isn't lost, and drains into (2) as each piece lands.

The failure mode is writing all three in the same present tense, so a reader can't tell whether a sentence is *why we did it*, *what the code does*, or *what we still intend*. "`BATCH_SIZE` is 1024" reads as current fact. "The fixed `BATCH_SIZE` of 1024 was what this replaced" reads as the starting point the decision moved past. A human skims past a wrong present-tense claim. A model repeats it as generated code. So the reference layer stays ruthlessly current and the decision layer stays rationale-only.

## Format

```markdown
# Decision NNNN — Short title

**Status:** Accepted (YYYY-MM-DD).

**Current architecture:** [<Area>](../<area>.md).

**TL;DR.** In the context of <use case>, facing <concern>, we chose
<option> to achieve <quality>, accepting <downside>.

## Context

What was the situation? What constraints forced a decision?
Be concrete: name the systems, the data formats, the friction.
Past tense. This is the world at decision time.

## Decision

What we chose, with enough specificity to act on.
Numbered sub-points if multiple commitments.

## Alternatives considered

The options we looked at and rejected, with the reason for each.
Tie each reason to this project's constraints, not generic preference.

## Consequences

What this bought us, what it cost us, and what would trigger a walk-back.
Be honest about the costs.

## Walk-back options

(Optional, but strongly encouraged.) Conditions under which this
decision should be revisited, and how to revisit it cheaply.

## Links

Spikes this rested on, related decisions, the area doc.
```

The **TL;DR** is a single-sentence summary in the (WH)Y form: *"in the context of X, facing Y, we chose Z to achieve Q, accepting D"*. It forces the author to name the trade-off out loud. It also gives skim-readers the shape of the decision before they commit to the prose.

The **Alternatives considered** section is the one most often skipped, and the one future readers most often need. Without it, the next person to hit the same fork has to rediscover that Option B was already tried. Or they assume it wasn't, and re-propose it.

The **Current architecture** line is the forward-link to the area doc this decision shaped. The area doc links back from its "Decisions behind this" section. A reader on either side reaches the other in one hop.

### Prefer durable abstractions

When the decision is meant to last, prefer platform-neutral patterns over framework-of-the-month. If the choice is tightly coupled to a tool or library that may be replaced in 12–18 months, say so in **Consequences** and add a **Walk-back option** for the day the dependency goes away. This doesn't ban new tools. It asks you to be honest about which decisions are load-bearing for the long term and which are situational.

## What's mutable, and what isn't

The body of a decision record (Context, Decision, Alternatives, Consequences) is **never edited** after the decision is accepted. Only two lines change:

- **The `Status:` line**, as the decision moves through its lifecycle.
- **The `Current architecture:` forward-link**, if the area doc it points at is renamed or split.

When the code moves, edit the area reference doc, not the decision. When the *decision itself* changes, write a new record:

1. Write Decision `M`, which says what it replaces and why.
2. Set the old record's status to `Superseded by Decision M (YYYY-MM-DD)`.
3. Move the old file to `docs/architecture/decisions/archive/`. Keep its number.
4. Update the area doc to describe the new current state.

This is what stops decision records from rotting: history can't go stale.

### Why not amend in place?

An earlier version of this discipline let records accrete dated `## Amendment` blocks when their scope grew, with the original text relegated below. It kept the audit trail, but it made each record a mix of three tenses that a reader had to untangle. And the amendments existed only because the record was the sole place current state could live. Once the reference layer carries current state, nothing pushes you to edit a decision record. A refinement that changes *what the code does* is an area-doc edit. A refinement that changes *why* is a new decision.

## Status lifecycle

- **Proposed** — drafted, not yet ratified. Everything a Proposed record describes is unbuilt, so open the body with one line saying what the code does today ("nothing built; the code today is X"). Then the rest of the record can describe the proposal in the present without a reader mistaking it for reality.
- **Accepted (YYYY-MM-DD)** — the decision is in effect in the code.
- **Accepted (partial) (YYYY-MM-DD)** — ratified, and only some of it is built. The area doc's `## Implementation status` section says which parts.
- **Superseded by Decision NNNN (YYYY-MM-DD)** — replaced. The record moves to `archive/`.
- **Withdrawn (YYYY-MM-DD)** — abandoned without replacement (rare). Also moves to `archive/`.

## Status must match the code

A `Status:` line is a **claim about the codebase**, not a statement of intent. Before you set or change it, **verify the claim against the implementation**. Read the code. Don't trust the previous status, or the fact that a feature "shipped". The same applies to every present-tense sentence in the reference layer, and to user-facing docs and `--help` text. A sentence describing how the tool behaves is a checkable claim, so check it before writing it.

- **Don't bump Proposed → Accepted just because a design merged.** Confirm the decision is actually in effect in the code.
- **A ratified, partly built design is `Accepted (partial)`.** Don't inflate it to a clean `Accepted`, and don't leave it at `Proposed`. Record which parts are real in the area doc's Implementation status, with file references for what's built and the specific gap for what isn't.
- **Deferred work gets a home.** A plan under `docs/plans/` and a tracking issue, linked from the Implementation status section, so the unbuilt half isn't lost. When the last deferred piece lands, the status moves to a plain `Accepted`.

This keeps the record trustworthy. A reader can rely on `Accepted` meaning "in effect", and `Accepted (partial)` sends them to the exact list of what's real. The failure mode it prevents is a design that reads as shipped but is ~40% built. The next contributor takes it at face value and builds on vapour.

## Numbering and the index

Use sequential zero-padded numbers: `0001-foo.md`, `0002-bar.md`. The number is a **stable ID** cited from docs, code, and commits. Don't reuse numbers and don't renumber, even when a record moves to `archive/`.

Keep the number out of the reading title. The `# H1` and the `SUMMARY.md` link text are what readers see.

Maintain `docs/architecture/decisions/README.md` as the index:

```markdown
| # | Title | Status |
|---|---|---|
| [0001](0001-external-oracle.md) | External tool X as correctness oracle | Accepted (2026-04-15) |
| [0002](0002-ir-format.md) | Intermediate representation format | Accepted (2026-04-20) |
| [0003](archive/0003-in-process-reference.md) | Tool Y as in-process reference | Superseded (2026-05-01), spike failed |
```

## Never delete a decision

A superseded record moves to `archive/`. It doesn't leave the repo. Future readers tracing the history of a decision need both the old one and the new one.

This is uncomfortable when the old record is wrong; *that's the point*. A wrong decision marked Superseded is more useful than a clean repo with no record of the wrong turn.

## A worked example

The cleanest sequence is one where a decision proposes a path, a spike tests it, the spike fails, and a new decision replaces the old one:

- Decision 0001: "Use external tool X as our oracle." Accepted.
- Decision 0003: "Add tool Y as our in-process reference." Proposed.
- Spike `decisions/spikes/tool-y-on-real-inputs.md`: time-boxed validation of Y on real workloads. **Resolved NO. Y can't parse our inputs.**
- Decision 0003 status set to `Superseded (2026-05-01), spike failed`. The file moves to `archive/`.
- Decision 0004: "X is both oracle and sole analysis path." Accepted. It cites the spike as evidence and says it replaced 0003.
- The area doc for the analysis stack is edited to describe X as the only path, and lists 0001 and 0004 under "Decisions behind this".

A reader asking "why are we using X out of process?" lands on the area doc, follows the link to Decision 0004, and from there to the spike and the archived 0003. They get the full story without anything having been rewritten.

## Template

A copy-paste-ready template lives at [`starter/docs/architecture/decisions/0000-template.md`](https://github.com/robtaylor/claude-project-discipline/blob/main/starter/docs/architecture/decisions/0000-template.md). Drop it into your project's `docs/architecture/decisions/` and rename it to the next available number.
