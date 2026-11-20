---
title: "Level 4: Add a command and review it"
description: Implement done and ask an independent read-only worker to review the change.
order: 5
level: 4
---

# Level 4: Add a command and review it

## Goal

Add `done`, get an independent review, and fix reproduced findings.

## Input and task

Give the installed software-engineering-expert agent your brief and one bounded task: implement `done` and focused tests without changing `add` or `list` behavior. Use the native agent file you inspected in level 0. Preserve its harness metadata.

The command is:

```text
python -m study_queue --file practice-level-4.json done 1
```

Create a fixture item with `add` before running it. On success, `done` exits zero and returns the saved item object as JSON with `done: true`. It keeps the ID, text, unknown item fields, other items, and unrelated root keys. An unknown ID must exit nonzero without changing bytes. Malformed JSON must produce a nonzero exit and preserve the bytes for `add`, `list`, and `done`. Do not replace corrupted data with an empty store.

After implementation stops, delegate a read-only review to a fresh general-purpose worker in Copilot or a fresh general worker in OpenCode. Use your harness's supported controls. Give the worker the brief, changed-file scope, diff or before/after excerpts, and commands/results. Git is not required: provide saved before/after text and the changed files if no diff tool exists.

```text
Review this done-command change against BRIEF.md and the supplied
before/after input. Do not edit files. Check data preservation,
unknown IDs, malformed JSON, and regressions in add/list.
For each finding, name the file, the failing input, and reproduction.
Report checks you ran, evidence, and anything you could not verify.
```

Keep the implementer and reviewer from editing shared files at the same time. If the harness cannot spawn a worker, the orchestrator must start an independent review session and supply the same bounded input. Record the review as pending until that session returns findings. Do not claim a review that did not occur.

Reproduce findings before fixing them. Ask the implementer to fix confirmed bugs and rerun `check-work`. Keep evidence for any finding you reject. Run your own checks:

```text
python -m unittest discover -s tests -v
python workshop/lab/check.py --level 4 --project student-project
```

Run the test command from the student project; adjust the checker paths for your current folder. Level 4 runs the level 2 checks plus completion, unknown-ID preservation, and completion with metadata. See [Work with two agents](two-agents.md) for the review/handoff loop.

## Evidence and checkpoint

Keep the changed-file scope, reviewer/session identity, review input, actual findings, reproductions, fixes, and final commands/results. Record "no findings" with what the reviewer checked if that is the result. A pending review remains a gap even if tests pass.

<details>
<summary>Hint</summary>

Give a reviewer a fixture with a root `course` field and an item `topic` field. Ask it to compare the entire object before and after `done`, including the metadata.

</details>

Previous: [Level 3: Make a check-work skill](level-3-skill.md) · Next: [Level 5: Hand off the context](level-5-context.md)
