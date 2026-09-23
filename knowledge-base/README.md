---
last_edited: 2026-09-23
---

# Knowledge Base

Durable reference material — SOPs and articles — stored as linked,
searchable `.mmd` (MultiMarkdown) files with metadata. Populated by the
`librarian` skill (`.agents/skills/librarian`), which pulls from a dump
source (e.g. Raindrop), converts each item to markdown, and categorizes and
links it into this folder.

## Shape

Each entry is one `.mmd` file, built from `templates/kb_entry.mmd`:

- `title` — entry title.
- `type` — `sop` or `article`.
- `source` — the origin URL, or `manual` if there isn't one.
- `saved_from` — where it was pulled from (`raindrop`, `manual`, `other`).
- `raindrop_bookmark_id` — set when `saved_from: raindrop`, blank otherwise.
- `category` — a single top-level grouping, assigned during processing.
- `tags` — free-form labels.
- `related` — other entry filenames (without `.mmd`) this one is linked to.
  Links are **bidirectional**: when entry A is linked to entry B, both
  files carry the relationship in `related`. This is a deliberate
  trade-off — `.mmd` doesn't get Obsidian-style automatic backlinks, so the
  librarian skill maintains both sides by hand. If you'd rather keep links
  one-directional (only the newer entry records the relationship), that's a
  one-line change to the skill's workflow.
- `created` / `last_edited` — dates, `YYYY-MM-DD`.

## Adding entries

Run the `librarian` skill rather than writing entries by hand where
possible — it fills `category`, `tags`, and `related` for you. See
`.agents/skills/librarian/SKILL.md`.
