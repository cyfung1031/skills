# Failed Validation and Correction Audit Example

## Scenario
A package validator failed because a new documentation file was added but not listed in `PACKAGE-MANIFEST.json`.

## Old claim
`measured`: package validation passed.

## Validator evidence before correction
- Command: `python3 scripts/validate-ai-dev-loop-package.py`
- Working directory: package root
- Exit status: `1`
- Output summary: validator reported `manifest missing file: <new-doc>.md`.

## Corrected claim
`measured`: package validation failed before the manifest was regenerated; it passed only after inventory, checksums, and byte counts were updated.

## Mistaken assumption
The author assumed the manifest was advisory. It is part of the release contract.

## Failed safeguard
The whole-change impact scan did not include release artifact inventory after adding documentation.

## Amendment
Regenerate `PACKAGE-MANIFEST.json`, rerun `python3 scripts/validate-ai-dev-loop-package.py`, and preserve exact output in the K response.

## Validator evidence after correction
- Command: `python3 scripts/validate-ai-dev-loop-package.py`
- Working directory: package root
- Exit status: `0`
- Output summary: `AI Development Loop standalone package validation passed.`

## Obsolete conclusion
The earlier approval based on the stale manifest is obsolete and must not be reused.

## Residual risk
External packaging or upload systems may add metadata after validation; final zip hygiene must be checked separately.
