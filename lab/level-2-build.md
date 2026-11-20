---
title: "Level 2: Build the first slice"
description: Implement add and list, then check the CLI from outside its code.
order: 3
level: 2
---

# Level 2: Build the first slice

## Goal

Build the smallest working `add` and `list` commands, with focused tests.

## Input and task

Give your coding agent `AGENTS.md`, the approved `BRIEF.md`, and the [level 1 contract](level-1-brief.md). Ask it to implement a Python 3.9+ standard-library CLI and `unittest` tests. Keep `done` out of this change.

Require `python -m study_queue --file <path> add "Read chapter 1"` and `... list`. An add returns its new JSON object; list returns a JSON array in stored order. IDs start at 1 and increase by max + 1. Check missing-file behavior, whitespace-only text, malformed JSON, and preservation of root/item metadata. Use the exact contract in your brief, with diagnostics on stderr and nonzero error exits.

Ask the agent for tests that would catch a real failure: repeated adds and list, blank-text rejection with no writes, and malformed bytes that survive failed commands. Include a metadata fixture. Inspect the changes before you run code.

From the student project, run your tests and the CLI yourself. Use a new practice filename:

```text
python -m unittest discover -s tests -v
python -m study_queue --file practice-level-2.json list
python -m study_queue --file practice-level-2.json add "Read chapter 1"
python -m study_queue --file practice-level-2.json add "Review notes"
python -m study_queue --file practice-level-2.json list
```

Before the first add, confirm that list printed `[]` and did not create the file. After the adds, expect IDs 1 and 2, with `done` false.

Run the workshop checker from any folder, substituting paths:

```text
python workshop/lab/check.py --level 2 --project student-project
```

The checker uses your selected Python interpreter and runs your code from the project directory. It creates disposable data paths inside the project, passes them with `--file`, and removes its scratch directory when done. It does not pass your real queue path. Review code first: the checker cannot sandbox student code that ignores `--file`. Each subprocess has a five-second timeout; there is no timed grade.

The checker covers the default project at levels 2 and 4. For another idea, record equivalent black-box checks from your approved brief.

## Evidence and checkpoint

Keep the changed file list, test command/output, manual JSON results, and checker command/output with its exit status. Resolve failures and rerun. Read a store file to verify that stdout and saved data agree before you proceed.

<details>
<summary>Hint</summary>

Tell the agent to separate argument parsing, reading/writing JSON, and queue operations. Ask it to explain the point where it validates data before writing.

</details>

Previous: [Level 1: Write the brief](level-1-brief.md) · Next: [Level 3: Make a check-work skill](level-3-skill.md)
