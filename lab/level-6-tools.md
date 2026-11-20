---
title: "Level 6: Try a read-only MCP tool"
description: Explore a fixed-path queue summary tool, or record a safe fallback.
order: 7
level: 6
---

# Level 6: Try a read-only MCP tool

## Goal

Expose a read-only queue summary through MCP and verify a tool result. This level is an optional bonus.

## Input and task

MCP, the Model Context Protocol, gives a harness a standard way to discover and invoke external tools. A skill supplies instructions; an MCP server supplies callable tools. You will build one local Python tool, with no new service or API account.

Check `python --version` first. The core labs support Python 3.9. The PyPI `mcp` package requires Python 3.10 or newer in current releases; check the package's supported version before installing. If your interpreter cannot run it, skip installation and use the fallback below. Do not download another interpreter.

For a supported interpreter, create a venv in the student project and install uv inside it if unavailable:

```text
python -m venv .venv
.venv/bin/python -m pip install uv
.venv/bin/python -m uv pip install --python .venv/bin/python "mcp[cli]"
```

On Windows, use `.venv\Scripts\python.exe` in place of `.venv/bin/python`. Keep dependencies inside the venv. Use `FastMCP` from `mcp.server.fastmcp`; do not install a separate FastMCP package for this exercise. If package compatibility or PyPI access blocks setup, use the fallback.

Ask your agent for a small server with one tool, `queue_summary`, and focused tests. Require:

- One fixed fixture path anchored to the student project, for example `mcp_fixture/queue.json`. Do not accept user-supplied paths or use the process working directory to pick a file.
- No writes, shell commands, network calls, or path-selection arguments. Do not connect your real queue.
- A structured result with total, open, and done counts. Missing or malformed data must produce an explicit error without creating or changing files.
- Stdio transport. Keep stdout for MCP messages; send diagnostics to stderr. Do not add stdout debug prints.

Create a known fixture with two items: one with `done: false` and one with `done: true`. Review the code and tests before launch.

Use the harness's current documentation to configure a local stdio server with the absolute venv interpreter path and server path:

- [OpenCode MCP servers](https://opencode.ai/docs/mcp-servers/)
- [GitHub Copilot MCP documentation](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/extend-copilot-with-tools-and-context/extend-copilot-chat-with-mcp)

Use facilitator-provided copies if you cannot reach the docs. Copilot surfaces and OpenCode use different configuration locations and fields. Do not guess a shared JSON configuration. Keep the tool local; do not enable unrelated servers or credentials.

Ask the connected harness to list tools, select `queue_summary`, and invoke it with the known fixture. Inspect the actual structured result: total 2, open 1, done 1. Compare file bytes before and after. Stop the server through your harness when you finish.

## Evidence and checkpoint

Keep interpreter/package versions, server and fixture paths, tests/results, tool listing, invocation arguments, and actual result. Record connection errors as errors, not successful tool calls.

### Required safe fallback

If the interpreter, provider, or harness cannot connect, do not add a service. Read the fixture with a local stdlib Python check, compute the same counts, and compare bytes before/after. Record the command and actual result, plus "MCP connection not demonstrated" and the reason. This completes the fallback; a local function call does not prove an MCP connection.

The workshop checker has no level 6 mode. A human checks this evidence.

<details>
<summary>Hint</summary>

Separate the summary function from the MCP wrapper. You can test its fixed-path read and error behavior without starting a server, and reuse that function for the fallback.

</details>

Previous: [Level 5: Hand off the context](level-5-context.md) · Next: [Start here](start-here.md)
