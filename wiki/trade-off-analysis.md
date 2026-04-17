# Trade-off Analysis

**Summary**: The architect's core skill, worked through in Chapter 2 of Richards and Ford. Architecture questions cannot be Googled — every solution has advantages *and* disadvantages, and the answer to "which is better?" is almost always "it depends." Architectural thinking is the disciplined practice of enumerating trade-offs on each candidate solution and deciding which one fits the current business drivers, environment, and constraints.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-02-architectural-thinking.md`

**Last updated**: 2026-04-16

---

## The core claims

> Architecture is the stuff you can't Google. — Mark Richards (source: chapter-02-architectural-thinking.md)

> There are no right or wrong answers in architecture — only trade-offs. — Neal Ford (source: chapter-02-architectural-thinking.md)

Everything in architecture is a trade-off, which is why "it depends" is the famous answer to every architecture question. You cannot Google whether REST or messaging is better, or whether microservices is the right style, because it depends on deployment environment, business drivers, company culture, budgets, timeframes, developer skill set, and dozens of other factors (source: chapter-02-architectural-thinking.md). Every environment, situation, and problem is different.

This is the applied form of the [[laws-of-software-architecture|First Law of Software Architecture]] ("everything in software architecture is a trade-off"). The law is the *claim*; trade-off analysis is the *practice*.

## The Hickey warning

Richards and Ford quote Clojure creator Rich Hickey (source: chapter-02-architectural-thinking.md):

> Programmers know the benefits of everything and the trade-offs of nothing. Architects need to understand both.

This is the load-bearing discipline of architectural thinking: looking past the obvious advantage of a solution to enumerate the negatives too. A solution that looks clearly superior after listing its benefits may look markedly worse after listing its costs.

## The auction-system worked example

Chapter 2 illustrates trade-off analysis with a bid-processing system (source: chapter-02-architectural-thinking.md). A Bid Producer service must send each bid to three downstream services: Bid Capture, Bid Tracking, and Bid Analytics. Two options:

- **Topic (pub/sub)** — producer publishes to one topic; all three subscribers receive the message.
- **Queues (point-to-point)** — producer writes the bid to three separate queues, one per consumer.

### The seemingly obvious answer: topic

The topic solution has clear advantages:

- **Extensibility** — adding a new Bid History service needs no changes to the Bid Producer; the new service just subscribes to the existing topic. With queues, a new queue must be created *and* the producer modified to write to it.
- **Decoupling** — the Bid Producer doesn't know how many consumers exist or what they do with the data. With queues, the producer knows exactly who the consumers are.

The topic solution "seems clear" and "obvious" (source: chapter-02-architectural-thinking.md). This is where most developers would stop.

### The trade-offs the architect has to see

Architectural thinking requires looking at the disadvantages too. The chapter walks through three for the topic option (source: chapter-02-architectural-thinking.md):

1. **Data access and security** — anyone can subscribe to a topic, so a rogue service can silently wiretap bid data. With queues, a rogue consumer *takes* the message, meaning the intended consumer notices the loss. It is easy to wiretap a topic; not a queue.
2. **Homogeneous contracts** — all subscribers to a topic must accept the same contract. If Bid History needs the current asking price alongside each bid, adding that field changes the contract for every other subscriber. With queues, each consumer has its own channel and its own contract; adding a field for one consumer doesn't touch the others.
3. **Monitoring and auto-scaling** — a topic doesn't support monitoring the number of messages in flight or applying per-consumer programmatic load balancing. Queues can be monitored individually and consumers auto-scaled independently. (Note: this is technology-specific — AMQP with its exchange/queue separation supports both.)

### Which is better?

> And the answer? It depends! (source: chapter-02-architectural-thinking.md)

The point is not to arrive at a universal winner. The point is that the architect must enumerate the trade-offs, then ask the contextual question: **"which is more important here: extensibility or security?"** The decision always depends on business drivers, environment, and the other factors listed above.

## The trade-off analysis discipline

Distilled from the chapter, trade-off analysis is a loop:

1. **List the candidate solutions** — at least two. (This is where [[technical-breadth-vs-depth]] pays off — you cannot analyse trade-offs between options you don't know exist.)
2. **List the benefits of each** — the easy part; developers do this naturally.
3. **List the disadvantages of each** — the hard part; the Hickey quote is a warning against skipping it.
4. **Ask which of the disadvantages matter most in this context** — guided by the business drivers and the [[architecture-characteristics|architecture characteristics]] the system has to preserve.
5. **Decide** — and capture the reasoning (per the [[laws-of-software-architecture|Second Law]]: why beats how) in an [[architecture-decision-record|Architecture Decision Record]]. The Consequences section of the ADR is where this trade-off analysis lands as durable artefact.

## Relationship to the rest of the wiki

The wiki is already full of pages whose entire content is a named trade-off, produced by this discipline applied to concrete domains:

- [[cap-theorem]], [[linearizability]] vs [[eventual-consistency]]
- [[reversible-vs-irreversible-decisions]], [[cost-of-change]]
- [[schema-on-read-vs-write]], [[partitioning-strategies]]
- [[replicated-load-balanced-service]] vs [[sharded-service-pattern]] vs [[scatter-gather-pattern]]
- [[robustness-vs-resilience]]
- [[message-brokers]] vs [[rpc]]

Each of these is a site where architectural thinking has already been applied and the opposing forces named. The [[architecture-characteristics|characteristics star-rating]] model the book uses for its style chapters (10–18) is trade-off analysis made comparable across styles.

## Relationship to business drivers

The chapter's fourth aspect of architectural thinking — understanding business drivers — is what makes trade-off analysis land on a decision. Without knowing *why* the business needs extensibility (or security, or performance, or cost), no amount of enumerating trade-offs produces a choice. See [[architect-expectations|expectation #6]] (business domain knowledge) for the Chapter 1 framing of the same point.

## Related pages

- [[architectural-thinking]]
- [[laws-of-software-architecture]]
- [[technical-breadth-vs-depth]]
- [[architecture-characteristics]]
- [[architecture-decisions-vs-design-principles]]
- [[reversible-vs-irreversible-decisions]]
- [[cost-of-change]]
- [[schema-on-read-vs-write]]
- [[message-brokers]]
- [[fundamentals-of-software-architecture]]
