#requires -Version 5.1
<#
.SYNOPSIS
Install or update GitHub Copilot, Visual Studio Code, and stable Python 3.

.DESCRIPTION
Run on Windows 10 or 11 as the user who will use these tools, not as another
administrator account. Requires internet access and WinGet (App Installer).
Approve any Windows permission prompts.

For File Explorer, double-click install.cmd. That launcher embeds this installer;
you can distribute install.cmd alone.

The script accepts package and source agreements. It installs Copilot CLI,
VS Code, Python's install manager, the latest stable Python 3 runtime, and the
Copilot and Python VS Code extensions. WinGet supplies its latest available
releases; the Python install manager selects the Python runtime.

Review this file before running it. The example changes execution policy only
for the new PowerShell process. Organization policies may still block execution.
This script has not undergone an installation test on Windows.

.EXAMPLE
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install-prerequisites.ps1

.EXAMPLE
pwsh -NoProfile -File ./install-prerequisites.ps1 -BuildLauncher

Maintainers: regenerate install.cmd after editing this script.

.LINK
https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli

.LINK
https://docs.python.org/3/using/windows.html
#>

[CmdletBinding()]
param([switch]$BuildLauncher)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
# Check native exit codes ourselves, including WinGet's "no upgrade" result.
$PSNativeCommandUseErrorActionPreference = $false

if ($BuildLauncher) {
    $header = @'
@echo off
setlocal DisableDelayedExpansion
rem Generated from install-prerequisites.ps1 -BuildLauncher. Distribute this file alone.
set "PREREQUISITES_LAUNCHER=%~f0"
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoLogo -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference = 'Stop'; try { $parts = [regex]::new('(?m)^# POWERSHELL_PAYLOAD\r?\n').Split([IO.File]::ReadAllText($env:PREREQUISITES_LAUNCHER), 2); if ($parts.Count -ne 2) { throw 'The launcher is incomplete. Download install.cmd again.' }; & ([scriptblock]::Create($parts[1])); exit 0 } catch { [Console]::Error.WriteLine($_.ToString()); exit 1 }"
set "INSTALL_EXIT_CODE=%ERRORLEVEL%"
echo.
if "%INSTALL_EXIT_CODE%"=="0" (echo Installation finished.) else (echo Installation failed. See the error above.)
pause
exit /b %INSTALL_EXIT_CODE%
# POWERSHELL_PAYLOAD
'@
    $source = [IO.File]::ReadAllText($PSCommandPath)
    $content = ($header + "`n" + $source).Replace("`r`n", "`n").Replace("`n", "`r`n")
    $launcherPath = Join-Path $PSScriptRoot 'install.cmd'
    [IO.File]::WriteAllText($launcherPath, $content, [Text.UTF8Encoding]::new($false))
    Write-Host "Created self-contained launcher: $launcherPath"
    return
}

if ($env:OS -ne 'Windows_NT') {
    throw 'Run install.cmd or install-prerequisites.ps1 on Windows 10 or 11, outside WSL.'
}

function Find-Application {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        [string[]]$FallbackPaths = @()
    )

    $command = Get-Command -Name $Name -CommandType Application -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($command) {
        return $command.Source
    }

    foreach ($path in $FallbackPaths) {
        if (Test-Path -LiteralPath $path -PathType Leaf) {
            return $path
        }
    }

    throw "Cannot find $Name. Reopen install.cmd or PowerShell and rerun install-prerequisites.ps1. Check PATH and Windows app execution aliases if this persists."
}

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        [string[]]$ArgumentList = @(),
        [int[]]$SuccessExitCodes = @(0)
    )

    & $FilePath @ArgumentList | Out-Host
    $exitCode = $LASTEXITCODE
    if ($SuccessExitCodes -notcontains $exitCode) {
        throw "'$FilePath $($ArgumentList -join ' ')' failed with exit code $exitCode. Resolve the error above, then rerun install.cmd or install-prerequisites.ps1. If Windows requests a restart, restart first."
    }
}

$wingetCommand = Get-Command -Name winget.exe -CommandType Application -ErrorAction SilentlyContinue |
    Select-Object -First 1
if (-not $wingetCommand) {
    throw 'WinGet is missing. Install or update App Installer from https://apps.microsoft.com/detail/9NBLGGH4NNS1, then rerun install.cmd or install-prerequisites.ps1.'
}
$winget = $wingetCommand.Source

Write-Host 'Refreshing the WinGet catalog...'
Invoke-CheckedCommand -FilePath $winget -ArgumentList @(
    'source', 'update', '--name', 'winget', '--disable-interactivity'
)

$packages = @(
    @{ Id = 'Microsoft.VisualStudioCode'; Source = 'winget' }
    @{ Id = 'GitHub.Copilot'; Source = 'winget' }
    # Python documents this Microsoft Store ID for its install manager.
    @{ Id = '9NQ7512CXL7T'; Source = 'msstore' }
)

foreach ($package in $packages) {
    Write-Host "`nInstalling or updating $($package.Id)..."
    Invoke-CheckedCommand -FilePath $winget -ArgumentList @(
        'install', '--id', $package.Id, '--exact', '--source', $package.Source,
        '--silent', '--accept-package-agreements', '--accept-source-agreements',
        '--disable-interactivity'
    ) -SuccessExitCodes @(0, -1978335189) # 0x8A15002B: no applicable upgrade.
}

# Include installer PATH changes without discarding this session's entries.
$env:Path = @(
    [Environment]::GetEnvironmentVariable('Path', 'Machine')
    [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path
    "$env:LOCALAPPDATA\Microsoft\WindowsApps"
    "$env:LOCALAPPDATA\Microsoft\WinGet\Links"
) -join ';'

$pythonManager = Find-Application -Name 'pymanager.exe' -FallbackPaths @(
    "$env:LOCALAPPDATA\Microsoft\WindowsApps\pymanager.exe"
    "$env:LOCALAPPDATA\Microsoft\WindowsApps\PythonSoftwareFoundation.PythonManager_qbz5n2kfra8p0\pymanager.exe"
    "$env:LOCALAPPDATA\Microsoft\WindowsApps\PythonSoftwareFoundation.PythonManager_3847v3x7pw1km\pymanager.exe"
)

Write-Host "`nInstalling or updating stable Python 3..."
Invoke-CheckedCommand -FilePath $pythonManager -ArgumentList @(
    'install', '--update', '--yes', '3'
)
Invoke-CheckedCommand -FilePath $pythonManager -ArgumentList @(
    'exec', '-V:3', '--version'
)

$code = Find-Application -Name 'code.cmd' -FallbackPaths @(
    "$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin\code.cmd"
    "$env:ProgramFiles\Microsoft VS Code\bin\code.cmd"
    "${env:ProgramFiles(x86)}\Microsoft VS Code\bin\code.cmd"
)

foreach ($extension in @('GitHub.copilot', 'GitHub.copilot-chat', 'ms-python.python')) {
    Write-Host "`nInstalling or updating $extension..."
    Invoke-CheckedCommand -FilePath $code -ArgumentList @(
        '--install-extension', $extension, '--force'
    )
}

Write-Host "`nChecking installed applications..."
Invoke-CheckedCommand -FilePath $code -ArgumentList @('--version')
$copilot = Find-Application -Name 'copilot.exe' -FallbackPaths @(
    "$env:LOCALAPPDATA\Microsoft\WinGet\Links\copilot.exe"
)
Invoke-CheckedCommand -FilePath $copilot -ArgumentList @('--version')

Write-Host @'

Setup finished. Close and reopen your terminals and VS Code to load PATH changes.
In a new terminal, run copilot and follow the sign-in prompt (or enter /login).
In VS Code, use the Copilot menu to sign in with your GitHub account.
You need Copilot access; organization policies and plan limits still apply.
Use pymanager exec -V:3 to run the installed Python 3 runtime if an older
python or py command takes precedence on PATH.
'@
