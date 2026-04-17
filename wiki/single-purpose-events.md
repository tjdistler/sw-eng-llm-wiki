# Single-Purpose Events

**Summary**: Bellemare's guideline that every event should represent a single, specific business occurrence — not a union of "similar yet different" sub-events discriminated by a `type` field. Overloading an event with a type parameter looks like a simplification but pushes complexity to every consumer and makes [[schema-evolution]] progressively harder.

**Sources**: `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`

**Last updated**: 2026-04-17

---

## The anti-pattern: a `type` field

The warning sign is an event schema with a field like `eventType` or `productType` or `actionType` whose value switches the meaning of the other fields (source: chapter-03-communication-and-data-contracts.md). It usually starts as a time-saver — "these things are similar, let's just have one event" — but it has several pathologies:

1. **Each `type` value has a fundamentally different business meaning**, even if the technical representation is close. The intent behind a `ProductEngagement{type=Movie}` is genuinely different from a `ProductEngagement{type=Book}`.
2. **Meanings drift over time.** New sub-types accumulate fields that apply only when the parent type has a specific value. Nullable "only applies if type=X" fields multiply.
3. **Consumers must filter.** Every consumer downstream has to know about every type value and filter the ones it does not care about — wasted compute, and a surface for bugs (silently mis-handling an unfamiliar type).
4. **Schema evolution gets harder.** Each sub-type's fields evolve on a different schedule; the union schema becomes a tangle of conditional optionality.

## Bellemare's worked example

Chapter 3 walks through an overloaded `ProductEngagement` event:

```
TypeEnum: Book, Movie
ActionEnum: Click
ProductEngagement {
  productId: Long,
  productType: TypeEnum,
  actionType: ActionEnum
}
```

A new requirement arrives: track whether a user watched the movie trailer. The "simple" evolution adds a nullable `watchedPreview` field that "only applies to productType=Movie" — enforced by a schema comment. Then another requirement adds bookmarks for books, which pushes in `pageId` with "only applies to productType=Book, actionType=Bookmark." The schema has become an implicit decision tree.

Bellemare's refactoring is to split the event into three single-purpose event definitions (and, following the [[singular-event-definition-per-stream]] guideline, three streams):

```
MovieClick    { movieId: Long, watchedPreview: Boolean }
BookClick     { bookId: Long }
BookBookmark  { bookId: Long, pageId: Int }
```

The enums disappear. Each schema is flat. Triggering logic is explicit per stream. Consumers subscribe to exactly what they care about.

## Why "just add a type field" fails the complexity test

Bellemare's sharp observation (source: chapter-03-communication-and-data-contracts.md):

> "Adding type fields does not reduce or eliminate the underlying complexity inherent in the data being produced. In fact, this complexity is merely shifted from multiple distinct event streams with distinct schemas to a union of all the schemas merged into one event stream. It could be argued that this actually increases the complexity."

The inherent complexity of the domain is fixed. The only choice is where it lives — in several small, focused, independently evolvable schemas, or in one sprawling schema that every consumer must navigate.

## The warning sign in practice

> "If it seems like you need a generic event with various type parameters, that's usually a tell-tale sign that your problem space and bounded context is not well defined." (source: chapter-03-communication-and-data-contracts.md)

When a type-field temptation appears, the correct first question is whether the [[bounded-context]] is right — not whether the schema should stretch to fit. Often, carving off sub-events is also a signal that the service itself should be split.

## The original author did not make a mistake

Bellemare is explicit that the overloaded-event pattern frequently arises from a *correct* initial design that the business then outgrew (source: chapter-03-communication-and-data-contracts.md). At the time the original `ProductEngagement` event was created, the business only cared about product engagements in the aggregate. The first new requirement that cared about a subtype-specific detail is the signal to re-evaluate, not the sign that the original was wrong. Treat the refactor as a response to new information, not a retrospective error.

## Related pages

- [[event-design-guidelines]]
- [[singular-event-definition-per-stream]]
- [[data-contract]]
- [[schema-evolution]]
- [[bounded-context]]
- [[event-structure]]
- [[event-driven-microservices]]
