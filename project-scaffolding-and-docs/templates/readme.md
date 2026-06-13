<!--
TEMPLATE: README.md — the front door. Shortest path from "never seen this" to
"building/using it." Everything deep is a LINK, not a copy. Delete guidance
comments. See SKILL.md §2.1.
-->

# <Product>

<One-paragraph pitch. Link to SPEC.md for the full specification.>

**Status: v<version> — <maturity, e.g. internal preview>.** <One line on what
works end-to-end; pointer to "current scope" below and CHANGELOG for history.>

Project documentation:

- [SPEC.md](SPEC.md) — product & technical specification
- [docs/ROADMAP.md](docs/ROADMAP.md) — release train + versioning/interruption
  policy
- [docs/plans/](docs/plans/) — one detailed, executable plan per release
- [docs/ENGINEERING.md](docs/ENGINEERING.md) — build/test reality, conventions,
  release checklist
- [CHANGELOG.md](CHANGELOG.md) — what each release shipped

## Building

```sh
<quickstart build/run/test commands>
```

<Any one critical gotcha; defer the rest to ENGINEERING.md.>

## Layout

```
<short directory map matching the module boundaries SPEC declares>
```

## Current scope (v<version>)

Working: <comma-separated list of what works now>.

Deferred — scheduled across the release plans in
[docs/ROADMAP.md](docs/ROADMAP.md): <what's not built yet, with the release
each item is scheduled for>.
## Project policies

License: <license or "not yet chosen">.
Contributing: <link to CONTRIBUTING.md or contribution policy, if public>.
Security: <link to SECURITY.md or vulnerability reporting path, if public>.

