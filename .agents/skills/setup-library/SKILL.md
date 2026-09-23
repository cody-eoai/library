---
name: setup-library
description: First-run setup for a freshly downloaded copy of this template — personalise the agent instructions, create the user's real projects, and check everything works. Use when the user has just cloned or unzipped the repo, says "set this up", "get me started", or "onboard me", or the README has no Active Projects section yet.
last_edited: 2026-09-23
---

# Set Up Library

Turn a fresh copy of the template into the user's own workspace. Ask one
question at a time, and take the default whenever they don't care.

## Workflow

1. **Read** `AGENTS.md` and `README.md`. If `README.md` already has an
   `## Active Projects` section, setup has run before: ask what they want
   to change rather than starting over.
2. **How should agents work with you?** Ask about tone, how much pushback
   they want, and anything agents must never do. Rewrite the Collaboration
   Style and Safety sections of `AGENTS.md` to match, keeping the existing
   bullets for anything they don't mention. Bump its `last_edited`.
3. **What are you working on?** For each piece of work, create it with the
   `new-project` skill (long-lived) or `new-experiment` (a short spike).
   Then add an `## Active Projects` section near the top of `README.md`
   with one line per entry: ``- `projects/<slug>/`: <one-line summary>``.
4. **Remove the example?** Once there's at least one real project, offer to
   delete `projects/example-project/`. Only delete it if they say yes.
5. **Who do you work with?** Offer to create notes for key collaborators
   with `new-person`. Skip it if they'd rather not. Keep notes public-safe
   (see `people/README.md`).
6. **Knowledge base.** Explain in two sentences: drop material into
   `knowledge-base/inbox/`, then run the `librarian` skill. Ask whether
   they save articles to Raindrop; if so, note that the librarian can pull
   from it once a Raindrop connector or API token is set up.
7. **Check it works.** Run `python -m pytest tests`. On Windows, a failing
   `test_every_skill_is_mirrored_for_claude_code` means git checked the
   `.claude/skills` links out as plain files; see the README's Windows
   note.
8. **Version control.** If the folder isn't a git repo, offer to run
   `git init` and make a first commit. Ask before doing either, and never
   push or create a remote without an explicit yes.

## Output

A short summary: what changed in `AGENTS.md`, projects and people created,
whether the example was removed, and the test result.
