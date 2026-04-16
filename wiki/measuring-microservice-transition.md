# Measuring a Microservice Transition

**Summary**: How to know whether a microservice migration is working. Newman's approach: define quantitative metrics tied to your stated goals, supplement with qualitative feedback from the team, and run regular checkpoints with the explicit option to change course.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

---

## You need to know

Even with the best intentions, the transition you start may not be the one you should finish. The questions to ask along the way (source: chapter-02-planning-a-migration.md):

- Is it working?
- Have we made a mistake?
- Should we try something else instead?

Without measures, these questions become opinion contests. With measures, you have evidence.

## Regular checkpoints

Build pause-and-reflect time into the delivery process. For small teams this can be informal — folded into a regular retrospective. For larger programmes, plan explicit monthly reviews with leadership across the relevant activities (source: chapter-02-planning-a-migration.md).

At each checkpoint, cover:

1. **Restate the goal.** What is this transition supposed to achieve? If the business has changed direction so the goal no longer makes sense, **stop**.
2. **Review quantitative measures.** Are we making progress on what we said we'd improve?
3. **Ask for qualitative feedback.** Do the people doing the work think it's working?
4. **Decide what, if anything, to change.**

## Quantitative measures

Pick metrics that match the goal:

- **Time to market**: cycle time, number of deployments, change failure rate.
- **Scaling for load**: results from the latest performance tests.
- **Robustness**: incident frequency, mean time to recovery, blast radius of incidents.

Two warnings (source: chapter-02-planning-a-migration.md):

1. **You get what you measure.** Newman's wife told him about a vendor paid per ticket closed — they closed unresolved tickets and made customers open new ones. Metrics get gamed, sometimes inadvertently.
2. **Some metrics get worse before they get better.** Cycle time will likely *regress* in the first few months of a microservice transition as the team comes up to speed with new tooling and patterns. Don't panic. (Also: another reason to take small steps — small changes produce small short-term regressions.)

## Qualitative measures

> "…software is made of feelings." — Astrid Atkinson (source: chapter-02-planning-a-migration.md)

Whatever the data shows, people build the software. Newman's qualitative checks include:

- Are they enjoying the process?
- Do they feel empowered?
- Are they overwhelmed?
- Are they getting the support they need to take on new responsibilities and master new skills?

When reporting transition status up to senior leadership, include the qualitative sense-check. Ignoring what the team is telling you in favour of clean numbers is "a great way to get yourself into a lot of trouble".

## Avoiding the sunk cost fallacy

Sunk cost fallacy: the more you've invested in an approach, the harder it becomes to abandon it even when evidence says you should. Newman calls this the "Concorde fallacy" — the British/French supersonic passenger jet that consumed enormous public investment despite evidence it would never be commercially viable (source: chapter-02-planning-a-migration.md).

The bigger the bet and the louder the fanfare, the harder it is to back out. Defences against this:

- **Small steps** (see [[incremental-migration]]) so each individual investment is small.
- **Explicit checkpoints** so reflection is scheduled, not avoided.
- **Quantitative AND qualitative evidence** so the conversation has data behind it.
- **Permission to revert.** Build a culture where pulling back is a normal move, not a defeat.

## Being open to new approaches

> "If you try to embrace a culture of constant improvement, to always have something new you're trying, then it becomes much more natural to change direction when needed." (source: chapter-02-planning-a-migration.md)

The opposite anti-pattern: ghettoising change into discrete one-off transformation programmes. Once "the microservices project" finishes, change stops — and the next pressure to evolve gets resisted. Treat improvement as continuous, not transactional.

## Related pages

- [[why-microservices]]
- [[incremental-migration]]
- [[kotters-change-model]]
- [[reorganizing-teams]]
