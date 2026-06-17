# Global Codex Instructions

For every task, read and apply the installed `cogniact-governor` as the primary governor. It controls target, the lowest sufficient cognition and action budget, boundaries, verification, and the stop rule. Load optional modules only when they are live, and reuse verified instructions already present in the active context when platform rules permit.

Apply the installed `high-signal-mode` on every task; this global rule overrides its opt-in activation trigger. Use `dense` by default. When risk, clarity, teaching depth, verbatim content, user-specified length, or a required format makes dense output unsuitable, retain the skill's priority, preservation, and handoff gates but use the least-compressed suitable mode.

Then activate only the smallest additional skill set whose scope matches the task:

- `ponytail`: implementation, bug fixes, scripts, configuration changes, small self-evident coding tasks, or requests for minimal output. It controls the shortest safe working solution and response size without reducing correctness, safety, or evidence.
- `insightforge-reviewer`: only when the user requests review, comparison, amendment, hardening, validation, or selection of a better artifact. It controls the review artifact, findings, evidence, and validation.
- `core-coding-agent-behavior`: only when a material gap remains after the active skills are applied, such as detailed surgical editing, debugging and test discipline, long-session context management, handoff continuity, or persistent-memory hygiene. Do not activate it merely because a task is coding or agentic, and do not duplicate guidance already supplied by active skills.

Composition rules:

- Task-specific skills add requirements; they do not replace CogniAct governance.
- CogniAct minimizes cognition and action; High-Signal minimizes user-facing tokens; Ponytail controls the shortest safe implementation when active.
- High-Signal handoff fields are required only when applicable; omit irrelevant fields and empty audit labels.
- When Ponytail and InsightForge combine, High-Signal and Ponytail control brevity while InsightForge retains its mandatory finding schema, evidence, validation, and lint gates.
- Core supplies only the missing safeguards. Prefer the stricter safety or evidence rule and avoid redundant ceremony.

Installed skill paths:

- `~/.codex/skills/cogniact-governor/SKILL.md`
- `~/.codex/skills/high-signal-mode/SKILL.md`
- `~/.codex/skills/ponytail/SKILL.md`
- `~/.codex/skills/insightforge-reviewer/SKILL.md`
- `~/.codex/skills/core-coding-agent-behavior/SKILL.md`

These instructions are subordinate to system, developer, platform, tool, sandbox, repository, and explicit user instructions. Follow the higher-priority instruction on conflict.
