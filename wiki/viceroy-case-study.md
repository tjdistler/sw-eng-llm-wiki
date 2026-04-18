# Viceroy: Cross-SRE Monitoring Dashboard Consolidation

**Summary**: Chapter 31's case study in successful cross-SRE collaboration — the consolidation of multiple parallel monitoring-dashboard projects into Viceroy, Google's general SRE monitoring solution. The story runs 2012-2014: duplicated efforts spawned by Monarch migration, initial Viceroy + Consoles++ incompatibility, eventual convergence as technical differences narrowed, and the December 2014 declaration of Viceroy as the recommended (not mandated) SRE monitoring console solution.

**Sources**: `raw/site-reliability-engineering/chapter-31-communication-and-collaboration-in-sre.md`

**Last updated**: 2026-04-17

---

## The structural problem

Before Viceroy, Google SRE had *"a serious litter problem of many smoldering, abandoned hulks of monitoring frameworks lying around"* (source: chapter-31-communication-and-collaboration-in-sre.md). The chapter names the incentives that caused it:

- Each team was rewarded for developing its own solution.
- Working outside the team boundary was hard.
- The infrastructure provided SRE-wide was typically closer to a **toolkit** than a **product**.

Result: individual engineers used the toolkit to make *"another burning wreck"* rather than fix the problem for the largest number of people possible, because fixing it generally takes much longer.

The chapter's wry footnote: *"In this particular case, the road to hell was indeed paved with JavaScript."*

## Timeline

### 2012 — Monarch migration triggers duplicate efforts

[[borgmon|Borgmon]]-era consoles used a custom HTML templating system that was special-cased, full of funky edge cases, and difficult to test. Monarch — Google's new monitoring system — was maturing and being adopted by non-SRE teams, but SRE is deeply conservative with respect to monitoring. When SRE teams started trying Monarch, they discovered its console support fell short on two axes (source: chapter-31-communication-and-collaboration-in-sre.md):

- Consoles were easy to set up for a small service but didn't scale well to complex consoles.
- No support for the legacy monitoring system — making transition painful.

With no viable unified alternative, **team-specific projects launched in parallel**. Multiple teams from Spanner, Ads Frontend, and others spun up their own efforts over 12-18 months. Notable example: **Consoles++**.

### Mid 2012 — Viceroy is born

Engineers from the parallel efforts eventually discovered each other and decided to join forces. Viceroy was explicitly founded as a *general solution for all of SRE*.

### Early 2013 — initial interest, initial failure to merge

Teams who hadn't yet moved off the legacy system started showing interest. Teams with larger existing monitoring projects were harder to convert: the low maintenance cost of a working legacy solution is hard to trade for the uncertain cost of adopting something new. Differing requirements compounded the reluctance:

- Multiple data sources outside the core monitoring systems
- Configuration-based vs explicit-HTML console definition
- No JavaScript vs full JavaScript with AJAX
- Static content for browser caching vs dynamic

**The Consoles++ team examined Viceroy in the first half of 2013** and decided the fundamental differences were too large to integrate — **Viceroy by design did not use much JavaScript, Consoles++ was mostly JavaScript** (source: chapter-31-communication-and-collaboration-in-sre.md).

Two underlying similarities gave the merger a distant possibility:

- Similar HTML-template-rendering syntax
- Shared long-term goals neither team had started on (caching monitoring data; offline pipeline for expensive precomputation)

The unified console discussion was parked.

### Late 2013 — convergence

Both projects evolved. **Viceroy had started using JavaScript to render its monitoring graphs**. The technical gap narrowed. Integration became feasible: serve Consoles++ data out of the Viceroy server.

### Early 2014 — integrated prototypes

First prototypes demonstrated the systems could work together. Both teams committed to a joint effort. **Because Viceroy had already established its brand as a common monitoring solution, the combined project kept the Viceroy name.**

### End of 2014 — Viceroy declared the SRE-wide monitoring solution

Combined system was complete. The declaration was characteristically Google: *"this declaration didn't require that teams adopt Viceroy: rather, it recommended that teams should use Viceroy instead of writing another monitoring console"* (source: chapter-31-communication-and-collaboration-in-sre.md).

## What the merger bought

Once combined (source: chapter-31-communication-and-collaboration-in-sre.md):

- Viceroy received Consoles++'s data sources and JavaScript clients.
- **JavaScript compilation was rewritten to support separate modules that can be selectively included** — essential to scale to any number of teams with their own JavaScript code.
- Consoles++ benefited from ongoing Viceroy improvements (cache, background data pipeline).
- Development velocity on the combined solution was **much larger than the sum** of the individual efforts.

The load-bearing factor was the **common future vision**. Each team saw value in expanding the development team and benefited from the other's contributions.

## Challenges

Merging two projects across sites surfaced problems the chapter catalogues (source: chapter-31-communication-and-collaboration-in-sre.md):

### Remote coordination and cue misinterpretation

When meeting for the first time, subtle cues in writing and speaking get misinterpreted because communication styles vary substantially. Team members outside Mountain View missed the impromptu water-cooler discussions that happen around meetings. This is the specific friction [[cross-sre-collaboration]] names and the reason the chapter recommends in-person time for project leaders.

### Core team stability vs extended team churn

The core Viceroy team stayed consistent. The **extended contributor pool was dynamic** — contributors had other responsibilities and could usually dedicate 1-3 months to the project. Each new contributor required training on overall design and structure.

The unexpected upside: when an SRE finished their rotation and returned to their team, they became a local expert on Viceroy. **This unanticipated dissemination of local experts drove more adoption and usage** — a systemic benefit of treating the rotation as a feature rather than a cost.

### Casual contribution: useful but costly

**Dilution of ownership**. When a contributor delivered a feature and left, the feature became unsupported over time and was generally dropped. Features tied to engaged-owner-then-gone contributors had the worst longevity.

### Scope creep

The project's scope grew as it matured. Ambitious goals at launch with initially limited scope eventually struggled to deliver on core features on time. **The team had to improve project management and set clearer direction to keep the project on track.**

### Distributed ownership friction

Even with the best intentions, *"people generally default to the path of least resistance and discuss issues or make decisions locally without involving the remote owners, which can lead to conflict"* (source: chapter-31-communication-and-collaboration-in-sre.md). This is the specific Conway-flavoured failure mode that cross-site projects have to actively defend against.

## What the case study teaches

The chapter uses Viceroy to derive the [[cross-site-project-recommendations]] — its explicit list of rules for cross-site engineering projects. The headline lessons:

- **Do cross-site projects only when you have to, but do them when you must.** The cost is higher action latency and more communication; the benefit is much higher throughput if the mechanics are right.
- **Motivated contributors vary in value.** Check that contributors are committed, not chasing a notch on their belt.
- **Project structure matters.** Leaders provide vision; decisions should be made locally when trust is high.
- **Divide and conquer.** Split into components assignable to a small group within one site.
- **Standards, reviews, written records** — the chapter-level versions of software engineering best practices.
- **In-person when possible** — leaders meeting the team, ideally a team summit at a neutral location.

## Context: SRE's toolkit-vs-product problem

The Viceroy story is an instance of a more general SRE pattern. The chapter's opening framing of the problem — *"the infrastructure that tended to be provided SRE-wide was typically closer to a toolkit than a product"* — applies beyond monitoring consoles. [[auxon|Auxon]] (Chapter 18) is the capacity-planning version of the same trajectory: an SRE-developed internal product that replaces dozens of ad hoc team-specific efforts. [[sre-product-adoption]] distils the general adoption playbook across both cases.

## Related pages

- [[communication-and-collaboration-in-sre]]
- [[cross-sre-collaboration]]
- [[cross-site-project-recommendations]]
- [[borgmon]]
- [[auxon]]
- [[sre-product-adoption]]
- [[fostering-software-engineering-in-sre]]
- [[global-vs-local-optimization]]
