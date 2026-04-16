# Skills Self-Assessment

**Summary**: A practical technique Newman uses for assessing which skills a team needs and how individuals want to grow into them. Each developer rates themselves privately against a list of relevant skills; the anonymised aggregate informs team-level investments.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

---

## The technique

From a project Newman worked on at ThoughtWorks helping The Guardian rebuild its online presence (source: chapter-02-planning-a-migration.md):

1. **Agree the list of core skills** important for the work ahead. (For The Guardian, it included a new programming language and associated technologies.)
2. **Each developer self-assesses** on each skill, scoring 1 ("This means nothing to me") to 5 ("I could write a book about this").
3. **Each individual's score is private**, shared only with the person mentoring them. Each person sets *their own* targets — the goal is not for everyone to reach 5 on everything.
4. **The mentor's job** is to make sure individuals get the chance to grow toward their targets — assigning relevant stories, recommending videos, suggesting training courses or conferences.
5. **Aggregate the anonymised data** into a team-level skill map.

## Why scores must stay private

Public scores break the technique (source: chapter-02-planning-a-migration.md). Suddenly people are worried about how their score affects performance reviews and start gaming. The point is honest self-direction; that requires safety.

## What the aggregate is for

Even though individual scores are private, the *anonymised* aggregate is useful at team level. Newman's example: an individual is happy with their PACT testing skill (no need to grow), but the team-level aggregate shows PACT is broadly weak — and Kafka and Kubernetes even weaker. That signal might justify:

- Group learning sessions.
- An internal training course.
- Bringing in a hire who already has the skill.

Sharing the team-level picture also lets individuals see how their growth might serve the team's needs.

## Hiring as an alternative to growing

Newman explicitly notes that changing the team's skill set doesn't always mean upskilling existing members (source: chapter-02-planning-a-migration.md). Sometimes the right answer is to hire someone with the needed expertise — who then becomes the in-team coach for everyone else. This is faster for the short-term need *and* compounds over time.

## Why this matters for microservice migration

A move to microservices typically demands skills the existing team doesn't have: container orchestration, observability tooling, distributed tracing, on-call for distributed systems, asynchronous messaging, [[change-data-capture]], etc. [[reorganizing-teams|Reorganising teams]] to take on these responsibilities without first assessing the skills gap is the road to burnout and quitting. The self-assessment makes the gap visible before it becomes a crisis.

## Related pages

- [[reorganizing-teams]]
- [[team-autonomy]]
- [[kotters-change-model]]
- [[microservices]]
