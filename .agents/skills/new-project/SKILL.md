---
name: new-project
description: Create a new long-lived project folder with a README and AGENTS.md from templates. Use when the user asks to create or start a project, add a workspace entry, scaffold a project folder, or set up durable work that other agents should be able to find later.
metadata:
  last_edited: 2026-09-23
---

# New Project

Create a project that agents can discover later.

## Workflow

1. If the workspace has an `AGENTS.md` or `README.md` at its root, read
   them first; they may have naming or placement rules.
2. Decide whether this is really a long-lived project. For a short spike,
   use the `new-experiment` skill instead.
3. From the workspace root, run the script bundled with this skill
   (`scripts/new_project.py` in this skill's folder):

```sh
python <this skill's folder>/scripts/new_project.py "Project Name" --summary "One-line summary"
```

It creates `projects/<slug>/README.md` and `AGENTS.md` from the templates
in this skill's `assets/`, stamped with today's date. Add `--no-agents` to
skip `AGENTS.md`, or `--root PATH` to target a different folder.

4. Fill in project-specific commands, sources of truth, and safety gates
   in the new `AGENTS.md` if they matter.
5. If the workspace `README.md` lists active projects, add this one.

## Output

Report the created folder and any fields that still need the user's input.
