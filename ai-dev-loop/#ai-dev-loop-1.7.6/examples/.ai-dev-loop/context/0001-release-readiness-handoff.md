# Context 0001: Release readiness handoff

## Why this note exists

The release-readiness example touches docs, examples, validator behavior, installer behavior, and manifest consistency. This compact note preserves the working context so the next R or K turn does not depend on chat memory.

## Current goal

Publish a clean, auditable workflow-template package where release-critical expectations are enforced by both documentation and executable validation.

## Current state

- Latest R review: `examples/.ai-dev-loop/reviews/0001-r-bootstrap-review.md`
- Latest K response: `examples/.ai-dev-loop/responses/0001-k-validation-response.md`
- Active decision: `examples/.ai-dev-loop/decisions/0001-release-validation-gate.md`
- Current approval state: Approved with notes in the illustrative example
- Open required findings: None in the example record

## Evidence already recorded

- K recorded the intended validation command: `python3 scripts/validate-template.py`
- K recorded the expected pass summary: `Template validation passed.`
- K recorded whole-change impact coverage across docs, examples, installer, validator, and manifest expectations

## Evidence limits

This is an illustrative package example. Commit labels are placeholders. This context note is not evidence by itself; it only tells the next role which evidence to load. In a live project, R must verify actual repository files, command output, manifest checksum state, and git status before terminal approval.

## Next role should load first

1. `examples/.ai-dev-loop/status.md`
2. `examples/.ai-dev-loop/decisions/0001-release-validation-gate.md`
3. Latest R and K records
4. Actual validator output from the live repository

## Residual risk

A future package edit may change docs or examples without regenerating the manifest. The durable decision requires validator enforcement so drift is caught before release. If validation cannot run, status must become blocked or approved only with an explicit accepted risk from R.
