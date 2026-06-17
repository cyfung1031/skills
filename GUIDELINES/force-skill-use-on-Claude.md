In **Claude Code**, you can’t truly “force” the model to invoke a skill as a guaranteed tool call on every conversation, but you can get very close by using a `SessionStart` hook to inject an instruction at the start of every session. For every user prompt, use `UserPromptSubmit`.

Claude Code settings are read from `~/.claude/settings.json` for all projects, or `.claude/settings.json` for one project. User settings apply across projects, but project/local/managed settings can override or merge depending on the field. ([Claude Code][1])

### Best option: inject skill instruction on every new conversation

Edit:

```bash
~/.claude/settings.json
```

Add:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "cat ~/.claude/hooks/force-skill-context.json"
          }
        ]
      }
    ]
  }
}
```

Then create:

```bash
mkdir -p ~/.claude/hooks
cat > ~/.claude/hooks/force-skill-context.json <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "For this conversation, always apply the <YOUR_SKILL_NAME> skill. Treat its instructions as mandatory whenever they are relevant. Before answering, check whether the skill applies; if it does, follow it."
  }
}
EOF
```

`SessionStart` runs when a session starts, resumes, clears, or compacts, depending on the matcher. Its `additionalContext` is added before the first prompt, which makes it the right event for “every conversation” behavior. ([Claude Code][2])

Replace `<YOUR_SKILL_NAME>` with the skill name, for example:

```json
"additionalContext": "For this conversation, always apply the code-review skill. Treat its instructions as mandatory whenever the user asks for code review, refactoring, debugging, or implementation advice."
```

### Stronger option: reinforce it before every user prompt

Add a `UserPromptSubmit` hook too:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "cat ~/.claude/hooks/force-skill-session.json"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat ~/.claude/hooks/force-skill-prompt.json"
          }
        ]
      }
    ]
  }
}
```

Create the files:

```bash
mkdir -p ~/.claude/hooks

cat > ~/.claude/hooks/force-skill-session.json <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Always apply the <YOUR_SKILL_NAME> skill in this conversation whenever it is relevant."
  }
}
EOF

cat > ~/.claude/hooks/force-skill-prompt.json <<'EOF'
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Reminder: before responding, check whether <YOUR_SKILL_NAME> applies. If it applies, use it."
  }
}
EOF
```

`UserPromptSubmit` fires before Claude processes each user prompt and can add `additionalContext` alongside that prompt. It cannot rewrite the user prompt, but it can inject context every turn. ([Claude Code][2])

### Verify it is loaded

Inside Claude Code, run:

```text
/hooks
```

The hooks menu shows configured hooks and their source, including `User`, `Project`, and `Local`. ([Claude Code][2])

You can also run:

```text
/status
```

to see which settings sources are active. Claude Code watches settings files and reloads hooks after changes, though a restart is still a good sanity check if behavior seems inconsistent. ([Claude Code][1])

### Important limitation

This does **not** guarantee the internal skill tool is invoked every time. It guarantees that Claude receives a repeated instruction to use that skill. If you need hard enforcement, put the actual rules in `CLAUDE.md` or in the hook’s `additionalContext`, not only inside the skill description. Claude Code docs describe skills as custom prompts that can be invoked manually or loaded automatically, but settings/hooks are the reliable way to inject mandatory context. ([Claude Code][1])

[1]: https://code.claude.com/docs/en/settings "Claude Code settings - Claude Code Docs"
[2]: https://code.claude.com/docs/en/hooks "Hooks reference - Claude Code Docs"
