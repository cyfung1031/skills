<!--
TEMPLATE: docs/ROADMAP.md — an INDEX of release plans + the versioning and
interruption policy. Not a plan itself. Delete guidance comments.
See SKILL.md §2.3 and §7.
-->

# <Product> Roadmap

Index of release plans. Each plan in `docs/plans/` is self-contained: feature
specs, UI/UX requirements, technical design, ordered work breakdown with
verification, acceptance criteria, risks, and safe pause points. A developer —
human or LLM — should be able to pick up any plan cold and execute it.

Companion documents:
- [SPEC.md](../SPEC.md) — product & technical specification (the what/why)
- [docs/ENGINEERING.md](ENGINEERING.md) — build/test reality, conventions,
  release checklist (the how, on this repo)
- [CHANGELOG.md](../CHANGELOG.md) — what actually shipped

## Versioning & interruption policy
<!-- Define what your version components mean, why this scheme fits, and the
rules that keep the project interruptible. Pick one pattern; delete the rest.

Options/tradeoffs:
- 0.x minor/patch discipline: good for evolving products before a stable 1.0;
  minor = planned themes, patch = interruptions.
- Strict SemVer: good for libraries/public APIs; major = breaking, minor =
  backward-compatible features, patch = backward-compatible fixes.
- Date-based versions (YYYY.MM.DD or YYYY.MM.N): good for data/content/internal
  tools where chronology matters more than API compatibility.
-->

Chosen scheme: <0.x minor/patch | strict SemVer | date-based | other>.
Rationale: <why this makes ordering, compatibility, and interruptions legible>.

- **Planned releases:** <how they are numbered and what they carry>.
- **Interrupting releases:** <how bug reports / UX corrections / small requests
  are numbered and prioritized>. Interrupting work takes priority over the
  active plan when it is release-blocking or user-blocking.
- Rules that make interruptions cheap:
  1. The main branch must always build, pass tests, and run. Land plan work in
     verifiable slices, never half-wired.
  2. Every plan's work breakdown is ordered so each completed task is a safe
     pause point: ship-ready, documented, tested.
  3. After any patch release, re-check the active plan's "Assumptions about
     current code" against what the patch changed.
  4. Version bump + CHANGELOG + any in-app version string are part of every
     release, patch or minor (checklist in ENGINEERING.md).
  5. Shipped/superseded plans may move to `plans/archive/`; keep this roadmap
     as the primary plan index, linked to archived files. Historic changelog or
     decision-log links should avoid brittle plan-header anchors.

## Release train

| Version | Theme | Plan | Status |
|---|---|---|---|
| 0.1.0 | Baseline reader with synthetic fixture corpus | — | ✅ shipped <2026-01-15> |
| **0.2.0** | **Changed-region pairing** | [plans/0.2.0-changed-region-pairing.md](plans/0.2.0-changed-region-pairing.md) | planned |
| **1.0.0** | **Public workflow stabilization** | [plans/1.0.0-public-stabilization.md](plans/1.0.0-public-stabilization.md) | planned |

Ordering rationale:
<!-- Why this sequence — the dependencies a re-planner needs. -->
- 0.2.0 before 0.3.0 because reliable changed-region pairing is the prerequisite for export and review workflows.
- Cross-cutting concerns (accessibility, security, perf) are acceptance
  criteria in *every* earlier plan — retrofitting is the expensive path.

Unscheduled candidates:
<!-- Future work not yet on the train. -->
- Export review packet for auditor handoff (SPEC §9; depends on stable changed-region pairing).
- <item> (SPEC §<n>)
