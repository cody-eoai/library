from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SKILLS = ROOT / ".agents" / "skills"
CLAUDE_SKILLS = ROOT / ".claude" / "skills"
# Raw drop zones: files land here without frontmatter by design.
UNSTRUCTURED_DIRS = {("knowledge-base", "inbox"), ("tmp",)}
# Tooling directories that write their own markdown.
TOOLING_DIRS = {".git", ".pytest_cache", ".venv", "node_modules"}


def in_unstructured_dir(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    return any(parts[: len(prefix)] == prefix for prefix in UNSTRUCTURED_DIRS)


def locked_skill_names() -> set[str]:
    lock_path = ROOT / "skills-lock.json"
    if not lock_path.exists():
        return set()
    return set(json.loads(lock_path.read_text()).get("skills", {}))


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text()
    assert text.startswith("---\n"), f"missing frontmatter: {path}"
    _, raw, _ = text.split("---", 2)
    data: dict[str, object] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        assert sep, f"frontmatter line must be key/value: {path}: {line}"
        data[key.strip()] = value.strip()
    return data


def test_markdown_has_last_edited_frontmatter() -> None:
    markdown_files = sorted(
        path
        for path in ROOT.glob("**/*.md")
        if not TOOLING_DIRS & set(path.relative_to(ROOT).parts)
        and not in_unstructured_dir(path)
    )
    assert markdown_files
    for path in markdown_files:
        data = frontmatter(path)
        last_edited = data.get("last_edited")
        assert isinstance(last_edited, str) and DATE_RE.match(last_edited), (
            f"last_edited must be a YYYY-MM-DD date: {path}"
        )


def skill_dirs() -> list[Path]:
    return sorted(p for p in SKILLS.glob("*") if (p / "SKILL.md").exists())


def test_skill_frontmatter_shape() -> None:
    """Repo-native skills share one frontmatter shape. Skills listed in
    skills-lock.json are vendored from elsewhere, so they're exempt."""
    locked = locked_skill_names()
    skill_files = [d / "SKILL.md" for d in skill_dirs() if d.name not in locked]
    assert skill_files
    for path in skill_files:
        data = frontmatter(path)
        assert set(data) == {"name", "description", "last_edited"}, path
        assert isinstance(data["name"], str) and data["name"]
        assert isinstance(data["description"], str) and data["description"]
        assert DATE_RE.match(data["last_edited"]), path


def test_every_skill_is_mirrored_for_claude_code() -> None:
    """Claude Code only reads .claude/skills, so every skill needs a working
    link there. On Windows, a git checkout without symlink support turns
    these links into plain files, which this test catches."""
    for skill in skill_dirs():
        link = CLAUDE_SKILLS / skill.name
        assert (link / "SKILL.md").is_file(), (
            f"{skill.name} isn't reachable from .claude/skills; run: "
            f"ln -s ../../.agents/skills/{skill.name} .claude/skills/{skill.name}"
        )
    for entry in CLAUDE_SKILLS.iterdir():
        assert (entry / "SKILL.md").is_file(), f".claude/skills/{entry.name} is broken"
