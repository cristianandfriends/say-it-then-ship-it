---
title: "Level 2: Build your first feature"
description: Ask your agent to build one feature, then try it yourself.
order: 3
level: 2
---

# Level 2: Build your first feature

## Goal

Build the first feature from `BRIEF.md` and check what it does.

## Input and task

Use the approved `BRIEF.md` from [level 1](level-1-brief.md). Ask the `software-engineering-expert` agent to build the first feature and leave the "Later" list alone. Its instructions cover how to write tests and get a separate review.

A **test** is a small piece of code that checks whether something gives the expected result. Your agent can write and run tests. You will try the feature yourself too.

Paste this into chat, replacing the brackets:

```text
Use the software-engineering-expert agent to build [the first feature I approved].
Use BRIEF.md and follow the agent's engineering instructions.
Check the example that should work and the example with a mistake.
Explain how I can open or run the project and try those examples.
Tell me what files changed and what you could not check.
```

Use made-up information while checking. If the project saves information, check that a failed action does not erase something you wanted to keep. Ask the agent to explain what code and new packages will do before you approve running or installing them.

## Try it yourself

Ask the agent to run the checks from your brief and show the results. You will turn those steps into the `check-work` skill in level 3. You do not need to choose a test command from someone else's project.

Have the agent write your project's run instructions and check commands in `BRIEF.md`. Follow its run instructions, with your facilitator's help if needed. Try your two examples and compare what you see with what the brief says you should see.

If something differs, save the error or describe what happened. Ask the agent to explain the cause before you approve a fix. Keep your original expected result unless you decide to change the plan.

## Evidence and checkpoint

Save the changed-file list and test report. For each example, record what you did, what you expected, and what happened. Demonstrate your first feature and the example with a mistake. Note anything you could not check.

<details>
<summary>Hint</summary>

If the agent starts building several features, stop it. Point to the one feature you approved in `BRIEF.md`.

</details>

Previous: [Level 1: Write the brief](level-1-brief.md) · Next: [Level 3: Make a check-work skill](level-3-skill.md)
