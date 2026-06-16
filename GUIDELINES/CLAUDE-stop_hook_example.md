# Stop Hook

A **Stop hook** is a shell command in `settings.json` that runs **before Claude Code yields back to you**, reads `.ai-dev-loop/status.md`, and enforces the continuation rule mechanically. If the status says the next action is R or K (not `Stop`), the hook injects an error or re-prompt that forces me to continue instead of stopping.

## How it works

Instead of relying on my reading and following the Operating instruction, the hook makes stopping **mechanically impossible** if `Next Expected Role Action` names a role. It's the enforcement layer.

- **Runs at Stop**: Before Claude Code would yield back to you
- **Reads `.ai-dev-loop/status.md`**: Gets the `Next Expected Role Action` field
- **If `Stop`**: Allows stopping normally
- **If `R-NNNN` or `K-NNNN`**: **Blocks the stop** and returns:
  - `continue: false` (prevents the stop)
  - `stopReason`: Shows you why the loop isn't complete
  - `additionalContext`: Injected back to me so I know what role to execute next

This makes the continuation rule **mechanically enforced**.

## How to set it up

Use the `update-config` skill to add a before-stop hook.

1. Read `.ai-dev-loop/status.md`
2. Extract the `Next Expected Role Action` value
3. **Block the stop** if it's anything other than `Stop`
4. **Re-inject** the required action to force continuation

### Manual File

Create the file.

### the `/config` command

You can try:
```
/config update .claude/settings.json hooks
```

And paste the JSON.

## Claude CLI command

* /update-config

## Path

* your_project_folder/.claude/settings.json
* ~/.claude/settings.json

# settings.json

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c '\nstatus_file=\".ai-dev-loop/status.md\"\nif [ ! -f \"$status_file\" ]; then\n  echo \"{\\\"continue\\\":true}\"\n  exit 0\nfi\naction=$(grep \"^## Next Expected Role Action$\" \"$status_file\" -A 1 | tail -1 | awk '\''NF{print $1}'\'' | sed '\''s/:$//'\'')\nif [ \"$action\" = \"Stop\" ] || [ -z \"$action\" ]; then\n  echo \"{\\\"continue\\\":true}\"\nelse\n  echo \"{\\\"continue\\\":false,\\\"stopReason\\\":\\\"ai-dev-loop: Next action is $action. Continuing the loop.\\\",\\\"hookSpecificOutput\\\":{\\\"hookEventName\\\":\\\"Stop\\\",\\\"additionalContext\\\":\\\"Must perform: $action\\\"}}\"\nfi\n'",
            "statusMessage": "Checking ai-dev-loop status..."
          }
        ]
      }
    ]
  }
}
```
