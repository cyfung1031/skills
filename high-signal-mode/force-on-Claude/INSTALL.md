# high-signal-mode hook enforcement — install

SessionStart injects an IMPERATIVE behavioral directive (distilled core, ~760 chars),
NOT the full SKILL.md. Reason: injecting the skill's Trigger/Stop activation logic made
the model reason about *invoking the Skill tool* and meta-discuss the mode instead of
just writing tersely. Per-turn reminder is throttled (silent on ~5 of every 6 turns).

## Install

```bash
# 1. dirs
mkdir -p ~/.claude/hooks

# 2. scripts
cp high-signal-session.py high-signal-reminder.py ~/.claude/hooks/
chmod +x ~/.claude/hooks/high-signal-session.py ~/.claude/hooks/high-signal-reminder.py

# 3. merge the "hooks" block from settings.json into ~/.claude/settings.json
#    (do NOT overwrite the file — merge, preserving existing hooks/permissions)

# OPTIONAL — only if you also want manual /high-signal-mode invocation as a Skill:
#   mkdir -p ~/.claude/skills
#   ln -s /Users/cyfung/Documents/GitHub/cy-skills/high-signal-mode ~/.claude/skills/high-signal-mode
# The hooks no longer depend on this symlink (they no longer read SKILL.md).
```

## Alternative mechanism: output style

If hooks still feel like the wrong layer, Claude Code's **output styles** are the
native tool for "always write every response this way" — they modify the system
prompt directly, persist for the session, cost no per-turn tokens, and carry zero
skill/tool ambiguity. Put the same directive text in `~/.claude/output-styles/high-signal.md`
and activate with `/output-style high-signal`. Consider this if directive-injection
still drifts.

## Tuning

- `EVERY` in high-signal-reminder.py: raise (8–10) for more savings, lower (3–4) if drift appears.
- After install, verify SubagentStart honors additionalContext (run a subagent task); if not, drop that block — harmless no-op.

## Files

- settings.json          — hooks block to merge
- high-signal-session.py — SessionStart: load full skill (startup|resume|clear|compact)
- high-signal-reminder.py — UserPromptSubmit: throttled nudge
