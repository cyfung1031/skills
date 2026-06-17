from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sanitize_ai_dev_loop_commits.py"


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed:\n{result.stderr}")
    return result.stdout


class RewriteTests(unittest.TestCase):
    def test_rewrite_target_tail_leaves_worktree_clean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            git(repo, "init", "-b", "main")
            git(repo, "config", "user.name", "Test User")
            git(repo, "config", "user.email", "test@example.com")

            (repo / "kept.txt").write_text("base\n", encoding="utf-8")
            git(repo, "add", "kept.txt")
            git(repo, "commit", "-m", "base")

            artifact = repo / ".ai-dev-loop" / "reviews" / "0001-r-review.md"
            artifact.parent.mkdir(parents=True)
            artifact.write_text("review\n", encoding="utf-8")
            git(repo, "add", ".ai-dev-loop")
            git(repo, "commit", "-m", "R: review commit abc1234")

            result = subprocess.run(
                [sys.executable, str(SCRIPT), "rewrite", "--target-tail", "--apply"],
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(git(repo, "status", "--porcelain"), "")
            self.assertEqual(git(repo, "ls-tree", "-r", "--name-only", "HEAD", "--", ".ai-dev-loop"), "")


if __name__ == "__main__":
    unittest.main()
