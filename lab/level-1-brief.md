---
title: "Level 1: Write the brief"
description: Choose an idea, describe one feature, and decide how to check it.
order: 2
level: 1
---

# Level 1: Write the brief

## Goal

Choose an idea and write a short plan in `BRIEF.md` before asking for code.

## Input and task

Open your student project from level 0. Describe something you want to make and who would use it. If you have no idea, tell the agent about an interest and ask it to suggest two projects you could try.

Pick **one thing** your first version should do. Ask whether you can build it with Python on your workshop computer. If your full idea needs tools you do not have, choose a smaller version you can try here and list what you will leave for later.

`BRIEF.md` is a Markdown file containing that plan. Use `stop-slop` to help write it in plain language. Paste this into chat, replacing the brackets. In OpenCode, use `@stop-slop`.

```text
/stop-slop Help me write BRIEF.md, a short plan for my project.
I want to build [idea] for [who will use it].
The first thing I want them to do is [one action].
Keep the first version small enough to run on this workshop computer.
Ask me about choices instead of guessing.
Include examples I can try, what I should see, and a short build plan.
Explain unfamiliar terms. Do not write the app yet.
```

## Agree on what to build

Agree on:

- **Who:** the person you are building for. That person can be you.
- **First feature:** one thing they can do with your project.
- **How to try it:** what they type, click, or give it, and what they should see.
- **Limits:** what this version will leave out.

Write one example that should work and one where the person gives it something unexpected. An **acceptance check** is an example you try to decide whether the feature works as agreed.

For example, if you choose a quiz game:

- Pick the correct answer to a sample question. You should see "Correct" and earn a point.
- Leave the answer blank. You should see a request to choose an answer, and your score should stay the same.

Use your own idea for your checks. Write the steps so a classmate could try them. If your app saves information, say what should stay unchanged when someone makes a mistake.

Read `BRIEF.md` and ask the agent to explain anything you cannot follow. Approve the plan or request changes before level 2. Keep extra ideas in a "Later" section.

## Evidence and checkpoint

Save `BRIEF.md` and your approval in the chat or your notes. Explain the first feature in your own words and show the examples you will use to check it.

<details>
<summary>Hint</summary>

Try saying, "When I do this, I expect to see that." Then ask, "What should happen if I leave something blank?" Choose a mistake that makes sense for your project.

</details>

Previous: [Level 0: Bootstrap your project](level-0-bootstrap.md) · Next: [Level 2: Build your first feature](level-2-build.md)
