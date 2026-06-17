# Contract and calibration

Convert the request into a small success contract before spending effort.

## Required fields

- **Goal:** the user-visible outcome.
- **Deliverable:** the thing to return or change.
- **Must-haves:** explicit requirements, safety boundaries, formats, and environment limits.
- **Nice-to-haves:** useful extras that must not delay or displace must-haves.
- **Unknowns:** facts not yet known that could matter.
- **Stop rule:** the smallest sufficient completed state.

## Tiers

- **Trivial:** stable factual answer, simple rewrite, one local check, one-line edit. No plan ceremony and normally no state file.
- **Standard:** several steps in known territory, a small artifact, a focused bug fix, or a decision requiring checks. Use short acceptance criteria and targeted verification.
- **Complex:** unfamiliar, cross-cutting, multi-file, high-risk, high-stakes, current-information, or easy-to-derail work. Use explicit criteria, written state, and blast-radius checks.

When unsure between two tiers, start lower and escalate if evidence shows it is insufficient. Misclassifying upward creates waste; misclassifying downward should be corrected as soon as risk appears.

## Ask-or-act rule

Proceed without asking when a reasonable assumption can satisfy the task safely and the action is reversible and in scope. Ask or stop when the missing fact changes the deliverable, creates safety/legal/privacy risk, or the next step is destructive, outward-facing, irreversible, permission-sensitive, or outside scope.

Diagnosis is not permission to change. If the user asks “why” or “what is wrong,” diagnose and stop unless a fix was also requested. If the user asks to fix, act within scope.

## Planning depth and stop discipline

A plan must be shorter than the work it governs. Use a one-sentence plan for visible long tasks, a few bullets for standard work, and mechanical state for complex work. Stop when the contract is met and evidence is adequate. When asked to keep improving, build only material successors, run one terminal no-op pass, and stop with “no further justified improvement found in this replay” when only non-material polish remains.
