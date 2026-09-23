---
name: new-person
description: Create or update a public-safe note about a collaborator under people/ from a template. Use when the user asks to add a collaborator, create a person profile, remember someone's preferences or working style, or make a people note.
metadata:
  last_edited: 2026-09-23
---

# New Person

Create a durable, public-safe note about a human collaborator.

## Workflow

1. If the workspace has a `people/README.md`, read it for local rules.
2. From the workspace root, run the script bundled with this skill:

```sh
python <this skill's folder>/scripts/new_person.py "Person Name" --role "Role or context"
```

It creates `people/<slug>.md` from this skill's `assets/person.md`,
stamped with today's date. It won't overwrite an existing note unless you
pass `--force`.

3. Fill in only useful, non-sensitive context: how you work together,
   preferences, open threads.
4. Keep secrets, account data, health details, and anything confidential
   out of the note. These notes may be shared or committed.

## Output

Report the created or updated path and any fields that still need the
user's input.
