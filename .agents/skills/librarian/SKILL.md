---
name: librarian
description: Process new material into the knowledge base — convert to markdown, categorise, and link it to related entries. Use when the user asks to process their inbox or reading list, run the librarian, update the knowledge base, file new articles or SOPs, or organise what they've saved.
last_edited: 2026-09-23
---

# Librarian

Turn raw material into structured, linked entries under `knowledge-base/`.
Run it whenever there's something to file: daily, weekly, or on demand.

## Workflow

1. **Read `knowledge-base/README.md`** for the current entry shape.
2. **Collect what's new.**
   - Always: every item in `knowledge-base/inbox/` (except `.gitkeep`). A
     `.txt` file of URLs is one item per URL; fetch each.
   - Optionally: unprocessed Raindrop bookmarks, if a Raindrop connector
     or API token is available in this session. Skip any bookmark whose ID
     already appears as a `source_id` in `knowledge-base/*.mmd`.
   - If both are empty, say so and stop.
3. **Convert to markdown.** Keep the substance; strip navigation, ads,
   cookie banners, and boilerplate.
4. **Categorise and link.** For each item, decide:
   - `type`: `sop` or `article`.
   - `category`: reuse a category already used in `knowledge-base/` where
     one fits, rather than inventing a near-duplicate.
   - `tags`: free-form labels.
   - `related`: existing entries this one is genuinely connected to. An
     empty list is a correct answer; don't force links.

   Use `/typesafe:typesafe-ai` (Jev) for this if it's available in the
   session. Otherwise, judge from the content and the existing entries'
   titles and categories.
5. **Write the entry.** Copy `templates/kb_entry.mmd` to
   `knowledge-base/<slug>.mmd` (lowercase-hyphenated slug from the title),
   fill every field, and set `created` and `last_edited` to today. Keep
   `tags` and `related` as single-line inline lists
   (`related: ["other-entry"]`); the repo's tests only parse single-line
   `key: value` frontmatter.
6. **Update the other side of every link.** For each entry named in the
   new entry's `related`, add the new slug to *that* entry's `related` (if
   it isn't there already) and bump its `last_edited`.
7. **Clear the inbox.** Delete each inbox item whose entry was written.
   Leave anything that failed in `inbox/`.
8. **Check.** Run `python -m pytest tests/test_knowledge_base.py` and fix
   anything it flags before reporting.

## Output

A short summary: entries created, links added (both sides), anything left
in `inbox/` and why, and any categorisation you weren't confident about.
