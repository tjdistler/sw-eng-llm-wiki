# Cohesion

**Summary**: A measure of how related the things grouped together inside a module are. Newman uses the succinct definition "the code that changes together, stays together." High cohesion of business functionality — not of technology — is the goal that justifies modeling microservices around a business domain.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`

**Last updated**: 2026-04-16

---

## Definition

> "The code that changes together, stays together." (source: chapter-01-just-enough-microservices.md)

For microservices, this is a useful enough definition. The microservice architecture is optimized around ease of making changes in business functionality, so we want functionality grouped such that each change touches as few places as possible. If you want to change how invoice approval is managed, you do not want to hunt the change across multiple services and coordinate releases (source: chapter-01-just-enough-microservices.md).

## Cohesion of business functionality vs cohesion of technology

A traditional three-tier architecture (UI / business logic / database) has **high cohesion of related technology**: all the database stuff lives together, all the UI stuff lives together. But it has **low cohesion of business functionality**: a single business change (say, "let customers specify a favorite music genre") cuts across all three tiers, owned by three different teams (source: chapter-01-just-enough-microservices.md).

Microservices invert the priority. Each service may contain a thin slice of UI, application logic, and storage — a *local* implementation concern. But each service, end to end, owns one slice of business functionality. The result is high cohesion of business functionality at the cost of low cohesion of technology — the opposite of the three-tier model.

This is why owning your own data ([[microservices|one of the three defining properties]]) matters: it is what gives a microservice the cohesive end-to-end slice of business functionality that makes change cheap (source: chapter-01-just-enough-microservices.md).

## Cohesion and coupling together

Constantine's law:

> "A structure is stable if cohesion is high, and coupling is low." — Larry Constantine

The two are linked. If two pieces of tightly related code live in different services, cohesion is low (related code is spread) and coupling is high (the services must change together). Both problems have the same fix: put related code together.

Larry Constantine first articulated cohesion and coupling in 1968 at the National Symposium on Modular Programming — the same conference where [[conways-law|Conway's law]] got its name. *Structured Design* by Larry Constantine and Edward Yourdon (Prentice Hall, 1979) made the concepts standard university curriculum.

## In a monolith

The trap of a [[monolith]], Newman argues, is that it is often the *opposite* of both — code that is unrelated gets stuck together (low cohesion) and even a one-line change cannot be deployed without redeploying everything (high deployment coupling). See [[coupling]].

## Related pages

- [[coupling]]
- [[microservices]]
- [[bounded-context]]
- [[information-hiding]]
- [[monolith]]
- [[independent-deployability]]
