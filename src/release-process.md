# Release process

A lightweight release process complements the rest of the discipline. It doesn't *have* to live alongside decisions, plans, and handoffs, but the same instincts apply: keep it short, version-control the steps, make the punch-list visible.

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

[SemVer](https://semver.org/), starting once the first numbered release ships. Pre-1.0 versions (`0.x.0`) carry the standard SemVer caveat: minor bumps may include breaking changes; specific stable contracts (a JSON schema, a binary format) are documented in their own decision records and follow stricter rules.

A useful pattern is to declare the **stable contracts** explicitly:

```markdown
Stable contracts (additive-only, breaking changes require a major
bump and a deprecation window):

- `--report` JSON schema — `src/report.rs::SCHEMA_VERSION`,
  governed by Decision 0008.
- IR FlatBuffers schema — `crates/ir/schemas/ir.fbs`,
  governed by Decision 0002.
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

## Release notes lead with what changed for the user

Write the release notes in `[Unreleased]` as work lands, not at release time. Open them with a short **"What this means for you"** block before the technical `### Added` / `### Changed` sections:

```markdown
## [Unreleased]

### What this means for you

- You can now simulate designs with multiple clock domains.
- Install is one command on macOS: `brew install org/tap/tool`.

### Added
- Multi-clock scheduler (`docs/architecture/simulation-engine.md`).
```

A few benefit-framed bullets say what a user can now *do*. The technical changelog then gives the detail. If your release notes come from the CHANGELOG (a release workflow that extracts the section for the tag), this block becomes the first thing a reader sees on the release page.

## Release candidates: main *is* the candidate

If you cut release candidates (`X.Y.Z-rc.N`) to validate install paths before a final release, **don't roll `main` to the final version before the candidate validates.** During the RC window, `main` stays at `X.Y.Z-rc.N` with the notes still under `[Unreleased]`. Each new RC is a `main` commit bumped to the next `-rc.N`, so `main` always matches the latest RC tag. Only the promote step rolls `[Unreleased]` into a dated `[X.Y.Z]` block and bumps to `X.Y.Z`.

Rolling first leaves `main` advertising a version that has no release. The dated changelog entry and the manifest version both claim `X.Y.Z` shipped while only the RC tag exists. Tools that read `main`'s version to find a release tarball then fetch one that doesn't exist.

A GitHub (or equivalent) **prerelease** makes a good staging tier for binary channels: it's never shown as "Latest", and an install-validation job can run the documented install commands against it before promotion.

## What does NOT need to change at release time

Be explicit about this — it stops well-meaning maintainers from sweeping in changes that should land in their own PRs:

- Vendored / submodule pins (unless deliberately bumping a vendored dep).
- License files (unless re-licensing).
- Area docs in `docs/architecture/` (unless the release changes the design they describe).

## Template

A copy-paste-ready `release-process.md` with placeholders lives at [`starter/docs/release-process.md`](https://github.com/robtaylor/claude-project-discipline/blob/main/starter/docs/release-process.md).
