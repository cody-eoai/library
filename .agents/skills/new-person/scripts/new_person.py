from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


TEMPLATE = Path(__file__).absolute().parent.parent / "assets" / "person.md"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "new-person"


def build_note(name: str, role: str) -> str:
    today = date.today().isoformat()
    note = TEMPLATE.read_text().replace("<Person Name>", name)
    note = note.replace(
        "What this person does or how they relate to this workspace.",
        role or "TBD",
    )
    note = note.replace("YYYY-MM-DD", today)
    return re.sub(r"^last_edited: .*$", f"last_edited: {today}", note, count=1, flags=re.M)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a people note.")
    parser.add_argument("name")
    parser.add_argument("--role", default="")
    parser.add_argument("--slug", default="")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--root", default=".", help="workspace root (default: current folder)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    path = root / "people" / f"{args.slug or slugify(args.name)}.md"
    if path.exists() and not args.force:
        print(f"exists: {path.relative_to(root)}")
        return 0

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_note(args.name, args.role))
    print(f"created: {path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
