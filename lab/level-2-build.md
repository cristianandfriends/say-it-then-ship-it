---
title: "Level 2: Build the first slice"
description: Implement the first behavior from your brief and check the result.
order: 3
level: 2
---

# Level 2: Build the first slice

## Goal

Build the first behavior from your approved brief, with focused checks.

## Input and task

Give your coding agent `AGENTS.md` and the approved `BRIEF.md` from [level 1](level-1-brief.md). Ask it to implement the first behavior and tests for the agreed examples. Keep deferred features out of this change.

Use this prompt after replacing the bracketed field:

```text
Read AGENTS.md and BRIEF.md. Implement [the approved first behavior].
Keep the change within that scope and use our agreed interface.
Add focused tests for the normal case and failure or boundary case.
Explain how I can run it and reproduce each acceptance check.
Report changed files, commands/results, and anything you could not check.
```

Ask for tests that would fail if the required behavior were missing or broken. Use synthetic inputs or disposable fixtures. If the project writes data, check what it should preserve when an operation fails. Review code and dependency changes before running them.

From the student project, run the agreed checks with your selected interpreter. For a project using standard-library `unittest` tests in `tests/`, the command is:

```text
python -m unittest discover -s tests -v
```

Use your project's command if it differs, and record it in `BRIEF.md`. Try the feature through its intended interface and compare the result with your examples. For UI behavior, keep the manual steps and observed result alongside automated tests of the underlying logic.

If a check fails, keep the failure evidence, ask for a scoped fix, and rerun it. Ask before changing an acceptance criterion to accommodate the implementation.

## Evidence and checkpoint

Keep the changed file list, exact check commands or manual steps, expected results, and observed results. Demonstrate the first behavior and the failure or boundary case from your brief. Name anything you could not verify.

<details>
<summary>Hint</summary>

If the first version is too large to check, choose a smaller behavior with a visible result and revise the brief before implementing more.

</details>

Previous: [Level 1: Write the brief](level-1-brief.md) · Next: [Level 3: Make a check-work skill](level-3-skill.md)
