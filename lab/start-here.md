---
title: Start here
description: Learn how to ask your agent for help, then build your own idea.
order: 0
---

# Start here

Say it, then ship it · El Camino College ScaleUP 2026

Build something you want to use. You need no programming experience. Set up your project folder in level 0, then choose your idea in level 1. Keep working on that idea through the remaining levels.

Your coding agent can write code and explain it. You decide what to build and check what it does. At the end of each level, save the files and results listed under **Evidence and checkpoint** so you can show your progress.

## What to bring

- Access to GitHub Copilot or OpenCode, arranged with your facilitator. For Copilot, you need a [GitHub account](https://github.com/copilot); you may qualify for the [education pack](https://education.github.com/pack).
- Python 3.15 or newer, supplied with the workshop environment.
- The workshop folder and a separate empty project folder, supplied by your facilitator.

Your project will use Python and, if needed, packages from PyPI, the Python package directory. Choose a first version that runs on your workshop computer. You do not need to install Git, Node, or the workshop website, or sign up for another service.

## Talk to your agent

Paste the prompt examples into your **agent's chat**, not into a terminal. A terminal runs computer commands; your agent can run those commands after you approve them. Replace text in `[square brackets]` with your own details.

A **skill** is a named set of instructions your agent can follow. For example, `stop-slop` helps it write plain language. The prompt examples use Copilot's `/skill-name` form. OpenCode uses `@skill-name`:

| App | Example to paste into chat |
| --- | --- |
| Copilot | `/stop-slop Write a short description of my idea.` |
| OpenCode | `@stop-slop Write a short description of my idea.` |

Make the same change for `/bootstrap-lab`, `/frontend-design`, and `/check-work`. You create `check-work` in level 3; it will not exist before then.

An **agent role** gives a worker a job, such as writing code or reviewing it. A skill gives that worker steps to follow. Your facilitator may call Copilot or OpenCode a **harness**: the app that lets the agent read files and use tools.

Ask your agent to explain unfamiliar words before you approve a change.

## Paths and Python

In examples, `workshop` means the supplied workshop folder and `student-project` means your own project folder. A **path** is a folder or file's location on your computer. Ask your facilitator for these two paths, then give them to your agent. Keep your project outside the workshop folder.

A **virtual environment**, often named `.venv`, keeps one project's added Python packages separate from other projects. `uv` is the package tool your agent will use. You do not need to memorize its commands.

Level 0 copies starter files without installing packages. If your project needs an extra package, use [Prepare Python dependencies](../.agents/skills/bootstrap-lab/SKILL.md#prepare-python-dependencies) in `bootstrap-lab`. A **dependency** is a package your project needs to run. Paste this into chat, using `@bootstrap-lab` in OpenCode:

```text
/bootstrap-lab Prepare a Python environment for [package my project needs].
Follow Prepare Python dependencies.
Explain what you will install and ask for approval first.
Use the Python already on this computer and packages from PyPI.
Do not install into system Python or download another Python version.
```

If you do not know which package you need, ask the agent to explain its proposal before using this prompt. Ask it to show which Python environment it used. Your copied `AGENTS.md` contains the rules; `bootstrap-lab` contains the setup steps.

Some computers use `python3` or `py -3` instead of `python`. Let your agent check which command works. If setup fails, keep the error and ask your facilitator for help. Do not approve a system-wide installation to get past it.

Your project does not need network access beyond PyPI. Your facilitator can provide copies of linked reference pages.

## Route

| Level | Work | Evidence to keep |
| --- | --- | --- |
| [0: Bootstrap](level-0-bootstrap.md) | Set up your project with a skill | Folder locations and copied files |
| [1: Brief](level-1-brief.md) | Choose your idea and one thing it should do | Your approved `BRIEF.md` plan |
| [2: Build](level-2-build.md) | Build and try that first feature | Expected and actual results |
| [3: Skill](level-3-skill.md) | Make a skill that checks your project | Skill file and two check reports |
| [4: Subagent](level-4-agent.md) | Create a specialist for your idea and try it | Agent file and its response to a task |
| [5: Review](level-5-review.md) | Improve one thing and get a second opinion | Review, fixes, and check results |
| [6: Context](level-6-context.md) | Continue your project in a new chat | `HANDOFF.md` and a working change |
| [7: Tools](level-7-tools.md) | Bonus: give your agent a read-only tool | Tool result or local-only result |

Use [Work with two agents](two-agents.md) during review and handoff. Keep your prompts, results, and decisions in project notes. Use made-up sample data instead of private information. Ask what code will do before you approve running it.

An **acceptance check** is an example you try to decide whether a feature does what you asked. You choose those examples for your idea in level 1. Try them before moving on, and record anything you could not check.

Next: [Level 0: Bootstrap your project](level-0-bootstrap.md).
