from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


# absolute(), not resolve(): new-experiment links to this file and should use
# its own bundled assets, not new-project's.
ASSETS = Path(__file__).absolute().parent.parent / "assets"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "new-project"


def stamp(text: str, today: str) -> str:
    return re.sub(r"^last_edited: .*$", f"last_edited: {today}", text, count=1, flags=re.M)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a project or experiment.")
    parser.add_argument("name")
    parser.add_argument("--type", choices=["project", "experiment"], default="project")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--slug", default="")
    parser.add_argument("--no-agents", action="store_true")
    parser.add_argument("--root", default=".", help="workspace root (default: current folder)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    today = date.today().isoformat()
    entry_id = args.slug or slugify(args.name)
    if args.type == "experiment":
        if not entry_id.startswith("exp-"):
            entry_id = f"exp-{entry_id}-{today}"
        project_dir = root / "experiments" / entry_id
        template = ASSETS / "experiment_README.md"
    else:
        project_dir = root / "projects" / entry_id
        template = ASSETS / "project_README.md"

    rel_path = project_dir.relative_to(root).as_posix()
    if project_dir.exists():
        raise FileExistsError(f"path already exists: {rel_path}")

    project_dir.mkdir(parents=True)
    readme = template.read_text()
    for placeholder in ("<Project Name>", "<Experiment Name>"):
        readme = readme.replace(placeholder, args.name)
    readme = readme.replace("<Summary>", args.summary)
    (project_dir / "README.md").write_text(stamp(readme, today))
    if not args.no_agents:
        agents = (ASSETS / "PROJECT_AGENTS.md").read_text()
        (project_dir / "AGENTS.md").write_text(stamp(agents, today))

    print(f"created: {rel_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
