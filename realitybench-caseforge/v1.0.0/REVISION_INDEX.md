# RealityBench CaseForge v0.9.1–v0.9.10 Revision Index

Ten LLM-characteristic review passes applied after v0.9.0 and before v1.0.0.

- **v0.9.1 — LLM target identity map:** Adds explicit mapping of model type, interaction mode, context budget, tools, safety envelope, output contract, and judge/scorer dependency before case synthesis.
- **v0.9.2 — Prompt-sensitivity and instruction-conflict coverage:** Adds cases that distinguish robust task understanding from fragile compliance with surface phrasing, role conflicts, and hidden prompt leakage.
- **v0.9.3 — Stochasticity and variance controls:** Adds repeatability policy, acceptable answer bands, confidence intervals, and one-shot vs multi-run distinction for probabilistic model outputs.
- **v0.9.4 — Context-window and memory pressure:** Adds long-context, retrieval, truncation, recency/primacy, state carryover, and irrelevant-context resistance dimensions.
- **v0.9.5 — Hallucination and evidence discipline:** Adds explicit source attribution, abstention, uncertainty, quote fidelity, citation grounding, and fabricated-tool-output failure modes.
- **v0.9.6 — Tool-use and environment realism:** Adds tool call contract, side-effect safety, unavailable-tool behavior, stale external data handling, and tool-output reconciliation.
- **v0.9.7 — Multilingual, locale, and register robustness:** Adds language-code, script, locale convention, code-switching, cultural context, and translation-loss controls.
- **v0.9.8 — Judge/scorer reliability:** Adds rubric calibration, judge bias checks, oracle ambiguity audits, adversarial answer formatting, and score drift controls.
- **v0.9.9 — Safety, refusal, and boundary behavior:** Adds under-refusal, over-refusal, safe completion, privacy, policy ambiguity, and high-stakes uncertainty dimensions.
- **v0.9.10 — LLM suite release hardening:** Consolidates LLM characteristic coverage into release gates, matrices, diagnostic capture, and validity-weighted reporting.
