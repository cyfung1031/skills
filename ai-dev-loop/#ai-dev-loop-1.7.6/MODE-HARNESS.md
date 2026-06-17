# Mode Decision Table

Version: 1.7.6

Use the smallest mode that preserves source identity, role separation, evidence, validation-tier honesty, observability, auditability, compatibility, and same-session handoff.

| Mode | Use when | Minimum behavior | Escalate when |
|---|---|---|---|
| Minimal mode | Small safe task, known affected files, clear acceptance criteria | Load status/latest records, perform one grounded R or K turn, validate or cap claims, update status, hand off | Scope grows, files disagree, validation is uncertain, or package/release artifacts are touched |
| Standard loop | Normal repository change or review | Full R/K record discipline, whole-change scan, validation, status update | Release, benchmark, or contradiction risk appears |
| Review-only mode | User asks for critique without edits | Source-grounded findings, assumptions, validation plan, no file mutation | User requests implementation or terminal approval |
| Degraded mode | Git, commands, writes, credentials, network, or authority are unavailable | Record limitation, inspect safe sources, run static checks if possible, avoid live-success claims | Limitation blocks correctness, safety, or approval |
| Blocker mode | Missing authority, unsafe request, destructive risk, unresolved contradiction, or failed required validation | Stop broad edits, record blocker and safe partial path | R records accepted risk or user grants safe authority |
| Release mode | Package, benchmark, challenged-score, version, archive, manifest, installer, validator, schema, or example work | Whole-change package scan, manifest refresh, validator run, artifact hygiene, version consistency, release handoff | Any release gate fails |

## Release mode guardrail
Release mode requires whole-change impact scanning across docs, examples, scripts, validators, manifests, installers, fixtures, and release archives. Token efficiency cannot compensate for a failed production-critical gate.

## Simple versus full release path
Use minimal mode only when affected files and acceptance criteria are already clear. Escalate to release mode for package-wide version changes, manifest updates, validator changes, benchmark/scoring artifacts, release archives, or any contradiction between docs, scripts, schemas, examples, and metadata.
