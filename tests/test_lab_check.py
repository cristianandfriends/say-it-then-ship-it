"""Tests for the workshop checker, without shipping a student implementation."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
from unittest import mock
import uuid


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("workshop_lab_check", ROOT / "lab" / "check.py")
lab_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab_check)


class LabCheckTests(unittest.TestCase):
    def setUp(self):
        self.project = ROOT / "lab" / (".lab-check-test-" + uuid.uuid4().hex)
        self.project.mkdir()
        self.addCleanup(shutil.rmtree, str(self.project))
        self.data = self.project / "fixture.json"

    def test_import_does_not_execute_student_code(self):
        with mock.patch.object(subprocess, "run") as run:
            spec = importlib.util.spec_from_file_location(
                "workshop_lab_check_import_test", ROOT / "lab" / "check.py"
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        run.assert_not_called()

    def test_command_reports_failures_and_requires_json_stdout(self):
        cases = [
            (0, "not JSON", "", True, "stdout must contain one JSON value"),
            (1, "", "broken store", True, "expected exit 0, got 1. broken store"),
            (0, "[]", "", False, "expected a nonzero exit"),
        ]
        for status, stdout, stderr, expect_success, message in cases:
            with self.subTest(message=message):
                result = subprocess.CompletedProcess([], status, stdout, stderr)
                with mock.patch.object(lab_check.subprocess, "run", return_value=result):
                    with self.assertRaisesRegex(lab_check.CheckFailure, message):
                        lab_check.run_cli(
                            self.project, self.data, ["list"], expect_success=expect_success
                        )

    def test_timeout_uses_selected_interpreter_and_project_directory(self):
        with mock.patch.object(
            lab_check.subprocess, "run", side_effect=subprocess.TimeoutExpired("study_queue", 0.1)
        ) as run:
            with self.assertRaisesRegex(lab_check.CheckFailure, "timed out"):
                lab_check.run_cli(self.project, self.data, ["list"], timeout=0.1)
        command = run.call_args.args[0]
        self.assertEqual(
            command,
            [sys.executable, "-m", "study_queue", "--file", str(self.data), "list"],
        )
        self.assertEqual(run.call_args.kwargs["cwd"], str(self.project))
        self.assertEqual(run.call_args.kwargs["timeout"], 0.1)

    def test_rejected_input_must_preserve_bytes_and_missing_file(self):
        original = b'{"items": [\n'
        self.data.write_bytes(original)
        failure = subprocess.CompletedProcess([], 1, "", "invalid data")
        with mock.patch.object(lab_check.subprocess, "run", return_value=failure):
            lab_check.reject_without_change(self.project, self.data, ["add", "task"])
        self.assertEqual(self.data.read_bytes(), original)

        def reset_corrupted_store(*args, **kwargs):
            self.data.write_bytes(b'{"items":[]}')
            return failure

        with mock.patch.object(lab_check.subprocess, "run", side_effect=reset_corrupted_store):
            with self.assertRaisesRegex(lab_check.CheckFailure, "changed the store bytes"):
                lab_check.reject_without_change(self.project, self.data, ["add", "task"])

        self.data.unlink()
        with mock.patch.object(lab_check.subprocess, "run", return_value=failure):
            lab_check.reject_without_change(self.project, self.data, ["add", " "])
        self.assertFalse(self.data.exists())
        with mock.patch.object(lab_check.subprocess, "run", side_effect=reset_corrupted_store):
            with self.assertRaisesRegex(lab_check.CheckFailure, "created/deleted"):
                lab_check.reject_without_change(self.project, self.data, ["add", " "])

    def test_list_rejects_mutation_and_wrong_json_types(self):
        expected = [{"id": 1, "text": "Read notes", "done": False, "topic": "math"}]
        original = json.dumps({"course": "ScaleUP", "items": expected}).encode("utf-8")
        self.data.write_bytes(original)
        with mock.patch.object(lab_check, "run_cli", return_value=expected):
            lab_check.check_list(self.project, self.data, expected, 5.0)
        for field, wrong_value in [("id", True), ("done", 0)]:
            wrong_item = dict(expected[0], **{field: wrong_value})
            with self.subTest(field=field):
                with mock.patch.object(lab_check, "run_cli", return_value=[wrong_item]):
                    with self.assertRaisesRegex(lab_check.CheckFailure, "JSON types"):
                        lab_check.check_list(self.project, self.data, expected, 5.0)

        def drop_metadata(*args, **kwargs):
            self.data.write_text(json.dumps({"items": expected}), encoding="utf-8")
            return expected

        with mock.patch.object(lab_check, "run_cli", side_effect=drop_metadata):
            with self.assertRaisesRegex(lab_check.CheckFailure, "list changed the store"):
                lab_check.check_list(self.project, self.data, expected, 5.0)

    def test_real_subprocess_failure_has_nonzero_result_and_cleans_fixtures(self):
        # A broken module exercises cwd, subprocess errors, and fixture cleanup.
        (self.project / "study_queue.py").write_text(
            "raise SystemExit('fixture failure')\n", encoding="utf-8"
        )
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            status = lab_check.main(["--level", "2", "--project", str(self.project)])
        self.assertEqual(status, 1)
        self.assertIn("fixture failure", stderr.getvalue())
        self.assertFalse(list(self.project.glob(".study-queue-check-*")))


if __name__ == "__main__":
    unittest.main()
