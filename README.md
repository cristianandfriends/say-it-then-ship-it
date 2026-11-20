# Say it, then ship it

An El Camino College ScaleUP workshop (2026) for building with GitHub Copilot and OpenCode.

[![Open the workshop site](https://img.shields.io/badge/workshop-open-444444?style=flat-square)](https://cristians.space/say-it-then-ship-it/)
[![Read the workshop slides](https://img.shields.io/badge/slides-read-444444?style=flat-square)](https://docs.google.com/presentation/d/e/2PACX-1vRgWXcd3VTgfIUE0qp6972ijj1sA6HPSrSgOzt0O8eHMBFqTroFWwSJ43UzPcBTRos33YO6-PLOwQf6/pub?start=false&loop=false&delayms=3000)
[![Join the workshop Discord chat](https://img.shields.io/badge/Discord-chat-444444?style=flat-square)](https://discord.gg/sMafw3ktj)

```text
[setup] -> [idea] -> [build]
                       |
[handoff] <- [review + check]
```

## Start the lab

Follow [the lab guide](lab/start-here.md) through levels 0 to 6. Level 0 covers setup. Choose your idea and define a small first version in Level 1.

Build your project using its acceptance checks, write a reusable skill, review with another agent, and hand work to a fresh session. The last level offers a read-only MCP exercise for your project.

You need **Python 3.9+ and access to PyPI**. The facilitator supplies the coding harness and workshop folder. The bootstrap uses Python's standard library. If your project needs dependencies, use `uv` in a virtual environment; follow the [setup instructions](lab/start-here.md#paths-and-python) without installing into system Python.

## Take the starter agents and skills

Use [bootstrap-lab](.agents/skills/bootstrap-lab/SKILL.md) to install the starter skills, the software-engineering-expert agent, and Python project instructions into a separate project. You can finish setup before choosing an idea.

From the workshop folder, preview the installation:

```text
python .agents/skills/bootstrap-lab/scripts/bootstrap_lab.py --harness copilot --target ../my-project --dry-run
```

Replace `../my-project` with your separate project path and quote paths that contain spaces. Use `--harness opencode` for OpenCode. Inspect the proposed paths, then run the same command without `--dry-run` to install. The installer preserves unrelated files and refuses conflicts.

The starter skills cover [project setup](.agents/skills/bootstrap-lab/SKILL.md), [prose editing](.agents/skills/stop-slop/SKILL.md), and [frontend design](.agents/skills/frontend-design/SKILL.md). Adapt them and develop roles and skills for your project.

The engineering agent has native formats for [Copilot](.github/agents/software-engineering-expert.agent.md) and [OpenCode](.opencode/agents/software-engineering-expert.md), with the same role and engineering guidance.

[Workshop source](https://github.com/cristianandfriends/say-it-then-ship-it)
