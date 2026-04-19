# Granularity Integrators

**Summary**: The four forces that justify keeping services together (or putting them back together after over-decomposition), from Chapter 7 of *Software Architecture: The Hard Parts*. Integrators answer the question *"When should I consider putting services back together?"* They are the counterweight to [[granularity-disintegrators]], and the book argues that most architects under-weight them — leading to systemic over-decomposition.

**Sources**: `raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md`

**Last updated**: 2026-04-19

---

## The four drivers

Ford, Richards, Sadalage, and Dehghani name four integrators (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md):

| # | Driver | Question |
|---|---|---|
| 1 | **Database transactions** | Is an [[acid|ACID]] transaction required between separate services? |
| 2 | **Workflow and choreography** | Do services need to talk to one another? |
| 3 | **Shared code** | Do services need to share code among one another? |
| 4 | **Data relationships** | Although a service can be broken apart, can the data it uses be broken apart as well? |

## 1. Database transactions

The starkest integrator. Inside one service writing to one database, multi-table writes can be wrapped in a single ACID unit-of-work — atomic commit or atomic rollback. Across two services, that envelope vanishes; you get either a [[saga]]-style eventual-consistency arrangement (with compensating actions and complex failure handling) or partial-write inconsistency.

The chapter's worked example: customer functionality split into a Customer Profile Service and a Password Service. The split is good for **security** (a [[granularity-disintegrators|disintegrator]]) — password operations live in a dedicated service with tighter access control. But the new-customer-registration flow has to write profile data to one service and password data to the other. If the second write fails, the first is already committed; reversing it requires error-prone compensating logic (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md).

The book's framing: *"if having a single-unit-of-work ACID transaction is required from a business perspective, these services should be consolidated into a single service."* The trade-off is explicit: ACID consistency vs the [[granularity-disintegrators|disintegrator]] that pulled the split apart in the first place. Resolved by talking to the business — see the worked dialogues in [[service-granularity]].

This is the same integrator named in [[data-decomposition-drivers-and-integrators]] at the data layer; both sides of the architecture (services and data) face it identically.

## 2. Workflow and choreography

When services have to talk to each other to complete business work — inter-service or "east-west" communication — too much chatter degrades the architecture across three dimensions (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md):

### Fault tolerance

If Service A → B → C and Service C goes down, A and B both fail too. Synchronous transitive dependencies form a single failure domain. The chapter's pointed observation: *"fault tolerance is one of the granularity disintegration drivers from the previous section — yet when those services need to talk to one another, nothing is really gained from a fault-tolerance perspective."* Splitting for fault tolerance and then introducing synchronous calls between the splits is a self-defeating decomposition.

### Performance and responsiveness

Each inter-service call adds network + security latency. The chapter's number: 300 ms per hop. A request that traverses five services in [[choreography|choreography]] takes 1500 ms in latency alone, before any actual work. The rule of thumb: *count the percentage of requests that need cross-service workflow versus the percentage that are purely atomic, and weight by criticality.* If 70% are atomic and the cross-service 30% are non-critical, separation is fine. Reverse the proportions and consolidate.

[[orchestration|Orchestration]] (Chapter 11) is the alternative to choreography for high-fan-out workflows but doesn't eliminate the latency cost — it just moves the coordination logic.

### Reliability and data integrity

Five-service workflows require five separate local commits. A failure mid-flight leaves the first three services with committed state and the last two without. The same compensating-action mess as integrator #1 reappears here, just with more services involved. Sagas help (Chapter 12 / [[saga]]) but the integrator says: if data integrity is critical, keep the services together.

### When chatter is OK

Asynchronous, non-critical chatter doesn't trigger this integrator nearly as hard. Backend functionality with no human waiting has more latency budget. The integrator is mostly about **synchronous critical-path** chatter.

## 3. Shared code

Domain code shared via library (JAR, GEM, DLL) couples services at compile time. A change to the shared library eventually requires every service that uses it to be retested and redeployed in lockstep. If the shared library is *infrastructure* code (logging, monitoring, auth) this is fine — those are well-versioned and rarely break. If it's *domain* code, the tight coupling argues for keeping the services together (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md).

The chapter offers three sub-criteria for treating shared code as an integrator:

- **Specific shared domain functionality** — the larger the proportion of shared domain code (chapter's threshold: ~40% of the collective codebase), the more it argues for consolidation.
- **Frequent shared code changes** — high churn on shared libraries forces frequent coordinated deployments. Versioning helps but doesn't fully solve it.
- **Defects that can't be versioned** — security fixes, business-rule changes, or critical bugs that *must* be applied to all services simultaneously. If these are common, splits are exposing the architecture to risk it could avoid.

Code-reuse patterns are covered in detail in Chapter 8.

## 4. Data relationships

If two services own data that is tightly relational — every operation in Service B has to look up data owned by Service C, and vice versa — the [[bounded-context]] discipline that prevents direct cross-service queries forces every read to become an inter-service call. The result is either chatter (integrator #2) or shared databases (collapsing the [[architectural-quantum|quanta]]).

The chapter's worked example: a service split into A, B, and C, where B owns table 3 and C owns table 5. *Every* operation in B needs to read table 5 and *every* operation in C needs to read table 3. The dependency is symmetric and total. Bounded context says B can't directly query table 5, so the architecture devolves into back-and-forth synchronous chatter. The honest call is to consolidate B and C (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md).

The chapter saves this driver for last because it's the **least-tradeoff integrator** — when data is genuinely entangled, splitting almost never works. The Chapter 6 work on [[database-decomposition]] is partly about distinguishing entanglement that's real from entanglement that's an artifact of historical schema design.

## Why integrators matter more than architects think

Ford and Richards's emphasis: *"One common mistake many development teams make is focusing too much on granularity disintegrators while ignoring granularity integrators"* (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md). The result is over-decomposition — a [[distributed-monolith]] or worse, where the splits look clean on the deployment diagram but the runtime is one tangled call graph that fails together, scales together, and deploys together.

The book's prescription, stated as the central principle of getting granularity right:

> The secret of arriving at the appropriate level of granularity for a service is achieving an equilibrium between these two opposing forces.

In practice this means: identify the disintegrator forces, identify the integrator forces, weight them against the specific business needs, and resolve via [[trade-off-analysis]] and an [[architecture-decision-record|ADR]]. See [[service-granularity]] for the worked architect/sponsor dialogues.

## Related pages

- [[service-granularity]]
- [[granularity-disintegrators]]
- [[acid]]
- [[saga]]
- [[transactions]]
- [[distributed-transactions]]
- [[choreography]]
- [[orchestration]]
- [[bounded-context]]
- [[architectural-quantum]]
- [[fault-tolerance]]
- [[fallacies-of-distributed-computing]]
- [[distributed-monolith]]
- [[data-decomposition-drivers-and-integrators]]
- [[database-decomposition]]
- [[trade-off-analysis]]
- [[architecture-decision-record]]
- [[software-architecture-the-hard-parts]]
