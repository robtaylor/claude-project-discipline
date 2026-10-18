"""Tests for starter/docs/scripts/doctool.py, driven through its CLI entry point.

Run with:  uv run --with pytest pytest tests/
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("doctool", REPO / "starter/docs/scripts/doctool.py")
assert SPEC is not None and SPEC.loader is not None
doctool = importlib.util.module_from_spec(SPEC)
sys.modules["doctool"] = doctool  # dataclasses look the module up while it executes
SPEC.loader.exec_module(doctool)


def write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def git_init(root: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "base"],
                   cwd=root, check=True)


def run(root: Path, *args: str) -> int:
    return doctool.main(["--root", str(root), *args])


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    write(tmp_path, "CLAUDE.md", "See [roadmap](docs/plans/old.md) and `docs/plans/old.md`.\n")
    write(tmp_path, "src/lib.rs", "// Phase plan: docs/plans/old.md\n// not this: docs/plans/old.md.bak\n")
    write(tmp_path, "docs/README.md", "- [Old plan](plans/old.md#ws1)\n- [Live](plans/live.md)\n")
    write(tmp_path, "docs/guide.md", "# Guide\n")
    write(tmp_path, "docs/plans/live.md",
          "**Status:** Active.\n\nFollows [old](old.md), see `old.md`.\n\n```sh\ncat old.md\n```\n")
    write(tmp_path, "docs/plans/old.md",
          "# Plan — old\n\n**Status:** Implemented (2026-01-01).\n\n"
          "Next: [live](live.md) and `live.md`; guide `../guide.md`; [self](#top); [web](https://x.y/a.md).\n"
          "Repo path `docs/guide.md` stays.\n")
    git_init(tmp_path)
    return tmp_path


def test_archive_repoints_both_directions(repo: Path) -> None:
    assert run(repo, "archive", str(repo / "docs/plans/old.md")) == 0
    moved = repo / "docs/plans/archive/old.md"
    assert moved.is_file() and not (repo / "docs/plans/old.md").exists()

    assert (repo / "docs/README.md").read_text().startswith("- [Old plan](plans/archive/old.md#ws1)")
    live = (repo / "docs/plans/live.md").read_text()
    assert "[old](archive/old.md)" in live and "`archive/old.md`" in live
    assert "cat old.md" in live, "fenced code is left alone"

    claude = (repo / "CLAUDE.md").read_text()
    assert claude == "See [roadmap](docs/plans/archive/old.md) and `docs/plans/archive/old.md`.\n"
    lib = (repo / "src/lib.rs").read_text()
    assert "// Phase plan: docs/plans/archive/old.md\n" in lib
    assert "docs/plans/old.md.bak" in lib, "a longer path is not a match"

    text = moved.read_text()
    assert "[live](../live.md)" in text and "`../live.md`" in text
    assert "`../../guide.md`" in text, "relative mention re-depthed against the old location"
    assert "[self](#top)" in text and "https://x.y/a.md" in text
    assert "`docs/guide.md`" in text, "repo-root mention is not re-depthed"

    status = subprocess.run(["git", "status", "--porcelain"], check=True, cwd=repo,
                            capture_output=True, text=True).stdout
    assert "RM docs/plans/old.md -> docs/plans/archive/old.md" in status, "a git rename, then the re-depth edit"
    assert run(repo, "lint") == 0


def test_archive_dry_run_changes_nothing(repo: Path) -> None:
    before = (repo / "docs/README.md").read_text()
    assert run(repo, "archive", "--dry-run", str(repo / "docs/plans/old.md")) == 0
    assert (repo / "docs/plans/old.md").exists()
    assert (repo / "docs/README.md").read_text() == before


def test_archive_refuses_unfinished_unless_forced(repo: Path) -> None:
    live = str(repo / "docs/plans/live.md")
    assert run(repo, "archive", live) == 2
    assert (repo / "docs/plans/live.md").exists()
    assert run(repo, "archive", "--force", live) == 0


def test_archive_is_idempotent(repo: Path) -> None:
    old = str(repo / "docs/plans/old.md")
    assert run(repo, "archive", old) == 0
    assert run(repo, "archive", old) == 0


def test_archive_batch_links_between_moved_files(repo: Path) -> None:
    write(repo, "docs/plans/live.md", "**Status:** Implemented.\n\nFollows [old](old.md).\n")
    assert run(repo, "archive", str(repo / "docs/plans/old.md"), str(repo / "docs/plans/live.md")) == 0
    assert "[old](old.md)" in (repo / "docs/plans/archive/live.md").read_text()
    assert "[live](live.md)" in (repo / "docs/plans/archive/old.md").read_text()


def test_archive_decision(tmp_path: Path) -> None:
    write(tmp_path, "docs/architecture/decisions/0001-a.md",
          "# Decision 0001 — A\n\n**Status:** Superseded by Decision 0002 (2026-01-02).\n\n"
          "See [b](0002-b.md) and [area](../area.md).\n")
    write(tmp_path, "docs/architecture/decisions/0002-b.md", "**Status:** Accepted.\n\nReplaces [0001](0001-a.md).\n")
    write(tmp_path, "docs/architecture/area.md", "# Area\n")
    git_init(tmp_path)
    assert run(tmp_path, "archive", str(tmp_path / "docs/architecture/decisions/0001-a.md")) == 0
    moved = (tmp_path / "docs/architecture/decisions/archive/0001-a.md").read_text()
    assert "[b](../0002-b.md)" in moved and "[area](../../area.md)" in moved
    assert "[0001](archive/0001-a.md)" in (tmp_path / "docs/architecture/decisions/0002-b.md").read_text()


def lint_codes(root: Path, capsys: pytest.CaptureFixture[str], *args: str) -> set[str]:
    run(root, "lint", *args)
    out = capsys.readouterr().out
    return {line.split()[2] for line in out.splitlines() if line.strip()}


def test_lint_flags_each_rule(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    d = "docs/architecture/decisions"
    write(tmp_path, f"{d}/README.md",
          "## Index\n\n| # | Title | Status |\n|---|---|---|\n\n| # | Title | Status |\n|---|---|---|\n"
          "| [0001](0001-split.md) | Split | Proposed |\n")
    write(tmp_path, f"{d}/0001-split.md",
          "# Decision 0001\n\n**Status:** Accepted, and the sentence goes\n\n"
          "**Current architecture:** [Area](../area.md).\non here.\n\n## Amendment (2026-01-01)\n")
    write(tmp_path, f"{d}/0002-old.md", "**Status:** Superseded by Decision 0001.\n")
    write(tmp_path, f"{d}/archive/0002-dup.md", "**Status:** Superseded.\n")
    write(tmp_path, f"{d}/spikes/s.md", "**Status:** Maybe.\n")
    write(tmp_path, "docs/architecture/area.md", "# Area\n\n[gone](missing.md)\n")
    write(tmp_path, "docs/plans/done.md", "**Status:** Implemented (2026-01-01).\n")
    for i in range(5):
        write(tmp_path, f"docs/handoffs/t{i}-handoff.md", "# h\n")
    write(tmp_path, "docs/handoffs/badname.md", "# h\n")

    codes = lint_codes(tmp_path, capsys, "--people", "2")
    assert {"L001", "M001", "D001", "D002", "D004", "D006", "S001", "R001",
            "H001", "H002", "A001", "A002"} <= codes
    without_people = lint_codes(tmp_path, capsys)
    assert "D002" in without_people and "H001" not in without_people


def test_lint_clean_starter(capsys: pytest.CaptureFixture[str]) -> None:
    """The starter kit itself lints without errors (templates are exempt)."""
    starter = REPO / "starter"
    assert doctool.main(["--root", str(starter), "lint"]) == 0, capsys.readouterr().out


def test_new_decision_numbers_and_indexes(tmp_path: Path) -> None:
    d = tmp_path / "docs/architecture/decisions"
    write(tmp_path, "docs/architecture/decisions/0000-template.md",
          "# Decision NNNN — <Short title>\n\n**Status:** Proposed.\n")
    write(tmp_path, "docs/architecture/decisions/README.md",
          "## Index\n\n| # | Title | Status |\n|---|---|---|\n| [0001](archive/0001-x.md) | X | Superseded |\n\n## Next\n")
    write(tmp_path, "docs/architecture/decisions/archive/0001-x.md", "**Status:** Superseded.\n")
    assert run(tmp_path, "new", "decision", "Use Flat Files!") == 0
    created = d / "0002-use-flat-files.md"
    assert created.read_text().startswith("# Decision 0002 — Use Flat Files!\n")
    index = (d / "README.md").read_text()
    assert "| [0001](archive/0001-x.md) | X | Superseded |\n| [0002](0002-use-flat-files.md) | Use Flat Files! | Proposed |\n" in index
    assert run(tmp_path, "new", "decision", "Use Flat Files!") == 0
    assert (d / "0003-use-flat-files.md").exists()


def test_new_other_kinds_use_title(tmp_path: Path) -> None:
    write(tmp_path, "docs/plans/_template.md", "# Plan — <Phase or topic>: <goal>\n")
    assert run(tmp_path, "new", "plan", "GPU port") == 0
    assert (tmp_path / "docs/plans/gpu-port.md").read_text().startswith("# Plan — GPU port: <goal>")
    assert run(tmp_path, "new", "plan", "GPU port") == 2


@pytest.mark.parametrize("text, expected", [
    ("**Status:** Accepted (2026-01-01).", "accepted"),
    ("> **Status (2026-07-06):** Implemented and green.", "implemented"),
    ("**Status:** ✅ **SHIPPED** in v0.3.0", "shipped"),
    ("# Plan\n\n## Status\n\nActive, two workstreams left.", "active"),
    ("# Plan\n\nNo status here.", ""),
])
def test_status_forms(text: str, expected: str) -> None:
    status, _ = doctool.status_of(text)
    assert doctool.status_word(status) == expected
