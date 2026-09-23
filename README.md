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
- `archive/` for completed or retired work
- `templates/` for the starter files everything else scaffolds from
- `tmp/` and `output/` for scratch space that is gitignored on purpose —
  see "Everything Has A Place" in `AGENTS.md`

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
   `experiments/`, `people/`, or `archive/`. `tmp/` and `output/` are
   scratch — gitignored, never a home for anything you want to keep.

## Setup

```sh
git clone <this-repo-url>
cd library
```

Open it in Claude Code or Codex and start working — both read `AGENTS.md`
from the root.

### Adding skills

`.agents/skills/` and `skills-lock.json` start empty. To add a skill from
an external source, install it under `.agents/skills/<name>/`, record where
it came from in `skills-lock.json` (source repo, path, content hash), then
expose it to Claude Code:

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

Two example skills ship with this template — `new-project` and
`new-person` — both already wired up under `.codex/skills/` and mirrored to
`.claude/skills/`.

## Structure

- `projects/`: long-lived work. `projects/example-project/` shows the
  default layout.
- `experiments/`: short-lived spikes, named `exp-<topic>-YYYY-MM-DD`.
- `people/`: notes about collaborators, human or agent. Keep this
  public-safe — see `people/README.md`.
- `archive/`: completed or retired work.
- `templates/`: starter files (`project_README.md`, `experiment_README.md`,
  `PROJECT_AGENTS.md`, `GOAL.md`, `RESULT.md`, `people/person.md`,
  `people/agent.md`).
- `tests/`: repo-integrity checks (`test_skills.py` verifies every
  markdown file carries a `last_edited` date and every Codex skill's
  frontmatter has the right shape).
- `.agents/`, `.codex/`, `.claude/`: skills, per the "Adding skills" section
  above.

## Credit

Structurally descended from
[`jxnl/personal-monorepo-template`](https://github.com/jxnl/personal-monorepo-template),
with Claude Code skill support, the single-`AGENTS.md` convention, and the
`tmp`/`output` scratch-space rule added on top.
