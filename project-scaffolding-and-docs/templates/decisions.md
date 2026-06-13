<!--
TEMPLATE: DECISIONS.md — optional standalone decision log for larger projects.
Copy to docs/DECISIONS.md only when the SPEC.md decision log gets large enough
to interrupt spec readability. Keep one decision log, not two: SPEC.md should
then link here. When migrating, update cross-references that pointed at SPEC.md
decision anchors. When plans move to docs/plans/archive/, update decision links
that pointed into the old active path. Delete guidance comments.
See SKILL.md §5 and §10.2.
-->

# Decision Log

Append-only record of non-obvious product and engineering choices. The changelog
says what shipped; this file says why choices were made and which alternatives
were rejected.

## Entry format

──────────────────────────────────────────────────────────────────────────────
ENTRY FORMAT — every active entry below must include trigger, root cause,
chosen option, rejected alternative and cost accepted, enforcement/tests, and
measurements or named fixtures when applicable. Missing rejected alternatives
fails the §10 audit.
──────────────────────────────────────────────────────────────────────────────

1. **<Decision in a sentence> (<ver/date>)** — <trigger: report / measurement /
   constraint>. <root cause; structural or cosmetic?>. Chose <option> because
   <reason>. Rejected <alternative> because <cost accepted>. Enforced by
   <test/manual pass/fixture>. Measurement or fixture: `case-renamed-field` /
   `unrelated pairings 867 → 522`.
2. ...

## Superseded decisions

Do not edit old entries to make history look cleaner. Add a new entry that
references the old number and explains why conditions changed.
