---
name: librarian
description: Process new material into the knowledge base — convert to markdown, categorize, and link it to related entries. Use when the user asks to process their reading list, run the librarian, update the knowledge base, file new articles or SOPs, or organize what they've saved.
last_edited: 2026-09-23
---

# Librarian

Turn dumped source material (a reading list, saved articles, written-up
SOPs) into structured, linked entries under `knowledge-base/`. This is an
agent-run skill: invoke it when you want the knowledge base processed —
daily, weekly, or on demand — there is no unattended automation here.

The reference implementation below pulls from Raindrop and categorizes with
`typesafe-ai`'s Jev. Neither is a hard requirement: swap the source or the
categorizer for whatever you actually have, as long as the output still
matches the shape in `knowledge-base/README.md`.

## Workflow

1. **Read `knowledge-base/README.md`** for the current metadata shape
   before writing anything.
2. **Find what's new.** Pull unprocessed items from the dump source (e.g.
   Raindrop bookmarks not yet represented by a `raindrop_bookmark_id` in
   `knowledge-base/*.mmd`). If no source integration is configured, ask the
   user for the items directly (URLs, pasted text, or files).
3. **Convert to markdown.** Fetch each item's content and turn it into
   clean markdown — strip navigation, ads, and boilerplate; keep the
   substance.
4. **Categorize and link.** For each item, determine:
   - `type`: `sop` or `article`.
   - `category`: a single top-level grouping, consistent with categories
     already in use in `knowledge-base/` — scan existing entries' `category`
     values first rather than inventing near-duplicates.
   - `tags`: free-form labels.
   - `related`: existing entries this one is meaningfully connected to.

   Use `/typesafe:typesafe-ai` (Jev) for this when it's available in the
   session; otherwise use your own judgment from the converted content and
   the existing entries' titles/descriptions. Do not force a `related` link
   that isn't genuinely there — an empty list is a correct result.
5. **Write the entry.** Copy `templates/kb_entry.mmd` into
   `knowledge-base/<slug>.mmd` (lowercase-hyphenated slug from the title),
   fill every field, and set `created`/`last_edited` to today. Keep `tags`
   and `related` as single-line inline lists — `tags: ["a", "b"]`,
   `related: ["other-entry-slug"]` — not multi-line YAML blocks; the repo's
   frontmatter tooling only parses single-line `key: value` pairs.
6. **Update the other side of every link.** For each filename listed in the
   new entry's `related`, open that existing file and add the new entry's
   slug to *its* `related` list too (if not already present), bumping its
   `last_edited`. Links are bidirectional — see `knowledge-base/README.md`
   for why.
7. **Report.** List what was created, what got linked to what, and flag
   anything you weren't confident categorizing so the user can fix it by
   hand.

## Output

A summary of new entries written, links updated on both sides, and any
low-confidence categorizations that need a human look.
