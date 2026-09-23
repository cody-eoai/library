---
name: librarian
description: File new reading material into a linked knowledge base of .mmd entries — convert each item to markdown, categorise it, and link it to related entries. Use when the user asks to process their inbox or reading list, run the librarian, update the knowledge base, file new articles or SOPs, or organise what they've saved.
metadata:
  last_edited: 2026-09-23
---

# Librarian

Turn raw material into structured, linked entries in `knowledge-base/`.
Run it whenever there's something to file: daily, weekly, or on demand.

## Entry shape

One `.mmd` file per item, at `knowledge-base/<slug>.mmd`, built from this
skill's `assets/kb_entry.mmd`:

- `title`, `type` (`sop` or `article`), `source` (URL, or `manual`)
- `saved_from` (`inbox`, `raindrop`, `manual`, or `other`) and `source_id`
  (the item's ID in that source, so it's never filed twice; blank for
  inbox and manual items)
- `category`: one top-level grouping
- `tags` and `related`: single-line inline lists, e.g.
  `related: ["other-entry"]`. `related` holds other entries' filenames
  without `.mmd`.
- `created` and `last_edited`: `YYYY-MM-DD`

Links are two-way: if A lists B in `related`, B lists A.

## Workflow

1. **Find the knowledge base.** Work in `knowledge-base/` at the workspace
   root, creating it and `knowledge-base/inbox/` if they don't exist. If
   the workspace has a `knowledge-base/README.md`, read it for local rules.
   If there's no workspace folder at all (e.g. a chat), take the material
   the user pasted or attached and hand the finished entries back as
   files.
2. **Collect what's new.**
   - Everything in `knowledge-base/inbox/` except `.gitkeep`. A `.txt`
     file of URLs is one item per URL; fetch each.
   - Optionally, unprocessed Raindrop bookmarks, if a Raindrop connector
     or API token is available. Skip any whose ID already appears as a
     `source_id` in an existing entry.
   - If there's nothing new, say so and stop.
3. **Convert to markdown.** Keep the substance; strip navigation, ads,
   cookie banners, and boilerplate.
4. **Categorise and link.** Decide `type`, `category`, `tags`, and
   `related` for each item. Reuse a category already in use where one
   fits, rather than inventing a near-duplicate. Only link entries that
   are genuinely connected; an empty `related` list is a correct answer.
   Use `/typesafe:typesafe-ai` (Jev) for this if it's available;
   otherwise judge from the content and the existing entries.
5. **Write the entry** from `assets/kb_entry.mmd`, filling every field and
   setting `created` and `last_edited` to today.
6. **Update the other side of every link.** Add the new slug to each
   related entry's `related` list (if it isn't there already) and bump
   that entry's `last_edited`.
7. **Clear the inbox.** Delete each inbox item whose entry was written.
   Leave anything that failed in `inbox/`.
8. **Check.** If the workspace has `tests/test_knowledge_base.py`, run it
   and fix anything it flags.

## Output

A short summary: entries created, links added (both sides), anything left
in the inbox and why, and any categorisation you weren't confident about.
