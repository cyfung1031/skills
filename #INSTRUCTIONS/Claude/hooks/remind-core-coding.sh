#!/usr/bin/env bash
# PreToolUse(Write|Edit): once per session, remind to load the core-coding-agent-behavior
# skill (per ~/.claude/CLAUDE.md "When to load the mechanics"). Uses a per-session
# sentinel so the reminder fires only on the FIRST edit, then stays silent.
input=$(cat)
sid=$(printf '%s' "$input" | jq -r '.session_id // "nosession"' 2>/dev/null)
sentinel="${TMPDIR:-/tmp}/cc-coreload-${sid}"
[ -e "$sentinel" ] && exit 0
: > "$sentinel" 2>/dev/null
cat <<'EOF'
{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"First file edit this session. Per ~/.claude/CLAUDE.md, if you have not already loaded the core-coding-agent-behavior skill, load it now to pick up the full coding mechanics (surgical editing, verification ladder, persistent memory) before editing."},"suppressOutput":true}
EOF
exit 0
