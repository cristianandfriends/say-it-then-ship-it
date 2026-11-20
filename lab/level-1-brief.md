---
title: "Level 1: Write the brief"
description: Approve one goal, examples, acceptance criteria, and a bounded plan.
order: 2
level: 1
---

# Level 1: Write the brief

## Goal

Write an approved `BRIEF.md` before asking for code.

## Input and task

Use your project instructions from level 0. Choose one goal: manage a local study queue from a Python CLI, or your own project with equivalent observable checks. Ask the agent to draft `BRIEF.md` with the user, goal, constraints, examples, acceptance criteria, and a small implementation plan. Use the installed stop-slop skill for its prose. Approve or revise the brief. Do not write application code yet, or invoke a skill that builds a large app in one pass.

Use an instruction, context, examples, and an output contract in your prompt:

```text
Read AGENTS.md. Draft BRIEF.md for a local Python study queue.
I want to save study tasks and inspect the queue from a terminal.
Use Python 3.9+ standard library. No service or network calls.
Include the CLI/data contract from this level, failure cases, and a
bounded plan for add/list. Reserve done for level 4.
Return the brief and open decisions. Do not write application code.
```

### Default project contract

Run commands from the student project:

```text
python -m study_queue --file queue.json add "Read chapter 1"
python -m study_queue --file queue.json list
```

- Store UTF-8 JSON with an object root and an `items` array. The first add creates a missing store with `{"items":[{"id":1,"text":"Read chapter 1","done":false}]}`.
- Give each new item an integer ID of the current maximum plus one, starting at 1 for an empty queue. Keep IDs after completion.
- `add` writes one JSON item object to stdout. `list` writes the JSON array of stored items in stored order, with no prose on stdout or data changes. Both exit zero on success.
- A missing-file `list` returns `[]` without creating the file.
- Reject blank or whitespace-only text with a nonzero exit and no data change, including no file creation for a missing store.
- Preserve unrelated root keys and fields of existing items when writing. For example, keep root `course` and an existing item's `topic` field after an add.
- On malformed JSON, exit nonzero and preserve the original bytes. Do not reset the store. Put error messages on stderr.

At level 4, add `python -m study_queue --file queue.json done <id>`. It must set that item's `done` to `true`, return the updated object as JSON, and preserve its other fields, other items, and root metadata. Unknown IDs must exit nonzero without changing bytes. Keep the same malformed-JSON behavior.

The checker uses separate fixture files passed through `--file`. It checks repeated adds, list, blank input, corrupted JSON, metadata preservation, and, at level 4, completion and unknown IDs. It does not grade your prose. For your own idea, write equivalent checks in the brief and keep their results instead.

## Evidence and checkpoint

Save `BRIEF.md` and your approval. Include an empty-queue example, two adds with IDs 1 and 2, and a failed blank add. Name the files and focused tests you expect at level 2. Keep the plan limited to `add` and `list`.

<details>
<summary>Hint</summary>

Replace vague acceptance criteria such as "handles errors" with a command, exit status, expected stdout, and expected file state.

</details>

Previous: [Level 0: Bootstrap your project](level-0-bootstrap.md) · Next: [Level 2: Build the first slice](level-2-build.md)
