# A Mirror of My Becoming™ — Suite: Overseer™

The dispatcher that treats failure as the default condition.

An orchestrator for a local-first RAG archive: five workers (three vector collections, direct SQLite, and a canon-registry reader), reciprocal-rank fusion with a visible quorum table, an adaptive threat-level armor system (GREEN/ELEVATED/RED), checkpoint worker pairs, an advancing heartbeat, atomic state-file resume, and a tier system where the registry — never the model — answers factual questions.

## The failure doctrine

This was built on an 8GB Intel MacBook Air that fails definitely. Every mechanism exists because something actually failed: the model server wedged (600-second timeout), the model fabricated facts the pipeline had already answered correctly (the canon tier was the response), workers returned spam and empties (the quorum table exposed both). The architecture assumes death and receipts everything.

## Tiers

- **Canon tier** — counts, titles, dates, inventories: answered raw from the canonical registries (manifest.json, evidence.json). No model consulted. Zero hallucination surface.
- **Corpus tier** — meaning, history, synthesis: five workers retrieve, RRF fuses with visible quorum, a judge scores at ELEVATED+, the model composes *within* the evidence. NOT IN CORPUS governs.

## Armor

GREEN: fast path. ELEVATED: judge on. RED: full pairs, both servers. Levels are set by preflight from observed reality and re-earned every query.

## License

AGPL-3.0 for open use; commercial license available from the author.
© 2026 Evelyn Caro. All rights reserved. A Mirror of My Becoming™
