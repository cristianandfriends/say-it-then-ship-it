---
title: "Level 3: Make a check-work skill"
description: Make a skill that runs your project's checks and reports the results.
order: 4
level: 3
---

# Level 3: Make a check-work skill

## Goal

Make a `check-work` skill so you can ask for your project's checks by name.

## Input and task

Use your working project and the checks from level 2. Open the installed [stop-slop](../.agents/skills/stop-slop/SKILL.md) file. It has a name, a description, and instructions. Your new skill will have those parts too.

Ask the agent to write the skill in plain language. Paste this into chat; use `@stop-slop` in OpenCode:

```text
/stop-slop Create a check-work skill for this project.
Read AGENTS.md and the checks we recorded in BRIEF.md.
Put the skill in the right folder for my coding app.
Tell it to read the brief, run our checks, and report what passed or failed.
It must report missing checks and ask before fixing code or changing the plan.
Add references/what-to-check.md with our examples and expected results.
Link that file from SKILL.md and say when to read it.
Show me the files and explain how to use the skill.
```

Find the file it creates:

- Copilot: `.github/skills/check-work/SKILL.md`
- OpenCode: `.opencode/skills/check-work/SKILL.md`

The first lines should look like this. They are **YAML frontmatter**, the information the app uses to find the skill:

```yaml
---
name: check-work
description: Run this project's checks and report what passed, failed, or could not be checked.
---
```

Keep the steps in `SKILL.md` short. The reference file holds your longer examples, so the agent can read them when it needs them. This is **progressive disclosure**: load a skill's instructions when you use it, then load its extra files when a step needs them.

Some skills also have `scripts/` for code they run and `assets/` for templates or other files they use. Your skill needs the reference you asked for; you do not have to create every kind of folder.

## Use your new skill twice

Start a new chat in the project if your app has not found the skill. Paste this into chat; use `@check-work` in OpenCode:

```text
/check-work Check my project against BRIEF.md.
Run the checks and report what passed, failed, or could not be checked.
Do not change the app.
```

If the skill is missing, give the agent the `SKILL.md` path above and ask it to read and follow that file.

Next, ask the agent to add one automatic check for another example from your brief. Read its explanation and approve that test change. Use the skill again:

```text
/check-work Run our checks again after the test change.
Show the new test result and any failures. Do not fix them yet.
```

## Evidence and checkpoint

Save the skill, its reference file, and both check reports. Look in the chat's tool activity for the skill and reference-file reads, then find the test command and its result. Ask your facilitator if you cannot find them. An agent saying "I used the skill" is not enough to show that it ran the checks.

<details>
<summary>Hint</summary>

The skill should name your project's real checks from level 2. It should not copy a test command for a different project.

</details>

Previous: [Level 2: Build your first feature](level-2-build.md) · Next: [Level 4: Extend and review](level-4-review.md)
