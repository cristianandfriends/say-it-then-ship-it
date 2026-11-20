---
title: "Level 7: Try a read-only MCP tool"
description: "Bonus: let your agent use one safe project feature as a tool."
order: 8
level: 7
---

# Level 7: Try a read-only MCP tool

## Goal

Let your agent call one project feature as a tool and check the result. This level is an optional bonus.

## Input and task

A **skill** tells your agent how to do a task. A **tool** lets it ask a program to do something and return a result. **MCP**, the Model Context Protocol, is one way to connect those programs to a coding agent.

Look at the problem you described in `BRIEF.md`. Choose one useful action your agent could perform for that project without changing saved information. For a writing project, that might mean checking a draft against a word limit. For a game, it might mean checking whether a sample move follows your rules. Use made-up data and a result you can check yourself.

Ask your agent to suggest a tool based on your brief:

```text
Use BRIEF.md and our conversation to suggest two read-only MCP tools
that would help with this project's problem.
For each, explain when we would use it and give an example request and result.
Keep the tool local, with made-up data and no outside services.
Recommend one small option. Do not write code until I choose.
```

Choose one and add its purpose to your brief. Agree on what you will give the tool, what it should return, and what should happen if you give it something invalid. You will build a small MCP server that offers that tool for your project.

## Ask the setup skill for the package

Paste this into chat; use `@bootstrap-lab` in OpenCode:

```text
/bootstrap-lab Prepare this project's environment for the mcp[cli] package.
Explain the plan and ask before installing anything.
Reuse our project environment. Keep packages inside a virtual environment.
Use PyPI and do not download another Python version.
If setup cannot work here, stop and explain why.
```

If setup fails, go to **Required safe fallback** below. You can finish that route without installing MCP.

## Build one read-only tool

A **server** is the program that offers the tool to your agent. **Read-only** means the tool must not change files or saved information. Ask the engineering agent to build it with this prompt. Replace the brackets; the technical lines tell the agent how to keep the connection local:

```text
Use software-engineering-expert to build one local MCP tool for [project action].
Use the purpose and examples we agreed on in BRIEF.md.
Follow the engineering agent's instructions.
Use FastMCP from mcp.server.fastmcp, from the mcp[cli] package.
Allow only the agreed inputs. Return a clear error for invalid input.
The tool must not write files, run commands, make network calls, or use credentials.
If the tool reads a file, allow only a fixed sample file in this project.
Use stdio transport; reserve stdout for MCP and send diagnostics to stderr.
Explain how I can check the result. Ask before starting the server.
```

Ask the agent to explain what the server will do before you approve running it. The restrictions above apply to the tool; its setup and tests may create project files with your approval.

```text
/check-work Test the tool's normal example and invalid example.
Compare the results with BRIEF.md and check that no saved data changes.
Do not start the MCP server yet.
```

Use `@check-work` in OpenCode.

## Connect and try it

Ask your facilitator to help connect your coding app to the local server. Give them the Python environment and server file locations your agent reports. The two apps use different connection settings:

- [OpenCode MCP servers](https://opencode.ai/docs/mcp-servers/)
- [GitHub Copilot MCP documentation](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/extend-copilot-with-tools-and-context/extend-copilot-chat-with-mcp)

Your facilitator can supply copies of these pages. Ask the agent to follow the instructions for your app, show its proposed settings, and wait for approval. Keep the connection local and leave unrelated tools disabled.

Once connected, paste this request into chat:

```text
List the connected tools and find [my tool's name].
Call it with [the example from my brief].
Show the result and compare it with what we expected.
Check that it did not change our sample files or saved information.
```

Compare the tool's result yourself. Stop the server through your coding app when you finish; ask your facilitator if you cannot find that control.

## Required safe fallback

If you cannot install MCP or connect the tool, ask the agent to run the same calculation or check in Python without MCP. It should use the examples from your brief and show the results. Keep the same read-only restrictions.

If you have not built that Python code, ask the engineering agent to write and test it first, without installing MCP. Then use your checking skill:

```text
/check-work Check our tool's behavior in Python without MCP.
Use the examples in BRIEF.md and show the actual results.
Confirm that the operation changes no saved data.
Explain that we have not demonstrated an MCP connection.
```

Use `@check-work` in OpenCode. Save **"MCP connection not demonstrated"** and the reason. A working Python calculation completes this fallback; it does not prove that the agent connected to an MCP tool.

## Evidence and checkpoint

Keep the setup report, your examples, expected and actual results, and check report. If you connected MCP, save the tool listing and its call result. If you used the fallback, save the reason and the Python result. Ask your facilitator to look at what you demonstrated.

<details>
<summary>Hint</summary>

Ask the agent to keep the calculation separate from the MCP connection code. That lets you check the calculation even if you cannot connect the tool.

</details>

Previous: [Level 6: Hand off the context](level-6-context.md) · Next: [Start here](start-here.md)
