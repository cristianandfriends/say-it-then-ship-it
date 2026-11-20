---
title: "Level 5: Hand off the context"
description: Use a compact handoff to extend the project in a fresh session.
order: 6
level: 5
---

# Level 5: Hand off the context

## Goal

Give a fresh session enough evidence to implement one bounded extension.

## Input and task

Use your working project, brief, skill, review, and check results. A model has a finite context window. Long sessions can crowd out instructions or make the agent miss earlier decisions, a failure pattern people call context rot. Keep durable facts in project files rather than trust the chat history.

Ask the current agent to write a compact `HANDOFF.md` with:

- The goal, current behavior, decisions, and the files that justify them.
- Interpreter, working directory, exact check commands, results, and unresolved review findings.
- Constraints: Python-only setup, JSON contract, metadata preservation, and malformed-data failure.
- One next task, its acceptance criteria, and work to leave out.

Choose a small extension, such as an optional due-date filter for `list`. Define its flag, date format, missing-date behavior, and error cases before coding. Keep unfiltered list output and the existing commands unchanged. No network or new dependency is needed.

Start a fresh harness session in the student project. Do not paste the whole old conversation. Ask it to read `AGENTS.md`, `BRIEF.md`, `HANDOFF.md`, and `check-work`, restate the next task, and identify any missing evidence before changing code.

Use your harness's documented new-session or compaction controls. Slash commands differ between harnesses. Compaction produces a smaller account of a conversation; inspect it for lost decisions. A fresh session plus a checked handoff gives you a separate test of what the next worker can recover.

Let the fresh agent implement the approved extension and its focused tests. Reuse the check-work skill, run the extension's acceptance commands yourself, and rerun the level 4 checker for regression evidence. See [Work with two agents](two-agents.md) for a handoff prompt.

## Evidence and checkpoint

Keep `HANDOFF.md`, the fresh session's task restatement, files it read, implementation changes, and exact extension commands/results. Include the regression check output. Correct a missing handoff fact in the file, then show that the fresh session can use it. Do not claim success from a summary alone.

<details>
<summary>Hint</summary>

A useful handoff might fit on one screen. Link to longer fixtures or the brief instead of copying them. Include a failed or skipped command if it affects the next task.

</details>

Previous: [Level 4: Add a command and review it](level-4-review.md) · Next: [Level 6: Try a read-only MCP tool](level-6-tools.md)
