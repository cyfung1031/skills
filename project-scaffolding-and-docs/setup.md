# One-time bootstrap checklist

Use this once when copying the templates into a real project. After this pass,
read the copied docs through the normal README → SPEC → ROADMAP → plan flow.

## 1. Copy templates to their target paths

```text
templates/readme.md       → README.md
templates/spec.md         → SPEC.md
templates/roadmap.md      → docs/ROADMAP.md
templates/release-plan.md → docs/plans/<version>-<theme>.md
templates/engineering.md  → docs/ENGINEERING.md
templates/changelog.md    → CHANGELOG.md
```

Optional — copy only if needed for larger projects or long-running decision history:

```text
templates/decisions.md    → docs/DECISIONS.md
```

If you use `docs/DECISIONS.md`, replace the decision-log section in `SPEC.md`
with a short pointer to that file. Keep one decision log, not two.

## 2. Create the directories before checking links

Create `docs/` and `docs/plans/` before opening the copied docs. The template
links intentionally point to the target project layout, not back into
`templates/`, so some relative links may look broken before this bootstrap copy
step is complete.

```bash
mkdir -p docs/plans docs/plans/archive
# Optional for disposable discovery notes referenced from the decision log:
# mkdir -p docs/spikes
# Optional once SPEC.md is split for a larger project:
# mkdir -p docs/specs
```

## 3. Fill the minimum viable set first

For a tiny prototype, start with only:

- `README.md` — pitch, status, quickstart, current scope.
- `SPEC.md` — observable requirements, out-of-scope, and a short decision log.
- `CHANGELOG.md` — dated record of what actually shipped.

Add `docs/ROADMAP.md`, `docs/plans/`, and `docs/ENGINEERING.md` when the project
has multiple planned releases, non-trivial implementation slices, or build/test
steps that a newcomer could get wrong. Add `docs/specs/` only when SPEC.md has
become too large or conflict-prone; keep SPEC.md as the router.

## 4. Run the cold-start read-through

Run this after the initial docs are filled, not before. Pretend you know nothing
about the project. Starting at `README.md`, verify that
you can answer:

1. What works today, and what is target design?
2. What is explicitly out of scope?
3. What is the next planned release and why is it next?
4. Which exact command builds/tests/runs the project?
5. Where are decisions recorded, and why do rejected alternatives matter?

Fix broken links, vague requirements, and duplicate facts before treating the
scaffold as ready.
