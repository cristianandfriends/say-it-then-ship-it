---
title: Start here
description: Choose a project and follow the workshop levels.
order: 0
---

# Start here

Say it, then ship it · El Camino College ScaleUP 2026

Build a local Python study queue with a coding agent. You can use your own idea if you keep equivalent acceptance checks. Use the ordered levels, hints, and evidence checkpoints as a route map. We collect no passwords and keep no scoreboard. No software gate checks your prose or unlocks the next level.

## What to bring

- A free [GitHub account and Copilot access](https://github.com/copilot). Check the [education pack](https://education.github.com/pack) if you qualify.
- Python 3.9 or newer. The facilitator supplies coding-harness access, the workshop folder, and a separate empty student project.
- One small goal and permission to run code in your student project.

You need no Git, Node, npm, containers, paid service, or new API account. Core labs use Python's standard library. The workshop's `web/` Node project belongs to maintainers; do not build it.

## Paths and Python

In examples, `workshop` means the supplied workshop folder and `student-project` means your separate project. Replace those paths, including spaces, with your own paths. Quote paths that contain spaces. Run project commands from the student project unless a level says otherwise.

Use `python` for your selected interpreter. On macOS or Linux you might use `python3`; on Windows you might use `py -3`. Check it with `python --version`. Replace `python` in each command with the command that selects your interpreter.

Core levels need no dependency installation. If an extension needs a PyPI dependency, create a venv, then install and run uv inside that venv:

```text
python -m venv .venv
.venv/bin/python -m pip install uv
.venv/bin/python -m uv pip install --python .venv/bin/python PACKAGE
```

Replace `PACKAGE` with the approved dependency. On Windows, replace `.venv/bin/python` with `.venv\Scripts\python.exe`. Use that venv interpreter for project commands after installing dependencies. Do not install into system Python or download another interpreter. Network access beyond PyPI is not part of the exercises; read linked reference pages through facilitator-provided copies if needed.

## Route

| Level | Work | Evidence to keep |
| --- | --- | --- |
| [0: Bootstrap](level-0-bootstrap.md) | Inspect Markdown and install project instructions | Paths and generated files |
| [1: Brief](level-1-brief.md) | Define one goal and a contract | Approved `BRIEF.md` |
| [2: Build](level-2-build.md) | Implement `add` and `list` | Commands, tests, checker result |
| [3: Skill](level-3-skill.md) | Create and reuse a check-work skill | Invocation trace and results |
| [4: Review](level-4-review.md) | Add `done` and get a second review | Review findings and checks |
| [5: Context](level-5-context.md) | Hand off to a fresh session | `HANDOFF.md` and extension checks |
| [6: Tools](level-6-tools.md) | Try a read-only MCP tool | Tool result or safe fallback |

Use [Work with two agents](two-agents.md) during review and handoff. Keep prompts, command results, and decisions in your project evidence notes. Review code before running it. Use fixture data, not private records.

The optional checker covers the default CLI at levels 2 and 4. You judge the remaining checkpoints from artifacts and observed runs. Keep failed results with the fix that resolved them.

Next: [Level 0: Bootstrap your project](level-0-bootstrap.md).
