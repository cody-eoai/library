from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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
        if ".git" not in path.parts
    )
    assert markdown_files
    for path in markdown_files:
        data = frontmatter(path)
        last_edited = data.get("last_edited")
        assert isinstance(last_edited, str) and DATE_RE.match(last_edited), (
            f"last_edited must be a YYYY-MM-DD date: {path}"
        )


def test_skill_frontmatter_shape() -> None:
    """Every repo-native skill (not tracked in skills-lock.json) must carry
    the same {name, description, last_edited} frontmatter. Externally-sourced
    skills are vendored content this repo doesn't own, so they're exempt."""
    locked = locked_skill_names()
    skill_files = sorted(
        skill_dir / "SKILL.md"
        for parent in ("agents", "codex")
        for skill_dir in (ROOT / f".{parent}" / "skills").glob("*")
        if skill_dir.is_dir()
        and skill_dir.name not in locked
        and (skill_dir / "SKILL.md").exists()
    )
    assert skill_files
    for path in skill_files:
        data = frontmatter(path)
        assert set(data) == {"name", "description", "last_edited"}, path
        assert isinstance(data["name"], str) and data["name"]
        assert isinstance(data["description"], str) and data["description"]
        assert DATE_RE.match(data["last_edited"]), path
