# Reorganizing Teams

**Summary**: Aligning team structure with a microservice architecture means moving away from competency silos (Java team, DBA team, ops team) toward end-to-end product teams. Newman's advice: don't copy other companies' structures; map your current state, decide where you want to go, and shift incrementally.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

---

## The historical pattern

IT was historically structured around core competency (source: chapter-02-planning-a-migration.md):

- Java developers in one team.
- Testers in another.
- DBAs in a third.
- Operations in a fourth.

Software delivery required hand-offs between them: BA → developers → testers → ops. By [[conways-law]], the architectures these organisations produced mirrored that structure — three-tier architectures with specialist teams owning each tier.

## The shift

Silos have been breaking down. Dedicated test teams are increasingly history; test specialists are embedded in delivery teams. The DevOps movement has pushed operational responsibility from centralised ops into delivery teams. Where centralised teams remain, their role has shifted from *doing* the work to *enabling* the work — embedding specialists, building self-service tooling, providing training (source: chapter-02-planning-a-migration.md).

The end state Newman describes: independent, autonomous teams responsible for end-to-end delivery, organised around areas of the *product* rather than around technologies or activities. This mirrors microservices' shift from technical-layer slicing to vertical slices of business capability.

## Don't copy the Spotify model

Newman is direct about this (source: chapter-02-planning-a-migration.md): the 2012 Kniberg/Ivarsson paper "Scaling Agile @ Spotify" popularised "Squads, Chapters, and Guilds" — terms Spotify itself never used as a "model". Companies adopted "the Spotify model" without considering that:

- Spotify is a Swedish music-streaming company, not (e.g.) an investment bank.
- The paper was a 2012 snapshot; even Spotify doesn't work that way anymore.
- Organisational structures emerge from a specific business model, culture, and customer base.

> "Copy the questions, not the answers." — Jessica Kerr (source: chapter-02-planning-a-migration.md)

The questions worth copying: what problems were they solving? What did they try? What was the *attitude* toward organisational design? The specific answers are unlikely to transfer.

## DevOps doesn't mean NoOps

A common misreading: that DevOps means developers do all the operations and there are no operations specialists (source: chapter-02-planning-a-migration.md). DevOps is a cultural movement about breaking down barriers between dev and ops. You may still want specialists — what you want is *common alignment and understanding* across everyone who delivers software.

Newman recommends *Team Topologies* (Pais & Skelton) and *The DevOps Handbook* (Kim, Humble & Debois) for deeper treatments.

## A practical approach: as-is, then to-be

Newman's recommended starting point (source: chapter-02-planning-a-migration.md):

1. **List all the activities and responsibilities** involved in delivering software in your company.
2. **Map them to the existing organisational structure** ("as-is"). If you've modelled your path to production, overlay ownership boundaries on it.
3. **Brainstorm with stakeholders from all the roles** to make sure nothing's missed. Siloed orgs struggle to even know what other silos do.
4. **Be honest about the current state.** Some teams may already do a lot for themselves; others are entirely dependent on other teams for testing or deployment. The starting line is not the same everywhere.
5. **Redraw with your vision** for how things should be in the future, on a sensible timescale (Newman suggests six months to a year).
6. **Identify the moves**: what responsibilities change hands? What new skills do teams need? What is the priority order?
7. **Take it incrementally.** Each change is its own piece of work, with its own enablement (training, hires, embeds).

A worked example from Newman: merge frontend and backend team responsibilities; have ops provide a self-service test environment platform; let delivery teams handle their own test deployments now and incidents during working hours soon, with ops coaching, before eventually owning 24/7 support.

## The pager-flip warning

Newman gives a specific anti-pattern: the bold pronouncement "Right, now you all need to deploy your software and run 24/7 support." For developers used to 9–5 work and no on-call exposure, this is "a great way to alienate your staff and lose a lot of people" (source: chapter-02-planning-a-migration.md). State it as an aspiration. Build the journey. Train people, embed ops engineers in delivery teams, and let the change land in pieces.

## Connection to skills

Reorganising responsibility implies changing the skills present in each team. See [[skills-self-assessment]] for Newman's recommended approach.

## Related pages

- [[conways-law]]
- [[team-autonomy]]
- [[skills-self-assessment]]
- [[kotters-change-model]]
- [[microservices]]
- [[independent-deployability]]
