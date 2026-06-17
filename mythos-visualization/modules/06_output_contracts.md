# Module 06 — Output Contracts and Report Schemas

Load this module when writing saved reports, comparing artifacts, or enforcing a consistent answer shape.

## Direct answer contract

Use the smallest answer that covers:

1. What the artifact is.
2. What matters for the user's task.
3. Evidence that supports the reading.
4. What is uncertain or not verified.

## Per-sample report schema

```markdown
# Analysis Report: <sample id>

## Identity and route
- Artifact role:
- Visible/source role:
- Dominant lens:
- Mode:
- Route confidence:

## Evidence boundary
- Evidence used:
- Evidence not verified:
- Exactness level:

## Compact model
<objects/source structures/relations that matter>

## Detail-overall bridge
<how local evidence supports meaning/task/classification/risk>

## Risks and limits
- ...

## Validation
- Depth:
- Tools/checks run:
- Checks not run:
```

## Corpus summary schema

```markdown
# Corpus Summary

## Scope
## Inventory
## Routing and coverage
## Cross-artifact patterns
## Conflicts, degraded artifacts, and outliers
## Validation limits
## Handoff artifacts
```

## Release audit schema

```markdown
# Release Audit

## Target map
## Preserved behavior
## Candidate variants
## Score matrix
## Selected version
## Rejected changes and why
## Validation run
## Residual risk
## Artifact links/checksums
```

## Compression rule

Repeated prose belongs in corpus/release summaries, not every report. Per-sample reports should carry only sample-specific identity, route, evidence, bridge, risks, and validation status.
