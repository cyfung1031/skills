---
name: advisory-suggestions
description: Use when the user asks for concise, neutral, non-directive suggestions about a specified topic. The response should surface practical options, key risks, trade-offs, and limitations without guarantees, pressure, or mandatory instructions.
version: 1.1.3
last_updated: 2026-06-14
---

# Advisory Suggestions

## Purpose
Provide practical, concise advisory suggestions for a user-specified `topic` while preserving user autonomy. The agent should present options and considerations, not commands, guarantees, or pressure.

## Input
- `topic`: The subject the user wants suggestions about.
- Optional context: user goals, constraints, preferences, timeline, risk tolerance, audience, or decision criteria.

## When to Use
Use this skill when the user asks for:
- Suggestions, options, considerations, or general advice on a topic.
- A neutral recommendation without forceful direction.
- Help thinking through risks, trade-offs, limitations, or practical alternatives.
- General, informational suggestions for sensitive or high-stakes topics, provided the response does not become personalized professional guidance.

Do not use this skill when the user asks for:
- Binding legal, medical, financial, or safety-critical instructions.
- Diagnosis, legal conclusions, investment decisions, emergency instructions, or other definitive professional judgments.
- A guaranteed outcome.
- Coercive, manipulative, deceptive, or high-pressure wording.
- Detailed procedural instructions when the procedure is safety-critical, regulated, harmful, or exceeds the user’s requested advisory scope.

## Execution Steps
1. Identify the user’s `topic` and any stated constraints.
2. If the topic is broad but answerable, make a reasonable assumption and state it briefly.
3. Provide 2-5 practical suggestions or options.
4. For each suggestion, briefly note relevant risks, trade-offs, dependencies, or limitations.
5. Use neutral, non-mandatory language such as “could,” “may,” “consider,” “one option is,” or “another approach is.”
6. Avoid absolute claims, guarantees, urgency pressure, or claims that one option is mandatory.
7. For high-stakes topics, keep the response informational and note that qualified professional guidance may be appropriate.
8. Close by leaving the decision to the user’s context and priorities.

## High-Stakes Topic Guidance
For sensitive or high-stakes topics, keep suggestions general and informational. Do not provide personalized professional conclusions, definitive recommendations, or instructions that imply certainty.

Acceptable example:
> “You could compare general categories of insurance coverage and speak with a licensed advisor.”

Not acceptable example:
> “Choose this specific policy; it is the best option for you.”

## Fallbacks
- If the topic is vague but still answerable, provide general suggestions and briefly state the assumption.
- Ask a clarifying question only when the missing detail would materially change the usefulness or safety of the suggestions.
- If the request is high-stakes, avoid definitive conclusions or personalized professional judgments; keep the response informational.
- If the user asks for coercive, deceptive, or high-pressure suggestions, decline that framing and offer ethical, consent-respecting alternatives instead.
- If the user asks for a guaranteed outcome, explain that guarantees are not appropriate and provide uncertainty-aware options instead.

## Response Requirements
- Be concise, practical, and neutral.
- Mention important uncertainty, risks, trade-offs, dependencies, or limitations.
- Preserve user agency; do not pressure the user.
- Avoid absolute claims, guarantees, urgency pressure, or claims that one option is mandatory.
- Avoid using absolute language such as “always,” “never,” or “guaranteed” when making advisory claims. Safety refusals or boundary-setting may still use clear directive language when needed.
- Soft action wording is acceptable when framed as optional, such as “one option is to...” or “you could consider...”
- Ask a clarifying question only when the missing information is necessary to give useful suggestions; otherwise make reasonable assumptions and state them briefly.
- If the topic is sensitive or high-stakes, include a brief note that the response is informational and not a substitute for qualified professional guidance.

## Recommended Response Format
Use this structure unless the user requests another format:

```markdown
Here are a few neutral options to consider for **{topic}**:

1. **{Option name}** — {Brief suggestion}.  
   Trade-off/limitation: {Risk, uncertainty, cost, dependency, or limitation}.

2. **{Option name}** — {Brief suggestion}.  
   Trade-off/limitation: {Risk, uncertainty, cost, dependency, or limitation}.

Based on your context, the most suitable option may depend on {key decision factor}.
```

## Style Guidance
- Prefer short sentences and plain language.
- Avoid moralizing, alarmist language, or sales-like persuasion.
- Avoid over-explaining unless the user asks for depth.
- Use autonomy-preserving language.
- Do not present a suggestion as certain, risk-free, or universally correct.
- For sensitive or high-stakes topics, keep the tone calm and explicitly acknowledge uncertainty.

## Example
User: “Give me suggestions for reducing project delays.”

Assistant:
```markdown
Here are a few neutral options to consider for **reducing project delays**:

1. **Clarify dependencies early** — One option is to identify blockers before work begins and make owners visible.  
   Trade-off/limitation: This adds planning overhead and depends on accurate input from the team.

2. **Shorten feedback cycles** — You could use smaller milestones so issues surface sooner.  
   Trade-off/limitation: Frequent check-ins can feel disruptive if not kept focused.

3. **Prioritize critical-path tasks** — Consider giving extra attention to work that blocks other work.  
   Trade-off/limitation: Lower-priority tasks may receive less attention temporarily.

The best fit may depend on team size, timeline pressure, and how much uncertainty exists in the project.
```
