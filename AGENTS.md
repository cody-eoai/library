---
last_edited: 2026-09-23
---

# Root Agent Instructions

Claude Code reads this file natively. Codex, and any other AGENTS.md-aware
tool, reads it too — this is the single, agent-neutral source of truth for
how to work in this repo. Do not fork it into a separate `CLAUDE.md`; see
"Skills" below for why.

## Default Model

Use the strongest available coding model unless the user or task explicitly
calls for a different model.

## Collaboration Style

- Match the user's tone: direct, practical, low-ceremony, and comfortable
  with rough edges while the work is still forming.
- Be curious before being certain. When the request is blurry, ask the
  smallest useful question that would change the work.
- Do not ask questions just to avoid making a reasonable call. If the
  tradeoff is minor or reversible, choose a sensible default and keep moving.
- Push back when a request is likely to create churn, hide important
  context, damage future maintainability, leak private data, or skip a
  necessary verification step.
- Name disagreements plainly and briefly. Offer the better path, explain the
  reason, and then proceed when the direction is clear.
- Prefer concrete work over abstract planning. Show progress through edits,
  checks, and durable notes.
- Keep summaries concise and useful. Lead with what changed, what was
  verified, and what still needs attention.
- Avoid generic assistant voice. Do not over-explain obvious steps, apologize
  performatively, or pad responses with motivational filler.

## Start Here

- Start with `projects/`, `experiments/`, and `README.md` for discovery.
- If the task names a project, experiment, person, agent, or skill, locate
  it before planning changes.
- Read the nearest relevant `AGENTS.md` before working in any subdirectory.
- Nested `AGENTS.md` files supplement these root rules unless they conflict.
  When they conflict, follow the more specific local rule and mention the
  conflict in your summary.

## Everything Has A Place

Every file belongs somewhere on purpose:

- `projects/` — long-lived work.
- `experiments/` — short-lived spikes, named `exp-<topic>-YYYY-MM-DD`.
- `people/` — durable, public-safe notes about collaborators (human or agent).
- `archive/` — completed or retired work, moved here instead of deleted.
- `templates/` — the starter files this repo scaffolds new entries from.
- `tmp/` and `output/` — scratch space only. Both are gitignored: nothing
  placed there is expected to survive or ship. If something in `tmp/` or
  `output/` turns out to matter, move it into `projects/`, `archive/`, or
  wherever it actually belongs — do not leave durable state in scratch dirs.

Nothing durable lives loose at the repo root. If you're about to create a
file and none of the above feels right, stop and ask where it should go
rather than guessing.

## Durable State

Keep important context on disk:

- Project status belongs in project `README.md` files.
- Long-running objectives belong in `GOAL.md`.
- Completed work and verification belong in `RESULT.md`.
- Human and agent collaboration notes belong in `people/*.md`.
- Cross-project discovery belongs in repo-level docs such as `README.md`.

Do not leave decisions only in chat when they will matter later.

## Working On Projects

- Use `projects/` for long-lived work and `experiments/` for short-lived
  spikes.
- When creating a new project, use the `new-project` skill
  (`.codex/skills/new-project`, mirrored at `.claude/skills/new-project`) or
  follow `templates/project_README.md` and `templates/PROJECT_AGENTS.md`.
- When creating a new person note, use the `new-person` skill
  (`.codex/skills/new-person`, mirrored at `.claude/skills/new-person`) or
  follow `people/person.md`.
- Update the relevant project or experiment `README.md` when adding,
  archiving, renaming, or changing the status of work.
- Before editing, read enough surrounding context to understand the local
  pattern.
- Keep changes small and reversible unless the user explicitly asks for a
  larger reshaping.
- If a request points at a symptom, look one level deeper for the cause
  before patching.

## Safety

- Do not commit secrets, credentials, account numbers, private keys, or
  private personal data.
- Do not perform external side effects such as sending messages, spending
  money, placing orders, deleting data, or changing account state without
  explicit user approval.
- Prefer small, reversible edits and focused validation.
- If data is stale or copied from memory, verify it before treating it as
  current.
- Ask before destructive actions, irreversible account changes,
  public/shared writes, or anything that could surprise the user later.
- Push back instead of silently complying when the safer or more useful
  move is different from the literal request.
- When validation is blocked, say exactly what was not run and why.

## Skills

Skills are meant to be read and used in place. Do not assume they are
installed globally.

- `.agents/skills/` is the agent-neutral home for skills pulled from
  external sources. `skills-lock.json` tracks where each one came from
  (source repo, path, content hash) so it can be re-synced. It starts empty
  in this template — add skills the same way you'd add any other dependency.
- `.codex/skills/` holds Codex-specific skills. Most only make sense under
  Codex (a persistent assistant persona, thread heartbeats, goal trees) and
  stay there. `new-project` and `new-person` are plain repo-bootstrapping,
  so they're also mirrored to Claude Code.
- `.claude/skills/` is what Claude Code actually reads. Claude Code has no
  native way to "import" skills from elsewhere, so every skill it should see
  needs an actual entry here — this template uses a symlink into
  `.agents/skills/` or `.codex/skills/` rather than a copy, so there's one
  copy of the content and no drift.
- When you add a skill to `.agents/skills/`, or want to expose a
  `.codex/skills/` skill to Claude Code, mirror it by hand:
  `ln -s ../../.agents/skills/<name> .claude/skills/<name>` (or
  `../../.codex/skills/<name>` for a Codex-specific one).

**Why one `AGENTS.md` instead of a separate `CLAUDE.md`:** Claude Code loads
`CLAUDE.md` when present and falls back to `AGENTS.md` only when no
`CLAUDE.md` exists — and Claude Code's own docs call that fallback "not
recommended for new projects." This template accepts that trade-off
deliberately: a second file would either duplicate this one (drift risk) or
need Claude to be told to go read `AGENTS.md` itself (an extra, skippable
step). One file, one set of rules, every agent reads the same thing. If
Claude Code ever adds a real import mechanism, switch to a thin `CLAUDE.md`
that pulls this file in instead of forking it.
