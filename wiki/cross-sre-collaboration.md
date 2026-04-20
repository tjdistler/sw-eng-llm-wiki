# Cross-SRE Collaboration

**Summary**: Chapter 31's framing of how SRE teams collaborate across sites, virtual teams, and specialisation boundaries inside Google's distributed SRE organisation. Local collaboration is easy; the interesting case is cross-site. Specialisation is a productive tactic for concentrating technical mastery but slips into siloization without deliberate resistance. The practical techniques are written-first communication, travel when needed, and divide-and-conquer decomposition.

**Sources**: `raw/site-reliability-engineering/chapter-31-communication-and-collaboration-in-sre.md`

**Last updated**: 2026-04-17

---

## Why SRE collaboration is mostly cross-site

SRE emergency-response and pager-rotation requirements make a multi-site SRE team table stakes — at least a few time zones apart for follow-the-sun coverage (see [[multi-site-on-call]]). The practical consequence is that "team" has very fluid definitions in SRE (source: chapter-31-communication-and-collaboration-in-sre.md): local teams, site teams, cross-continental teams, virtual teams of various sizes and coherence, and everything in between. *"This creates a cheerfully chaotic mix of responsibilities, skills, and opportunities."*

Local collaboration faces no particular obstacle. The interesting cases are:

- Cross-team
- Cross-site
- Across a virtual team
- Anything else that crosses a meaningful boundary

## Specialisation: the double-edged strategy

SRE's raison d'être is technical mastery, and technical mastery is hard (source: chapter-31-communication-and-collaboration-in-sre.md). The natural response is **specialisation** — team X works only on product Y — to reduce cognitive load and concentrate expertise.

### The upside

Higher chances of improved technical mastery. You can know Bigtable deeply only if Bigtable is what you work on.

### The downside

- **Siloization** — the team's knowledge becomes bounded by its charter.
- **Ignorance of the broader picture** — teams lose visibility into adjacent systems that their service depends on or is depended on by.

### The partial remedy

*Crisp team charters* — explicitly define what the team will and **won't** support. The chapter is honest: *"we try to have a crisp team charter … but we don't always succeed"* (source: chapter-31-communication-and-collaboration-in-sre.md).

A crisp charter is the mechanism that prevents specialisation from degenerating into siloization. It names the boundary, which makes cross-boundary collaboration an explicit activity rather than an accident.

## Homogeneity by design

Despite the wide role variety, Google SRE aims for *"strongly homogeneous approaches to problems"* — by design. The chapter frames this as SRE's shared culture and values doing the work of coordination where direct structural mechanisms are absent: *"culture beats strategy every time"* (source: chapter-31-communication-and-collaboration-in-sre.md, citing Mer11). This is the cultural substrate that makes cross-team collaboration land on consistent architectural choices rather than fracturing into local variants.

## Singleton projects usually fail

A specific cultural rule from the chapter (source: chapter-31-communication-and-collaboration-in-sre.md):

> In general, singleton projects fail unless the person is particularly gifted or the problem is straightforward. To accomplish anything significant, you pretty much need multiple people. Therefore, you also need good collaboration skills.

This is the structural reason SRE invests so heavily in collaboration skills at both the team and individual level. A project with one owner is a project with a single point of failure for both delivery and institutional knowledge.

## Practical techniques

For collaborations outside the building — across sites, across time zones — the chapter names two requirements:

- **Great written communication**, *or*
- **Lots of travel** to supply the in-person experience

The chapter's pithy observation: *"Even if you're a great writer, over time you decay into just being an email address until you turn up in the flesh again"* (source: chapter-31-communication-and-collaboration-in-sre.md). Writing alone is insufficient for sustaining a relationship; periodic in-person time is the refresh.

## Relationship to project-level mechanics

Cross-SRE collaboration at the **project** level gets its own treatment in the chapter's dashboard-consolidation case study and the distilled [[cross-site-project-recommendations|recommendations]]. The high-level lessons:

- Reduce communication costs via divide-and-conquer — split the project into reasonably sized components, assign each to a small group preferably within one site.
- Use design documents and reviews; writing things down offsets physical and logical distance.
- Establish standards (coding style, decision-making process, arbitration) — every debate has a strict time limit, then pick a solution and move on.
- In-person time matters most for project leaders and team summits (ideally neutral locations).

## Cheap-to-run vs expensive-to-run collaboration

Collaboration outside SRE — with product development teams — is tracked using the OKR process (see [[sre-dev-collaboration]]). Within SRE, the primary instruments are the [[production-meetings|production meeting]] (for local and near-local collaboration), design-document reviews, and cross-team collaborations that create shared infrastructure.

## Related pages

- [[communication-and-collaboration-in-sre]]
- [[production-meetings]]
- [[sre-team-composition]]
- [[cross-site-project-recommendations]]
- [[sre-dev-collaboration]]
- [[multi-site-on-call]]
- [[conways-law]]
- [[team-autonomy]]
- [[global-vs-local-optimization]]
