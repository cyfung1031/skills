# R Review 0001: Release-readiness workflow bootstrap

## Scope

Reviewed the illustrative release-readiness workflow surface: compact skill instructions, reference templates, installer behavior, validator expectations, examples, manifest requirement, context handoff expectations, durable decision handling, and documentation consistency.

## Summary

Changes requested until K demonstrates evidence-backed validation, whole-change impact coverage, manifest consistency, and synchronized documentation. This review intentionally separates a temporary context handoff from a durable release decision so future sessions can resume without turning chat memory into evidence.

## Evidence

- Branch: `main` in illustrative workspace
- Git status: clean in illustrative workspace
- Recent commits reviewed: None; initial example review
- Files reviewed: `SKILL.md`, `LOOP-HARNESS.md`, `README.md`, `VALIDATION.md`, `scripts/validate-template.py`, `scripts/install-template.py`, `examples/.ai-dev-loop/status.md`, `examples/.ai-dev-loop/context/README.md`, `examples/.ai-dev-loop/decisions/README.md`
- Commands run by R: None; R requested K to run validation after edits
- Coverage: repository structure, role templates, status vocabulary, whole-change guidance, context/decision separation, and deliverable cleanup
- Validation result: limited; R reviewed requirements and requested K validation evidence

## Findings

### Finding R-0001-01: Validator must enforce release-critical invariants
- Severity: High
- Status: Open
- Type: Validation
- Location: `scripts/validate-template.py`, `PACKAGE-MANIFEST.json`, `examples/.ai-dev-loop/status.md`
- Evidence: Release artifacts can drift unless checks cover manifest entries, checksums, example record shape, status vocabulary, required template headings, installer smoke behavior, stale versions, and forbidden artifacts.
- Details: A repository may appear complete while missing checksum, status, template, example, or artifact checks. Documentation-only review would not reliably detect those failures.
- Required action: Ensure the validator checks required files, canonical statuses, embedded R/K templates, manifest checksums, installer output, version references, context/decision example presence, and forbidden artifacts.

### Finding R-0001-02: Whole-change impact language must be visible outside the compact instructions
- Severity: Medium
- Status: Open
- Type: Process issue
- Location: `README.md`, `QUICKSTART.md`, `INSTALLATION.md`, `COMPLETE-PACKAGE-GUIDE.md`, `LOOP-HARNESS.md`
- Evidence: K behavior depends on understanding that R findings are not exhaustive task lists and that related docs, examples, scripts, installers, validators, and manifests may need synchronized updates.
- Details: Documentation should prevent narrow implementation that only edits files named in R findings.
- Required action: Keep whole-change impact guidance in the major docs and ensure examples demonstrate that the scan includes affected artifacts R did not explicitly name.

### Finding R-0001-03: Context notes and decision records need clearer examples
- Severity: Medium
- Status: Open
- Type: Documentation
- Location: `examples/.ai-dev-loop/context/`, `examples/.ai-dev-loop/decisions/`, `examples/.ai-dev-loop/status.md`
- Evidence: The example should teach when a continuation note belongs in `context/` and when a durable policy or release choice belongs in `decisions/`.
- Details: Without concrete examples, users may either skip important decisions or overuse decisions for temporary notes.
- Required action: Add one concrete context handoff and one durable decision record, then cite both from `status.md`.

## Clarifications Needed

None.

## Clarification and Objection Responses

None. No K question or objection was pending for this R turn.

## Approval Status

- Spec/Plan Status: Changes requested
- Implementation Status: Changes requested
- Overall Status: Changes requested

## Next Expected K Action

Address all findings, update directly related docs/examples/scripts/manifest expectations, run validation, update `status.md`, and hand back to R with evidence and limitations.
