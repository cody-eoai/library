from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


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
    skill_files = sorted((ROOT / ".codex" / "skills").glob("*/SKILL.md"))
    assert skill_files
    for path in skill_files:
        data = frontmatter(path)
        assert set(data) == {"name", "description", "last_edited"}, path
        assert isinstance(data["name"], str) and data["name"]
        assert isinstance(data["description"], str) and data["description"]
        assert DATE_RE.match(data["last_edited"]), path
