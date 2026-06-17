# Evidence and mechanical state

Verification effort must match risk. Do not claim more than the evidence supports.

## Evidence ladder

1. **Self-consistency:** the answer satisfies every must-have in the contract.
2. **Source check:** claims are grounded in provided files, authoritative sources, or stable reasoning.
3. **Mechanical check:** scripts, linters, validators, tests, builds, schema checks, or zip tests pass.
4. **Behavior check:** the changed system, artifact, UI, command, or document behaves as intended.
5. **Blast-radius check:** nearby uses, edge cases, dependent artifacts, privacy exposure, and regression risks still make sense.

Small routine tasks may need only the first two levels. Code, data, artifacts, high-stakes, current, safety-sensitive, or user-facing actions need higher levels when available.

## Evidence quality

Evidence must be observable, name what was checked, and include the observed result. Avoid hedges such as “looks right”, “should work”, “probably”, “not run”, and empty placeholders. For code/artifact work, prefer command/result evidence; for document or visual work, name the inspected source, page, row, or rendered artifact.

Good evidence examples:

- `ran python3 scripts/verified_effort_lint.py . -> 12 passed, 0 failed`
- `opened final zip with python -m zipfile -t -> OK`
- `checked SKILL.md module map against modules/ -> all linked files exist`
- `rendered page 2 screenshot -> table header and total row visible without clipping`

Bad evidence examples: `looks good`, `should work`, `probably fixed`, `not run`, `manual check` without what was checked and observed.

## State policy

Use `scripts/state.py` for long, risky, multi-file, multi-session, package, or easy-to-derail work. The state file is disposable scratch; never store secrets or unnecessary private data in it. Update it after material discoveries, edits, failed checks, and completed verification.

`state.py check` passes only when all criteria are met with accepted evidence, no open questions remain, and the phase is `report` or `done`. If it fails, the task is not done; either finish the work or clearly report the partial result and blocker.
