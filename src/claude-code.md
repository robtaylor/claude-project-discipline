# Working with Claude Code

This discipline emerged from many months of human-and-Claude-Code collaboration. A few patterns are worth calling out specifically because they're load-bearing to how the discipline survives long sessions.

## What Claude Code does well with this convention

- **Reading the architecture map before suggesting changes.** Once `CLAUDE.md` points at `docs/architecture/README.md`, Claude starts there, reads the area doc for what the code does now, and follows its links to the decisions behind it. Decisions become guard rails that prevent re-litigating settled questions.
- **Updating plan docs in place.** "Mark WS-P1.1.b as shipped in commit `<sha>`" is a low-friction request that produces a clean diff.
- **Writing handoffs at session end.** When asked, Claude produces a handoff that follows the template. The discipline of "what's in flight, what's blocked" is a natural fit for end-of-session reflection.
- **Folding handoffs at session start.** "Resume from `docs/handoffs/foo-handoff.md`" can be combined with "and migrate any resolved items into the plan doc, then delete the handoff if everything's resolved."

## What Claude Code needs explicit help with

- **Skill toolkit defaults.** Various Claude Code skill toolkits (the `create_handoff` / `resume_handoff` family) default to YAML under `thoughts/shared/handoffs/` with database indexing. These overrides need to be in `CLAUDE.md` so Claude picks the project convention over the skill default. The starter snippet handles this.
- **Knowing when *not* to write a handoff.** Without a hint, Claude tends to write one at every session end. The CLAUDE.md snippet says "skip the handoff if the session ended at a clean stopping point."
- **Distinguishing decision-worthy from commit-message-worthy.** Without a hint, Claude tends to write decision records for trivial choices. The CLAUDE.md snippet includes the test: *would someone six months from now wonder why this was chosen?*
- **Leaving decision records alone.** Claude's instinct when the code moves is to "update the docs", which means editing the decision. The snippet says to edit the area doc instead and write a new record if the *why* changed.
- **Moving files.** Claude will happily `git mv` a finished plan and leave a trail of broken links. The snippet tells it to use `doctool.py archive`, which repoints them.

## The CLAUDE.md snippet

The full text is in [`starter/CLAUDE.md.snippet`](https://github.com/robtaylor/claude-project-discipline/blob/main/starter/CLAUDE.md.snippet) in this repo. Append it verbatim to your project's `CLAUDE.md`.

The snippet covers:

1. Where each kind of doc lives.
2. The immutable-decision rule and the `doctool.py` commands.
3. The smell tests (handoff overflow, current state in decisions, plans in the wrong place, plan stagnation).
4. Override notes for the YAML/database default of various skill toolkits.
5. A pointer to `docs/prose-style.md` and back to this repo for the long-form discipline.

## Useful one-shot prompts

A few prompts that work well with this convention:

**At session start (resuming work):**
> Read `docs/handoffs/{topic}-handoff.md`. Run its verification command and confirm the result matches, then proceed with the next-up item.

**At session end (work in progress, partial state):**
> Write a handoff at `docs/handoffs/{topic}-handoff.md`. Use the template at `docs/handoffs/_template.md`. Goal: `{X}`. Open follow-ups: `{list}`. Critical context: `{gotchas}`.

**At session end (work fully resolved):**
> Migrate the contents of `docs/handoffs/{topic}-handoff.md` into `docs/plans/{plan}.md`, the `{area}` area doc, and a new decision record if one is needed, then `git rm` the handoff. Run `doctool.py lint`. Combine into a single commit.

**Mid-session (decision point):**
> Before we decide on `{X}` vs `{Y}`, run `uv run docs/scripts/doctool.py new decision "{title}"` and draft it proposing `{X}`. Status: Proposed. Open the Context with what the code does today.

**Mid-session (validating an assumption):**
> Run `uv run docs/scripts/doctool.py new spike "{topic}"` and write it up with the question `{Q}`, a time-box of 2 days, and a decision matrix for the three plausible outcomes. Status: Open.

**After a plan's exit criteria are met:**
> Set `docs/plans/{plan}.md` to `Implemented ({date})`, archive it with `uv run docs/scripts/doctool.py archive docs/plans/{plan}.md`, move its row under Completed in the index, and run lint.

## Anti-patterns to watch for

Claude has a few biases that this discipline mostly resists, but watch for:

- **Reaching for handoffs as the universal output format.** A handoff is for ephemeral working memory. If Claude proposes writing a "handoff" that contains `Why we chose X over Y`, redirect to a decision record.
- **Reproducing plan content inside decisions.** "Decision 0007 — Roadmap for the Q3 work" is a plan doc, not a decision. Redirect.
- **Present-tensing a decision.** "The scheduler batches 1024 edges" in a decision record will be wrong the day someone changes the batch size. That sentence belongs in the area doc.
- **Mixing decision and rationale into commit messages.** Commit messages should reference the decision, not embed it. "Per Decision 0006, …" is the right shape.

## Pairing this with other Claude Code conventions

Nothing here conflicts with the broader Claude Code conventions you might already use:

- **CLAUDE.md as the primary instructions file.** Yes — this discipline lives in `CLAUDE.md`.
- **Memory systems** (the `~/.claude/memory/` user-memory pattern). Memory and decision records cover different things: memory is *cross-project, about the user and their preferences*; decisions are *project-specific, about the code and its design*. They don't compete.
- **Skill toolkits** (`create_handoff` etc.). These work fine with the convention as long as the directory and format overrides are in `CLAUDE.md`.
