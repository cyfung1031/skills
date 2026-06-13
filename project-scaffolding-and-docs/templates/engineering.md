<!--
TEMPLATE: docs/ENGINEERING.md — repo-specific build/test/release reality,
conventions, and mechanical verification checklists. This is the "how, in this
repo" guide that does not belong in the product spec. Delete guidance comments.
See SKILL.md §2.5, §6, §7, and §10.
-->

# Engineering Guide

How this repository is actually built, tested, and released. Read this before
executing any plan in `docs/plans/`. `SPEC.md` describes the product; this file
describes the working reality, including workarounds, fixtures, and manual
verification.

## 1. Building

```sh
<exact build commands, each with a one-line comment on what it produces>
```

<Notes on module/dependency order, generated artifacts, environment variables,
or anything an implementer would otherwise get wrong.>

## 2. Testing

```sh
<exact test command(s)>
```

<What the suites cover; the end-to-end / regression corpus and how to run it;
what can and cannot be verified automatically. Use synthetic/anonymized fixture
names in shared documentation; keep real customer/project data only in the
private repository.>

Example fixture table:

| Fixture | Purpose | Expected signal |
| --- | --- | --- |
| `case-renamed-field` | Renamed-but-related input pair | match stays above <threshold> |
| `case-inserted-row` | Inserted row shifts alignment | unrelated pairings do not spike |
| `case-nested-block` | Nested block / grouped input | block boundaries remain stable |

## 3. Performance / resource checks

Document the exact command and threshold, not just the intent.

| Check | Budget | How verified |
| --- | --- | --- |
| `case-renamed-field` first useful result | <150 ms p95 on CI hardware | <command or dashboard> |
| Full synthetic fixture corpus | <2 s p95 / <256 MB peak RSS | <command or dashboard> |

## 4. LLM / contributor context bundles
<!-- Optional but useful once docs grow. Name the minimum docs a human or LLM
should read for common work modes so nobody has to ingest the whole repo by
default. Keep this routing list current when specs split or plans archive. If a
vector store/indexer is used, configure archived plans as low-priority or
history-only sources by default. -->

| Work mode | Read first | Add if needed |
| --- | --- | --- |
| Bug fix | `README.md`, `SPEC.md` current behavior, `CHANGELOG.md` recent entries | relevant decision entry, failing fixture |
| Feature plan | `README.md`, `SPEC.md`, `docs/ROADMAP.md`, active plan | `docs/specs/*` slice, related decisions |
| Release verification | active plan, this guide §7–§9, `CHANGELOG.md` draft | manual fixtures / screenshots |
| Architecture audit | `SPEC.md`, `docs/specs/technical.md` if present, decision log | active and archived plans only as evidence |

## 5. Toolchain / environment workarounds
<!-- If any exist. Each: the defect, the workaround, the ROOT cause, and a
"do not clean up without testing" warning. Future-you will be tempted. -->

1. **<Defect>** — <symptom>. Worked around by <how>. Root fix: <what>.
   Do not remove without testing on the affected environment.

## 6. Code conventions
<!-- The house style a contributor must match: language mode, module
boundaries, naming, error-handling idiom, theming, comment density. Keep it to
constraints the code cannot show on its own. -->

- ...

## 7. Versioning checklist (every release, patch or minor)
<!-- Mechanical, run every time, never partially skipped. -->

1. Bump version everywhere it appears: <list the exact files/strings>.
2. Add a dated `CHANGELOG.md` entry using user-facing wording.
3. Update README "current scope" if scope changed.
4. Update `SPEC.md` shipped-vs-target markers if behavior diverged from target.
5. Build + automated tests green.
6. Manual verification pass (§9) complete, with unverified areas stated.
7. Regression corpus run if the change touched behavior covered by fixtures.
8. Move shipped/superseded plans to `docs/plans/archive/` when the active plan
   directory gets noisy. Update the primary plan index in `docs/ROADMAP.md`;
   historic links in CHANGELOG/decision logs should target the archived file or
   archive directory, not brittle header anchors.
9. At major/stabilization releases, normalize old inline shipped markers in
   `SPEC.md`; leave markers only for current target-vs-shipped deltas.

## 8. Interruption protocol (patch releases mid-plan)

1. Stop at the current safe pause point; make the main branch shippable.
2. Implement the request as the next patch release, following §7.
3. Re-read the active plan's "Assumptions about current code"; update the plan
   doc if the patch invalidated anything.
4. Resume the plan; note the interruption in its status line.

If a spike/prototype invalidates the active design, mark the invalidated section
or plan `superseded`, add a decision-log entry for the trigger/root cause when
the change is non-obvious, and create one clear revised execution path. Do not
leave two active plans competing.

## 9. Manual verification pass (~<n> minutes)
<!-- The documented substitute for whatever cannot be automated: GUI,
perceptual checks, hardware, third-party integrations, or other human-observed
flows. Release summaries must state what was and was not machine-verified. -->

- <screen/flow>: <what to do, what to observe, fixture data if any>.
- `case-renamed-field` (synthetic): <manual path, expected visible result>.
- `case-inserted-row` (synthetic): <manual path, expected visible result>.
