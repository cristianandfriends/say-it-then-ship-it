#!/usr/bin/env python3
"""Install the workshop's starter skills and agent without network access."""

import argparse
import os
from pathlib import Path
import sys
from typing import Dict, List, Optional, Sequence, Set, Tuple
from uuid import uuid4


SKILLS: Tuple[str, ...] = ("bootstrap-lab", "stop-slop", "frontend-design")
AGENT: str = "software-engineering-expert"
BEGIN: bytes = b"<!-- bootstrap-lab:begin -->"
END: bytes = b"<!-- bootstrap-lab:end -->"


class InstallError(Exception):
    """Report a safe-to-act-on installation failure."""


def absolute_path(value: str) -> Path:
    path: Path = Path(os.path.expanduser(value)).absolute()
    check_path(path)
    return Path(os.path.abspath(path))


def check_path(path: Path) -> None:
    """Reject symlinks and non-directory ancestors, including dangling links."""
    for component in (*reversed(path.parents), path):
        if component.is_symlink():
            raise InstallError("Symlink paths are not supported: {}".format(component))
        if component != path and component.exists() and not component.is_dir():
            raise InstallError("Expected a directory: {}".format(component))


def destination(target: Path, relative: Path) -> Path:
    path: Path = target / relative
    try:
        path.relative_to(target)
    except ValueError as error:
        raise InstallError("Destination escapes the target: {}".format(path)) from error
    if ".." in relative.parts or relative.is_absolute():
        raise InstallError("Destination escapes the target: {}".format(relative))
    check_path(path)
    return path


def read_source(path: Path) -> bytes:
    check_path(path)
    if not path.is_file():
        raise InstallError(
            "Missing canonical source file: {}. Use --source <workshop> with the "
            "original .agents/skills and .github/agents layout; installed native "
            "copies are not a workshop source. No downloads were attempted.".format(path)
        )
    return path.read_bytes()


def opencode_agent(content: bytes) -> bytes:
    lines: List[str] = content.decode("utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise InstallError("The canonical agent needs YAML frontmatter.")
    closing: Optional[int] = next(
        (index for index in range(1, len(lines)) if lines[index].strip() == "---"), None
    )
    if closing is None or not any(
        line.startswith("description:") for line in lines[1:closing]
    ):
        raise InstallError("The canonical agent needs YAML description frontmatter.")
    header: str = "".join(
        line for line in lines[1:closing] if not line.startswith("name:")
    )
    body: str = "".join(lines[closing + 1 :])
    return ("---\n" + header + "mode: subagent\n---\n" + body).encode("utf-8")


def merge_instructions(existing: bytes, template: bytes) -> bytes:
    block: bytes = template.rstrip(b"\n")
    if (
        not block.startswith(BEGIN)
        or not block.endswith(END)
        or block.count(BEGIN) != 1
        or block.count(END) != 1
    ):
        raise InstallError("The source AGENTS.md template has invalid block boundaries.")
    begin_count: int = existing.count(BEGIN)
    end_count: int = existing.count(END)
    if begin_count == 0 and end_count == 0:
        separator: bytes = (
            b"" if not existing else (b"\n" if existing.endswith(b"\n") else b"\n\n")
        )
        return existing + separator + template
    start: int = existing.find(BEGIN)
    stop: int = existing.find(END)
    if (
        begin_count != 1
        or end_count != 1
        or stop < start
        or existing[start : stop + len(END)] != block
    ):
        raise InstallError(
            "AGENTS.md has a changed or malformed bootstrap-lab block. Manually "
            "merge it with bootstrap-lab/assets/AGENTS.md, preserving prose outside "
            "the markers, then rerun."
        )
    return existing


def walk_error(error: OSError) -> None:
    raise InstallError("Cannot read the complete source directory: {}".format(error)) from error


def source_plan(source: Path, harness: str) -> Tuple[Dict[Path, bytes], Set[Path]]:
    files: Dict[Path, bytes] = {}
    directories: Set[Path] = set()
    native: str = ".github" if harness == "copilot" else ".opencode"
    for skill in SKILLS:
        origin: Path = source / ".agents" / "skills" / skill
        read_source(origin / "SKILL.md")
        for root, dirs, names in os.walk(origin, followlinks=False, onerror=walk_error):
            dirs[:] = sorted(name for name in dirs if name != "__pycache__")
            root_path: Path = Path(root)
            relative: Path = Path(native) / "skills" / skill / root_path.relative_to(origin)
            directories.add(relative)
            for name in dirs:
                check_path(root_path / name)
            for name in sorted(name for name in names if not name.endswith(".pyc")):
                files[relative / name] = read_source(root_path / name)
    agent: bytes = read_source(source / ".github" / "agents" / (AGENT + ".agent.md"))
    suffix: str = ".agent.md" if harness == "copilot" else ".md"
    files[Path(native) / "agents" / (AGENT + suffix)] = (
        agent if harness == "copilot" else opencode_agent(agent)
    )
    files[Path("AGENTS.md")] = read_source(
        source / ".agents" / "skills" / "bootstrap-lab" / "assets" / "AGENTS.md"
    )
    return files, directories


def preflight(
    target: Path, files: Dict[Path, bytes], directories: Set[Path]
) -> List[Tuple[Path, bytes, Optional[bytes]]]:
    check_path(target)
    if target.exists() and not target.is_dir():
        raise InstallError("The target must be a directory: {}".format(target))
    for relative in sorted(directories):
        path: Path = destination(target, relative)
        if path.exists() and not path.is_dir():
            raise InstallError("Expected a skill directory: {}".format(path))
    changes: List[Tuple[Path, bytes, Optional[bytes]]] = []
    conflicts: List[str] = []
    for relative, content in sorted(files.items()):
        path = destination(target, relative)
        if path.exists() and not path.is_file():
            conflicts.append("{} is not a regular file".format(path))
            continue
        previous: Optional[bytes] = path.read_bytes() if path.exists() else None
        if relative == Path("AGENTS.md"):
            content = merge_instructions(previous or b"", content)
        elif previous is not None and previous != content:
            conflicts.append(str(path))
            continue
        if previous != content:
            changes.append((path, content, previous))
    if conflicts:
        raise InstallError(
            "Existing files differ or collide:\n  {}\nNo files were changed. "
            "Preserve your work and merge by hand, or choose a clean target. "
            "There is no overwrite flag.".format("\n  ".join(conflicts))
        )
    return changes


def atomic_write(path: Path, content: bytes, previous: Optional[bytes]) -> None:
    check_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    check_path(path)
    staged: Path = path.with_name("." + path.name + ".bootstrap-" + uuid4().hex)
    try:
        with staged.open("xb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        check_path(path)
        if previous is None:
            # A hard link publishes a complete file without replacing a racing writer.
            os.link(staged, path)
        else:
            if not path.is_file() or path.read_bytes() != previous:
                raise InstallError("File changed after preflight: {}".format(path))
            os.replace(staged, path)
    finally:
        if staged.exists():
            staged.unlink()


def install(source: Path, target: Path, harness: str, dry_run: bool) -> int:
    for protected in (
        *(source / ".agents" / "skills" / skill for skill in SKILLS),
        source / ".github" / "agents",
    ):
        if target == protected or protected in target.parents:
            raise InstallError(
                "The target cannot sit inside a canonical source directory: {}. "
                "Choose a separate project directory.".format(protected)
            )
    files: Dict[Path, bytes]
    directories: Set[Path]
    files, directories = source_plan(source, harness)
    changes: List[Tuple[Path, bytes, Optional[bytes]]] = preflight(target, files, directories)
    if dry_run:
        print(
            "Dry run: {} file(s) would change under {}. "
            "No files changed.".format(len(changes), target)
        )
        return 0
    completed: int = 0
    try:
        for path, content, previous in changes:
            atomic_write(path, content, previous)
            completed += 1
        for relative in sorted(directories):
            directory: Path = destination(target, relative)
            directory.mkdir(parents=True, exist_ok=True)
    except (OSError, InstallError) as error:
        raise InstallError(
            "Installation interrupted after {} of {} file changes; the target may "
            "contain a partial installation. Completed files remain. Fix the cause "
            "and rerun; matching files will not change. Cause: {}".format(
                completed, len(changes), error
            )
        ) from error
    if changes:
        print("Installed {} file(s) for {} under {}.".format(completed, harness, target))
    else:
        print("Already installed: all managed files match under {}.".format(target))
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harness", choices=("copilot", "opencode"), required=True)
    parser.add_argument("--target", required=True, help="Destination student project")
    parser.add_argument(
        "--source",
        default=str(Path(__file__).absolute().parents[4]),
        help="Workshop root with the canonical .agents/skills layout",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate and preview without writes")
    args: argparse.Namespace = parser.parse_args(argv)
    try:
        return install(
            absolute_path(args.source), absolute_path(args.target), args.harness, args.dry_run
        )
    except (InstallError, OSError, UnicodeError) as error:
        print("bootstrap-lab: {}".format(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
