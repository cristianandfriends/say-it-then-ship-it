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
2. Read [bootstrap-lab](../.agents/skills/bootstrap-lab/SKILL.md), then ask your agent to use it with the prompt below. Replace the paths with your workshop and project folders. Keep the two folders separate.

```text
Use the bootstrap-lab skill. Read and follow
workshop/.agents/skills/bootstrap-lab/SKILL.md.

Ask whether I use GitHub Copilot or OpenCode.
Install the starter skills, engineering agent, and project instructions
from workshop into student-project.
Show me the plan and ask for approval before changing files.
I will choose my project idea in level 1. Leave project planning until then.
```

3. Answer the harness question and approve the bootstrap operation after reviewing the plan. The agent runs the skill's included Python installer; you do not need to type its script path. If your harness does not discover the skill, it can read and follow the file named in the prompt.
4. Inspect the installer result. If it reports a modified-file collision, inspect the difference rather than overwrite your work.

You need no packages or virtual environment to copy the starter material. When your project needs a PyPI dependency, ask the agent to follow [Prepare Python dependencies](../.agents/skills/bootstrap-lab/SKILL.md#prepare-python-dependencies) in the same skill.

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
