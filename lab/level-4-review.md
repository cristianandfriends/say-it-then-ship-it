---
title: "Level 4: Extend and review"
description: Improve one thing and ask a different agent to review the change.
order: 5
level: 4
---

# Level 4: Extend and review

## Goal

Improve one thing, get a second opinion, and fix any problems you confirm.

## Input and task

Choose one item from the "Later" section of your brief, or a bug you can make happen again. Before asking for code, update the plan. Paste this into chat; use `@stop-slop` in OpenCode:

```text
/stop-slop Update BRIEF.md for this one change: [improvement or bug].
Add an example I can try and the result I should expect.
Name something that works now and must keep working.
Ask me to approve the plan before anyone changes the app.
```

After approving the plan, ask the `software-engineering-expert` agent to build the change:

```text
Use the software-engineering-expert agent to make the change I approved.
Read AGENTS.md and BRIEF.md. Leave other features alone.
Write a test that catches the missing feature or bug before changing the app.
Show its failing result, make the change, then run the checks again.
Have a different worker review the change without editing files.
Show me the changes, check results, and that worker's review.
```

Ask your facilitator to help you select or launch that agent if needed. A prompt naming an agent is a request to use it; check the app's activity to see whether it started.

Run your skill after the change. In OpenCode, use `@check-work`:

```text
/check-work Check the new example and our existing examples.
If the app saves information, check that unrelated saved information stays safe.
Report the results and anything you could not check.
```

## Get a second opinion

The engineering agent should ask a separate worker to review its code. Find that review in its response. A **read-only review** means the reviewer can read files and report problems but cannot change the app.

If you have not received a separate review, ask your facilitator to help you start one. Copilot calls a general worker `general-purpose`; OpenCode calls it `general`. Use a new chat for the reviewer if your app cannot start another worker.

Give the reviewer your brief, the changed files, a copy of what changed, and the check results. Your agent can prepare before-and-after copies; you do not need Git. Give this prompt to the reviewer:

```text
/check-work Review this change against BRIEF.md.
Read the supplied changed files, before-and-after copies, and check results.
Do not edit files. Check whether the agreed examples work
and whether the change broke something that worked before.
For each problem, name the file and steps to make it happen.
Report what you checked and what you could not check.
```

Wait for the reviewer to respond. If it has not responded, record "review pending." The first agent looking at its own work does not count as a second opinion.

Try the reported problems before asking for fixes. Give confirmed problems to the agent that wrote the code, then use `/check-work` again. Keep one agent in charge of file changes at a time. Try the new feature yourself and check that your earlier examples still work.

See [Work with two agents](two-agents.md) for the review loop.

## Evidence and checkpoint

Save the plan, changed-file list, check reports, and the separate review. Record who reviewed it, any problems you confirmed, and what you fixed. If the reviewer found no problems, keep its explanation of what it checked.

<details>
<summary>Hint</summary>

Show the reviewer an example that worked before your change. Ask it to try that example as well as the new one.

</details>

Previous: [Level 3: Make a check-work skill](level-3-skill.md) · Next: [Level 5: Hand off the context](level-5-context.md)
