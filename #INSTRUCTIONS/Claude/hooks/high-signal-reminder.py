#!/usr/bin/env python3
"""UserPromptSubmit hook: throttled salience nudge for high-signal-mode.
Full rules are already loaded at SessionStart, so this only re-asserts the mode
every EVERY-th prompt and emits NOTHING (zero added tokens) on all other turns.
Per-session counter lives in /tmp, namespaced by session_id."""
import sys, json, hashlib
from pathlib import Path

EVERY = 6  # nudge once every N prompts; raise for more savings, lower if drift appears

try:
    sid = json.load(sys.stdin).get("session_id", "default")
except Exception:
    sid = "default"

f = Path("/tmp") / f"hsm-{hashlib.sha1(sid.encode()).hexdigest()[:16]}.count"
try:
    n = int(f.read_text()) + 1
except Exception:
    n = 1
f.write_text(str(n))

if n % EVERY == 0:  # silent on every other turn
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "high-signal-mode active: answer-first, terse, no meta-commentary about the mode; keep full caveats unless user asks verbose."
        }
    }))
