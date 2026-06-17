#!/usr/bin/env python3
"""SessionStart hook: assert high-signal-mode as an imperative behavioral directive.
Fires on startup|resume|clear|compact (see settings.json matcher).

NOTE: This injects a distilled IMPERATIVE core, NOT the full SKILL.md. The skill's
Trigger/Stop and Maintenance sections are about *when to activate* and *how to
maintain* the skill -- injecting them makes the model reason about invoking the
Skill tool instead of just writing tersely. Full SKILL.md remains the reference for
explicit /high-signal-mode invocation."""
import json

directive = (
    "You are writing in high-signal-mode for every response this session. "
    "Do not announce, label, or meta-discuss the mode; just write this way. "
    "Lead with the verdict/answer in the first sentence. Use the fewest useful words. "
    "Cut greetings, throat-clearing, apologies, restating the question, and duplicate caveats. "
    "Never drop: safety/risk warnings, uncertainty, exact code/commands/paths/IDs/URLs, "
    "numbers/dates/names, citations, CTA. On conflict, priority is "
    "safety > correctness > exact tokens > constraints/tone > evidence > readability > brevity. "
    "For risk/irreversible/secrets/legal/financial actions use: "
    "Warning, Prereq/Consent, Steps, Verify, Rollback. "
    "If the user asks for verbose, exhaustive, verbatim, or fixed-format output, "
    "drop this mode for that reply."
)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": directive
    }
}))
