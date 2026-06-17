# Decision 0001: Release validation must be executable, not documentation-only

## Status

Accepted for the illustrative release-readiness workflow.

## Context

The workflow template is distributed as a package containing skill instructions, reference docs, examples, installer scripts, validator scripts, and a manifest. Documentation can describe release requirements, but documentation alone cannot reliably catch missing files, stale version references, forbidden packaging artifacts, invalid example status values, or manifest checksum drift.

## Decision

Release readiness must be enforced by an executable validator in addition to documentation. K must update directly affected docs, examples, scripts, installer behavior, and manifest expectations whenever release-facing behavior changes. R must not grant terminal approval until validation evidence is recorded or an explicit accepted risk is documented.

## Options considered

### Option A: Documentation-only release checklist

Rejected. It is easy to forget or partially apply, and it does not produce measured evidence.

### Option B: Executable validator plus documentation

Chosen. It keeps human-readable guidance while providing repeatable checks for package structure, required files, example record shape, status vocabulary, whole-change guidance, installer smoke behavior, forbidden artifacts, version references, and manifest checksums.

### Option C: External CI-only enforcement

Rejected for this package example. CI can be added later, but the standalone package should remain locally verifiable without assuming a hosted CI service.

## Consequences

- Package edits may require manifest regeneration.
- Validator changes must stay synchronized with docs and examples.
- R can ask K for command output instead of accepting prose claims.
- The package has a slightly higher maintenance burden, but release drift becomes easier to detect.
- If the validator fails, R may not grant terminal approval unless R records an explicit accepted risk and rollback/retry path.

## Enforcement owner

K owns running or updating validation after release-facing changes. R owns deciding whether the recorded evidence is enough for terminal approval. Neither role may convert missing command evidence into a pass by restating this decision.

## Validation and enforcement

Expected validation command in this illustrative package shape:

```bash
python3 scripts/validate-template.py
```

In a live package, use the actual package validator command and record the working directory, exit status, output summary, skipped checks, and any limitations.

## Revisit trigger

Revisit this decision if the package stops shipping scripts, moves validation to a guaranteed CI gate, changes distribution format, or introduces a stronger reproducible release process.
