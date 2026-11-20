---
title: "Level 4: Extend and review"
description: Make one project improvement and get an independent read-only review.
order: 5
level: 4
---

# Level 4: Extend and review

## Goal

Make one bounded improvement, get an independent review, and fix reproduced findings.

## Input and task

Choose one improvement from your project's deferred work, or a bug you can reproduce. Update `BRIEF.md` with its acceptance criteria and name the existing behavior the change must preserve.

Give the installed software-engineering-expert agent the brief and that bounded task. Ask it to implement the change and focused tests within the approved scope. Use the native agent file you inspected in level 0. Preserve its harness metadata.

Run `check-work` after implementation. Include checks for the new behavior and regressions in the working version. Check preservation of unrelated data when your change writes data.

After implementation stops, delegate a read-only review to a fresh general-purpose worker in Copilot or a fresh general worker in OpenCode. Use your harness's supported controls. Give the worker the brief, changed-file scope, diff or before/after excerpts, and commands/results. Git is not required: provide saved before/after text and the changed files if no diff tool exists.

```text
Review this change against BRIEF.md and the approved scope.
Use the supplied changed files, before/after input, and check results.
Do not edit files. Look for bugs, missing acceptance criteria,
and regressions in existing behavior.
For each finding, name the file, the failing input, and reproduction.
Report checks you ran, evidence, and anything you could not verify.
```

Keep the implementer and reviewer from editing shared files at the same time. If the harness cannot spawn a worker, the orchestrator must start an independent review session and supply the same bounded input. Record the review as pending until that session returns findings. Do not claim a review that did not occur.

Reproduce findings before fixing them. Ask the implementer to fix confirmed bugs and rerun `check-work`. Keep evidence for any finding you reject. Run the new acceptance checks and the existing checks yourself. Use the commands and manual steps recorded for your project. See [Work with two agents](two-agents.md) for the review/handoff loop.

## Evidence and checkpoint

Keep the changed-file scope, reviewer/session identity, review input, actual findings, reproductions, fixes, and final commands/results. Record "no findings" with what the reviewer checked if that is the result. A pending review remains a gap even if tests pass.

<details>
<summary>Hint</summary>

Give the reviewer a concrete example the change could break. Ask it to compare expected and observed behavior, including work outside the changed feature that must remain intact.

</details>

Previous: [Level 3: Make a check-work skill](level-3-skill.md) · Next: [Level 5: Hand off the context](level-5-context.md)
