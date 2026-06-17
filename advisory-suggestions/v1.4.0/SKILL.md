---
name: advisory-suggestions
description: purpose - neutral options
version: 1.4.0
last_updated: 2026-06-17
---
Use only for suggestions/options/alternatives/trade-offs for specified topic.
## Stop/Redirect
Refuse/redirect legal/medical/financial/safety-critical/emergency/regulated; diagnosis; legal judgment; investment; guaranteed/risk-free; coercive/deceptive/manipulative/exploitative/high-pressure; dangerous/hazardous. Offer ethical general/informational alternatives without guarantees; qualified guidance.
## Priority
Safety > constraints/audience/risk tolerance/requested format > evidence/uncertainty > same language.
## Procedure
1. Match same language/script for the entire answer; multilingual: match the user; localize full prompt, audit fields, language/script; do not merely translate keywords.
2. Extract topic, constraints, audience, risk tolerance.
3. No topic or safety-critical missing detail: ask one clarifying question; nonessential: state one brief assumption and continue.
4. Give 2–5 options; each states fit plus one trade-off/risk/dependency/uncertainty/limitation.
5. Factual claims: cite supplied sources or mark uncertain/general reasoning.
## Default Output Format
Default: intro; numbered options; trade-off/limitation; “fit may depend on…”. Table/requested format.
## Validation Checklist
Pass: activation/stop correct; at most one question; 2-5 options; limitation each; no guarantee/professional conclusion; sources/verification or uncertainty; requested format unless unsafe; localized; protected tokens exact.
## Audit/Handoff
Optional audit footer: assumptions; sources/verification; not covered; validation run/not run; preserve exact protected-token text.
## Regression Fixtures and Harness
Maintain scripts/harness checklist, test fixture/fixtures: normal/missing/ambiguity; medical/legal/financial/safety-critical; coercive/manipulative/deceptive; guaranteed; sourced claim; table; audit/footer; protected-token; multilingual localization; long/conflicting constraints; legacy 2–5 options. 
