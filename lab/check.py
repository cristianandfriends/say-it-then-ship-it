#!/usr/bin/env python3
"""Black-box checks for the default study queue at workshop levels 2 and 4."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any, List, Optional, Sequence
import uuid


class CheckFailure(Exception):
    """An observed command or data state violates the workshop contract."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckFailure(message)


def json_equal(actual: Any, expected: Any) -> bool:
    # Python equality treats True as 1, but the CLI contract requires JSON booleans.
    return json.dumps(actual, sort_keys=True) == json.dumps(expected, sort_keys=True)


def run_cli(
    project: Path,
    data_file: Path,
    arguments: Sequence[str],
    expect_success: bool = True,
    timeout: float = 5.0,
) -> Any:
    command = [
        sys.executable,
        "-m",
        "study_queue",
        "--file",
        str(data_file),
    ] + list(arguments)
    label = " ".join(arguments)
    try:
        result = subprocess.run(
            command,
            cwd=str(project),
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise CheckFailure(
            "{}: timed out after {} seconds".format(label, timeout)
        ) from error
    except (OSError, UnicodeError) as error:
        raise CheckFailure("{}: could not run CLI: {}".format(label, error)) from error

    detail = (result.stderr.strip() or result.stdout.strip())[:500]
    if expect_success:
        require(
            result.returncode == 0,
            "{}: expected exit 0, got {}. {}".format(label, result.returncode, detail),
        )
        try:
            return json.loads(result.stdout)
        except ValueError as error:
            raise CheckFailure(
                "{}: stdout must contain one JSON value, got {!r}".format(
                    label, result.stdout[:500]
                )
            ) from error

    require(
        result.returncode != 0,
        "{}: expected a nonzero exit, got 0. {}".format(label, detail),
    )
    return None


def reject_without_change(
    project: Path, data_file: Path, arguments: Sequence[str], timeout: float = 5.0
) -> None:
    before = data_file.read_bytes() if data_file.exists() else None
    run_cli(project, data_file, arguments, expect_success=False, timeout=timeout)
    after = data_file.read_bytes() if data_file.exists() else None
    require(
        before == after,
        "{}: rejected input changed the store bytes or created/deleted it".format(
            " ".join(arguments)
        ),
    )


def read_store(path: Path) -> Any:
    try:
        store = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        raise CheckFailure("Could not read saved JSON at {}: {}".format(path, error)) from error
    require(isinstance(store, dict), "Saved JSON must have an object root")
    require(isinstance(store.get("items"), list), "Saved JSON must have an items array")
    return store


def new_item(value: Any, item_id: int, text: str) -> Any:
    require(isinstance(value, dict), "add must return a JSON item object")
    require(
        type(value.get("id")) is int and value["id"] == item_id,
        "add: expected integer ID {}, got {!r}".format(item_id, value.get("id")),
    )
    require(value.get("text") == text, "add: returned text differs from input")
    require(value.get("done") is False, "add: a new item's done field must be false")
    return value


def check_list(
    project: Path, data_file: Path, expected: List[Any], timeout: float
) -> None:
    before = data_file.read_bytes() if data_file.exists() else None
    require(
        json_equal(run_cli(project, data_file, ["list"], timeout=timeout), expected),
        "list must return stored items in order with their JSON types and metadata",
    )
    after = data_file.read_bytes() if data_file.exists() else None
    require(before == after, "list changed the store bytes or created/deleted it")


def _check_fixtures(
    level: int, project: Path, scratch: Path, timeout: float
) -> List[str]:
    passed = []
    queue = scratch / "queue.json"
    check_list(project, queue, [], timeout)
    reject_without_change(project, queue, ["add", " \t "], timeout)
    passed.append("missing-file list and blank add leave no file")

    first = new_item(
        run_cli(project, queue, ["add", "Read chapter 1"], timeout=timeout),
        1,
        "Read chapter 1",
    )
    second = new_item(
        run_cli(project, queue, ["add", "Practice café notes"], timeout=timeout),
        2,
        "Practice café notes",
    )
    expected = [first, second]
    require(json_equal(read_store(queue)["items"], expected), "Saved items differ from add output")
    check_list(project, queue, expected, timeout)
    reject_without_change(project, queue, ["add", ""], timeout)
    reject_without_change(project, queue, ["add", " \t "], timeout)
    passed.append("repeated adds/list agree, with IDs 1 and 2; blank input preserves bytes")

    metadata_file = scratch / "metadata.json"
    existing = {"id": 7, "text": "Keep notes", "done": False, "topic": "algebra"}
    metadata = {"course": "ScaleUP", "settings": {"view": "all"}}
    metadata_file.write_text(
        json.dumps(dict(metadata, items=[existing]), ensure_ascii=False),
        encoding="utf-8",
    )
    added = new_item(
        run_cli(project, metadata_file, ["add", "Check examples"], timeout=timeout),
        8,
        "Check examples",
    )
    saved = read_store(metadata_file)
    require(json_equal(saved["items"], [existing, added]), "add changed an existing item or its metadata")
    for key, value in metadata.items():
        require(json_equal(saved.get(key), value), "add changed root metadata: " + key)
    check_list(project, metadata_file, [existing, added], timeout)
    passed.append("max + 1 IDs and root/item metadata survive add/list")

    if level == 4:
        updated = dict(first, done=True)
        require(
            json_equal(run_cli(project, queue, ["done", "1"], timeout=timeout), updated),
            "done must return the updated item object",
        )
        expected = [updated, second]
        require(json_equal(read_store(queue)["items"], expected), "done changed unrelated item data")
        check_list(project, queue, expected, timeout)
        reject_without_change(project, queue, ["done", "999"], timeout)
        passed.append("done updates one item; unknown ID preserves bytes")

        updated_existing = dict(existing, done=True)
        require(
            json_equal(
                run_cli(project, metadata_file, ["done", "7"], timeout=timeout),
                updated_existing,
            ),
            "done lost existing item fields in its output",
        )
        saved = read_store(metadata_file)
        require(
            json_equal(saved["items"], [updated_existing, added]),
            "done changed unrelated items or item metadata",
        )
        for key, value in metadata.items():
            require(json_equal(saved.get(key), value), "done changed root metadata: " + key)
        passed.append("done preserves root metadata and unknown item fields")

    corrupted = scratch / "corrupted.json"
    corrupted.write_bytes(b'{"items": [\n')
    commands = [["list"], ["add", "Do not replace corrupted data"]]
    if level == 4:
        commands.append(["done", "1"])
    for arguments in commands:
        reject_without_change(project, corrupted, arguments, timeout)
    passed.append("malformed JSON fails without changing original bytes")
    return passed


def run_checks(level: int, project: Path, timeout: float = 5.0) -> List[str]:
    require(level in (2, 4), "Only levels 2 and 4 have automated checks")
    project = project.resolve()
    require(project.is_dir(), "Project directory does not exist: " + str(project))
    # Keep disposable fixture data inside the supplied project, not system temp.
    scratch = project / (".study-queue-check-" + uuid.uuid4().hex)
    scratch.mkdir()
    try:
        return _check_fixtures(level, project, scratch, timeout)
    finally:
        shutil.rmtree(str(scratch))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", required=True, type=int, choices=(2, 4))
    parser.add_argument("--project", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        passed = run_checks(args.level, args.project)
    except (CheckFailure, OSError) as error:
        print("FAIL: {}".format(error), file=sys.stderr)
        return 1
    for message in passed:
        print("PASS: " + message)
    print("Level {} default-project checks passed.".format(args.level))
    return 0


if __name__ == "__main__":
    sys.exit(main())
