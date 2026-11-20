<!-- bootstrap-lab:begin -->
## Project working agreement

Use the workshop skills and engineering agent as starting examples. Develop
project-specific roles and skills as you learn what this project needs. Keep
agent prompts focused on role, authority, inputs, outputs, and handoff
boundaries; put reusable execution procedures in skills.

Support Python 3.9+ with access to PyPI. Use the Python standard library for core
tooling. Do not require Node, npm, npx, Git, shell-specific utilities, extra
runtimes, API keys, or network services beyond PyPI. The coding-agent harness
comes from the workshop environment.

Use `uv` and virtual environments for project dependencies. If `uv` is missing,
create a virtual environment with `python -m venv .uv-tools` and install `uv`
with that environment's Python/pip. Do not install into system Python. Use the
participant's installed Python for project environments; avoid runtime
downloads.

Invoke `stop-slop` for every prose change. Remove duplicate or conflicting
guidance and link the authoritative contract. Make menial behavior explicit
and testable; prefer mechanical enforcement.

Follow the approved scope and preserve unrelated files. Consult `bootstrap-lab`
for setup procedures and the engineering agent for contribution and review
handoffs.
<!-- bootstrap-lab:end -->
