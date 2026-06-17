# InsightForge Review Harness

Use this only when `SKILL.md` is too compact for the review at hand. It expands the same obligations without changing them.

## Mode selector
- `quick`: small low-risk delta; inspect source/diff; run invariant, negative-space, and observability probes; return only material issues.
- `standard`: default; include target map, findings, amendment portfolio, validation tier, preserved behavior, assumptions, and residual risk.
- `deep`: release, security/privacy, migration, policy, high-cost, high-ambiguity, or contested work; include scoring, fixtures, rollback/migration, observability, and audit packet.

## Artifact-specific probes
- Code: diff locator, behavioral invariant, regression surface, boundary fixtures, dependency/API compatibility, error path, observability, smallest safe patch.
- Docs/specs: truth drift, version references, examples, audience fit, exact-token preservation, missing caveats, operational handoff.
- Prompts/skills: activation triggers, priority/precedence, refusal boundaries, exact token/code preservation, mode gates, unwanted behavior changes, token load, regression-firewall checks, whether the skill causes an artifact to be produced.
- Releases/packages: manifest/checksum/version agreement, forbidden artifacts, installer/validator smoke path, archive contents, generated-output hygiene, reproducibility.
- Migrations: rollback, old-client compatibility, data loss, partial failure, observability, operational runbook.

## Scoring rubric
Use 0-10 scoring only when comparing options or selecting a successor. Recommended categories and weights:
- target fit/user value: 20
- correctness/executability: 18
- safety/guardrails: 16
- evidence/validation/reproducibility: 16
- behavior preservation/compatibility: 12
- maintainability/clarity: 10
- token/runtime cost: 8

Scores above 8 require positive source evidence. Scores above 9 require strong evidence and no material missing requirement. Score target fit separately from feature richness; do not reward length, polish, filename recency, or assumed intent.

## Minimal output shapes
Quick review:
```text
Verdict: <pass / pass with notes / changes requested / blocked> (<confidence>, <validation tier>)
Must amend:
- <severity> | <finding> | <tag + locator> | <amendment> | <validation>
Preserve:
- <behavior>
Residual risk: <risk or none material>
```

Standard/deep review:
```text
Target map: <compact map>
Findings: <schema table>
Amendment portfolio: <must / high-leverage / innovative / preserve>
Validation: <run or proposed, tier, limits>
Score matrix: <only if useful>
Selected amendment: <why this wins>
Residual risk and next action: <bounded>
```

## Review linting
When a review is large or repeated, run `scripts/insightforge_review_lint.py <review.md>` to detect missing finding fields and absent evidence tags. The script is a deterministic guardrail; human review still decides substance.
