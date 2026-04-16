# When Microservices Are a Bad Idea

**Summary**: Newman's catalogue of situations where microservices are the wrong call: an unclear domain, true (pre-product/market-fit) startups, customer-installed software, and — above all — having no clear reason to adopt them.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

---

## Unclear domain

Getting service boundaries wrong is expensive: more cross-service changes, more coupling, sometimes worse than the [[monolith]] you started with (source: chapter-02-planning-a-migration.md).

Newman cites the SnapCI team at ThoughtWorks. Despite deep continuous-integration domain knowledge from their earlier Go-CD project, SnapCI's first take on service boundaries was wrong. After several months of high-cost cross-service changes, they merged everything back into a [[monolith]]. A year later, with a stable feature set and a firmer grasp of the domain, they re-decomposed — and *those* boundaries proved durable.

Lesson: if you don't yet understand the domain, decompose into microservices later, not now. Existing brownfield codebases are easier to decompose than greenfield products precisely because the domain is already understood.

## Startups (as distinct from scale-ups)

This is counter-intuitive — the famous microservices stories (Netflix, Airbnb) come from "startups" — but those companies adopted microservices only *after* finding product/market fit (source: chapter-02-planning-a-migration.md). Newman calls the post-fit phase "scale-up"; microservices solve the problems scale-ups have, not the problems startups have.

A real startup is small, underfunded, still searching for its product. The product domain itself is shifting, sometimes radically. Microservice boundaries laid down in this state will be wrong.

Brownfield decomposition is easier than greenfield microservice design because:

- You have running code to inspect.
- You can talk to the people who use and maintain it.
- You know what "good" looks like, so mistakes are detectable.
- You have a production performance baseline before any decomposition-induced regressions.

Newman's advice for startups that *do* adopt microservices: only split around boundaries that are clear at the start; keep everything else monolithic; and use the experience to assess your operational maturity. "If you struggle to manage two services, managing ten is going to be difficult."

## Customer-installed and managed software

If your product is shipped to customers who run it themselves, microservices are likely a bad fit (source: chapter-02-planning-a-migration.md). The migration pushes complexity into the operational domain, and your customers — unlike your own engineering team — won't have adopted new monitoring tools, distributed tracing, or container orchestration to compensate.

Customer-installed monoliths typically target a well-defined platform ("requires Windows 2016 Server", "needs macOS 10.12+"). Asking a customer to suddenly run 10–20 processes — or worse, a Kubernetes cluster — breaks the operational contract they bought into. Even customers with the skills may not have the *same* skills or platform you do (Kubernetes installs vary widely).

## Not having a good reason

The biggest reason not to adopt microservices: no clear idea of what you're trying to achieve (source: chapter-02-planning-a-migration.md). The desired outcome shapes both *where* you start the migration and *how* you decompose. Without it, you're fumbling in the dark.

"Doing microservices just because everyone else is doing it is a terrible idea."

## Related pages

- [[why-microservices]]
- [[microservices]]
- [[monolith]]
- [[modular-monolith]]
- [[bounded-context]]
- [[incremental-migration]]
