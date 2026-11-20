---
title: "Level 6: Hand off the context"
description: Write a note that helps you continue your project in a new chat.
order: 7
level: 6
---

# Level 6: Hand off the context

## Goal

Start a new chat and continue your project using a short handoff note.

## Input and task

Use your working project from level 5. An agent can keep a limited amount of text in view at once. That limit is its **context window**. In a long chat, it may miss earlier instructions or decisions.

Save important facts in project files so a new chat can read them. A **handoff** is a note explaining what works, what you decided, and what to do next.

Choose one remaining task from your brief. Agree on an example that should work, an example with a mistake, and the result you expect for each.

Ask the current agent to write the note. Paste this into chat; use `@stop-slop` in OpenCode:

```text
/stop-slop Write HANDOFF.md so I can continue in a new chat.
Include what works, important decisions, and the files to read.
Record our Python environment, how to run the project, and the latest checks.
Include failed or skipped checks and any review problems we have not fixed.
The next task is [one task from BRIEF.md].
Include our examples, expected results, and what must keep working.
Keep the note short and link to longer files. Do not change the app.
```

Read the note. Check its claims against the files and results you saved. Correct mistakes before using it.

## Continue in a new chat

Use your app's new-chat control while keeping the student project open. Ask your facilitator where to find it. Asking the old chat to "start fresh" does not open a new chat.

Paste this into the new chat:

```text
Read BRIEF.md and HANDOFF.md.
Explain what the project does and the one task I want to do next.
Tell me what should happen in our examples and what must stay unchanged.
List anything missing or unclear. Do not change files until I approve.
```

Compare its answer with your plan. If it missed a fact, add that fact to `HANDOFF.md` and ask the new agent to read the corrected file.

Approve the task once the new agent understands it. Ask it to use the engineering agent as you did in level 5. After the change, use your skill:

```text
/check-work Check the new feature and the examples that worked before.
Report the results and anything you could not check.
```

Use `@check-work` in OpenCode. Try the feature yourself too.

Some apps offer **compaction**, which shortens a long chat into a summary. Read that summary for missing decisions. In this level, use a new chat and your checked handoff note to see whether another agent can pick up the work.

## Evidence and checkpoint

Save `HANDOFF.md`, the new chat's explanation of the task, and the change it made. Keep the new check report and your own results from trying the feature. A correct summary does not prove that the new code works.

<details>
<summary>Hint</summary>

Think of the note as what you would leave a classmate who takes over tomorrow. Name the next action and where to find the files they need.

</details>

Previous: [Level 5: Extend and review](level-5-review.md) · Next: [Level 7: Try a read-only MCP tool](level-7-tools.md)
