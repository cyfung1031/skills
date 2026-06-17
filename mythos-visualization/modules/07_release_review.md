# Module 07 — Successor Release Review

Load this module when improving Mythos Visualization itself or selecting among candidate versions.

## Major-version gate

A major release is justified only when it changes structure, loading strategy, validation mechanics, or compatibility boundaries while preserving protected behavior. v3 uses a compact kernel plus optional modules and scripts; that is a structural/token-efficiency change, not a reason to weaken output discipline.

## Target map for successor work

- Intended outcome: safer, clearer, more token-efficient visual reasoning.
- Must preserve: core invariant, smallest sufficient mode, one-dominant-lens default, evidence boundaries, source/render/runtime separation, compact stop rule.
- Must not introduce: mandatory OCR/rendering/external lookup, decorative bloat, overconfident identity/domain claims, loss of direct-answer usability.
- Improvement budget: additive or structural only when it lowers always-load cost or improves mechanical validation.

## Candidate scoring rubric

Score 0–10:

- correctness and evidence discipline;
- target fit and user value;
- token efficiency;
- behavior preservation;
- safety/guardrails;
- maintainability;
- validation and observability;
- compatibility/migration;
- cost/complexity.

Scores above 9 require positive evidence and no material missing requirement. Reject variants that improve breadth while worsening correctness, safety, compactness, or unwanted behavior risk.

## Release artifacts

- `SKILL.md` compact kernel;
- modules with load triggers;
- scripts for package/report/corpus checks;
- `skill_contract.json` for machine validation;
- migration guide;
- release notes;
- validation log;
- checksums;
- zip package.

## Regression firewall

Before release, verify:

- YAML version equals title/version references.
- Module paths exist and are referenced.
- Protected invariants exist in `SKILL.md`.
- Optional modules are not required for direct answers.
- Scripts compile and produce non-empty validation output.
- No module converts optional tools into mandatory defaults.
- Package has checksums and a manifest.
