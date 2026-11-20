# Say it, then ship it

An El Camino College ScaleUP workshop (2026) for building with GitHub Copilot and OpenCode.

[![Open the workshop site](https://img.shields.io/badge/workshop-open-00ffff?style=flat-square&labelColor=000080)](https://cristians.space/say-it-then-ship-it/)
[![Read the workshop slides](https://img.shields.io/badge/slides-read-ffff55?style=flat-square&labelColor=000080)](https://docs.google.com/presentation/d/e/2PACX-1vRgWXcd3VTgfIUE0qp6972ijj1sA6HPSrSgOzt0O8eHMBFqTroFWwSJ43UzPcBTRos33YO6-PLOwQf6/pub?start=false&loop=false&delayms=3000)
[![Join the workshop Discord chat](https://img.shields.io/badge/Discord-chat-5865f2?style=flat-square&labelColor=000080)](https://discord.gg/WqcQTVW6fM)

```text
[setup] -> [idea] -> [build]
                       |
[handoff] <- [review + check]
```

## Start the lab

Follow [the lab guide](lab/start-here.md) through levels 0 to 7. Level 0 covers setup. Choose your idea and define a small first version in Level 1.

Build your project using its acceptance checks, write a reusable skill, and create a specialized subagent for your idea. Review with another agent and hand work to a fresh session. The last level offers a read-only MCP exercise for your project.

The workshop environment provides **Python 3.15+ and access to PyPI**. The facilitator supplies the coding harness and workshop folder. The bootstrap uses Python's standard library. If your project needs dependencies, use `uv` in a virtual environment; follow the [setup instructions](lab/start-here.md#paths-and-python) without installing into system Python.

## Take the starter agents and skills

Use [bootstrap-lab](.agents/skills/bootstrap-lab/SKILL.md) to install the starter skills, the software-engineering-expert agent, and Python project instructions into a separate project. You can finish setup before choosing an idea.

From the workshop folder, ask your agent to set up a separate project. Paste this into agent chat, using `@bootstrap-lab` in OpenCode:

```text
/bootstrap-lab Set up my separate project at [project path].
Ask whether I use Copilot or OpenCode.
Show the plan and ask before copying the starter files.
Do not build an app yet.
```

Replace `[project path]` with your project folder's location. Review the proposed paths before approving the installation. The installer preserves unrelated files and refuses conflicts.

The starter skills cover [project setup](.agents/skills/bootstrap-lab/SKILL.md), [prose editing](.agents/skills/stop-slop/SKILL.md), and [frontend design](.agents/skills/frontend-design/SKILL.md). Adapt them and develop roles and skills for your project.

The engineering agent has native formats for [Copilot](.github/agents/software-engineering-expert.agent.md) and [OpenCode](.opencode/agents/software-engineering-expert.md), with the same role and engineering guidance.

[Workshop source](https://github.com/cristianandfriends/say-it-then-ship-it)
