---
name: ai-dev-loop-sanitize-commits
description: Sanitize unpushed local git commits from ai-dev-loop R/K loops. Use when a branch has local `R:` or `K:` commits and an agent needs to remove `.ai-dev-loop/*` artifacts, rewrite human-readable commit messages, preserve authors/dates, and prepare history before push or review.
---

# AI Dev Loop Commit Sanitizer

Version: 1.0.2

Use this skill before sharing a branch that contains ai-dev-loop review/response commits.

The bundled script rewrites only local, unpushed commits selected from the current branch. It removes `.ai-dev-loop/*` files from targeted `R:`/`K:` commits, sanitizes commit subjects and bodies, and recreates commits with the original author, committer, author date, and committer date.

v1.0.2 requirement: do not create branches and do not switch branches while using this skill. The script rewrites by building commit trees, updating the current branch ref in place, and syncing a clean worktree/index to the rewritten `HEAD`; it prints the original HEAD for recovery through the reflog.

## Workflow

1. Inspect the branch state. If the branch has no upstream, or the only commits to sanitize are the contiguous `R:`/`K:` commits at `HEAD`, prefer `--target-tail`:

```bash
python3 <skill>/scripts/sanitize_ai_dev_loop_commits.py plan
python3 <skill>/scripts/sanitize_ai_dev_loop_commits.py plan --target-tail
```

2. Preview the rewrite:

```bash
python3 <skill>/scripts/sanitize_ai_dev_loop_commits.py rewrite
python3 <skill>/scripts/sanitize_ai_dev_loop_commits.py rewrite --target-tail
```

3. If any generated commit message is not good enough, create a JSON override file:

```json
{
  "014e52f1": "fix pageLoadCaches visibility and cache tests\n\nMake pageLoadCaches private and add cache-path coverage for getScriptsForTab.\n\nTests: 969 pass."
}
```

Then preview again:

```bash
python3 <skill>/scripts/sanitize_ai_dev_loop_commits.py rewrite --message-overrides /path/to/messages.json
python3 <skill>/scripts/sanitize_ai_dev_loop_commits.py rewrite --target-tail --message-overrides /path/to/messages.json
```

4. Apply only after the preview is correct:

```bash
python3 <skill>/scripts/sanitize_ai_dev_loop_commits.py rewrite --apply --message-overrides /path/to/messages.json
python3 <skill>/scripts/sanitize_ai_dev_loop_commits.py rewrite --apply --target-tail --message-overrides /path/to/messages.json
```

5. Verify the result:

```bash
git log --stat --format=fuller <base>..HEAD
git log --name-only <base>..HEAD -- .ai-dev-loop
```

The second command should produce no `.ai-dev-loop` paths.

## Rules

- Do not run `rewrite --apply` on a dirty worktree unless the user explicitly asks for `--allow-dirty`.
- Do not sanitize pushed commits. The script determines the default base from `@{upstream}` and refuses commits already reachable from remote refs.
- Do not create backup branches, temporary branches, or switch branches. In v1.0.2 the script must keep the current branch checked out, use `git update-ref` only after the new commit chain is built, and sync a clean worktree/index to the rewritten `HEAD`.
- Prefer `--target-tail` for ai-dev-loop review/response commits stacked at `HEAD`; it avoids scanning or replaying earlier pushed commits when the branch has no upstream or a PR ref has unusual topology.
- Do not use this on merge-heavy local history unless the script reports support for it. The rewrite path is intentionally linear-history only.
- Keep the default `--keep-empty-targets` behavior when preserving commit count and timestamps matters. Use `--drop-empty-targets` only if the user explicitly wants artifact-only `R:` commits removed.
- Prefer message overrides for important commits. The built-in sanitizer is conservative text cleanup, not a semantic commit-message author.
- Record the printed `Original HEAD` after `rewrite --apply`; use the reflog or `git update-ref refs/heads/<branch> <original-head>` to recover if needed.

## Script

Run:

```bash
python3 <skill>/scripts/sanitize_ai_dev_loop_commits.py --help
```

Useful features:

- `plan`: list local unpushed commits and show which commits match the target prefixes.
- `rewrite`: dry-run by default; add `--apply` to rewrite the branch.
- `--target-tail`: infer the contiguous `R:`/`K:` commit tail at `HEAD` and use its parent as the base. This is the fastest and safest mode for local ai-dev-loop cleanup.
- `--base <rev>`: choose the base explicitly instead of using `@{upstream}`.
- `--range <rev-range>`: inspect a custom range such as `main..HEAD`.
- `--message-overrides <json>`: supply exact replacement messages by full or short SHA.
- `--drop-empty-targets`: drop targeted commits that become empty after artifact removal.
- `--artifact-path <path>`: remove another artifact directory in addition to the default `.ai-dev-loop`.
