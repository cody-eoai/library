from __future__ import annotations

from pathlib import Path

from test_skills import DATE_RE, frontmatter


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIELDS = {
    "title",
    "type",
    "source",
    "saved_from",
    "source_id",
    "category",
    "tags",
    "related",
    "created",
    "last_edited",
}
VALID_TYPES = {"sop", "article"}


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def test_knowledge_base_entries_match_the_template_shape() -> None:
    entries = sorted((ROOT / "knowledge-base").glob("*.mmd"))
    for path in entries:
        data = frontmatter(path)
        missing = REQUIRED_FIELDS - set(data)
        assert not missing, f"{path} is missing fields: {sorted(missing)}"
        entry_type = unquote(str(data["type"]))
        assert entry_type in VALID_TYPES, f"{path} has an invalid type: {entry_type!r}"
        assert DATE_RE.match(data["created"]), path
        assert DATE_RE.match(data["last_edited"]), path


def test_knowledge_base_related_links_are_bidirectional() -> None:
    entries = sorted((ROOT / "knowledge-base").glob("*.mmd"))
    if not entries:
        return

    related_by_slug: dict[str, set[str]] = {}
    for path in entries:
        data = frontmatter(path)
        raw = str(data.get("related", "")).strip()
        if raw.startswith("[") and raw.endswith("]"):
            raw = raw[1:-1]
        slugs = {
            item.strip().strip('"').strip("'")
            for item in raw.split(",")
            if item.strip().strip('"').strip("'")
        }
        related_by_slug[path.stem] = slugs

    for slug, related in related_by_slug.items():
        for other in related:
            assert other in related_by_slug, f"{slug}.mmd links to unknown entry {other!r}"
            assert slug in related_by_slug[other], (
                f"{slug}.mmd lists {other!r} as related, but {other}.mmd doesn't link back"
            )
