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
Use 0-10 scoring only when comparing options or selecting a successor. With a single candidate (no candidate set), do not score — state that exemption explicitly in the output rather than omitting the matrix silently. Recommended categories and weights:
- target fit/user value: 20
- correctness/executability: 18
- safety/guardrails: 16
- evidence/validation/reproducibility: 16
- behavior preservation/compatibility: 12
- maintainability/clarity: 10
- token/runtime cost: 8

Scores above 8 require positive source evidence. Scores above 9 require strong evidence and no material missing requirement. Score target fit separately from feature richness; do not reward length, polish, filename recency, or assumed intent.

## Minimal output shapes
Quick review (each "Must amend" line is a minimum-viable finding: severity | finding | verbatim evidence tag + locator | amendment | validation):
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
Run `scripts/insightforge_review_lint.py <review.md>` and resolve every failure before finalizing any `standard` or `deep` review; recommended for `quick`. If skipped, state why in the handoff. The script is a deterministic guardrail (it checks finding-line structure and evidence tags); human review still decides substance. It accepts both the quick minimum-viable finding line and the full eight-field row.

## Validation escalation
Async/effect loops, retry or auto-reload conditions, concurrency/races, and unbounded recursion or memory growth require at least one T2 live reproduction; do not assert such a bug is real or fixed from T0/T1 inspection alone.
