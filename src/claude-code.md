# Working with Claude Code

This discipline emerged from many months of human-and-Claude-Code collaboration. A few patterns are worth calling out specifically because they're load-bearing to how the discipline survives long sessions.

## What Claude Code does well with this convention

- **Reading Architecture Decision Records (ADRs) before suggesting changes.** Once `CLAUDE.md` points at `docs/adr/`, Claude reads them. ADRs become guard rails that prevent re-litigating decided questions.
- **Updating plan docs in place.** "Mark WS-P1.1.b as shipped in commit `<sha>`" is a low-friction request that produces a clean diff.
- **Writing handoffs at session end.** When asked, Claude produces a handoff that follows the template. The discipline of "what's in flight, what's blocked" is a natural fit for end-of-session reflection.
- **Folding handoffs at session start.** "Resume from `docs/handoffs/foo-handoff.md`" can be combined with "and migrate any resolved items into the plan doc, then delete the handoff if everything's resolved."

## What Claude Code needs explicit help with

- **Skill toolkit defaults.** Various Claude Code skill toolkits (the `create_handoff` / `resume_handoff` family) default to YAML under `thoughts/shared/handoffs/` with database indexing. These overrides need to be in `CLAUDE.md` so Claude picks the project convention over the skill default. The starter snippet handles this.
- **Knowing when *not* to write a handoff.** Without a hint, Claude tends to write one at every session end. The CLAUDE.md snippet says "skip the handoff if the session ended at a clean stopping point."
- **Distinguishing ADR-worthy from commit-message-worthy.** Without a hint, Claude tends to over-write ADRs for trivial decisions. The CLAUDE.md snippet includes the test: *would someone six months from now wonder why this was chosen?*

## The CLAUDE.md snippet

The full text is in [`starter/CLAUDE.md.snippet`](https://github.com/robtaylor/claude-project-discipline/blob/main/starter/CLAUDE.md.snippet) in this repo. Append it verbatim to your project's `CLAUDE.md`.

The snippet covers:

1. Where each kind of doc lives.
2. The three smell tests (handoff overflow, ADR overflow, plan stagnation).
3. Override notes for the YAML/database default of various skill toolkits.
4. A pointer back to this repo for the long-form discipline.

## Useful one-shot prompts

A few prompts that work well with this convention:

**At session start (resuming work):**
> Read `docs/handoffs/` — there's a single handoff there. Confirm the verification command's expectation, then proceed with the next-up item.

**At session end (work in progress, partial state):**
> Write a handoff at `docs/handoffs/{topic}-handoff.md`. Use the template at `docs/handoffs/_template.md`. Goal: `{X}`. Open follow-ups: `{list}`. Critical context: `{gotchas}`.

**At session end (work fully resolved):**
> Migrate the contents of `docs/handoffs/{topic}-handoff.md` into `docs/plans/{plan}.md` and `docs/adr/{NNNN}-{…}.md`, then `git rm` the handoff. Combine into a single commit.

**Mid-session (decision point):**
> Before we decide on `{X}` vs `{Y}`, draft an ADR proposing `{X}`. Use the template at `docs/adr/0000-template.md`. Status: Proposed. Number it next available.

**Mid-session (validating an assumption):**
> Write a spike at `docs/spikes/{topic}.md` with the question `{Q}`, time-box of 2 days, and a decision matrix for the three plausible outcomes. Status: Open.

## Anti-patterns to watch for

Claude has a few biases that this discipline mostly resists, but watch for:

- **Reaching for handoffs as the universal output format.** A handoff is for ephemeral working memory. If Claude proposes writing a "handoff" that contains `Why we chose X over Y`, redirect to an ADR.
- **Reproducing plan content inside ADRs.** "ADR 0007 — Roadmap for the Q3 work" is a plan doc, not an ADR. Redirect.
- **Mixing decision and rationale into commit messages.** Commit messages should reference the ADR, not embed it. "Per ADR 0006, …" is the right shape.

## Pairing this with other Claude Code conventions

Nothing here conflicts with the broader Claude Code conventions you might already use:

- **CLAUDE.md as the primary instructions file.** Yes — this discipline lives in `CLAUDE.md`.
- **Memory systems** (the `~/.claude/memory/` user-memory pattern). Memory and ADRs cover different things: memory is *cross-project, about the user and their preferences*; ADRs are *project-specific, about the code and its design*. They don't compete.
- **Skill toolkits** (`create_handoff` etc.). These work fine with the convention as long as the directory and format overrides are in `CLAUDE.md`.
