---
name: new-experiment
description: Create a short-lived experiment folder with a README from a template. Use when the user asks to start an experiment, spike, prototype, or short investigation, as distinct from a long-lived project.
metadata:
  last_edited: 2026-09-23
---

# New Experiment

Create a short-lived experiment that agents can discover later.

## Workflow

1. If the workspace has an `AGENTS.md` or `README.md` at its root, read
   them first.
2. From the workspace root, run the script bundled with this skill:

```sh
python <this skill's folder>/scripts/new_project.py "Experiment Name" --type experiment --summary "One-line summary" --no-agents
```

It creates `experiments/exp-<topic>-YYYY-MM-DD/README.md` from this skill's
`assets/`. Drop `--no-agents` if the experiment may graduate into a
project and could use its own `AGENTS.md` from the start.

3. If the experiment graduates, move it into `projects/` and reshape its
   README as a project README. Don't leave a graduated experiment under
   `experiments/`.

## Output

Report the created folder, and whether the experiment should continue,
pause, or graduate (the README's Status and Decision Criteria sections).
