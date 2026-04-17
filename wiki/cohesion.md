# Cohesion

**Summary**: A measure of how related the things grouped together inside a module are. Newman uses the succinct definition "the code that changes together, stays together." High cohesion of business functionality — not of technology — is the goal that justifies modeling microservices around a business domain.

**Sources**: `raw/monolith-to-microservices/chapter-01-just-enough-microservices.md`, `raw/fundamentals-of-software-architecture/chapter-03-modularity.md`

**Last updated**: 2026-04-16

---

## Definition

> "The code that changes together, stays together." (source: chapter-01-just-enough-microservices.md)

For microservices, this is a useful enough definition. The microservice architecture is optimized around ease of making changes in business functionality, so we want functionality grouped such that each change touches as few places as possible. If you want to change how invoice approval is managed, you do not want to hunt the change across multiple services and coordinate releases (source: chapter-01-just-enough-microservices.md).

Richards and Ford's fuller formulation:

> "Cohesion refers to what extent the parts of a module should be contained within the same module. In other words, it is a measure of how related the parts are to one another. Ideally, a cohesive module is one where all the parts should be packaged together, because breaking them into smaller pieces would require coupling the parts together via calls between modules to achieve useful results." — Larry Constantine, quoted in chapter-03-modularity.md

Attempting to divide a cohesive module only increases [[coupling]] and decreases readability (source: chapter-03-modularity.md). The two framings converge: code that changes together should live together, and code that is cohesive *will* change together.

## Constantine's seven-level scale

Computer scientists have developed a finer-grained ordering of cohesion types than "high / low." Richards and Ford reproduce Constantine's seven-level scale, from best to worst (source: chapter-03-modularity.md):

1. **Functional cohesion** — every part of the module is related, and the module contains everything essential to its function. The target.
2. **Sequential cohesion** — two modules interact such that one's output is the other's input (pipeline-shaped).
3. **Communicational cohesion** — two modules form a communication chain where each operates on information and/or contributes to some output. Example: add a record to the database *and* generate an email based on that information.
4. **Procedural cohesion** — two modules must execute code in a particular order.
5. **Temporal cohesion** — modules are related only by timing. The canonical example is a block of initialisation tasks at system startup that have nothing in common except *when* they run.
6. **Logical cohesion** — data within the module is related logically but not functionally. Java's `StringUtils` package is the given archetype: a bag of static methods that operate on `String` but are otherwise unrelated.
7. **Coincidental cohesion** — elements are related only by being in the same source file. The worst form.

Cohesion is less precise than [[coupling]], and the boundaries between levels are often at the architect's discretion. The chapter walks a worked example: should a `Customer Maintenance` module contain `get customer orders` and `cancel customer orders`, or should those live in a separate `Order Maintenance` module? The correct answer, in Richards and Ford's words, is "it depends" — on whether those are the only order operations, how much Customer state Order needs, and whether Customer Maintenance is expected to grow (source: chapter-03-modularity.md). This is the kind of trade-off analysis that sits at the heart of the [[trade-off-analysis|architect's job]].

## LCOM — measuring lack of cohesion

Despite the subjectivity, a structural metric exists: the **Chidamber and Kemerer Lack of Cohesion in Methods (LCOM)** metric (source: chapter-03-modularity.md). Richards and Ford simplify the formal definition:

> "LCOM: the sum of sets of methods not shared via sharing fields." (source: chapter-03-modularity.md)

In plain terms: a class has private fields `a` and `b`. Some methods only touch `a`, other methods only touch `b`. Those methods don't *share state*, so they don't really belong in the same class — and LCOM reports a high number to flag it. A class where most methods touch a common set of fields reports a low number.

The practical use: LCOM exposes **incidental coupling** inside classes — classes that should probably have been two or more classes to begin with. It's particularly useful during architectural migrations, where shared "utility" classes are often the hardest thing to split up (source: chapter-03-modularity.md).

LCOM's limitation is its structural nature: it can only detect **lack of structural cohesion**. Two methods might legitimately share no fields and yet belong together logically, or share many fields and belong apart. This reflects the book's [[laws-of-software-architecture|Second Law]]: prefer *why* over *how*.

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
- [[coupling-metrics]]
- [[connascence]]
- [[modularity]]
- [[microservices]]
- [[bounded-context]]
- [[information-hiding]]
- [[monolith]]
- [[independent-deployability]]
- [[fundamentals-of-software-architecture]]
