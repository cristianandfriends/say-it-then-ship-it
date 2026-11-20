---
title: "Level 1: Write the brief"
description: Choose your idea and approve a small first version with observable checks.
order: 2
level: 1
---

# Level 1: Write the brief

## Goal

Choose an idea and write an approved `BRIEF.md` before asking for code.

## Input and task

Use your project instructions from level 0. Describe something you want to make and who would use it. If you have no idea in mind, ask the agent to suggest two based on your interests and choose one.

Scope a first version that you can run in the supplied Python/PyPI environment. If the full idea needs unavailable services or tools, agree on a local prototype and name the work you will defer. Choose an interface that fits the idea; the lab does not require a CLI or a particular storage format.

Ask the agent to draft `BRIEF.md`. Use the installed stop-slop skill for its prose. Replace the bracketed fields in this prompt:

```text
Read AGENTS.md. I want to build [idea] for [intended user].
The first useful thing they should be able to do is [behavior].

Draft BRIEF.md with a small first version that fits our environment.
Ask about decisions that affect scope instead of inventing requirements.
Include concrete examples, acceptance checks, and a bounded plan.
Return the brief and open decisions. Do not write application code.
```

## Define your project's contract

Agree on:

- **User and outcome:** who will use it and the result they need.
- **First behavior:** one action they can perform and the result they can observe.
- **Examples and checks:** a normal case and a meaningful failure or boundary case, with expected results.
- **Scope and constraints:** the interface, required inputs, environment limits, and work to leave for later.

For each acceptance check, name the starting state, action or input, and expected result. Include the command or manual steps you will use to verify it. For a UI, describe the action and visible outcome; for a function or automation, give sample inputs and expected outputs. Specify data preservation when your project writes data.

Ask for a small implementation plan limited to the first behavior. Keep additional features in a deferred-work list. Approve or revise the brief before asking for implementation.

Use your approved brief as the contract for later levels. There is no shared application specification to match.

## Evidence and checkpoint

Save `BRIEF.md` and your approval. You should be able to explain the first behavior and demonstrate how you will decide whether it works. Keep the expected results and deferred work with the plan.

<details>
<summary>Hint</summary>

Replace "it works" with an example someone else can try. Name what they should see or receive, including the result of a failure or boundary case.

</details>

Previous: [Level 0: Bootstrap your project](level-0-bootstrap.md) · Next: [Level 2: Build the first slice](level-2-build.md)
