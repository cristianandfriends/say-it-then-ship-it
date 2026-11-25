"""Check the standalone launcher's payload without installing Windows software."""

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
POWERSHELL = shutil.which("pwsh") or shutil.which("powershell.exe")


@unittest.skipUnless(POWERSHELL, "Requires PowerShell to check the embedded installer")
class InstallerLauncherTests(unittest.TestCase):
    def setUp(self):
        work = tempfile.TemporaryDirectory(prefix="setup 'quoted' & 100% ! \u00e9 ")
        self.addCleanup(work.cleanup)
        self.work = Path(work.name)
        self.launcher = self.work / "install.cmd"
        self.shipped = (ROOT / "install.cmd").read_text(encoding="utf-8")
        self.header, separator, self.payload = self.shipped.partition(
            "\n# POWERSHELL_PAYLOAD\n"
        )
        self.assertTrue(separator, "Missing embedded installer")
        command = re.search(r' -Command "([^"\r\n]+)"', self.header)
        self.assertIsNotNone(command, "Missing PowerShell loader")
        self.loader = command.group(1)

    def run_loader(self, content):
        self.launcher.write_text(content, encoding="utf-8")
        environment = dict(os.environ)
        environment["PREREQUISITES_LAUNCHER"] = str(self.launcher)
        environment["OS"] = "NotWindows"
        return subprocess.run(
            [
                POWERSHELL,
                "-NoLogo",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                self.loader,
            ],
            env=environment,
            cwd=self.work,
            text=True,
            capture_output=True,
            stdin=subprocess.DEVNULL,
            timeout=30,
            check=False,
        )

    def with_payload(self, payload):
        return self.header + "\n# POWERSHELL_PAYLOAD\n" + payload

    def test_shipped_launcher_loads_without_a_companion_script(self):
        result = self.run_loader(self.shipped)
        self.assertFalse((self.work / "install-prerequisites.ps1").exists())
        self.assertEqual(result.returncode, 1)
        self.assertIn("outside WSL", result.stderr)
        self.assertNotIn("Setup finished", result.stdout)

    def test_standalone_payload_success_returns_zero(self):
        result = self.run_loader(self.with_payload("Write-Output 'standalone success'"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("standalone success", result.stdout)

    def test_payload_errors_remain_failures(self):
        for payload in ("throw 'simulated installation failure'", "param(\n"):
            with self.subTest(payload=payload):
                result = self.run_loader(self.with_payload(payload))
                self.assertEqual(result.returncode, 1)
                self.assertTrue(result.stderr)
                self.assertNotIn("Setup finished", result.stdout)

    def test_incomplete_launcher_reports_a_visible_error(self):
        result = self.run_loader(self.header)
        self.assertEqual(result.returncode, 1)
        self.assertIn("launcher is incomplete", result.stderr)

    def test_regeneration_preserves_the_shipped_standalone_installer(self):
        source = self.work / "install-prerequisites.ps1"
        shutil.copyfile(ROOT / source.name, source)
        result = subprocess.run(
            [
                POWERSHELL,
                "-NoLogo",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(source),
                "-BuildLauncher",
            ],
            cwd=self.work,
            text=True,
            capture_output=True,
            stdin=subprocess.DEVNULL,
            timeout=30,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.launcher.read_bytes(), (ROOT / "install.cmd").read_bytes()
        )


if __name__ == "__main__":
    unittest.main()
