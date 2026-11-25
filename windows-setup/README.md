# Windows setup

Double-click **install.cmd** in File Explorer. You can distribute that file alone;
it contains the installer and needs no companion files.

Use Windows 10 or 11 with WinGet (App Installer) and internet access. Run as the
user who will use the tools. Approve Windows permission prompts if they appear.
By running the launcher, you accept package and source agreements.

Use it to install or update Copilot CLI, Visual Studio Code, stable Python 3, and
the Copilot and Python VS Code extensions. After setup, reopen your terminals and
VS Code, then sign in to Copilot with your GitHub account.

Windows installation remains untested.

## Maintain the installer

Edit `install-prerequisites.ps1`, then regenerate the standalone launcher from
this directory:

```powershell
pwsh -NoProfile -File ./install-prerequisites.ps1 -BuildLauncher
```

Keep `install.cmd`'s CRLF line endings; `.gitattributes` preserves them in Git.
Run the loader and regeneration checks with Python and PowerShell on PATH:

```text
python -m unittest discover -s tests -p test_install_prerequisites.py -v
```

These checks do not install Windows software.
