# Release process

A lightweight release process complements the four-document discipline. It doesn't *have* to live alongside Architecture Decision Records (ADRs), plans, and handoffs, but the same instincts apply: keep it short, version-control the steps, make the punch-list visible.

## Shape

Two distinct documents are useful:

1. **`CHANGELOG.md`** at the repo root, in [Keep a Changelog](https://keepachangelog.com/) format. The historical record of what shipped when.
2. **`docs/release-process.md`** describing *how* releases are cut. Short, prescriptive, version-controlled. Includes a **pre-release punch list** of one-time items that block the first numbered release.

## Why a pre-release punch list

Most release processes on the internet assume v1.0 has already shipped. The trickiest moment is *before* that, when "we should release at some point" turns into "what's actually blocking us?"

A visible, version-controlled punch list makes that explicit:

```markdown
## Pre-release checklist (one-time, before the first numbered release)

- [x] Phase 1 closed (per `docs/plans/phase-1.md`).
- [x] License posture confirmed; `NOTICE` file in place.
- [ ] All CI jobs green on `main`.
- [ ] End-to-end test for the headline feature.
- [ ] User-facing docs cover the install path.
```

Each item is a check-box. As they land, they're checked off in the same PR that landed them. When all are checked, you cut a release.

## When to release

Cut a release when:

- A user-visible feature or fix lands that you want consumers to be able to pin against.
- Schema or CLI changes happened and consumers need a stable reference point.
- A meaningful chunk of work in `docs/plans/` is closed (e.g. a phase exits all criteria).

There is no fixed cadence. Time-based releases force releases when there's nothing user-visible to release; demand-driven releases avoid the noise.

## Versioning

[SemVer](https://semver.org/), starting once the first numbered release ships. Pre-1.0 versions (`0.x.0`) carry the standard SemVer caveat: minor bumps may include breaking changes; specific stable contracts (a JSON schema, a binary format) are documented in their own ADRs and follow stricter rules.

A useful pattern is to declare the **stable contracts** explicitly:

```markdown
Stable contracts (additive-only, breaking changes require a major
bump and a deprecation window):

- `--report` JSON schema — `src/report.rs::SCHEMA_VERSION`,
  governed by ADR 0008.
- IR FlatBuffers schema — `crates/ir/schemas/ir.fbs`,
  governed by ADR 0002.
```

Everything not listed is fair game to evolve.

## Steps for cutting a release

```markdown
1. **Verify CI is green** on `main` for all jobs. If a job is offline, hold the release until it's restored.

2. **Roll the `[Unreleased]` section in `CHANGELOG.md` into a numbered version block.** Update the link references at the bottom. Leave a fresh empty `[Unreleased]` section.

3. **Bump version** in your project's manifest (`Cargo.toml`, `package.json`, etc.). Re-build to update the lockfile.

4. **Commit:** `chore: release v<X.Y.Z>` with whatever attribution conventions your project uses.

5. **Tag:** `git tag -a v<X.Y.Z> -m "v<X.Y.Z>"` then `git push --tags`.

6. **Create a release** on the platform of your choice from the tag. Body = the CHANGELOG section for that version.
```

## What does NOT need to change at release time

Be explicit about this — it stops well-meaning maintainers from sweeping in changes that should land in their own PRs:

- Vendored / submodule pins (unless deliberately bumping a vendored dep).
- License files (unless re-licensing).
- Long-lived design docs (unless the release changes the design they describe).

## Template

A copy-paste-ready `release-process.md` with placeholders lives at [`starter/docs/release-process.md`](https://github.com/robtaylor/claude-project-discipline/blob/main/starter/docs/release-process.md).
