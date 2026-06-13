<!--
TEMPLATE: docs/plans/<version>-<theme>.md — one cold-start-executable plan per
release/slice. Delete guidance comments as you go.
Test of done: a competent stranger could execute this without asking you
anything. See SKILL.md §2.4 and §4.2.
Use placeholders or anonymized names in shared templates. Replace them with real
repo details only inside the private project repository.
-->

# <version> — <Theme Title>

**Status:** planned   <!-- planned | in progress | shipped <date> | superseded. If a spike invalidates this plan, mark it superseded and link the revised plan/section; do not keep two active paths. -->
**Theme:** <one sentence: what capability this slice delivers, with SPEC refs §N>
**Estimated effort:** <rough size, note if interruption slack included>
**Boundary:** <root orchestration plan | service-local implementation plan>
<!-- For monorepos/microservices: root plans own cross-service contracts,
rollout sequencing, and links to service-local plans. Service-local plans own
files/tests/migrations for that service and link back to the root plan. Do not
duplicate the same fact in both. -->

## Assumptions about current code (re-check after any interrupting release)
<!-- The drift guard. Read the code NOW and name the exact files/types/shapes
this plan depends on. In a reusable template, keep these as placeholders; in a
real repo, replace them with precise project-local names. Example shape:
"`<Controller>` owns a read-only `<View>` rebuilt per reload through
`<Builder>`." A reader must be able to compare your assumption against today's
code. After any patch release lands mid-plan, re-read this section and update
the plan instead of executing a stale design. -->

- `<File/Type>` currently <its exact shape / responsibility this plan relies on>.
- ...

## Goals / non-goals

Goals: <what this slice does>.
Non-goals (deferred): <what it explicitly does not do, and where it is deferred>.

---

## F1 — <Feature name>

### UX requirements
<!-- Observable behavior. What the user sees/does. Verifiable statements. -->
- ...

### Technical design
<!-- How. Name the exact types you will touch, the tradeoff, the number, and an
explicit fallback that still ships (SKILL.md §10.3). Keep examples synthetic in
shared templates.
  weak:   "Refresh the preview when data changes."
  strong: "`<PreviewController>` listens to `<DataStore>.changeEvents`, batches
           updates for 150 ms, and recomputes only affected `<RecordGroup>`
           nodes. Fallback if p95 exceeds 75 ms: full refresh behind a visible
           'updating' state, with telemetry proving the slow path." -->
- ...

### Acceptance
<!-- What proves it works: the manual matrix, the tests, the measurement. -->
- ...

---

## F2 — <Feature name>
<!-- same shape -->

---

## Work breakdown (each step = safe pause point)
<!-- Order so each completed step leaves the project shippable: builds, tests
pass, runs. Test: could you ship after step 2 and resume step 3 next week?
Every step names its verification. -->

1. <Step>. *Verify:* <how>.
2. <Step>. *Verify:* <how>.
3. ...
N. Release: run the versioning checklist (ENGINEERING §<n>); flip SPEC markers
   to shipped; update README scope; CHANGELOG entry; mark this plan shipped.

## Risks
<!-- What's most likely to go wrong + mitigation/fallback. Check common
categories: performance regression, compatibility/API breakage, data migration,
security/privacy exposure, rollout/rollback, accessibility, dependency/tooling
risk, and manual-verification gaps. The highest-risk item should have an
explicit fallback that still ships something. -->

- **<Risk category>: <risk>** — <mitigation or fallback>.
