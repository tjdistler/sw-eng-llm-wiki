# Wiki Log

Append-only record of all operations.

---

## 2026-04-19 — Wiki redesign Phase 1: per-book H2 chapter renames

Renamed per-book summary H2 chapter headings to `## Chapter N: <Full Chapter Title>` so `[[book-name#chapter-N-title]]` wikilink anchors resolve via the linter's slug match. Prerequisite for MOCs introduced in later phases.

Files touched:

- `wiki/monolith-to-microservices.md` — 5 H2s (`## Chapter N concepts` → titled)
- `wiki/designing-data-intensive-applications.md` — 12 H2s
- `wiki/designing-distributed-systems.md` — 11 H2s (Chapters 2–12)
- `wiki/fundamentals-of-software-architecture.md` — 24 H2s
- `wiki/fundamentals-of-data-engineering.md` — 11 H2s (em-dash → colon; slugs unchanged but form normalised)
- `wiki/site-reliability-engineering.md` — 34 chapter H2s converted from `## <Topic> (Chapter N)` to `## Chapter N: <Title>`; two additional Chapter 1 H2s demoted to H3 subsections
- `wiki/building-event-driven-microservices.md` — 15 chapter H2/H3 headings converted; `## Foundations (Chapters 1–2)` split into Chapter 1 and Chapter 2 H2s; `## Microservice implementation styles (Chapters 9–12)` umbrella retained with chapter H3s retitled
- `wiki/software-architecture-the-hard-parts.md` — no per-chapter H2 sections exist; unchanged

Linter green (0 errors; 1 pre-existing warning unrelated to this change).
