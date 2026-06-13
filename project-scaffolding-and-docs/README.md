# Project Scaffolding & Documentation Skill

A generic, LLM-agnostic methodology for scaffolding a software project's
structure and keeping its documentation alive: repo layout, how to write a
spec, how to derive a roadmap, how to write cold-start-executable
implementation plans, how to update docs during implementation, and how to keep
durable change and decision records.

It is principle-based and tool-neutral: plain Markdown, no dependency on any
specific agent, framework, language, or private repository. The examples are
synthetic and sanitized so the skill can be shared without exposing product
names, file paths, customer details, internal architecture, or project history.

## Contents

- **[SKILL.md](SKILL.md)** — the methodology. Read this first. Nine core
  principles, the six-document system, and the workflows: write a spec → derive
  a roadmap → write a plan → execute while keeping docs in sync → record
  decisions → release/interrupt.
- **[templates/](templates/)** — fill-in-the-blank starting points, each with
  inline guidance comments:
  - [readme.md](templates/readme.md)
  - [spec.md](templates/spec.md) — includes the default decision-log section
  - [decisions.md](templates/decisions.md) — optional standalone decision log for larger projects
  - [roadmap.md](templates/roadmap.md)
  - [release-plan.md](templates/release-plan.md)
  - [engineering.md](templates/engineering.md)
  - [changelog.md](templates/changelog.md)

Template links assume each template has been copied to its target path in a
project repository. Some links may intentionally be broken while files remain
inside `templates/`. For a first-time setup, use [setup.md](setup.md) as the
one-time bootstrap checklist before reading the copied project docs as if you
were a newcomer.

## How to use it

0. **Run the one-time bootstrap checklist in [setup.md](setup.md).** It creates the expected target layout before template links are checked.
1. Read `SKILL.md` end to end.
2. New project: copy the templates into place, fill `SPEC.md` first
   (positioning → principles → features → out-of-scope → tech), then derive the
   roadmap, then write the first plan. After the initial docs are filled, run the cold-start read-through in `setup.md` as a newcomer would.
3. Existing project: use SKILL.md §8 as an audit checklist. Most projects are
   missing at least one of: a decision log, an explicit out-of-scope list, or
   shipped-vs-target markers.
4. During implementation, treat SKILL.md §4.3 as the rule that keeps docs
   honest: a behavior change and its doc change are one unit of work.
5. Before calling any document done, run the matching checklist in SKILL.md §10.
   Filling every section is the floor; §10 is the quality bar: numbers instead
   of vague adjectives, decisions with rejected alternatives and named fixtures,
   and plans that name exact files/types, risks, and fallback paths.

## Privacy and portability

This package intentionally contains no private project details. When adapting
it from an existing repository, replace concrete names, file paths, corpus
sizes, user reports, screenshots, and implementation classes with either:

- placeholders such as `<module>`, `<case-name>`, and `<measurement>`; or
- synthetic examples that preserve the lesson without identifying the source
  project.

Do not paste private release notes, customer cases, proprietary architecture,
or exact regression fixtures into a reusable skill package.
