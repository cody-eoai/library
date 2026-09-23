---
last_edited: 2026-09-23
---

# Root Agent Instructions

Shared instructions for every agent working in this repo (Claude Code,
Codex, or anything else that reads `AGENTS.md`).

## Collaboration Style

- Match the user's tone: direct, practical, low-ceremony, and comfortable
  with rough edges while the work is still forming.
- When a request is blurry, ask the smallest useful question that would
  change the work. When the tradeoff is minor or reversible, make a
  sensible call and keep moving.
- Push back when a request would create churn, hide important context,
  hurt maintainability, leak private data, or skip a needed check. Say
  so briefly, offer the better path, then proceed.
- Prefer concrete work over abstract planning. Lead summaries with what
  changed, what was verified, and what still needs attention.

## Start Here

- Discover work through `projects/`, `experiments/`, and `README.md`.
- If the task names a project, experiment, person, or skill, find it
  before planning changes.
- Read the nearest `AGENTS.md` before working in a subdirectory. Nested
  files supplement this one; where they conflict, follow the more specific
  one and mention the conflict.

## Everything Has A Place

- `projects/`: long-lived work.
- `experiments/`: short-lived spikes, named `exp-<topic>-YYYY-MM-DD`.
- `people/`: public-safe notes about collaborators, human or agent.
- `knowledge-base/`: linked reference material. Raw material goes in
  `knowledge-base/inbox/` until the `librarian` skill files it.
- `archive/`: finished or retired work, moved here rather than deleted.
- `templates/`: starter files for everything above.
- `tmp/`: gitignored scratch space. Move anything worth keeping out of it.

Nothing durable lives loose at the repo root. If nothing above fits, ask
where it should go.

## Durable State

- Project status: the project's `README.md`.
- Long-running objectives: `GOAL.md`. Completed work and verification:
  `RESULT.md`.
- Collaborator notes: `people/*.md`.
- Update the relevant `README.md` when adding, archiving, renaming, or
  changing the status of work. Don't leave decisions only in chat when
  they'll matter later.

## Skills

Skills live in `.agents/skills/<name>/` (Codex reads this folder
directly). Claude Code reads `.claude/skills/`, which holds a symlink to
each one. When you add a skill, link it:
`ln -s ../../.agents/skills/<name> .claude/skills/<name>`.

- `setup-library`: first-run setup for a fresh copy of this template.
- `new-project`, `new-experiment`, `new-person`: create entries from
  `templates/`.
- `librarian`: file `knowledge-base/inbox/` (and other sources) into
  linked knowledge-base entries.

## Safety

- Never commit secrets, credentials, account numbers, private keys, or
  private personal data.
- Ask before external side effects (sending messages, spending money,
  deleting data, changing accounts, public or shared writes) and before
  anything destructive or hard to undo.
- If data is stale or copied from memory, verify it before relying on it.
- Run `python -m pytest tests` after structural changes. If you can't run
  a check, say exactly what wasn't run and why.
