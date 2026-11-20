# Say it, then ship it

This repository supports El Camino College ScaleUP's hands-on workshop. Use the
levels in `lab/` to practice giving coding agents context, checking their work,
and handing off between sessions.

The shipped skills and agent give students a starting point. Develop roles and
skills for your own project; consult
[bootstrap-lab](.agents/skills/bootstrap-lab/SKILL.md) for installation and planning.
Keep detailed procedures in skills instead of duplicating them here.

Students need Python 3.9+ and access to PyPI. Student tooling must use the Python
standard library unless a project needs dependencies. Use `uv` with virtual
environments for those dependencies. If `uv` is missing, install it with
Python/pip inside a virtual environment, not into system Python. Do not require
Node, npm, npx, Git, shell-specific utilities, extra runtimes, API keys, or network
services beyond PyPI.

Invoke `stop-slop` for each prose change, including agent prompts and skill text.

## Website maintenance

Maintainers use the existing Node-based Astro site in `web/`. Its root commands
include `npm run dev`, `npm run check`, `npm run build`, `npm run preview`, and
`npm test`. This exception applies to website maintenance; students do not need
to build the site or copy its runtime requirements into their projects.
