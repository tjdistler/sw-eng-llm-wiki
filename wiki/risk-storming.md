# Risk Storming

**Summary**: A collaborative exercise — run by an architect with other architects, senior developers, and tech leads — for identifying and mitigating risk in a specific architectural dimension (availability, performance, scalability, security, data loss, single points of failure, unproven technology). Structurally similar to [[event-storming]] in its silent-individual-then-consensus-then-action rhythm, but focused on architectural risk rather than domain modelling. Three activities: **identification**, **consensus**, **mitigation**.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-20-analyzing-architecture-risk.md`

**Last updated**: 2026-04-16 (Chapter 20 ingested)

---

## Why collaborative

Richards and Ford open the chapter's risk-storming section with the reason it exists:

> No architect can single-handedly determine the overall risk of a system. The reason for this is two-fold. First, a single architect might miss or overlook a risk area, and very few architects have full knowledge of every part of the system. (source: chapter-20-analyzing-architecture-risk.md)

The worked example in the chapter makes this concrete: three of the four risk discoveries in the example came from perspectives the architect running the session would have missed alone. A senior developer knew a specific technology kept falling over under load. Another participant didn't recognise a named technology at all (Redis), flagging it for a documentation gap the architect had been blind to. The fourth discovery required two participants to surface a perspective the rest of the room then adopted.

Risk storming exists because architecture risk is a **multiple-viewpoints** problem, not an analytical one.

## Who attends

The chapter's explicit guidance (source: chapter-20-analyzing-architecture-risk.md):

- **Multiple architects** — the core group.
- **Senior developers and tech leads** — they bring implementation perspective and, equally important, *gain* architectural understanding during the session. The Redis anecdote in the worked example shows this in both directions: the developer's non-recognition of Redis was itself valuable risk information, *and* the session educated them on a technology they would now recognise.

The architect running the session is responsible for making sure the architecture diagram is **up to date and available** to everyone. A holistic risk-storming effort uses a comprehensive diagram; a targeted effort on a specific area uses a contextual one.

## One dimension at a time (usually)

Risk storming targets a single dimension per session where possible — performance, or availability, or security, not a mix. Common dimensions (source: chapter-20-analyzing-architecture-risk.md):

- **Unproven technology** — new stacks, new versions, new patterns the team hasn't run in production.
- **Performance** — throughput, latency, response-time budgets.
- **Scalability** — ability to grow with load (including transitive dependencies).
- **Availability** — uptime, including transitive dependencies on third-party systems.
- **Data loss** — durability of writes, replication lag, backup strategy.
- **Single points of failure** — nodes, services, queues, shared infrastructure.
- **Security** — authentication, authorization, data exposure, regulatory compliance.

Running multiple dimensions in one session is permitted if staff availability forces it; the mitigation is to write the dimension on each Post-it note alongside the rating, so a "6" for performance doesn't get conflated with a "6" for availability on the same component. Restrict to a single dimension whenever possible.

## The three activities

### 1. Identification (individual, asynchronous)

The architect sends an invitation to all participants **one to two days before** the session (source: chapter-20-analyzing-architecture-risk.md). The invitation includes:

- The architecture diagram (or where to find it).
- The dimension being analysed.
- The date, time, and location of the consensus session.

Each participant then, **individually and without collaboration**, walks the diagram and rates areas of risk using the [[architecture-risk-matrix|risk matrix]]. They prepare small Post-it notes in the corresponding colour (green / yellow / red) with the risk number written on them, one note per area of identified risk.

The rule matters:

> This noncollaborative part of risk storming is essential so that participants don't influence or direct attention away from particular areas of the architecture. (source: chapter-20-analyzing-architecture-risk.md)

This is the same reason [[event-storming]] starts with silent individual brainstorm before any grouping happens: premature discussion converges the group on the first-stated opinion and loses the diverse viewpoints the exercise was designed to capture.

### 2. Consensus (collaborative, in-person-or-virtual)

Participants arrive at the session and place their Post-it notes on a large, printed architecture diagram (or the architect places them electronically onto a shared display from each participant in turn). The full set of annotations is then visible to everyone for the first time (source: chapter-20-analyzing-architecture-risk.md).

Three cases fall out of the aggregated annotations:

- **Unanimous agreement** — all participants found the same risk at the same level. No discussion needed; the rating stands.
- **Disagreement on level** — two participants rated a component medium, one rated it high (or vice versa). The outlier explains their reasoning; the group discusses; a consensus rating emerges.
- **One participant found risk others didn't** — typically the most valuable case. The originator explains; the rest of the room learns something. Sometimes the rating stands (a genuine risk others missed), sometimes it resolves (an unknown-technology rating becomes a documentation action).

The chapter's worked example walks through all three cases on a single architecture diagram: a load balancer where participants disagreed (consensus brought a 6 down to a 3); a Push Expansion Server one participant knew had operational history others didn't (the 9 stood); a Redis cache one participant rated 9 because they didn't know what Redis was (the "unknown technology" rule kept the 9 but the action shifted from mitigation to education).

This activity ends when every Post-it has been discussed and the room agrees on the rating.

### 3. Mitigation (collaborative, decision-making)

The final activity is the payoff. For every risk area the team agreed on, the question now is: **what do we do about it?**

> Mitigating risk within an architecture usually involves changes or enhancements to certain areas of the architecture that otherwise might have been deemed perfect the way they were. (source: chapter-20-analyzing-architecture-risk.md)

Changes range from architecture refactoring (adding a queue for back-pressure; splitting a database) to wholesale topology changes. Because mitigation costs money, this is also where **stakeholder negotiation** happens. The chapter's worked example:

1. A central database is rated medium (4) for availability risk.
2. The team proposes clustering + splitting into two physical databases. Cost: $20,000.
3. The business stakeholder says the cost doesn't outweigh the risk. Rejected.
4. The architect counter-proposes: skip the clustering, just split into two. Cost: $8,000. Most of the risk mitigated.
5. Stakeholder agrees.

Risk storming is therefore also a tool for architect-stakeholder conversations: the numeric rating replaces "I feel this might be a problem" with "this is a 6, here are three mitigation options at three price points."

Not every risk gets mitigated. The four standard responses to identified risk:

- **Mitigate** — change the architecture to reduce impact or likelihood.
- **Accept** — acknowledge the risk, document it, move on (for rare, low-impact events, or when cost outweighs benefit).
- **Transfer** — push the risk to a third party (insurance; SLA-backed managed service).
- **Avoid** — remove the risky component from the architecture entirely.

The mitigation activity is where the team (and stakeholders) choose among these for each identified risk.

## The nurse-diagnostics worked example

The chapter closes with a three-session walkthrough of a nurse-diagnostics call-centre system (source: chapter-20-analyzing-architecture-risk.md). The architect runs three risk-storming sessions, one per dimension, and the architecture changes significantly between the initial design (Figure 20-9) and the final one (Figure 20-13):

### Availability session

- Central database rated 6 (high). Mitigation: split into two databases — one clustered for the nurse profile data the call router depends on, one single-instance for case notes. Side benefit: also resolves a security boundary for case notes.
- Diagnostics engine rated 9 initially (unknown availability). Mitigation: the architect researched and published the vendor's 99.99% SLA on the diagram.
- Medical records exchange rated 2 (low). Not required for core flow; published SLA (99.9%) for reference.

### Elasticity session

- Diagnostics engine interface rated 9 — the engine handles only 500 req/s and flu-season spikes will exceed that. Mitigation layered three techniques:
  1. Asynchronous queues between API gateway and engine (back-pressure).
  2. Two queue channels for priority routing (the **Ambulance Pattern**) — nurses get priority over self-service patients.
  3. A new **Diagnostics Outbreak Cache Server** so flu questions never reach the diagnostics engine.
- Result: capacity ceiling effectively removed.

### Security session

- Diagnostics API gateway rated 6 (high). One gateway handles admin, self-service, and nurse traffic with in-gateway security checks. Risk: a bug or misconfiguration could let a self-service user reach the medical-records interface.
- Mitigation: split into three API gateways — one per user type — so admin and self-service *never share a code path* with the medical-records call. Structural prevention, not runtime enforcement.

The chapter's editorial point:

> Without a risk storming effort, this risk might not have been identified until an outbreak or flu season happened. (source: chapter-20-analyzing-architecture-risk.md)

The architect had reviewed the architecture "numerous times and believes it is ready for implementation" before the sessions started. Three sessions later the architecture was materially different and demonstrably more robust.

## Cadence

Risk storming is not one-off. Richards and Ford recommend it as continuous, with triggers (source: chapter-20-analyzing-architecture-risk.md):

- After a major feature is added.
- At the end of every iteration.
- After an architecture refactoring effort.
- When a new dimension of risk becomes relevant (e.g., a new regulatory requirement).

This makes risk storming one of the mechanisms of [[architecture-vitality]] — alongside [[architecture-fitness-function|fitness functions]] and ADR discipline, it keeps the architecture honest about what's actually in it.

## Relationship to adjacent wiki concepts

- [[event-storming]] — same silent-then-collaborative rhythm, different output. Event storming finds domain structure (aggregates, bounded contexts, components); risk storming finds architectural weak points. Both rely on the one-to-two-day asynchronous individual phase and on bringing multiple perspectives into the room.
- [[architecture-risk-matrix]] — the rating scale risk storming applies on each Post-it note; without it, the ratings are incomparable across participants.
- [[architecture-fitness-function|fitness functions]] — the continuous measurement that tells you whether mitigations are working and which risk cells are trending the wrong way. Risk storming identifies the risk; fitness functions track it over time.
- [[architecture-decision-record]] — the output of a mitigation decision is typically an ADR: the Context describes the risk the storming session identified, the Decision states the chosen mitigation, the Consequences acknowledge the residual risk and cost.
- [[architecture-vitality]] — risk storming is one of the concrete mechanisms for keeping the vitality property alive.
- [[unknown-unknowns]] — risk storming is the structured way to surface the knowable unknowns (someone in the room knows it) while accepting that true unknown unknowns will remain.
- [[reversible-vs-irreversible-decisions]] — mitigation choices are often themselves decisions with different reversibility profiles; the risk rating helps rank which deserve the higher-ceremony treatment.

## Related pages

- [[architecture-risk-matrix]]
- [[event-storming]]
- [[architecture-fitness-function]]
- [[architecture-decision-record]]
- [[architecture-vitality]]
- [[unknown-unknowns]]
- [[reversible-vs-irreversible-decisions]]
- [[architect-expectations]]
- [[architecture-governance]]
- [[fundamentals-of-software-architecture]]
