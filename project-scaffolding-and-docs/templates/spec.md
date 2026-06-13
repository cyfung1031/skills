<!--
TEMPLATE: SPEC.md — the living "what & why" anchor document.
Delete every guidance comment as you fill it in.
Principles this template enforces (see SKILL.md): one fact one home,
target-vs-reality marked explicitly, decisions recorded with reasoning,
out-of-scope written down. Keep the decision log here by default; if it grows
large, move it whole to docs/DECISIONS.md and link to it.
-->

# <Product> — Product & Technical Specification

**Version:** <doc version, e.g. 1.0>
**Date:** <YYYY-MM-DD> (originally <YYYY-MM-DD>)
**Status:** Living specification.
<!-- State the shipped-vs-target convention here so the reader trusts the doc:
e.g. "Where this says 'shipped (0.1.x)' the behavior exists today; everything
else is target design. Older shipped markers are normalized at major/stable
releases so only live target-vs-shipped deltas stay marked. Release plans:
docs/ROADMAP.md. Build reality: docs/ENGINEERING.md. What shipped:
CHANGELOG.md." -->

<One-paragraph statement of what the product is.>

---

## Part I — Product Specification

### 1. Positioning
<!-- A small table forces clarity. If you can't fill this, don't spec features yet. -->

| | |
|---|---|
| **Product** | <one line> |
| **Competes with** | <alternatives and their weaknesses> |
| **Wedge** | <why this wins> |
| **Users** | <primary, then secondary> |
| **Business model** | <if relevant> |

### 2. Core principles
<!-- The non-negotiables. Every later decision cites these as tie-breakers. -->

1. **<Principle>.** <one-line consequence>
2. ...

### 3. Feature set
<!-- Behavior the reader could VERIFY, not implementation. Tables for
enumerable facts; prose for behavior. Tag shipped behavior inline, e.g.
"*Shipped (0.1.x).*", to distinguish reality from target.
QUALITY BAR (SKILL.md §9, §10.2): every requirement is OBSERVABLE — a check
could pass or fail on it. Numbers carry units; no bare "fast"/"efficient".
  weak:   "Import is fast and handles large files well."
  strong: "Importing a 1 MB sample file completes in < 150 ms (CI-enforced);
           input streams in 64 KB chunks; a record type repeating > 64× falls
           back to grouped processing flagged 'approximate'." -->

#### 3.1 <Capability>
- ...

### 4. Out of scope for v1.0 (explicit)
<!-- The boundary is a feature. List what you are deliberately NOT doing and
where (if anywhere) it's a candidate later. -->

<item> · <item> · <item>. (Candidates for later — see §<roadmap>.)

---

## Part II — UX / UI Specification

### 5. Information architecture
<!-- Layout, navigation model, the windows/screens and how they relate.
If this UX spec grows large or has separate owners, move it wholesale to
docs/specs/ux.md and leave a pointer here; do not maintain two copies. -->

### 6. <Interaction details> (keyboard, gestures, defaults)

### 7. Accessibility (release-blocking, not best-effort)
<!-- State the bar as a requirement, not an aspiration. -->

---

## Part III — Technical Specification

### 8. Build system
<!-- How it's built at the highest level. If this technical spec grows large,
split it wholesale into docs/specs/technical.md and keep this section as a
pointer/summary only. If reality diverges from the ideal
(a workaround, a not-yet-built piece), add a "shipped reality" callout: -->

> **Shipped reality (<ver>):** <what actually happens today and why it
> diverges from the design above>. Details: docs/ENGINEERING.md §<n>.

```
<directory / module layout the codebase should match>
```

### 9. Architecture (process / concurrency / data flow)

### 10. Resource budgets
<!-- Numbers, and which are enforced vs aspirational. -->

| Concern | Mechanism / budget |
|---|---|
| Memory | Peak RSS < <150 MB> for `case-nested-block` (CI-enforced / aspirational) |
| Input size | Stream in <64 KB> chunks; never materialize `<large artifact>` as one string |
| Fallback | Inputs over `<limit>` use `<coarse mode>` and show `<approximate marker>` |
| Telemetry / monitoring | <event/counter name, sampling rule, retention/privacy note, and dashboard/alert if applicable> |

### 11. Module specifications
<!-- Per module: single responsibility + public surface. This is the contract
between modules and the map an implementer follows. -->

#### 11.1 `<Module>` (<one-line responsibility>)
- Public interface: <key types/functions>
- Invariants / tests that must hold: <e.g. round-trip property>

### 12. Performance budgets (mark which are enforced)

| Scenario | Budget |
|---|---|
| First useful result for `case-renamed-field` | <150 ms p95 on CI hardware> (CI-enforced) |
| Refresh after `<common edit>` | <75 ms p95> (manual/telemetry until automated) |
| `<rare heavy workflow>` | <2 s> with visible progress and cancel affordance |

### 13. Error handling & edge cases (selected, normative)
<!-- The nasty cases and the REQUIRED behavior. Not exhaustive — pin the ones
that matter. -->

- <condition> → <required behavior>.

### 14. Distribution, signing, updates
<!-- How it ships to users. -->

### 15. Roadmap
<!-- Just a pointer + summary table. Detail lives in docs/ROADMAP.md and
docs/plans/. Don't duplicate. -->

Release plans live in **docs/ROADMAP.md** and `docs/plans/`. Summary:

| Release | Theme |
|---|---|
| <ver> | <theme> |

### 16. Testing strategy
<!-- Kinds of tests, the fixture corpus, what's automated vs manual. -->

### 17. Key decisions & their reasoning (decision log)
<!-- THE most valuable section for long-term maintenance. Append-only, numbered.
If this section grows large, move it wholesale to docs/DECISIONS.md, leave only
the stub below, and update cross-references that pointed at SPEC.md decision
numbers/anchors. Do not split the log.

──────────────────────────────────────────────────────────────────────────────
MOVED-LOG STUB — keep this visible here if the decision log is migrated:

<!-- CRITICAL: Delete the placeholder list items below when pasting this stub.
A file containing active entries below this line fails §10 audit checks. -->

> **Decision log moved:** use [docs/DECISIONS.md](docs/DECISIONS.md) as the
> single source of truth. Do not add new decision entries here.
──────────────────────────────────────────────────────────────────────────────

Each entry MUST have (SKILL.md §5, §10.2): the trigger (user report /
measurement / constraint), the root cause AND whether it was structural or
cosmetic, what was chosen, what was REJECTED and the cost accepted, where it's
enforced, and — when a measurement or real input drove it — the numbers and the
NAMED regression fixture. Missing the rejected alternative ⇒ it's a fact, not a
decision. When a later decision overrides an earlier one, add a new entry
referencing the old number — never silently edit history.

  weak:   "17. Improved matching (0.1.8) — items paired wrong; switched to a
           similarity match; works better now."
  strong: "17. Similarity pairing inside changed regions (0.1.8) — anonymized
           reports showed renamed records rendering as removed+added items.
           Root cause structural, not cosmetic: rows paired by position, so one
           inserted row shifted later pairs off by one. Replaced with monotonic
           max-similarity matching (Dice ≥ 0.3, DP cap 65,536); both-sided gaps
           stay one positional replace so genuine rewrites keep compact
           rendering — rejected re-segmenting every region because it degraded
           the common unrelated-rewrite case. Fixtures: case-renamed-field,
           case-inserted-row. Anonymized corpus: unrelated pairings 867 → 522." -->

1. **<Decision in a sentence> (<ver/date>)** — <trigger>. <root cause; structural
   or cosmetic?>. <chosen option; REJECTED alternative; cost accepted>. <where
   enforced/tested>. <measured impact + named fixture, if any>.
2. ...
