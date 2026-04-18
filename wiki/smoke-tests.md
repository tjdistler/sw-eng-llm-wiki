# Smoke Tests

**Summary**: The simplest kind of [[system-tests|system test]]: very simple but critical behaviours, exercised end-to-end. Smoke tests are sanity checks — they short-circuit more expensive testing when basic things are broken, and they're the **highest-impact-per-minute-of-engineering-time first test** to add to an untested codebase.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## The definition

> Smoke tests, in which engineers test very simple but critical behavior, are among the simplest type of system tests. Smoke tests are also known as sanity testing, and serve to short-circuit additional and more expensive testing. (source: chapter-17-testing-for-reliability.md)

The name comes from hardware bring-up: power it on, watch for smoke. A failed smoke test says "don't bother running the full suite, the basics are broken."

## The short-circuit role

Smoke tests live at the entry of the test pipeline for a reason. Running a multi-hour [[system-tests|full system test]] against a build that doesn't start is pure waste. The smoke suite is intentionally fast: if it fails, stop; if it passes, run everything else.

## Starting-point strategy

Chapter 17's advice to a team joining a prototype mid-development:

> It takes little effort to create a series of smoke tests to run for every release. This type of low-effort, high-impact first step can lead to highly tested, reliable software. (source: chapter-17-testing-for-reliability.md)

When coverage is zero or near-zero, the conversation often starts with "we need unit tests for every key function and class" — which the chapter calls *completely overwhelming*. Smoke tests are the tractable first step. See [[testing-entry-strategy]] for the full sequence.

## Cross-book connections

- [[synthetic-transactions]] (Newman) — synthetic transactions are production-side smoke tests: one critical end-to-end journey replayed continuously
- [[prober]] (Ch 10) — the Google tool that runs smoke-test-shaped probes against production

## Related pages

- [[system-tests]]
- [[testing-for-reliability]]
- [[testing-entry-strategy]]
- [[production-probes]]
- [[synthetic-transactions]]
