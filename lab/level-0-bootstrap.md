---
title: "Level 0: Bootstrap your project"
description: Inspect the workshop and install instructions into a separate project.
order: 1
level: 0
---

# Level 0: Bootstrap your project

## Goal

Choose a harness and install project instructions without building an app.

## Input and task

Use the supplied workshop folder and a separate empty student project. Choose GitHub Copilot or OpenCode from the access your facilitator provides. Do not install a harness. You will choose what to build in level 1; this level prepares the workspace.

1. Open this file as Markdown source. Find the YAML frontmatter between `---` lines, the heading, a link, and a code fence. Explain which fields describe the page and which text gives the task.
2. Read [bootstrap-lab](../.agents/skills/bootstrap-lab/SKILL.md). If your harness does not discover it, ask the agent to read `workshop/.agents/skills/bootstrap-lab/SKILL.md` and follow it. Reading the file is a supported way to invoke these instructions.
3. Give the agent your harness, workshop path, and destination path. Ask it to install the starter material and leave project-specific planning for level 1. Keep the two folders separate.
4. Approve the bootstrap operation. From the workshop's parent folder, the script command has this form:

```text
python workshop/.agents/skills/bootstrap-lab/scripts/bootstrap_lab.py --harness copilot --target student-project
```

Use `--harness opencode` for OpenCode. The script infers the source from its location; `--source workshop` can name it. It needs no dependencies. If it reports a modified-file collision, inspect the difference rather than overwrite your work.

Inspect the generated `AGENTS.md`, skills, and software-engineering-expert agent. Record the paths for your harness:

| Harness | Skills | Agent |
| --- | --- | --- |
| Copilot | `.github/skills/` | `.github/agents/software-engineering-expert.agent.md` |
| OpenCode | `.opencode/skills/` | `.opencode/agents/software-engineering-expert.md` |

Both use Markdown instructions, but the harnesses expect different agent frontmatter. Preserve that metadata. Keep Python-only constraints in your project instructions. Do not build Astro or run the workshop website.

## Evidence and checkpoint

Save the selected harness, source and destination paths, bootstrap command/result, and generated file paths. Ask the agent to identify one instruction it read from the generated project `AGENTS.md`. Inspect that instruction yourself. Confirm the bootstrap installed bootstrap-lab, stop-slop, frontend-design, and software-engineering-expert.

<details>
<summary>Hint</summary>

Open a `SKILL.md` and an agent file beside each other. A skill describes a reusable procedure. An agent file assigns a role and harness metadata. Neither file requires a new app dependency.

</details>

Previous: [Start here](start-here.md) · Next: [Level 1: Write the brief](level-1-brief.md)
