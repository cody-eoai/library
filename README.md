---
last_edited: 2026-09-23
---

# Library

A starter workspace for people who work alongside coding agents (Claude
Code, Codex, or both) across several projects at once. It gives an agent a
place to look before it acts, and gives every file a home.

## Setup

### 1. Get a copy

With git:

```sh
git clone https://github.com/cody-eoai/library.git
cd library
```

Or as a zip, no git needed: on GitHub, **Code → Download ZIP**, or from a
terminal:

```sh
gh api repos/cody-eoai/library/zipball/main > library.zip
unzip library.zip && mv cody-eoai-library-* library && cd library
```

### 2. Run first-time setup

Open the folder in Claude Code and run `/setup-library`, or in Codex ask
it to "set up this library". It will ask a few questions, personalise
`AGENTS.md`, create your real projects, and check everything works.

### Windows

`.claude/skills/` is made of symlinks. Git on Windows checks them out as
plain text files unless symlinks are enabled, and then Claude Code can't
find any skills. Before cloning, enable Developer Mode and run
`git config --global core.symlinks true`. The zip has the same problem
on Windows, so use git there. `python -m pytest tests` will tell you if
the links are broken.

## How it's organised

| Folder | What goes there |
| --- | --- |
| `projects/` | Long-lived work. `projects/example-project/` shows the layout. |
| `experiments/` | Short-lived spikes, named `exp-<topic>-YYYY-MM-DD`. |
| `people/` | Public-safe notes about collaborators (see `people/README.md`). |
| `knowledge-base/` | Linked reference material; drop raw items in `inbox/` (see `knowledge-base/README.md`). |
| `archive/` | Finished or retired work. |
| `templates/` | Starter files: project, experiment, goal, result, and knowledge-base entry. `people/` has its own `person.md` and `agent.md`. |
| `tmp/` | Gitignored scratch space. Nothing here is kept. |
| `tests/` | Checks that keep the structure honest (below). |

## Skills

| Skill | What it does |
| --- | --- |
| `setup-library` | First-run setup for a fresh copy. |
| `new-project` | Creates `projects/<slug>/` from the templates. |
| `new-experiment` | Creates `experiments/exp-<slug>-YYYY-MM-DD/`. |
| `new-person` | Creates `people/<slug>.md`. |
| `librarian` | Files everything in `knowledge-base/inbox/` (and, optionally, Raindrop) into linked `.mmd` entries. |

Every skill lives once, in `.agents/skills/<name>/`. Codex reads that
folder directly. Claude Code only reads `.claude/skills/`, so each skill
also has a symlink there. To add your own:

```sh
mkdir -p .agents/skills/<name>        # write .agents/skills/<name>/SKILL.md
ln -s ../../.agents/skills/<name> .claude/skills/<name>
```

**Skills from elsewhere.** If you install someone else's skill into
`.agents/skills/`, add its name to `skills-lock.json` under `"skills"`.
The frontmatter test skips anything listed there, since you don't own
that content. If your installer writes this file for you, leave it to
the installer.

## Tests

```sh
pip install pytest
python -m pytest tests
```

- `test_skills.py`: every markdown file carries a `last_edited` date,
  every skill of your own has the same frontmatter shape, and every skill
  is linked into `.claude/skills/`.
- `test_knowledge_base.py`: every knowledge-base entry has the required
  fields, and every `related` link is recorded on both sides.

They also run on every push via `.github/workflows/test.yml`.

## Design choices

- **One `AGENTS.md`, no `CLAUDE.md`.** Claude Code reads `AGENTS.md` when
  there's no `CLAUDE.md`, and Codex reads it natively, so one file serves
  both. Claude Code's docs call that fallback "not recommended for new
  projects", but a second file would either duplicate this one and drift,
  or depend on Claude choosing to open `AGENTS.md`. If Claude Code adds a
  way to import one file into another, switch to a thin `CLAUDE.md` that
  pulls `AGENTS.md` in.
- **Symlinks, not copies.** Each skill exists once, so a `.claude/skills/`
  copy can never fall out of date.
- **One scratch folder.** Only `tmp/` is disposable. Everything else has a
  named home, so nothing piles up at the root.

## Credit

Structurally descended from
[`jxnl/personal-monorepo-template`](https://github.com/jxnl/personal-monorepo-template).
