# Global vs Local Optimization

**Summary**: A standing tension in any organisation that delegates technical decisions to teams. Each team's locally-optimal choice (database, deployment process, language) can compose into globally-suboptimal duplication. The solution isn't to centralise — it's to build channels through which teams surface decisions that may benefit from a global view.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## The tension

Embracing [[team-autonomy|team autonomy]] — the model where teams own the full life cycle of their services — eventually produces decisions that look fine locally but bad globally (source: chapter-05-growing-pains.md).

Newman's worked example: three teams pick three different databases.

- The **Invoicing** team picks Oracle — they know it well.
- The **Notifications** team picks MongoDB — fits their programming model.
- The **Fulfillment** team picks PostgreSQL — they already have it.

Each individual decision makes sense. Stepping back: as an organisation, do you want to build skills, pay licence fees, and operate three databases with similar capabilities? Maybe one (imperfect for everyone, good enough for most) would be better. But without a way to *see* the local decisions in their global context, you can't even ask the question.

## When this hits

Newman places this problem later in the microservice journey (source: chapter-05-growing-pains.md):

- Early in adoption, teams share a clear understanding of "how things are done". Consistency is high, often by accident.
- Over time, each team optimises locally. The shared view drifts. Teams solve the same problem differently, and don't realise it.
- Periods of rapid hiring exacerbate this — informal information-sharing doesn't scale to a wave of new joiners. Information silos form.

The classic discovery moment is the lunchtime conversation: someone mentions a problem, someone else says "we built a tool for that six months ago." REA, the Australian real estate company, eventually realised every team had its own deployment approach — costly when people transferred between teams, hard to justify the duplication.

## Why pure central control isn't the answer

The temptation is to swing back to top-down standardisation. Newman warns this is the wrong move:

- Centralisation slows everything down. Every decision has to go through consensus.
- It undermines the autonomy that motivated microservices in the first place.
- It produces standards driven by central architects who don't know what each team actually needs.

The frame Newman uses: it's a balance, not a solved equation. Different organisations land in different places.

## Newman's mechanisms

### [[reversible-vs-irreversible-decisions]]

Re-introduced from Chapter 2. The higher the cost of changing a decision, the broader the consensus you should build before making it. The lower the cost, the more it can sit with the local team. (source: chapter-05-growing-pains.md)

Helping teams *recognise* where on the spectrum a decision sits is itself work. Teams need at least basic awareness of bigger-picture concerns to know when to pull others in.

### A cross-cutting technical group

A simple structure (source: chapter-05-growing-pains.md): one technical leader from each team participates in a cross-cutting group, often chaired by a CTO or chief architect. The group:

- Provides a forum where teams can surface decisions that may have global impact.
- Surfaces *cross-cutting* problems back to teams ("we've noticed three of you are solving X differently").
- Builds awareness of what other teams are doing without forcing top-down standardisation.

### Free-form proposals (Monzo)

Monzo's example: anyone can submit a free-form **proposal**, published in a shared space and broadcast to the company via Slack. Interested parties discuss and refine it. Proposals are not finished products — they're explicitly open to change. This works because Monzo's culture is set up for this kind of distributed sharing.

Newman is careful to note this depends on the culture. Don't import the mechanism without the culture that makes it work.

## The deeper trade-off

> "The more responsibility you push to the teams, the more you'll get the benefits of greater autonomy, but the trade-off is that you may have less consistency in how problems are solved. The more you drive things from the center, the more you'll need to build consensus and that will likely slow you down." (source: chapter-05-growing-pains.md)

Newman explicitly refuses to prescribe a balance: each organisation has to find its own. The job is to be *aware* the balance exists and to gather enough information to adjust it over time.

## Connection to ownership models

[[code-ownership-models|Collective ownership]] reduces this problem somewhat — the consistency required for collective ownership to work means you've already had to standardise. [[code-ownership-models|Strong ownership]] amplifies the problem because each team's local optimisation runs unchecked. Newman explicitly says: if you want collective ownership at scale, you have to solve global-vs-local; otherwise collective ownership won't scale.

## Related pages

- [[team-autonomy]]
- [[reversible-vs-irreversible-decisions]]
- [[reorganizing-teams]]
- [[code-ownership-models]]
- [[conways-law]]
