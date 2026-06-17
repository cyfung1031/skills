#!/usr/bin/env python3
"""Sanitize local ai-dev-loop R/K commits before a branch is pushed."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


VERSION = "1.0.1"


DEFAULT_PREFIXES = ("R:", "K:")
DEFAULT_ARTIFACT_PATHS = (".ai-dev-loop",)
AI_TRAILER_RE = re.compile(
    r"^Co-authored-by:\s+.*(?:claude|anthropic|codex|openai|chatgpt|ai-dev-loop).*<.*>$",
    re.IGNORECASE,
)
REVIEW_ID_RE = re.compile(r"\b[RK]-\d{4}(?:-\d+)?\b[:\s-]*", re.IGNORECASE)
ROLE_WORD_RE = re.compile(r"\b(?:r\s+role|k\s+role|response file|review file|ai-dev-loop)\b", re.IGNORECASE)
AI_PATH_RE = re.compile(r"(?:^|\s)\.ai-dev-loop/[^\s`'\"),]+")
COMMIT_REF_RE = re.compile(r"\b(?:review|verify)\s+(?:commits?|k)\s+[0-9a-f+]{7,40}\b", re.IGNORECASE)


class GitError(RuntimeError):
    pass


@dataclass(frozen=True)
class CommitInfo:
    sha: str
    tree: str
    subject: str
    body: str
    author_name: str
    author_email: str
    author_date: str
    committer_name: str
    committer_email: str
    committer_date: str
    parents: tuple[str, ...]


@dataclass(frozen=True)
class PlannedCommit:
    original: CommitInfo
    target: bool
    sanitized_message: str
    artifact_paths: tuple[str, ...]


def run_git(
    args: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    input_text: str | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        env=env,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        command = "git " + " ".join(args)
        raise GitError(f"{command} failed:\n{result.stderr.strip()}")
    return result


def repo_root(cwd: Path) -> Path:
    result = run_git(["rev-parse", "--show-toplevel"], cwd=cwd)
    return Path(result.stdout.strip())


def current_branch(repo: Path) -> str:
    result = run_git(["branch", "--show-current"], cwd=repo)
    branch = result.stdout.strip()
    if not branch:
        raise GitError("Current HEAD is detached; check out a branch before rewriting.")
    return branch


def try_upstream_base(repo: Path) -> str | None:
    result = run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"], cwd=repo, check=False)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def commits_in_range(repo: Path, rev_range: str) -> list[str]:
    result = run_git(["rev-list", "--reverse", rev_range], cwd=repo)
    return [line for line in result.stdout.splitlines() if line]


def merge_base_for_range(repo: Path, rev_range: str) -> str | None:
    if ".." not in rev_range or rev_range.count("..") != 1 or "..." in rev_range:
        return None
    base, head = rev_range.split("..", 1)
    if not base or not head:
        return None
    result = run_git(["merge-base", base, head], cwd=repo)
    return result.stdout.strip()


def get_commit(repo: Path, sha: str) -> CommitInfo:
    fmt = "%H%x00%T%x00%s%x00%B%x00%an%x00%ae%x00%aI%x00%cn%x00%ce%x00%cI%x00%P"
    result = run_git(["show", "-s", f"--format={fmt}", sha], cwd=repo)
    parts = result.stdout.split("\x00", 10)
    if len(parts) != 11:
        raise GitError(f"Could not parse commit metadata for {sha}.")
    parents = tuple(parts[10].strip().split()) if parts[10].strip() else ()
    return CommitInfo(
        sha=parts[0].strip(),
        tree=parts[1].strip(),
        subject=parts[2].strip(),
        body=parts[3].strip("\n"),
        author_name=parts[4],
        author_email=parts[5],
        author_date=parts[6],
        committer_name=parts[7],
        committer_email=parts[8],
        committer_date=parts[9],
        parents=parents,
    )


def status_is_clean(repo: Path) -> bool:
    result = run_git(["status", "--porcelain"], cwd=repo)
    return result.stdout == ""


def remote_contains(repo: Path, sha: str) -> list[str]:
    result = run_git(["branch", "-r", "--contains", sha], cwd=repo, check=False)
    if result.returncode != 0:
        return []
    return [line.strip().lstrip("* ").strip() for line in result.stdout.splitlines() if line.strip()]


def path_exists_in_head(repo: Path, path: str) -> bool:
    result = run_git(["ls-tree", "-r", "--name-only", "HEAD", "--", path], cwd=repo)
    return bool(result.stdout.strip())


def target_prefixes(value: str) -> tuple[str, ...]:
    prefixes = tuple(item.strip() for item in value.split(",") if item.strip())
    if not prefixes:
        raise argparse.ArgumentTypeError("at least one prefix is required")
    return prefixes


def is_target(subject: str, prefixes: Iterable[str]) -> bool:
    return any(subject.startswith(prefix) for prefix in prefixes)


def strip_target_prefix(subject: str, prefixes: Iterable[str]) -> str:
    for prefix in prefixes:
        if subject.startswith(prefix):
            return subject[len(prefix) :].strip()
    return subject.strip()


def cleanup_line(line: str, *, keep_ai_trailers: bool) -> str | None:
    original = line.rstrip()
    if not original:
        return ""
    if not keep_ai_trailers and AI_TRAILER_RE.match(original):
        return None
    if ".ai-dev-loop/" in original:
        return None
    if ROLE_WORD_RE.search(original):
        return None
    line = AI_PATH_RE.sub("", original)
    line = REVIEW_ID_RE.sub("", line)
    line = COMMIT_REF_RE.sub("", line)
    line = re.sub(r"\bAI Audit\b", "audit", line, flags=re.IGNORECASE)
    line = re.sub(r"\s+", " ", line).strip()
    line = re.sub(r"^[-:;,\s]+", "", line)
    return line or None


def sanitize_subject(subject: str, prefixes: Iterable[str]) -> str:
    cleaned = strip_target_prefix(subject, prefixes)
    lowered = cleaned.lower()
    if lowered.startswith("review commit") or lowered.startswith("review commits"):
        return "identify follow-up fixes"
    if lowered.startswith("verify k ") or lowered.startswith("verify commit") or lowered.startswith("verify commits"):
        return "verify follow-up fixes"
    cleaned = REVIEW_ID_RE.sub("", cleaned)
    cleaned = COMMIT_REF_RE.sub("", cleaned)
    cleaned = ROLE_WORD_RE.sub("", cleaned)
    cleaned = re.sub(r"\b(?:required findings?|findings closed|approved|approve)\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\(\s*(?:,\s*)*\)", "", cleaned)
    cleaned = re.sub(r"\s*[—-]\s*$", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" :-—")
    if not cleaned:
        return "update branch changes"
    return cleaned[0].lower() + cleaned[1:] if cleaned[:1].isalpha() else cleaned


def sanitize_message(commit: CommitInfo, prefixes: Iterable[str], *, keep_ai_trailers: bool) -> str:
    subject = sanitize_subject(commit.subject, prefixes)
    cleaned_lines: list[str] = []
    for line in commit.body.splitlines()[1:]:
        cleaned = cleanup_line(line, keep_ai_trailers=keep_ai_trailers)
        if cleaned is None:
            continue
        cleaned_lines.append(cleaned)

    compacted: list[str] = []
    previous_blank = False
    for line in cleaned_lines:
        blank = line == ""
        if blank and previous_blank:
            continue
        compacted.append(line)
        previous_blank = blank
    while compacted and compacted[0] == "":
        compacted.pop(0)
    while compacted and compacted[-1] == "":
        compacted.pop()

    if compacted:
        return subject + "\n\n" + "\n".join(compacted) + "\n"
    return subject + "\n"


def load_overrides(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("message override file must contain a JSON object")
    overrides: dict[str, str] = {}
    for key, value in data.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("message override keys and values must be strings")
        overrides[key] = value.rstrip("\n") + "\n"
    return overrides


def find_override(overrides: dict[str, str], sha: str) -> str | None:
    matches = [value for key, value in overrides.items() if sha.startswith(key)]
    if len(matches) > 1:
        raise ValueError(f"multiple message overrides match {sha}")
    return matches[0] if matches else None


def infer_target_tail(repo: Path, prefixes: Iterable[str]) -> tuple[str, list[str]]:
    result = run_git(["rev-list", "--first-parent", "HEAD"], cwd=repo)
    target_shas: list[str] = []
    for sha in result.stdout.splitlines():
        commit = get_commit(repo, sha)
        if not is_target(commit.subject, prefixes):
            if not target_shas:
                raise GitError("HEAD does not end with target R/K commits; pass --base or --range explicitly.")
            return commit.sha, list(reversed(target_shas))
        if len(commit.parents) > 1:
            raise GitError(f"Merge commit {commit.sha[:12]} is not supported by target-tail mode.")
        target_shas.append(commit.sha)
    raise GitError("Could not infer a base for target-tail mode; reached the root commit.")


def build_plan(args: argparse.Namespace, repo: Path) -> tuple[str, list[PlannedCommit]]:
    if args.target_tail and (args.base or args.range):
        raise GitError("--target-tail cannot be combined with --base or --range.")
    if args.target_tail:
        base, shas = infer_target_tail(repo, args.prefixes)
    elif args.range:
        rev_range = args.range
        base = merge_base_for_range(repo, rev_range)
        if base is None and args.base:
            base = args.base
        shas = commits_in_range(repo, rev_range)
    else:
        base = args.base or try_upstream_base(repo)
        if base is None:
            base, shas = infer_target_tail(repo, args.prefixes)
        else:
            rev_range = f"{base}..HEAD"
            shas = commits_in_range(repo, rev_range)
    if not shas:
        raise GitError("No commits found in selected range.")
    if base is None:
        first = get_commit(repo, shas[0])
        if len(first.parents) != 1:
            raise GitError("Could not infer a linear base for this range; pass --base <rev>.")
        base = first.parents[0]

    overrides = load_overrides(args.message_overrides)
    artifact_paths = tuple(dict.fromkeys([*DEFAULT_ARTIFACT_PATHS, *args.artifact_path]))
    planned: list[PlannedCommit] = []
    for sha in shas:
        commit = get_commit(repo, sha)
        target = is_target(commit.subject, args.prefixes)
        message = find_override(overrides, commit.sha) or commit.body.rstrip("\n") + "\n"
        if target:
            message = find_override(overrides, commit.sha) or sanitize_message(
                commit,
                args.prefixes,
                keep_ai_trailers=args.keep_ai_trailers,
            )
        planned.append(PlannedCommit(commit, target, message, artifact_paths))
    return base, planned


def print_plan(base: str, planned: list[PlannedCommit]) -> None:
    print(f"Base: {base}")
    print(f"Commits: {len(planned)}")
    target_count = sum(1 for item in planned if item.target)
    print(f"Target R/K commits: {target_count}")
    for item in planned:
        mark = "TARGET" if item.target else "keep"
        short = item.original.sha[:8]
        subject = item.original.subject
        new_subject = item.sanitized_message.splitlines()[0]
        suffix = f" -> {new_subject}" if item.target and new_subject != subject else ""
        print(f"  {mark:6} {short} {subject}{suffix}")


def print_message_preview(planned: list[PlannedCommit]) -> None:
    for item in planned:
        if not item.target:
            continue
        print("")
        print(f"--- {item.original.sha[:12]} sanitized message ---")
        print(item.sanitized_message.rstrip("\n"))


def validate_rewrite_inputs(
    repo: Path,
    base: str,
    planned: list[PlannedCommit],
    *,
    allow_dirty: bool,
    allow_remote_contained: bool,
) -> None:
    if not allow_dirty and not status_is_clean(repo):
        raise GitError("Working tree is dirty. Commit/stash changes or pass --allow-dirty explicitly.")
    for item in planned:
        if len(item.original.parents) > 1:
            raise GitError(f"Merge commit {item.original.sha[:12]} is not supported by this rewrite script.")
        if not allow_remote_contained:
            remotes = remote_contains(repo, item.original.sha)
            if remotes:
                joined = ", ".join(remotes)
                raise GitError(f"Refusing to rewrite pushed commit {item.original.sha[:12]} reachable from: {joined}")
    head = run_git(["rev-parse", "HEAD"], cwd=repo).stdout.strip()
    if planned[-1].original.sha != head:
        raise GitError("Selected range must end at HEAD for rewrite --apply.")
    if run_git(["merge-base", "--is-ancestor", base, "HEAD"], cwd=repo, check=False).returncode != 0:
        raise GitError(f"Base {base} is not an ancestor of HEAD.")


def paths_in_tree(repo: Path, treeish: str, artifact_paths: tuple[str, ...]) -> list[str]:
    paths: list[str] = []
    for artifact_path in artifact_paths:
        result = run_git(["ls-tree", "-r", "--name-only", treeish, "--", artifact_path], cwd=repo)
        paths.extend(line for line in result.stdout.splitlines() if line)
    return list(dict.fromkeys(paths))


def tree_without_artifacts(repo: Path, item: PlannedCommit) -> str:
    paths = paths_in_tree(repo, item.original.sha, item.artifact_paths)
    if not paths:
        return item.original.tree
    env = os.environ.copy()
    index_file = Path(os.environ.get("TMPDIR", "/tmp")) / f"ai-dev-loop-sanitize-{os.getpid()}.index"
    env["GIT_INDEX_FILE"] = str(index_file)
    try:
        run_git(["read-tree", item.original.tree], cwd=repo, env=env)
        run_git(["update-index", "--force-remove", "--stdin"], cwd=repo, env=env, input_text="\n".join(paths) + "\n")
        return run_git(["write-tree"], cwd=repo, env=env).stdout.strip()
    finally:
        index_file.unlink(missing_ok=True)


def commit_from_tree(repo: Path, item: PlannedCommit, tree: str, parent: str) -> str:
    commit = item.original
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": commit.author_name,
            "GIT_AUTHOR_EMAIL": commit.author_email,
            "GIT_AUTHOR_DATE": commit.author_date,
            "GIT_COMMITTER_NAME": commit.committer_name,
            "GIT_COMMITTER_EMAIL": commit.committer_email,
            "GIT_COMMITTER_DATE": commit.committer_date,
        }
    )
    return run_git(["commit-tree", tree, "-p", parent], cwd=repo, env=env, input_text=item.sanitized_message).stdout.strip()


def rewrite(args: argparse.Namespace, repo: Path, base: str, planned: list[PlannedCommit]) -> None:
    validate_rewrite_inputs(
        repo,
        base,
        planned,
        allow_dirty=args.allow_dirty,
        allow_remote_contained=args.allow_remote_contained,
    )
    branch = current_branch(repo)
    branch_ref = run_git(["symbolic-ref", "-q", "HEAD"], cwd=repo).stdout.strip()
    if not branch_ref:
        raise GitError("Current HEAD is detached; cannot update the current branch ref.")
    original_head = run_git(["rev-parse", "HEAD"], cwd=repo).stdout.strip()
    rewritten: dict[str, str] = {}
    dropped = 0
    parent = base
    for item in planned:
        tree = tree_without_artifacts(repo, item) if item.target else item.original.tree
        if item.target and args.drop_empty_targets:
            parent_tree = run_git(["show", "-s", "--format=%T", parent], cwd=repo).stdout.strip()
            if tree == parent_tree:
                dropped += 1
                continue
        new_sha = commit_from_tree(repo, item, tree, parent)
        rewritten[item.original.sha] = new_sha
        parent = new_sha
    new_head = parent
    run_git(["update-ref", "-m", f"ai-dev-loop sanitize {VERSION}", branch_ref, new_head, original_head], cwd=repo)

    target_count = sum(1 for item in planned if item.target)
    print(f"Replayed {len(rewritten)} commits on {branch}; sanitized {target_count} target commits.")
    if dropped:
        print(f"Dropped {dropped} empty target commits.")
    print(f"Original HEAD: {original_head}")
    print("No backup branch created. Recover with the branch reflog or git update-ref if needed.")
    remaining_artifacts = any(path_exists_in_head(repo, path) for path in DEFAULT_ARTIFACT_PATHS)
    if remaining_artifacts:
        print("Warning: .ai-dev-loop still exists at HEAD; inspect non-target commits.")


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--base", help="Base revision. Defaults to @{upstream}, or target-tail mode when no upstream exists.")
    parser.add_argument("--range", help="Revision range to inspect, for example main..HEAD.")
    parser.add_argument(
        "--target-tail",
        action="store_true",
        help="Infer the contiguous target R/K commit tail at HEAD and use its parent as the base.",
    )
    parser.add_argument("--prefixes", type=target_prefixes, default=DEFAULT_PREFIXES, help="Comma-separated target prefixes.")
    parser.add_argument(
        "--artifact-path",
        action="append",
        default=[],
        help="Artifact path to remove from target commits. Can be repeated.",
    )
    parser.add_argument("--message-overrides", type=Path, help="JSON object mapping full or short SHA to exact message.")
    parser.add_argument("--keep-ai-trailers", action="store_true", help="Keep AI-related Co-authored-by trailers.")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="List selected commits without rewriting.")
    add_common_args(plan_parser)
    plan_parser.add_argument("--messages", action="store_true", help="Show sanitized target messages.")

    rewrite_parser = subparsers.add_parser("rewrite", help="Preview or apply the history rewrite.")
    add_common_args(rewrite_parser)
    rewrite_parser.add_argument("--apply", action="store_true", help="Actually rewrite the current branch.")
    rewrite_parser.add_argument("--allow-dirty", action="store_true", help="Allow rewriting from a dirty worktree.")
    rewrite_parser.add_argument(
        "--allow-remote-contained",
        action="store_true",
        help="Allow commits reachable from remote refs. Use only for disposable local clones.",
    )
    rewrite_parser.add_argument("--drop-empty-targets", action="store_true", help="Drop target commits that become empty.")
    rewrite_parser.add_argument("--messages", action="store_true", default=True, help="Show sanitized target messages.")
    rewrite_parser.add_argument("--no-messages", action="store_false", dest="messages", help="Hide sanitized message preview.")

    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        repo = repo_root(Path.cwd())
        base, planned = build_plan(args, repo)
        print_plan(base, planned)
        if args.messages:
            print_message_preview(planned)
        if args.command == "rewrite":
            if not args.apply:
                print("")
                print("Dry run only. Re-run with --apply to rewrite history.")
                return 0
            rewrite(args, repo, base, planned)
        return 0
    except (GitError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
