---
name: new-experiment
description: Bootstrap a short-lived experiment directory under experiments/ with a README from the template. Use when the user asks to start an experiment, spike, prototype, or a short-lived investigation, as distinct from a long-lived project.
last_edited: 2026-09-23
---

# New Experiment

Create a short-lived experiment that agents can discover later. This is the
`experiments/`-only counterpart to `new-project` — same underlying helper,
different default and no `AGENTS.md` by default (experiments are usually
too short-lived to need one).

## Workflow

1. Read root `AGENTS.md` and `README.md`.
2. Use a lowercase hyphenated topic. The helper turns it into
   `exp-<topic>-YYYY-MM-DD`.
3. Run the helper (shared with `new-project`, `--type experiment`):

```sh
python .codex/skills/new-project/scripts/new_project.py "Experiment Name" --type experiment --summary "One-line summary" --no-agents
```

Drop `--no-agents` if this experiment is likely to graduate into a project
and could use its own `AGENTS.md` from the start.

4. If the experiment graduates, move it into `projects/` and use
   `new-project`'s `templates/project_README.md` shape instead — don't
   leave a graduated experiment under `experiments/`.

## Output

Report the created folder and whether it should be revisited, paused, or
graduated per `templates/experiment_README.md`'s Status field.
