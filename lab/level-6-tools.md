---
title: "Level 6: Try a read-only MCP tool"
description: Expose one read-only project operation as a tool, or record a safe fallback.
order: 7
level: 6
---

# Level 6: Try a read-only MCP tool

## Goal

Expose one read-only operation from your project through MCP and verify a tool result. This level is an optional bonus.

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

Choose one operation that fits your idea, such as validating sample input or computing a preview. Define its name, allowed inputs, expected output, and a failure case in your brief. Use synthetic input or a disposable fixture with a result you can check.

Ask your agent for a small server that exposes that operation as one tool, with focused tests. Require:

- A narrow input contract. If it reads a file, use a fixed disposable fixture path anchored to the student project; do not accept arbitrary paths.
- No writes, shell commands, network calls, or credentials. Keep private data out of the exercise.
- A structured result you can compare with the expected output in your brief. Invalid input must produce an explicit error without changing state.
- Stdio transport. Keep stdout for MCP messages; send diagnostics to stderr. Do not add stdout debug prints.

Review the code and tests before launch. Test the operation and its failure case with your known input.

Use the harness's current documentation to configure a local stdio server with the absolute venv interpreter path and server path:

- [OpenCode MCP servers](https://opencode.ai/docs/mcp-servers/)
- [GitHub Copilot MCP documentation](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/extend-copilot-with-tools-and-context/extend-copilot-chat-with-mcp)

Use facilitator-provided copies if you cannot reach the docs. Copilot surfaces and OpenCode use different configuration locations and fields. Do not guess a shared JSON configuration. Keep the tool local; do not enable unrelated servers or credentials.

Ask the connected harness to list tools, select your tool, and invoke it with the agreed input. Compare the actual structured result with your expected result. Confirm that the tool changed no state, including fixture bytes if it reads files. Stop the server through your harness when you finish.

## Evidence and checkpoint

Keep interpreter/package versions, server path, input or fixture, expected result, tests/results, tool listing, invocation arguments, and actual result. Record connection errors as errors, not successful tool calls.

### Required safe fallback

If the interpreter, provider, or harness cannot connect, do not add a service. Run the same read-only operation as a local Python function using the agreed input. Compare its result with your expected output and confirm that it changed no state. Record the command and actual result, plus "MCP connection not demonstrated" and the reason. This completes the fallback; a local function call does not prove an MCP connection.

Ask your facilitator to inspect the evidence against your project's agreed tool contract.

<details>
<summary>Hint</summary>

Separate the project operation from the MCP wrapper. Test its normal and error results without starting a server, then reuse that function for the fallback.

</details>

Previous: [Level 5: Hand off the context](level-5-context.md) · Next: [Start here](start-here.md)
