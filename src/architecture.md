# Architecture reference

The **architecture reference** describes the project's current design, one document per area, as it stands in the code today. It's the entry point. A reader (or an agent) who wants to know "how does X work right now" starts here, not in the decision log.

Each area doc lives at `docs/architecture/<area>.md`. A map at `docs/architecture/README.md` lists every area with its reference doc and the decisions behind it.

## Why a separate layer

Without it, the only place current state can live is the decision record. So the record has to be edited every time the code moves, and it ends up mixing *why we chose this* with *what the code does now* and *what we still intend*. That mix is what makes decision records go stale. (See [Three kinds of claim](decisions.md#three-kinds-of-claim-aged-differently).)

Splitting the two lets each one keep a simple rule:

| Layer | Holds | Tense | Mutability |
|---|---|---|---|
| Architecture reference | What the code does now | Present | Edited in place whenever the code moves |
| Decision log | Why it got that way | Past | Immutable; replaced by a new record when the decision changes |

[Diátaxis](https://diataxis.fr/reference-explanation/) names the same split. Its *reference* type (factual, present-tense, structured for lookup) is the architecture layer. Its *explanation* type (background and rationale, written for study) is the decision log. Diátaxis also names the failure mode: explanation bleeds into reference and drags time-bound claims into a doc that's supposed to state what is.

## The rules for an area doc

- **Present tense means "true today".** Every present-tense sentence is a verifiable claim about the code. Check it before you write it. If it's stale, the code moved and the doc didn't. That's a bug.
- **No rationale.** "We chose X because Y" goes in a decision record. The area doc says "X does Y" and links to the decision.
- **No dead history.** Don't keep "previously this used Z" paragraphs. `git log` and the archived decisions hold history.
- **Unbuilt work goes in `## Implementation status`.** Split *implemented* (with file references) from *deferred* (with the specific gap and a link to its plan or issue). Items move out of this section and into the body as they land.
- **Link both ways.** Each section names the decisions behind it. Each decision has a `**Current architecture:**` line pointing back here.
- **Keep sections self-contained.** A reader, or a model retrieving one section, should understand it without "as described above". Restate the subject.

## Anatomy

```markdown
# <Area name>

*Reference: the current design as it stands in the code. The why lives
in the decision records linked from each section. The not-yet-built work
is under Implementation status.*

One paragraph: what this area does and where it sits in the system.
Rationale for the overall shape: [Decision NNNN](decisions/NNNN-….md).

## <Component or concept>

What it does today. File references where they help. Decision links
where a reader will ask "why?".

## Constraints

Hard limits a contributor needs to know (sizes, supported platforms,
unsupported inputs).

## Implementation status

**Implemented:**

| Part | Where |
|---|---|
| <part> | `src/…` |

**Deferred:**

| Part | Gap | Tracking |
|---|---|---|
| <part> | <what's missing> | `docs/plans/<plan>.md`, issue #N |

## Decisions behind this

- [Decision NNNN — <title>](decisions/NNNN-….md)
- [Decision MMMM — <title>](decisions/MMMM-….md)
```

## Choosing the areas

An area is a part of the system a contributor could own: the simulation engine, the timing stack, distribution, a runtime. Aim for somewhere between three and eight. Fewer than three and each doc gets too long to retrieve usefully. More than eight and the map stops being a map.

A decision that cuts across areas is listed under each area it shaped. That's fine. The map's "Decisions behind it" column will show the overlap.

Don't create an area doc speculatively. Write one when there's code to describe, or when a contributor has asked "how does X work" and the answer was spread across three decision records.

## The map

`docs/architecture/README.md` is the first page a reader hits. Keep it to a short intro and one table:

```markdown
| Area | Reference | Decisions behind it |
|---|---|---|
| Timing | [timing](timing.md) | 0001, 0002, 0005 |
| Simulation engine | [simulation-engine](simulation-engine.md) | 0014, 0015 |
| Distribution | [distribution](distribution.md) | 0018 |
```

## Template

Copy-paste-ready templates live at [`starter/docs/architecture/README.md`](https://github.com/robtaylor/claude-project-discipline/blob/main/starter/docs/architecture/README.md) (the map) and [`starter/docs/architecture/_template.md`](https://github.com/robtaylor/claude-project-discipline/blob/main/starter/docs/architecture/_template.md) (an area doc).
