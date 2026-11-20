---
name: bootstrap-lab
description: Install the workshop's starter skills and engineering agent into a Copilot or OpenCode project, then plan project-specific roles and skills.
---

# Bootstrap a workshop project

Use this skill when a workshop participant wants to set up a project for coding
agents. Treat the shipped material as examples to evolve, not an exhaustive
rulebook.

## Establish the scope

1. Ask: **Are you using GitHub Copilot or OpenCode?** Ask even if the repository
   contains configuration for one of them.
2. Ask for the workshop source directory and destination project when you do
   not know them. An idea is optional during setup: install the starter material
   without inventing a project goal if the participant has not chosen one.
   The source must contain the canonical
   `.agents/skills/` directories and
   `.github/agents/software-engineering-expert.agent.md`.
3. Inspect the destination instructions and relevant files. Explain which
   directories you propose to add, how you will preserve existing files, and
   what the downstream Python-only agreement means for this project.
4. **Get the user's confirmation before editing files or installing tools.**
   You may run the installer's `--dry-run` first. Do not treat a successful dry
   run as permission to write.

Keep student setup within Python 3.9+ and access to PyPI. Do not require Node,
npm, npx, Git, shell-specific commands, extra runtimes, API keys, or network
services beyond PyPI. The workshop's Astro website belongs to maintainers;
students do not need to build it.

## Install the starter material

Run the shipped Python installer after confirmation. Replace the angle-bracketed
paths with the user's paths; quote paths that contain spaces.

```text
python <workshop>/.agents/skills/bootstrap-lab/scripts/bootstrap_lab.py --harness copilot --target <student-project>
python <workshop>/.agents/skills/bootstrap-lab/scripts/bootstrap_lab.py --harness opencode --target <student-project>
```

Use the Python 3.9+ executable available to the participant (`python` or
`python3`). Add `--dry-run` to preview without creating the target. The installer
uses the standard library and makes no network requests.

| Harness | Skill destination | Agent destination |
| --- | --- | --- |
| GitHub Copilot | `.github/skills/<skill>/` | `.github/agents/software-engineering-expert.agent.md` |
| OpenCode | `.opencode/skills/<skill>/` | `.opencode/agents/software-engineering-expert.md` |

Install the shipped `bootstrap-lab`, `stop-slop`, and `frontend-design`
directories, including scripts, references, assets, and licenses. The installer
copies from the workshop's canonical `.agents/skills/` source and skips Python
validation artifacts (`__pycache__/` and `*.pyc`). Both harnesses also recognize
that compatibility path; do not install duplicate copies there.

Use the canonical agent body for both harnesses. The OpenCode copy replaces its
Copilot name field with `mode: subagent` and retains its description. Do not add a
fixed model, speculative tools, global settings, or changes to `opencode.json`.
See the [Copilot agent documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents),
[OpenCode skills documentation](https://opencode.ai/docs/skills/), and
[OpenCode agents documentation](https://opencode.ai/docs/agents/).

The installer infers the workshop root from its own location. A copy installed
under `.github/skills/` or `.opencode/skills/` does not contain the canonical
source layout. Point that copy at the workshop with `--source <workshop>`.
If the source files are missing, locate the workshop checkout or copy; do not
fetch replacements from the network.

### Existing files and failures

- An identical skill or agent file needs no write. A differing file, directory
  collision, or symlink stops the installation before any planned changes.
  Inspect the conflict, preserve your work, and choose a clean destination or
  reconcile the files by hand. The installer has no overwrite flag.
- The [downstream AGENTS.md template](assets/AGENTS.md) defines the managed
  baseline. The installer appends that bounded block to existing instructions,
  preserving user prose. A changed or malformed managed block needs a manual
  merge before rerunning.
- The installer writes each file atomically. An operating-system error can
  interrupt a multi-file install. Read the error and its completed-file count,
  fix the cause, and rerun; matching files remain untouched.
- The installer preserves unrelated files. It does not configure global agents,
  install dependencies, or touch `opencode.json`.

Check the reported paths and restart or open a session if your harness needs to
discover the new skill and agent. Ask the harness to load `bootstrap-lab`; verify
that it can find the engineering agent.

## Plan before adding more roles or skills

Start project-specific planning after the participant chooses an idea. If they
have not chosen one, finish the starter installation and defer this step to
level 1. Do not make project selection a prerequisite for bootstrap.

Use the participant's project goal to identify the next deliverable, its
acceptance checks, and constraints. Ask which repeated tasks need a reusable
skill and which decisions need a separate role. Propose a small plan before
generating extra agents or skills, and get approval for their names and scope.

Give each agent a role, authority, required inputs, expected outputs, and handoff
boundary. Keep detailed procedures in skills. For a skill, start with a short
`SKILL.md`; move execution code into `scripts/`, supporting contracts into
`references/`, and reusable templates into `assets/`. Link those resources when
the agent needs them instead of loading the whole directory into each prompt.

For project dependencies, use `uv` and a project virtual environment. If `uv` is
missing, use the standard library to create a tool environment, then install
`uv` there with pip:

```text
python -m venv .uv-tools
```

| Platform | Install uv | Create the project environment |
| --- | --- | --- |
| macOS / Linux | `.uv-tools/bin/python -m pip install uv` | `.uv-tools/bin/uv venv --no-python-downloads --python <python-executable> .venv` |
| Windows | `.uv-tools\Scripts\python.exe -m pip install uv` | `.uv-tools\Scripts\uv.exe venv --no-python-downloads --python <python-executable> .venv` |

Use the path to the participant's installed Python for `<python-executable>`.
This prevents a runtime download. Keep dependency resolution on PyPI and use the
environment-local `uv` for project dependency commands. Do not install tools
into system Python. The bootstrap installer itself needs neither pip nor `uv`.

## Prose

- Invoke `stop-slop` for every prose change.
- Focus agent prompts on role, authority, inputs, outputs, and handoff boundaries.
- Put detailed execution procedures in skills.
- Remove duplicate or conflicting guidance and link authoritative contracts.
- Make menial behavior explicit and testable; prefer mechanical enforcement.
