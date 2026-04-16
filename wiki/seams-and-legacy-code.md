# Seams and Legacy Code

**Summary**: Michael Feathers's *seam* concept from *Working Effectively with Legacy Code* (Prentice Hall, 2004): a place in a codebase where you can change behaviour without editing existing code. Newman uses seams as the unit of refactoring inside a [[monolith]] when realigning code along business domain boundaries — and as the foundation for [[branch-by-abstraction]].

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`

**Last updated**: 2026-04-16

---

## Feathers's seam

A seam is a point at which you can swap out one implementation of behaviour for another without modifying the surrounding code. Feathers introduced the concept as a tool for working safely with legacy code: identify a seam around the section you want to change, build a new implementation of what's behind the seam, and substitute it in (source: chapter-03-splitting-the-monolith.md).

## Why Newman uses it

Existing monoliths are typically organised by *technical* category — Models, Views, Controllers — rather than by business domain. When you want to migrate a chunk of *business* functionality to a microservice, the code matching that functionality is scattered across the technical layers and can be hard to even locate (source: chapter-03-splitting-the-monolith.md).

Seams give you a way to define a boundary around the business behaviour you care about, regardless of how the existing code is organised. Newman maps Feathers's generic seams onto the more specific concept of [[bounded-context|bounded contexts]] from DDD: the seams worth establishing are the ones that align with the domain model (source: chapter-03-splitting-the-monolith.md).

## The path: seams → modules → services

Once you've identified seams in the monolith, the next natural step is to extract them into proper modules — turning the monolith into a [[modular-monolith]]. Different stacks express this differently: Java JARs, Ruby gems, .NET assemblies (source: chapter-03-splitting-the-monolith.md).

> "I've spoken to more than one team that has started breaking its monolith apart into a modular monolith, with a view to eventually move to a microservice architecture, only to find that the modular monolith solved most of its problems!" (source: chapter-03-splitting-the-monolith.md)

The modular monolith is genuinely valuable in its own right. The seam-then-module work is not "wasted" if you later decide microservices aren't worth the cost.

## Seams as the base for branch by abstraction

[[branch-by-abstraction]]'s first step — *create an abstraction for the functionality to be replaced* — is essentially Feathers's seam-extraction. If the existing code is well-factored, an IDE Extract Interface refactoring suffices; if not, you're doing seam work in the Feathers sense (source: chapter-03-splitting-the-monolith.md).

## Related pages

- [[branch-by-abstraction]]
- [[modular-monolith]]
- [[bounded-context]]
- [[information-hiding]]
- [[domain-driven-design]]
- [[migration-pattern-selection]]
