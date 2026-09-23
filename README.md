---
last_edited: 2026-09-23
---

# Library

A starter workspace for people who work alongside coding agents — Claude
Code, Codex, or both — across several projects at once.

It gives an agent a place to look before it acts:

- `projects/` for long-lived work
- `experiments/` for short-lived spikes
- `people/` for durable, public-safe notes about collaborators
- `knowledge-base/` for linked, structured reference material (SOPs,
  articles)
- `archive/` for completed or retired work
- `templates/` for the starter files everything else scaffolds from
- `tmp/` for scratch space that is gitignored on purpose — see "Everything
  Has A Place" in `AGENTS.md`

## Why this exists

Most agent-instruction files degrade into a pile of dos-and-don'ts that only
make sense to whoever wrote them. This template tries to keep three things
true instead:

1. **One instruction file.** `AGENTS.md` is the single source of truth for
   every agent — Claude Code reads it natively when no `CLAUDE.md` is
   present, Codex reads it as its root instructions. No forked, drifting
   copies per tool.
2. **Skills work the same way regardless of which agent you're using.**
   `.agents/skills/` is the agent-neutral home for anything you pull in from
   elsewhere; `.codex/skills/` holds Codex-specific skills; `.claude/skills/`
   is what Claude Code actually reads, kept as symlinks into the other two
   so there's one copy of the content, not three.
3. **Every file has a place.** Durable work lives under `projects/`,
   `experiments/`, `people/`, `knowledge-base/`, or `archive/`. `tmp/` is
   scratch — gitignored, never a home for anything you want to keep.

## Setup

### Option 1: git clone (recommended if you'll contribute back)

```sh
git clone <this-repo-url>
cd library
```

### Option 2: download the zip (no git required)

```sh
curl -L https://github.com/cody-eoai/library/releases/latest/download/library.zip -o library.zip
unzip library.zip -d library
cd library
```

On macOS you can use `ditto -x -k library.zip library` instead of `unzip`.
Every version tag (`vX.Y.Z`) repackages this zip via
`.github/workflows/release.yml` — `releases/latest/download/library.zip`
always points at the newest tagged release.

Either way: open the folder in Claude Code or Codex and start working —
both read `AGENTS.md` from the root.

### Adding skills

`.agents/skills/` holds two kinds of skill. **Repo-native** skills are
authored in this repo — `librarian` is one — no lock entry needed, they
*are* the source. **Externally-sourced** skills are pulled in from
elsewhere: install one under `.agents/skills/<name>/`, record where it came
from in `skills-lock.json` (source repo, path, content hash), then expose
it to Claude Code:

```sh
ln -s ../../.agents/skills/<name> .claude/skills/<name>
```

A Codex-specific skill (one that only makes sense under Codex — a
persistent assistant persona, thread automations) goes in
`.codex/skills/<name>/` instead, and is mirrored to Claude Code the same
way only if it's actually useful there:

```sh
ln -s ../../.codex/skills/<name> .claude/skills/<name>
```

Four skills ship with this template, all already wired up:

- `new-project` (`.codex/skills/`) — bootstrap a `projects/<slug>/`.
- `new-experiment` (`.codex/skills/`) — bootstrap an
  `experiments/exp-<slug>-YYYY-MM-DD/`.
- `new-person` (`.codex/skills/`) — bootstrap a `people/<slug>.md`.
- `librarian` (`.agents/skills/`) — process dumped material (reference
  implementation: Raindrop) into linked, categorized `knowledge-base/*.mmd`
  entries (reference categorizer: `typesafe-ai`'s Jev). See
  `knowledge-base/README.md` for the entry shape.

## Structure

- `projects/`: long-lived work. `projects/example-project/` shows the
  default layout.
- `experiments/`: short-lived spikes, named `exp-<topic>-YYYY-MM-DD`.
- `people/`: notes about collaborators, human or agent. Keep this
  public-safe — see `people/README.md`.
- `knowledge-base/`: linked, structured reference material — see
  `knowledge-base/README.md`.
- `archive/`: completed or retired work.
- `templates/`: starter files (`project_README.md`, `experiment_README.md`,
  `PROJECT_AGENTS.md`, `GOAL.md`, `RESULT.md`, `people/person.md`,
  `people/agent.md`, `kb_entry.mmd`).
- `tests/`: repo-integrity checks — `test_skills.py` verifies every
  markdown file carries a `last_edited` date and every repo-native skill's
  frontmatter has the right shape; `test_knowledge_base.py` verifies every
  `knowledge-base/*.mmd` entry has the required fields and that every
  `related` link is recorded on both sides.
- `.agents/`, `.codex/`, `.claude/`: skills, per the "Adding skills" section
  above.
- `.github/workflows/release.yml`: packages `library.zip` on every version
  tag — what Option 2 above downloads.

## Credit

Structurally descended from
[`jxnl/personal-monorepo-template`](https://github.com/jxnl/personal-monorepo-template),
with Claude Code skill support, the single-`AGENTS.md` convention, and the
`tmp` scratch-space rule added on top.
