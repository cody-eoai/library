"""Package this repo's own skills as uploadable .zip files in dist/skills/.

Each zip holds <name>/SKILL.md plus the skill's scripts and assets, with
symlinks replaced by the files they point to, so an uploaded skill works
without the rest of the repo. Skills listed in skills-lock.json are
vendored from elsewhere and aren't packaged.

    python dist/build_skills.py          # validate and rebuild
    python dist/build_skills.py --check  # fail if any zip is stale
"""

from __future__ import annotations

import io
import json
import os
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"
OUT = ROOT / "dist" / "skills"

# The Agent Skills spec, as enforced on upload to Claude.
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SKIP_NAMES = {".DS_Store", "__pycache__"}
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def skill_dirs() -> list[Path]:
    lock = ROOT / "skills-lock.json"
    locked = set(json.loads(lock.read_text()).get("skills", {})) if lock.exists() else set()
    return sorted(
        d for d in SKILLS.glob("*") if (d / "SKILL.md").is_file() and d.name not in locked
    )


def read_frontmatter(skill_md: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Return (top-level keys, metadata keys). Values are single-line strings."""
    text = skill_md.read_text()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("no frontmatter")
    top: dict[str, str] = {}
    metadata: dict[str, str] = {}
    current = None
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        key, _, value = line.strip().partition(":")
        if line[0].isspace():
            if current != "metadata":
                raise ValueError(f"unexpected indented line: {line!r}")
            metadata[key] = value.strip()
        else:
            current = key
            top[key] = value.strip()
    return top, metadata


def files_in(skill: Path) -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(skill):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_NAMES)
        for name in sorted(filenames):
            if name not in SKIP_NAMES and not name.endswith(".pyc"):
                found.append(Path(dirpath) / name)
    return found


def validate(skill: Path) -> list[str]:
    try:
        top, metadata = read_frontmatter(skill / "SKILL.md")
    except ValueError as error:
        return [f"{skill.name}: {error}"]
    errors = []
    if unexpected := set(top) - ALLOWED_KEYS:
        errors.append(f"{skill.name}: frontmatter keys not allowed on upload: {sorted(unexpected)}")
    name, description = top.get("name", ""), top.get("description", "")
    if name != skill.name:
        errors.append(f"{skill.name}: name {name!r} must match the folder name")
    if not NAME_RE.match(name) or len(name) > 64:
        errors.append(f"{skill.name}: name must be kebab-case, 64 characters max")
    if not description or len(description) > 1024:
        errors.append(f"{skill.name}: description must be 1-1024 characters")
    if "<" in description or ">" in description:
        errors.append(f"{skill.name}: description can't contain < or >")
    if not DATE_RE.match(metadata.get("last_edited", "")):
        errors.append(f"{skill.name}: metadata.last_edited must be a YYYY-MM-DD date")
    skill_mds = [p for p in files_in(skill) if p.name == "SKILL.md"]
    if len(skill_mds) != 1:
        errors.append(f"{skill.name}: must contain exactly one SKILL.md")
    for path in files_in(skill):
        if not path.exists():
            errors.append(f"{skill.name}: broken link {path.relative_to(skill)}")
    return errors


def expected_contents(skill: Path) -> dict[str, bytes]:
    """What the zip should hold: archive path -> file bytes (links followed)."""
    return {
        f"{skill.name}/{path.relative_to(skill).as_posix()}": path.read_bytes()
        for path in files_in(skill)
    }


def build(skill: Path) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for arcname, data in expected_contents(skill).items():
            info = zipfile.ZipInfo(arcname, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if arcname.endswith((".py", ".sh")) else 0o644
            info.external_attr = (0o100000 | mode) << 16
            archive.writestr(info, data)
    return buffer.getvalue()


def zip_contents(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def stale() -> list[str]:
    """Skills whose zip is missing or doesn't match the source, plus orphan zips."""
    problems = []
    skills = skill_dirs()
    for skill in skills:
        target = OUT / f"{skill.name}.zip"
        if not target.exists() or zip_contents(target) != expected_contents(skill):
            problems.append(f"dist/skills/{skill.name}.zip is out of date")
    names = {s.name for s in skills}
    problems += [
        f"dist/skills/{z.name} has no matching skill"
        for z in OUT.glob("*.zip")
        if z.stem not in names
    ]
    return problems


def main() -> int:
    errors = [e for skill in skill_dirs() for e in validate(skill)]
    if errors:
        print("\n".join(errors))
        return 1
    if "--check" in sys.argv:
        problems = stale()
        print("\n".join(problems) or "all skill zips are up to date")
        return 1 if problems else 0
    OUT.mkdir(parents=True, exist_ok=True)
    names = set()
    for skill in skill_dirs():
        (OUT / f"{skill.name}.zip").write_bytes(build(skill))
        names.add(skill.name)
        print(f"built dist/skills/{skill.name}.zip")
    for orphan in OUT.glob("*.zip"):
        if orphan.stem not in names:
            orphan.unlink()
            print(f"removed dist/skills/{orphan.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
