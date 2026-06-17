# Example Records

This example `.ai-dev-loop/` directory demonstrates a complete release-readiness loop for a workflow-template package. It is intentionally concrete: a package is being prepared for release, R asks for stronger validation and clearer continuity records, K implements them, and R performs terminal review.

The main teaching goal is to make **context** and **decisions** easy to distinguish:

- `context/` records help the next session resume the current work without relying on chat memory.
- `decisions/` records preserve durable choices that future work must obey.
- `reviews/` records show R's evidence, findings, closure, accepted risks, and approval state.
- `responses/` records show K's finding-by-finding answers, changed artifacts, validation evidence, and handoff back to R.
- `status.md` is the current index, not the full history.

## Scenario

A release package contains skill instructions, docs, examples, installer scripts, validator scripts, and a manifest. The team must decide whether release requirements should be documentation-only or enforced by an executable validator. R also notices that future sessions need a compact context note and a durable decision record so the same issue is not rediscovered repeatedly.

## Recommended reading order

1. `status.md` — current state and which records are active.
2. `reviews/0001-r-bootstrap-review.md` — R opens three findings.
3. `decisions/0001-release-validation-gate.md` — durable release validation choice.
4. `context/0001-release-readiness-handoff.md` — temporary continuity note for the current release task.
5. `responses/0001-k-validation-response.md` — K addresses each finding and records validation evidence.
6. `reviews/0002-r-terminal-review.md` — R closes the loop, confirms limits, and grants terminal approval with notes.

## Decision guide: context or decision?

| Record it in | Use when | Example from this directory | Do not use it for |
|---|---|---|---|
| `context/` | The next R/K turn needs a compact handoff about current state, evidence limits, next files to load, or residual risk. | `context/0001-release-readiness-handoff.md` explains current release-readiness state and next-load order. | A permanent policy, architecture choice, dependency decision, or release gate. |
| `decisions/` | The choice should guide future work even after the current loop ends. | `decisions/0001-release-validation-gate.md` requires executable release validation. | Temporary summaries, chat compression, routine edit notes, or facts that must be re-verified. |
| `status.md` | The team needs the current pointer to latest records and current approval state. | Latest R review now points to terminal approval. | Long evidence dumps or complete history. |

## Evidence and placeholder limits

Example commit labels such as `example-r0001`, `example-k0001`, and `example-r0002` are placeholders, not real repository history. Replace them with real commits, commands, file paths, outputs, and validation evidence in a live project.

Do not copy these records into a live repository unchanged. Keep the shape, but replace illustrative facts with observed or measured project evidence.

## Common mistakes this example prevents

- Treating `context/` as evidence. A context note can point to evidence, but R must still verify source files, command output, logs, commits, or explicit user instructions.
- Treating R finding locations as a complete implementation checklist. K must scan directly affected docs, examples, scripts, validators, installers, and manifests even when R did not list every file.
- Treating a decision record as permanent forever. Decisions stay active until a later record revisits them with evidence and a migration or rollback plan.
- Updating examples without updating the manifest. Package examples are release artifacts and can break distribution if checksums drift.

## Traceability pattern

A clear handoff should let a later reviewer trace each open finding to four things: K response, changed artifact, validation evidence, and remaining limitation. In this example, R-0001-03 traces to the K response, the new context and decision files, `status.md`, and the terminal R review that confirms the illustrative evidence limit.
