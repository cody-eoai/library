---
last_edited: 2026-09-23
---

# Knowledge Base

Durable reference material (SOPs and articles) stored as linked,
searchable `.mmd` (MultiMarkdown) files with metadata. The `librarian` skill
(`.agents/skills/librarian`) fills it: it converts each new item to
markdown, categorises it, and links it to related entries.

## Adding material

Drop anything into `knowledge-base/inbox/`: an article saved as a file, a
PDF, pasted notes, or a `.txt` file with one URL per line. Then run the
`librarian` skill. Each item becomes one entry here, and the raw item is
removed from `inbox/` once its entry is written (the entry keeps the
content and the `source`). Anything the librarian can't process stays in
`inbox/` and is reported back to you.

Other sources are optional. If you save articles to Raindrop and a
Raindrop connector or API token is available, the librarian can pull
unprocessed bookmarks from there too.

## Entry shape

Each entry is one `.mmd` file, built from `templates/kb_entry.mmd`:

- `title`: entry title.
- `type`: `sop` or `article`.
- `source`: the origin URL, or `manual` if there isn't one.
- `saved_from`: where it came in from (`inbox`, `raindrop`, `manual`,
  `other`).
- `source_id`: the item's ID in that source (e.g. a Raindrop bookmark ID),
  so it's never processed twice. Blank for inbox and manual items.
- `category`: one top-level grouping.
- `tags`: free-form labels, as an inline list: `tags: ["a", "b"]`.
- `related`: other entry filenames (without `.mmd`) this one links to, as
  an inline list. Links are **bidirectional**: when entry A lists B, B
  lists A too. `.mmd` files don't get Obsidian-style automatic backlinks,
  so the librarian keeps both sides in step, and
  `tests/test_knowledge_base.py` checks it.
- `created` / `last_edited`: dates, `YYYY-MM-DD`.
