# Cargo-Cult Engineering

**Summary**: Small data teams adopting the complex technologies and practices of giant tech companies without the context or scale that make them valuable. Reis and Housley's name for a specific [[technology-selection|selection]] failure mode driven by blog-post envy — "a big mistake that consumes a lot of valuable time and money, often with little to nothing to show in return."

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The pattern

Chapter 4 names the failure mode specifically (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> We sometimes see small data teams read blog posts about a new cutting-edge technology at a giant tech company and then try to emulate these same extremely complex technologies and practices. We call this cargo-cult engineering, and it's generally a big mistake that consumes a lot of valuable time and money, often with little to nothing to show in return.

The origin of the term is Richard Feynman's 1974 Caltech commencement address — South Pacific islanders, observing airplanes during WWII, built wooden replicas of airstrips and control towers hoping to draw the cargo back. The form was correct; the underlying causes were absent.

Applied to engineering: copying Netflix's architecture when you have 1/10,000th Netflix's scale; copying Uber's microservice structure when you have ten engineers; copying Airbnb's custom ML platform when off-the-shelf would do.

## Why it fails

The missing context:

- **Scale.** Big-tech architectures are expensive solutions to problems you don't have yet.
- **Team depth.** Netflix has many teams behind each piece; you have one engineer.
- **Time.** Those architectures took years and many failed attempts to reach their current form.
- **Differentiation.** Big-tech custom tooling exists where it provides competitive advantage. Your equivalent advantage is almost certainly somewhere else.

## Chapter 4's advice

The countermeasure is the team-size-and-capabilities criterion (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Especially for small teams or teams with weaker technical chops, use as many managed and SaaS tools as possible, and dedicate your limited bandwidth to solving the complex problems that directly add value to the business.

Also:

- **Take an inventory of your team's skills.** Low-code or code-first? Strong in Java, Python, Go? Pick tools that match.
- **Stick with what the team knows.** "We've seen data teams invest a lot of time in learning the shiny new data framework, only to never use it in production."
- **Invest wisely.** Learning new technologies, languages, and tools is a considerable time investment.

## Relationship to other anti-patterns

Chapter 4 groups cargo-cult engineering with two related greenfield failure modes named in Chapter 3:

- **[[brownfield-vs-greenfield|Shiny object syndrome]]** — reaching for the latest tech without understanding its value.
- **[[brownfield-vs-greenfield|Resume-driven development]]** — picking tech for career reasons rather than project fit.

All three share the same root: technology choice unmoored from the business problem and the team's capabilities.

## Cross-book framing

- [[virtue-of-boring]] (SRE release engineering) — the positive framing. Boring technology is a feature, not a defect.
- [[when-microservices-are-a-bad-idea]] (Newman) — cargo-culting microservices is one of Newman's explicit warnings.
- [[running-too-many-things]] (Burns/Newman) — cargo-cult complexity manifests operationally.

## Related pages

- [[technology-selection]]
- [[brownfield-vs-greenfield]]
- [[when-microservices-are-a-bad-idea]]
- [[virtue-of-boring]]
- [[type-a-vs-type-b-data-engineers]]
- [[speed-to-market]]
- [[principles-of-good-data-architecture]]
