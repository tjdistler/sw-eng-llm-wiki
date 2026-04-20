# Cross-Site Project Recommendations

**Summary**: Chapter 31's explicit list of recommendations for running engineering projects across sites — distilled from the dashboard-consolidation retrospective. Start from: only go cross-site when you have to, but recognise there often *are* good reasons to have to. The operating principles are divide-and-conquer decomposition, written-first communication to offset distance, standardisation as an ongoing activity, and in-person time concentrated on project leaders and occasional team summits.

**Sources**: `raw/site-reliability-engineering/chapter-31-communication-and-collaboration-in-sre.md`

**Last updated**: 2026-04-17

---

## When to go cross-site

Only when you have to — but *"often there are good reasons to have to"* (source: chapter-31-communication-and-collaboration-in-sre.md).

- **Costs**: higher latency for actions; more communication required.
- **Benefits** (when you get the mechanics right): much higher throughput.
- **Single-site risks** exist too: *"no one outside of that site knowing what you're doing."*

Both approaches have costs; the question is which costs you can afford to pay.

## Pick your contributors carefully

Motivated contributors are valuable, but **not all contributions are equally valuable** (source: chapter-31-communication-and-collaboration-in-sre.md). Watch for:

- Contributors chasing *"a notch on their belt"* by attaching their name to a shiny project.
- Contributors wanting to code on a new exciting project without committing to maintain it.

Contributors with a **specific goal to achieve** are better motivated and will better maintain what they contribute. This is the positive framing of the dashboard-consolidation dilution-of-ownership problem: people who solve a real need stay engaged after delivery; people scratching a CV-itch don't.

## Design the project structure up front

Projects grow, and you can't assume your local team will always be able to supply the needed contributors. Therefore (source: chapter-31-communication-and-collaboration-in-sre.md):

- **Project leaders are important** — they provide long-term vision and keep work aligned and prioritised.
- **Agree on a decision-making mechanism** — one that optimises for local decisions where trust and agreement are high.
- **Divide and conquer** — split the project into as many reasonably sized components as possible, and assign each component to a small group, preferably within one site.
- Establish clear deliverables and deadlines.

### Beware Conway's law distorting the software

The chapter names [[conways-law]] explicitly: *"Try not to let Conway's law distort the natural shape of the software too deeply"* (source: chapter-31-communication-and-collaboration-in-sre.md). Cross-site division-of-labour will push toward code that mirrors the team structure; the discipline is to notice and compensate rather than let the org chart arbitrate the architecture.

## Goal orientation

*"A goal for a project team works best when it's oriented toward providing some functionality or solving some problem"* (source: chapter-31-communication-and-collaboration-in-sre.md). This ensures individuals know what's expected of them, and that their work is **complete only when the component is fully integrated and used within the main project**. The definition-of-done is integration, not sprint-level feature delivery.

## Engineering practice

Standard best practices apply (source: chapter-31-communication-and-collaboration-in-sre.md):

- **Each component gets a design document and design review with the team** — everyone can stay abreast, influence, and improve designs.
- **Writing things down is one of the major techniques you have to offset physical and/or logical distance — use it.**

Writing is the substrate of cross-site collaboration, not an optional documentation layer.

## Standards

Chapter 31's explicit treatment (source: chapter-31-communication-and-collaboration-in-sre.md):

- **Coding style guidelines** are a starting point but usually tactical — only a seed for establishing team norms.
- **Every debate about a choice**: argue it out fully with the team but with a **strict time limit**. Then pick a solution, document it, move on.
- **If you can't agree**: pick an arbitrator everyone respects. Just move forward.
- Over time you'll build a collection of best practices that help new people come up to speed.

The rule behind the rules: decisions compound; indecision also compounds, more expensively.

## In-person time

*"Ultimately, there's no substitute for in-person interaction, although some portion of face-to-face interaction can be deferred by good use of VC and good written communication"* (source: chapter-31-communication-and-collaboration-in-sre.md).

Concrete suggestions:

- **Project leaders should meet the rest of the team in person** if at all possible.
- **Team summits** — organise one if time and budget allow. A great opportunity to hash out designs and goals.
- **Neutral location for summits** when neutrality matters, so no single site has the *"home advantage."*

## Match project management to the project's size

*"Use the project management style that suits the project in its current state. Even projects with ambitious goals will start out small, so the overhead should be correspondingly low. As the project grows, it's appropriate to adapt and change how the project is managed. Given sufficient growth, full project management will be necessary"* (source: chapter-31-communication-and-collaboration-in-sre.md).

Don't front-load heavyweight process; grow the process in step with the project.

## Summary checklist

1. Only go cross-site when you must; both approaches have costs.
2. Vet contributors for real commitment, not self-actualisation.
3. Strong project leaders. Explicit decision-making mechanism. Prefer local decisions.
4. Divide and conquer into small groups within single sites where possible.
5. Watch for Conway's law distortion and compensate.
6. Goals oriented toward functionality/integration, not output-volume.
7. Design documents and reviews for every component. Write things down.
8. Time-limited debates → decisions → documentation → forward motion.
9. Project leaders meet the team in person. Team summits at neutral locations.
10. Scale the project-management style with the project.

## Related pages

- [[communication-and-collaboration-in-sre]]
- [[cross-sre-collaboration]]
- [[conways-law]]
- [[architecture-decision-record]]
- [[architect-leadership-skills]]
- [[sre-team-composition]]
- [[global-vs-local-optimization]]
