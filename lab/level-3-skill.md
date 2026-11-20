---
title: "Level 3: Make a check-work skill"
description: Create a project procedure and prove that the agent reuses it.
order: 4
level: 3
---

# Level 3: Make a check-work skill

## Goal

Package your project's checks as a skill that the agent can invoke and reuse.

## Input and task

Use the commands and failure cases from level 2. Inspect the installed [stop-slop](../.agents/skills/stop-slop/SKILL.md) as a prose-skill example. You can inspect [frontend-design](../.agents/skills/frontend-design/SKILL.md) for a UI procedure; it applies if you choose a Python-served UI and does not imply Node.

Ask the agent to create `check-work/SKILL.md` inside your harness's skill directory:

- Copilot: `.github/skills/check-work/SKILL.md`
- OpenCode: `.opencode/skills/check-work/SKILL.md`

Use the mapping you inspected during bootstrap. Start the file with YAML:

```yaml
---
name: check-work
description: Run the study queue tests and acceptance checks before review or handoff.
---
```

Give the skill a short procedure: read the brief, run named checks with the selected interpreter, inspect failures, and report commands, results, and gaps. Add one on-demand resource, such as `references/acceptance.md` with failure examples or a Python script that runs checks. Link it from the procedure and state when the agent should read or run it. Do not paste the whole project into `SKILL.md`.

Use `scripts/` for executable checks, `references/` for detail, and `assets/` for files the procedure uses. This is progressive disclosure: the harness can use name/description to find a skill, read its procedure when needed, and load a resource for a specific step.

Ask the agent to invoke `check-work` on your current project. If discovery fails, tell it to read the exact `SKILL.md` path and follow it. In a second request, ask it to reuse `check-work` after you add or adjust one acceptance test from your brief.

## Evidence and checkpoint

Keep the skill and its resource. Capture the agent's invocation or file-read trace, its resource read or script execution, and the check commands/results from both requests. A statement that a skill "loaded" does not prove that the agent used it. Inspect the test change and verify the reported results.

<details>
<summary>Hint</summary>

Keep commands in the skill precise enough to copy. Put a long malformed-store example in the reference, then require the agent to consult that reference when checking data preservation.

</details>

Previous: [Level 2: Build the first slice](level-2-build.md) · Next: [Level 4: Add a command and review it](level-4-review.md)
