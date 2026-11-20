---
title: "Level 0: Bootstrap your project"
description: Use bootstrap-lab to set up your own project folder.
order: 1
level: 0
---

# Level 0: Bootstrap your project

## Goal

Use a skill to copy starter instructions into your project folder.

## Input and task

Use the workshop folder and separate empty project folder your facilitator supplies. Start Copilot or OpenCode in the workshop folder. Ask your facilitator for help opening it. You will choose what to build in level 1.

1. Open this lesson's `.md` file in a text editor. Markdown is plain text with marks for headings, links, and code. Find a heading starting with `#`, a link, and a block surrounded by three backticks. The lines between `---` at the top are **frontmatter**: information about the lesson, such as its title and level.
2. Read the beginning of [bootstrap-lab](../.agents/skills/bootstrap-lab/SKILL.md). A skill is a named set of instructions. This one asks which app you use and copies the right starter files.
3. Paste this into **agent chat**, replacing `[workshop path]` and `[project path]` with your folder locations. In OpenCode, start with `@bootstrap-lab` instead of `/bootstrap-lab`.

```text
/bootstrap-lab Set up my student project.
The workshop folder is [workshop path].
My separate project folder is [project path].
Ask whether I use GitHub Copilot or OpenCode.
Copy the starter skills, engineering agent, and project instructions.
Explain the plan and ask for approval before changing files.
I will choose my idea in level 1. Do not build an app yet.
```

Answer the agent's question about your app. Read its plan before approving it. The skill tells the agent which Python script to run; you do not need to type that script's command.

If a file exists and differs from the starter copy, stop and ask for help comparing them. Do not approve overwriting work you want to keep.

## Find the copied files

Ask the agent to show the files it copied. `AGENTS.md` holds your project's working rules. The skills hold reusable steps; `software-engineering-expert` describes a worker who can write or review code.

| App | Skills folder | Engineering agent file |
| --- | --- | --- |
| Copilot | `.github/skills/` | `.github/agents/software-engineering-expert.agent.md` |
| OpenCode | `.opencode/skills/` | `.opencode/agents/software-engineering-expert.md` |

The two apps use different agent-file settings. Let the skill choose those settings. Keep the Python rules in your copied `AGENTS.md`.

Open a new chat in your **student project folder** before level 1. Your coding app loads that project's instructions. Opening the workshop folder again would give it the workshop's instructions instead.

You need no extra packages or virtual environment to copy these files. If your idea needs a package later, use the same skill's [Python setup steps](../.agents/skills/bootstrap-lab/SKILL.md#prepare-python-dependencies). Do not build the workshop website.

## Evidence and checkpoint

Save which app you chose, both folder paths, your prompt, and the agent's copy report. Find `bootstrap-lab`, `stop-slop`, `frontend-design`, and `software-engineering-expert` in your project. Ask the agent to quote one rule from the copied `AGENTS.md`, then open the file and find that rule yourself.

<details>
<summary>Hint</summary>

You can ask, "Show me the full location of the copied AGENTS.md." A file path tells you where to open it. Ask your facilitator if the project and workshop locations look the same.

</details>

Previous: [Start here](start-here.md) · Next: [Level 1: Write the brief](level-1-brief.md)
