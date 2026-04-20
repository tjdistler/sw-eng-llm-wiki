# MOC: Architecture Risk and Communication

**Summary**: Entry point for the part of the architect's job that doesn't fit on a diagram — surfacing risk, communicating designs, leading teams without authority, and growing the practice over a career. Start here when the question is about how to *land* an architectural decision in a real organisation, not how to make it on paper.

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You have an architecture and you need to make it survive contact with stakeholders, peer architects, developers, and the next quarter's roadmap. Or you've been asked to assess how risky a proposed design is. Or your decisions are being ignored, your diagrams are being misread, your reviews are turning into shouting matches.

This MOC is the soft-skills counterpart to [[moc-architecture-fundamentals]]. The fundamentals MOC tells you *how to think* about an architectural decision; this one tells you *how to surface its risk* and *how to make people hear you when you call it out*. It's the half of the architect's job that determines whether good designs ever ship.

The canonical shape of a question that lands here: *"How do I show that this design is riskier than people realise?"*, *"How do I diagram this without burying the decision in the sprawl?"*, *"How do I push back on a stakeholder who wants five-nines on a marketing site?"*, *"What does an architect actually do day to day if they want to grow the practice?"*

## Surfacing and quantifying risk

Risk is the architecture-fundamentals discussion (trade-offs, characteristics) cashed out as something concrete enough that a stakeholder can act on it. If you can't say "this dimension scores a 6 out of 9 risk because…", you don't yet have an architectural argument — you have an opinion.

- [[architecture-risk-matrix]] — Richards and Ford's 3×3 impact × likelihood grid (ratings 1–9; bands 1–2 / 3–4 / 6–9); the risk-assessment report with row totals (which characteristic is at risk) and column totals (which area of the system contributes); audience filtering (developers / managers / business sponsors all see different cuts of the same data); the *plus/minus* and *arrow-with-target* techniques for showing direction over time. Fitness functions are the signal feeding the directional indicators.
- [[risk-storming]] — Richards and Ford's collaborative session: silent individual phase (people commit before they hear the consensus), then consensus discussion, then mitigation. One *dimension* per session (availability one round, security the next) — never mix them or you lose the signal. The nurse-diagnostics three-session walkthrough is the worked example. Structurally parallel with [[event-storming]]: collaborative, time-boxed, surface-and-then-converge.

Use the matrix for the *artefact* — the thing stakeholders read. Use risk-storming for the *process* — the workshop that produces a non-political view of where the risk actually lives. The two are complementary; the matrix is the deliverable from a risk-storming session.

Deeper reading: [[fundamentals-of-software-architecture#chapter-20-analyzing-architecture-risk]].

## Communicating architecture — diagrams and presentations

Architecture that isn't legible is architecture that doesn't get followed. The diagramming and presentation skills are first-class engineering competencies, not optional polish.

### Diagramming

- [[architecture-diagramming]] — the diagramming soft skill: representational consistency as the load-bearing principle; the *Irrational Artifact Attachment* anti-pattern (you keep the polished version because polish was expensive, not because the design hasn't moved on); the low-fidelity-first discipline (sketches invite challenge; polished diagrams shut conversation down); the three standards (UML; C4's Context/Container/Component/Class; ArchiMate); the six diagram guidelines including the solid-vs-dotted line convention for synchronous vs asynchronous communication.

The single most useful guideline on the page: *low-fidelity until the decision is locked, high-fidelity only after*. Most diagram fights are caused by polished diagrams arriving before the underlying decision was made.

### Presentations

- [[architecture-presentation]] — the presenting soft skill: document-vs-presentation time control as the foundation (when *you* control the pace, the audience reads ahead and stops listening); transitions and animations as deliberate emphasis tools; the *Bullet-Riddled Corpse* anti-pattern (slides as printed handouts) and the *Cookie-Cutter* anti-pattern (every slide identical); the *Incremental Build* pattern that lets the audience focus where you focus; the infodecks-vs-presentations distinction; the two-channel (verbal + visual) model; *Invisibility* as deliberate emphasis (when *nothing* is on the slide, the audience listens to you).

Diagramming gets the design *into* people's heads. Presentation determines whether they remember it after they leave the room.

Deeper reading: [[fundamentals-of-software-architecture#chapter-21-diagramming-and-presenting-architecture]].

## Documenting decisions so they survive turnover

Risk and communication overlap heaviest at the moment a decision is made and someone has to record it. The ADR material lives mostly under [[moc-architecture-fundamentals]]; cross-referenced here because the *why-was-this-decided* answer is the highest-stakes communication artefact an architect produces.

- [[architecture-decision-record]] — Nygard's ADR template (Title / Status / Context / Decision / Consequences) plus Compliance and Notes; the RFC Status workflow that turns proposals into commitments; ADRs as documentation *and* as standards. The single best defence against the future team relitigating today's call.
- [[architecture-decision-anti-patterns]] — *Covering Your Assets* (no decision), *Groundhog Day* (no justification), *Email-Driven Architecture* (no single system of record). All three are communication failures dressed up as decision failures. ADRs are the cure.

For the deeper *what counts as architecturally significant* discussion, see [[architecture-decisions-vs-design-principles]] under [[moc-architecture-fundamentals]].

## Leading effectively without authority

The architect rarely has reporting authority over the developers building the system. Influence is the only lever; the leadership pages catalogue how to wield it.

- [[architect-control-spectrum]] — Richards and Ford's three architect personalities (control freak / armchair / effective) and the *elastic-leadership* five-factor dial (team familiarity, team size, experience, project complexity, project duration). The same architect should not lead the same way across all teams. The page also catalogues the three team warning signs — *process loss*, *pluralistic ignorance*, *diffusion of responsibility* — that signal a team has slipped under the surface even though nothing has audibly broken.
- [[architect-leadership-skills]] — the 4 C's of architecture (communication, collaboration, clarity, conciseness) as the antidote to architect-introduced accidental complexity; the pragmatic-yet-visionary balance; leading by example (not by title) with collaborative grammar and people-skills techniques; meeting control as the integration mechanism that determines whether a 1-hour design meeting produces a decision or another meeting.
- [[architect-providing-guidance]] — design-principle guidance as the alternative to prescription; the two-question library filter (overlap *and* technical-and-business justification) — the worked answer to *can I add this library?*; the Scala-enthusiast anecdote (the moment "yes, but" stops working); the three-category layered-stack demarcation (what the architect prescribes, what the team chooses, what is open). Most "the architects are blocking us" complaints come from missing this distinction.
- [[architect-negotiation]] — Chapter 23's negotiation techniques per counterparty: *stakeholders* (five-nines-to-seconds reframing, grammar, validate-before-redirect, divide-and-conquer, save-cost-for-last), *peer architects* (demonstration defeats discussion; calm leadership; never argue from authority), *developers* (justification before demand; let them arrive at the solution; the *Ivory Tower* anti-pattern). The single most under-used skill in the architect's toolbox.
- [[architectural-checklists]] — Gawande's *Checklist Manifesto* applied to release / unit-test / code-completion lists; when checklists work for architecture (high-stakes, high-coverage, infrequent procedures) and when they don't (creative design work); the Hawthorne effect as a governance mechanism. A communication artefact disguised as a process artefact.
- [[cross-site-project-recommendations]] — concrete guidance for leading projects whose contributors are split across geographic sites: milestone cadence, kickoff meetings, written communication discipline, timezone overlap rules. The field manual when the team you're influencing isn't in the same building.

Deeper reading: [[fundamentals-of-software-architecture#chapter-22-making-teams-effective]] and [[fundamentals-of-software-architecture#chapter-23-negotiation-and-leadership-skills]].

## Growing the practice over a career

Architecture is a long game. The practice you build over a decade compounds; the techniques you don't refresh decay into the *frozen caveman* anti-pattern named in [[technical-breadth-vs-depth]].

- [[architect-career-path]] — Chapter 24's career-long practice loop: the *20-minute rule* (learn something new every day, first thing in the morning, before email defeats your willpower); the personal *developer radar* (four quadrants × four rings adapted from ThoughtWorks, with *Hold* explicitly extended to cover habits to break — not just technologies to avoid); McAfee's weak-link argument for using social media to populate the *Assess* ring; architecture katas as deliberate practice; the closing motto — *always learn, always practice, and go do some architecture*.
- [[architecture-katas]] — Ted Neward's 45-minute team exercise drilling the characteristic-identification + design-defence loop; *Silicon Sandwiches* as the worked kata. The deliberate-practice format Chapter 24 invokes for keeping the trade-off muscle warm even when no real project demands it.

Deeper reading: [[fundamentals-of-software-architecture#chapter-24-developing-a-career-path]].

## Sibling MOCs

- [[moc-architecture-fundamentals]] — owns the *what to think* half of the architect's job (definition, characteristics, fitness functions, ADRs, evolution, trade-offs). This MOC owns the *how to surface and convey it* half. The two MOCs are paired; an architect's job is the union.
- [[moc-components-and-partitioning]] — owns the inside-the-box modularity material. Risk and communication frequently target component boundaries; the partitioning MOC supplies the substrate this MOC's risk arguments operate on.
- [[moc-architecture-styles]] — owns the catalogue. Diagramming, presentation, and risk all attach to specific architectural styles; this MOC supplies the soft-skills layer that decides whether a style is adopted, deprecated, or left to rot.
- [[moc-decomposition]] — owns the monolith-extraction playbook. The risk and communication discipline this MOC sets up is the gating force on whether a "let's extract this" conversation ever turns into an actual extraction.
- [[moc-microservices]] — owns the team-and-ownership view of running microservices. The architect-leadership and negotiation material here is the prerequisite skill for the cross-team co-ordination microservices unavoidably create.
- [[moc-reliability-and-operations]] — owns the SLO/SLI/error-budget posture. The five-nines-to-seconds reframing technique on [[architect-negotiation]] is the canonical bridge between "the business wants 100%" and "here is the cost of one more nine."

## Related pages

- [[index]]
- [[fundamentals-of-software-architecture]]
- [[architecture-risk-matrix]]
- [[risk-storming]]
- [[architecture-diagramming]]
- [[architecture-presentation]]
- [[architecture-decision-record]]
- [[architect-control-spectrum]]
- [[architect-leadership-skills]]
- [[architect-providing-guidance]]
- [[architect-negotiation]]
- [[architect-career-path]]
- [[architectural-checklists]]
