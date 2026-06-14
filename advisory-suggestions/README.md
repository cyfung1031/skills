# advisory-suggestions

A hardened generic skill for producing concise, neutral, non-directive advisory suggestions.

## Purpose

Use this skill when a user asks for suggestions, options, considerations, general advice, trade-offs, alternatives, or a neutral recommendation about a specified topic.

The skill is designed to preserve user agency by presenting practical options with risks, trade-offs, dependencies, or limitations. It avoids guarantees, pressure, commands, and professional conclusions.

## Installation

Place this file in the same folder as `SKILL.md`:

```text
advisory-suggestions/
├── SKILL.md
└── README.md
```

No additional runtime dependencies are required.

## Skill Metadata

```yaml
name: advisory-suggestions
version: 1.2.0
```

## When to Use

Use for requests such as:

- “Give me suggestions for...”
- “What are my options for...”
- “Help me think through trade-offs...”
- “What should I consider before...”
- “Give a neutral recommendation...”

## When Not to Use

Do not use this skill for:

- Binding legal, medical, financial, safety-critical, or regulated instructions
- Diagnosis, legal conclusions, investment picks, emergency instructions, or definitive professional judgment
- Guaranteed outcomes
- Coercive, deceptive, manipulative, exploitative, or high-pressure messaging
- Detailed operational steps for harmful, regulated, dangerous, or safety-critical procedures

## Required Output Behavior

When active, the assistant should:

1. Identify the topic and explicit constraints.
2. Make a brief assumption only if missing details are not essential.
3. Provide 2–5 neutral options.
4. Include a trade-off, risk, dependency, uncertainty, or limitation for every option.
5. Use autonomy-preserving language such as “could,” “may,” “consider,” or “one option.”
6. Avoid guarantees, pressure, absolute claims, and mandatory wording.
7. Keep high-stakes topics informational and suggest qualified professional guidance when appropriate.

## Recommended Response Shape

```markdown
Here are a few neutral options to consider for **{topic}**:

1. **{Option}** — {Suggestion using non-mandatory wording}.  
   Trade-off/limitation: {Risk, uncertainty, cost, dependency, or limitation}.

2. **{Option}** — {Suggestion using non-mandatory wording}.  
   Trade-off/limitation: {Risk, uncertainty, cost, dependency, or limitation}.

The best fit may depend on {key decision factor}.
```

## Example

User:

```text
Give me suggestions for reducing project delays.
```

Assistant:

```markdown
Here are a few neutral options to consider for **reducing project delays**:

1. **Clarify dependencies early** — One option is to identify likely blockers before work begins and make owners visible.  
   Trade-off/limitation: This adds planning overhead and depends on accurate input from the team.

2. **Use smaller milestones** — You could break work into shorter checkpoints so issues surface earlier.  
   Trade-off/limitation: Frequent check-ins can feel disruptive if they are not kept focused.

3. **Prioritize critical-path work** — Consider giving more attention to tasks that block other tasks.  
   Trade-off/limitation: Lower-priority work may receive less attention temporarily.

The best fit may depend on team size, deadline pressure, and how uncertain the work is.
```

## Maintenance Notes

- Keep the skill concise so agents can load and follow it reliably.
- Prefer mandatory behavioral constraints over long explanations.
- Bump the version when changing activation rules, refusal rules, or required output behavior.
