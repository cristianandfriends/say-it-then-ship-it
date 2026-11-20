"""Behavior checks for the stdlib-only workshop installer."""

import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import unittest
from unittest import mock
from uuid import uuid4


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents" / "skills" / "bootstrap-lab"
SCRIPT = SKILL / "scripts" / "bootstrap_lab.py"
AGENT = ROOT / ".github" / "agents" / "software-engineering-expert.agent.md"


class BootstrapLabTests(unittest.TestCase):
    def setUp(self):
        self.work = ROOT / "tests" / (".bootstrap-lab-test-" + uuid4().hex)
        self.work.mkdir()
        self.addCleanup(shutil.rmtree, self.work)
        self.source = self.work / "workshop"
        self.target = self.work / "student project"
        self.home = self.work / "home"
        self.home.mkdir()
        (self.home / ".config").mkdir()
        (self.home / ".config" / "keep.json").write_bytes(b"Keep global settings\n")
        for name in ("bootstrap-lab", "stop-slop", "frontend-design"):
            skill = self.source / ".agents" / "skills" / name
            (skill / "references").mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: " + name + "\n---\n", encoding="utf-8")
            (skill / "references" / "example.md").write_text("Reference\n", encoding="utf-8")
            (skill / "LICENSE").write_text("Fixture license\n", encoding="utf-8")
        bootstrap = self.source / ".agents" / "skills" / "bootstrap-lab"
        (bootstrap / "assets").mkdir()
        (bootstrap / "assets" / "AGENTS.md").write_bytes((SKILL / "assets" / "AGENTS.md").read_bytes())
        (bootstrap / "assets" / "binary.dat").write_bytes(b"\x00\xff\x01")
        (bootstrap / "scripts").mkdir()
        shutil.copyfile(SCRIPT, bootstrap / "scripts" / "bootstrap_lab.py")
        (self.source / ".github" / "agents").mkdir(parents=True)
        shutil.copyfile(AGENT, self.source / ".github" / "agents" / AGENT.name)

    def run_installer(self, harness="copilot", target=None, script=SCRIPT, source=None, extra=()):
        command = [
            sys.executable,
            str(script),
            "--harness",
            harness,
            "--target",
            str(target or self.target),
        ]
        if source is not False:
            command.extend(("--source", str(source or self.source)))
        environment = dict(os.environ)
        environment.update({
            "HOME": str(self.home),
            "USERPROFILE": str(self.home),
            "XDG_CONFIG_HOME": str(self.home / ".config"),
            "APPDATA": str(self.home / ".config"),
            "LOCALAPPDATA": str(self.home / ".config"),
            "PYTHONDONTWRITEBYTECODE": "1",
        })
        return subprocess.run(
            command + list(extra), text=True, capture_output=True, check=False, env=environment
        )

    def snapshot(self, root):
        if not root.exists():
            return {}
        return {
            str(path.relative_to(root)): (
                "link",
                os.readlink(path),
            ) if path.is_symlink() else (
                ("file", path.read_bytes(), path.stat().st_mtime_ns)
                if path.is_file() else ("directory",)
            )
            for path in root.rglob("*")
        }

    def test_harness_mappings_complete_copies_and_frontmatter(self):
        canonical = AGENT.read_text(encoding="utf-8")
        canonical_body = canonical.split("---", 2)[2]
        for harness, native, filename in (
            ("copilot", ".github", "software-engineering-expert.agent.md"),
            ("opencode", ".opencode", "software-engineering-expert.md"),
        ):
            with self.subTest(harness=harness):
                target = self.work / harness
                result = self.run_installer(harness=harness, target=target)
                self.assertEqual(result.returncode, 0, result.stderr)
                for name in ("bootstrap-lab", "stop-slop", "frontend-design"):
                    self.assertEqual(
                        (target / native / "skills" / name / "references" / "example.md").read_bytes(),
                        b"Reference\n",
                    )
                    self.assertEqual(
                        (target / native / "skills" / name / "LICENSE").read_bytes(),
                        b"Fixture license\n",
                    )
                self.assertEqual(
                    (target / native / "skills" / "bootstrap-lab" / "assets" / "binary.dat").read_bytes(),
                    b"\x00\xff\x01",
                )
                installed = (target / native / "agents" / filename).read_text(encoding="utf-8")
                header = installed.split("---", 2)[1]
                self.assertIn("description:", header)
                self.assertNotIn("model:", header)
                self.assertNotIn("tools:", header)
                self.assertEqual(installed.split("---", 2)[2], canonical_body)
                if harness == "copilot":
                    self.assertEqual(installed, canonical)
                    self.assertIn("name: software-engineering-expert", header)
                else:
                    self.assertIn("mode: subagent", header)
                    self.assertNotIn("name:", header)
                    self.assertEqual(
                        installed,
                        (ROOT / ".opencode" / "agents" / filename).read_text(encoding="utf-8"),
                        "Keep the native OpenCode agent in sync with bootstrap output.",
                    )
                self.assertEqual(set(path.name for path in target.iterdir()), {native, "AGENTS.md"})

    def test_python_validation_artifacts_are_excluded_for_both_harnesses(self):
        for name in ("bootstrap-lab", "stop-slop", "frontend-design"):
            skill = self.source / ".agents" / "skills" / name
            for relative in (
                "__pycache__/bootstrap.cpython-39.pyc",
                "references/__pycache__/nested/not-a-reference.md",
                "references/example.pyc",
                "loose.pyc",
            ):
                artifact = skill / relative
                artifact.parent.mkdir(parents=True, exist_ok=True)
                artifact.write_bytes(b"Generated artifact\n")
        before = self.snapshot(self.source)
        for harness in ("copilot", "opencode"):
            with self.subTest(harness=harness):
                target = self.work / harness
                result = self.run_installer(harness=harness, target=target)
                self.assertEqual(result.returncode, 0, result.stderr)
                for path in target.rglob("*"):
                    self.assertNotIn("__pycache__", path.parts)
                    self.assertNotEqual(path.suffix, ".pyc")
        self.assertEqual(self.snapshot(self.source), before)

    def test_rerun_preserves_files_and_existing_instructions(self):
        self.target.mkdir()
        user_prose = b"# My project\n\nPreserve this instruction without edits."
        (self.target / "AGENTS.md").write_bytes(user_prose)
        for filename in ("opencode.json", "README.md"):
            (self.target / filename).write_text("User content", encoding="utf-8")
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        instructions = (self.target / "AGENTS.md").read_bytes()
        self.assertTrue(instructions.startswith(user_prose))
        for expected in (b"Python 3.9+", b"PyPI", b"uv", b"virtual environment", b"system Python"):
            self.assertIn(expected, instructions)
        self.assertEqual(instructions.count(b"<!-- bootstrap-lab:begin -->"), 1)
        with (self.target / "AGENTS.md").open("ab") as stream:
            stream.write(b"\nPreserve instructions after the block too.\n")
        before = self.snapshot(self.target)
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Already installed", result.stdout)
        self.assertEqual(self.snapshot(self.target), before)
        self.assertEqual((self.target / "opencode.json").read_text(encoding="utf-8"), "User content")

    def test_conflicts_preserve_everything_without_partial_writes(self):
        for relative in (
            ".github/skills/stop-slop/SKILL.md",
            ".github/agents/software-engineering-expert.agent.md",
        ):
            with self.subTest(relative=relative):
                target = self.work / ("conflict-" + uuid4().hex)
                conflict = target / relative
                conflict.parent.mkdir(parents=True)
                conflict.write_bytes(b"Keep my changes\n")
                (target / "AGENTS.md").write_bytes(b"Keep existing instructions\n")
                (target / "unrelated.txt").write_bytes(b"Keep this too\n")
                before = self.snapshot(target)
                for options in ((), ("--dry-run",)):
                    result = self.run_installer(target=target, extra=options)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("No files were changed", result.stderr)
                    self.assertIn("merge by hand", result.stderr)
                    self.assertEqual(self.snapshot(target), before)

    def test_changed_or_malformed_managed_block_requires_manual_merge(self):
        for content in (
            b"User prose\n<!-- bootstrap-lab:begin -->\nChanged\n<!-- bootstrap-lab:end -->\n",
            b"User prose\n<!-- bootstrap-lab:begin -->\n",
        ):
            with self.subTest(content=content):
                target = self.work / ("instructions-" + uuid4().hex)
                target.mkdir()
                (target / "AGENTS.md").write_bytes(content)
                before = self.snapshot(target)
                result = self.run_installer(target=target)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Manually merge", result.stderr)
                self.assertEqual(self.snapshot(target), before)

    @unittest.skipUnless(hasattr(os, "symlink"), "Host lacks symlink support")
    def test_symlink_destinations_and_source_escape_are_rejected(self):
        outside = self.work / "outside"
        outside.mkdir()
        (outside / "sentinel").write_bytes(b"Unrelated\n")
        links = (
            self.work / "linked-target",
            self.work / "linked-child" / ".github",
            self.work / "dangling-agent" / ".github" / "agents" / AGENT.name,
        )
        for index, link in enumerate(links):
            with self.subTest(link=link):
                link.parent.mkdir(parents=True, exist_ok=True)
                try:
                    link.symlink_to(
                        outside if index < 2 else outside / "missing", target_is_directory=index < 2
                    )
                except OSError as error:
                    self.skipTest("Host does not permit symlinks: " + str(error))
                target = link if index == 0 else self.work / ("linked-child" if index == 1 else "dangling-agent")
                before = self.snapshot(outside)
                result = self.run_installer(target=target)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Symlink", result.stderr)
                self.assertEqual(self.snapshot(outside), before)
                self.assertFalse((target / "AGENTS.md").exists())
        result = self.run_installer(target=links[0] / ".." / "escaped")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Symlink", result.stderr)
        self.assertFalse((self.work / "escaped").exists())
        source_file = self.source / ".agents" / "skills" / "stop-slop" / "references" / "escape"
        source_file.symlink_to(outside / "sentinel")
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Symlink", result.stderr)
        self.assertFalse(self.target.exists())

    def test_dry_run_and_installed_copy_need_no_network_or_global_edits(self):
        global_settings = self.snapshot(self.home)
        result = self.run_installer(extra=("--dry-run",))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.target.exists())
        self.target.mkdir()
        (self.target / "AGENTS.md").write_bytes(b"# Preserve my project instructions\n")
        (self.target / "opencode.json").write_bytes(b'{"keep": true}\n')
        before = self.snapshot(self.target)
        result = self.run_installer(harness="opencode", extra=("--dry-run",))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(self.target), before)
        result = self.run_installer(harness="opencode")
        self.assertEqual(result.returncode, 0, result.stderr)
        installed_script = self.target / ".opencode" / "skills" / "bootstrap-lab" / "scripts" / SCRIPT.name
        next_target = self.work / "next-project"
        result = self.run_installer(script=installed_script, target=next_target, source=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--source <workshop>", result.stderr)
        self.assertFalse(next_target.exists())
        result = self.run_installer(script=installed_script, target=next_target)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.work / ".config").exists())
        self.assertFalse((next_target / "opencode.json").exists())
        self.assertFalse((next_target / ".agents").exists())
        self.assertEqual(self.snapshot(self.home), global_settings)

    def test_target_inside_source_and_directory_collisions_fail_before_writes(self):
        target = self.source / ".agents" / "skills" / "bootstrap-lab" / "project"
        result = self.run_installer(target=target)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("inside a canonical source", result.stderr)
        self.assertFalse(target.exists())
        collision = self.target / ".github" / "agents" / AGENT.name
        collision.mkdir(parents=True)
        before = self.snapshot(self.target)
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a regular file", result.stderr)
        self.assertEqual(self.snapshot(self.target), before)

    def test_partial_write_error_reports_failure_and_cleans_staging_file(self):
        module = runpy.run_path(str(SCRIPT), run_name="bootstrap_lab_test")
        real_link = os.link
        calls = 0

        def fail_second_link(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected disk error")
            real_link(source, destination)

        with mock.patch.object(os, "link", side_effect=fail_second_link):
            with self.assertRaisesRegex(module["InstallError"], "partial installation"):
                module["install"](self.source, self.target, "copilot", False)
        self.assertFalse(any(".bootstrap-" in path.name for path in self.target.rglob("*")))
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
