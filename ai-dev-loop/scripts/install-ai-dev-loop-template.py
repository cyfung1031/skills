#!/usr/bin/env python3
"""Safely install the AI Development Loop project-local template."""
from __future__ import annotations

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

BROAD_DIRS = {
    Path('/'),
    Path('/mnt'),
    Path('/mnt/data'),
    Path('/tmp'),
    Path('/var/tmp'),
    Path('/workspace'),
    Path('/workspaces'),
    Path('/home'),
    Path.home(),
}

PROJECT_MARKERS = {
    '.git',
    'README.md',
    'README.rst',
    'pyproject.toml',
    'package.json',
    'Cargo.toml',
    'go.mod',
    'pom.xml',
    'build.gradle',
}

LOOP_README = """# AI Development Loop Coordination Directory

This directory is the durable handoff layer for the R/K development loop.

- `reviews/`: R review and audit records.
- `responses/`: K response, implementation, and validation records.
- `context/`: compact durable handoff notes when the loop is long or state is easy to lose.
- `decisions/`: durable decision records only when a choice affects product behavior, risk, scope, or future work.
- `status.md`: current state summary; update after every R or K role turn.
- `SKILL.md`: project-local copy of the operating instructions.
- `REFERENCE.md`: optional expansion reference for edge cases.

Do not rely on chat memory as the source of truth. Copy important facts here before relying on them.
"""

STATUS_TEMPLATE = """# AI Development Loop Status

## Current Branch

Template only. Replace with the project branch before starting the first R review.

## Current Focus

Template only. Replace this file with project-specific status before starting the first R review.

## Latest R Review

None.

## Latest K Response

None.

## Latest Context Note

None.

## Decisions

None.

## Approval State

- Spec/Plan Status: Not started
- Implementation Status: Not applicable
- Overall Status: Blocked

## Open Required Findings

None yet; first R review must populate any blockers, required findings, or unresolved K questions/objections.

## Completed Items

None.

## Next Expected Role Action

R bootstrap review.

## Next Item

Run the first R review against the available specs, plans, roadmap, tickets, or design notes. If none exist, record the missing requirements as the safe stopping point.

## Blockers

Template only. No project-specific requirements have been loaded yet.
"""

CONTEXT_README = """Create `NNNN-context.md` files when a long loop, milestone handoff, spec-to-implementation transition, or stale-context risk needs a compact durable summary.
"""

DECISIONS_README = """Create `NNNN-decision.md` files only for durable decisions that affect scope, product behavior, risk, architecture, external dependencies, data, cost, or future review assumptions.
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Install .ai-dev-loop template into a project root.')
    parser.add_argument('project_root', type=Path, help='Target project root.')
    parser.add_argument(
        '--force',
        action='store_true',
        help='Replace an existing .ai-dev-loop directory after creating a timestamped backup.',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be installed without writing files.',
    )
    parser.add_argument(
        '--allow-unmarked-root',
        action='store_true',
        help='Allow installation into a directory with no common project marker. Use only after manually confirming the project root.',
    )
    parser.add_argument(
        '--force-live-records',
        action='store_true',
        help='With --force, also replace an existing .ai-dev-loop directory that appears to contain live R/K records.',
    )
    return parser.parse_args()


def is_broad_path(path: Path) -> bool:
    resolved = path.resolve()
    return resolved in BROAD_DIRS


def has_project_marker(path: Path) -> bool:
    return any((path / marker).exists() for marker in PROJECT_MARKERS)


def has_live_records(target: Path) -> bool:
    """Return True when an existing coordination directory appears to hold project-specific records."""
    if not target.exists():
        return False
    record_dirs = ['reviews', 'responses', 'context', 'decisions']
    for dirname in record_dirs:
        directory = target / dirname
        if not directory.exists():
            continue
        for path in directory.rglob('*'):
            if path.is_file() and path.name != 'README.md':
                return True
    return False


def backup_existing(target_root: Path, target: Path) -> Path:
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = target_root / f'.ai-dev-loop.backup-{stamp}'
    counter = 1
    while backup.exists():
        backup = target_root / f'.ai-dev-loop.backup-{stamp}-{counter}'
        counter += 1
    target.rename(backup)
    return backup


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def install_template(package_root: Path, target: Path) -> None:
    """Install template files with local write-error diagnostics.

    File handles may be locked by IDE indexers, background tasks, or operating
    system policy. Convert those local write failures into concise, actionable
    CLI errors instead of exposing a raw traceback.
    """
    skill = package_root / 'SKILL.md'
    reference = package_root / 'REFERENCE.md'
    if not skill.is_file():
        raise FileNotFoundError(f'package skill not found: {skill}')
    if not reference.is_file():
        raise FileNotFoundError(f'package reference not found: {reference}')

    try:
        target.mkdir(parents=True, exist_ok=True)
        for dirname in ['reviews', 'responses', 'context', 'decisions']:
            (target / dirname).mkdir(parents=True, exist_ok=True)
        write_text(target / 'README.md', LOOP_README)
        write_text(target / 'status.md', STATUS_TEMPLATE)
        write_text(target / 'context' / 'README.md', CONTEXT_README)
        write_text(target / 'decisions' / 'README.md', DECISIONS_README)
        shutil.copy2(skill, target / 'SKILL.md')
        shutil.copy2(reference, target / 'REFERENCE.md')
    except PermissionError:
        print(
            f"error: Permission denied writing to '{target}'. Check your directory permissions.",
            file=sys.stderr,
        )
        sys.exit(1)
    except OSError as exc:
        detail = exc.strerror or str(exc)
        print(
            f"error: Could not write template files to '{target}' ({detail}).\n"
            "Please ensure no other process or IDE workspace has locked these files.",
            file=sys.stderr,
        )
        sys.exit(1)


def main() -> int:
    args = parse_args()
    package_root = Path(__file__).resolve().parents[1]
    target_root = args.project_root.resolve()
    target = target_root / '.ai-dev-loop'

    if not (package_root / 'SKILL.md').is_file():
        print(f'error: package SKILL.md not found under: {package_root}', file=sys.stderr)
        return 1
    if not (package_root / 'REFERENCE.md').is_file():
        print(f'error: package REFERENCE.md not found under: {package_root}', file=sys.stderr)
        return 1
    if is_broad_path(target_root):
        print(f'error: refusing to install into broad workspace path: {target_root}', file=sys.stderr)
        return 1
    if not target_root.exists() or not target_root.is_dir():
        print(f'error: target project root does not exist or is not a directory: {target_root}', file=sys.stderr)
        return 1
    if target.exists() and not args.force:
        print(f'error: {target} already exists; use --force to create a timestamped backup and replace it', file=sys.stderr)
        return 1
    if target.exists() and args.force and has_live_records(target) and not args.force_live_records:
        print(
            f'error: {target} appears to contain live R/K records; use --force-live-records with --force after manually confirming replacement is intended',
            file=sys.stderr,
        )
        return 1

    if not has_project_marker(target_root) and not args.allow_unmarked_root:
        print(
            f'error: target has no common project marker such as .git, README.md, pyproject.toml, package.json, Cargo.toml, go.mod, pom.xml, or build.gradle: {target_root}; use --allow-unmarked-root only after manually confirming this is the project root',
            file=sys.stderr,
        )
        return 1

    print(f'package root:    {package_root}')
    print(f'target template: {target}')
    if args.dry_run:
        print('dry run: no files written')
        return 0

    if target.exists():
        backup = backup_existing(target_root, target)
        print(f'backed up existing template to: {backup}')
    install_template(package_root, target)
    print('installed .ai-dev-loop template')
    print('next: edit .ai-dev-loop/status.md, then start with an R review')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
