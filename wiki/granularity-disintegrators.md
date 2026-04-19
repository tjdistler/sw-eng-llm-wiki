# Granularity Disintegrators

**Summary**: The six forces that justify breaking a service apart into smaller services, from Chapter 7 of *Software Architecture: The Hard Parts*. Disintegrators answer the question *"When should I consider breaking apart a service into smaller pieces?"* They are one half of the [[service-granularity]] trade-off; the other half is [[granularity-integrators]].

**Sources**: `raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md`

**Last updated**: 2026-04-19

---

## The six drivers

Ford, Richards, Sadalage, and Dehghani name six disintegrators. In most real splits more than one is in play; a single driver alone is usually weak justification (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md):

| # | Driver | Question |
|---|---|---|
| 1 | **Service scope and function** | Is the service doing too many unrelated things? |
| 2 | **[[code-volatility|Code volatility]]** | Are changes isolated to only one part of the service? |
| 3 | **[[scalability]] and throughput** | Do parts of the service need to scale differently? |
| 4 | **[[fault-tolerance]]** | Are there errors that cause critical functions to fail within the service? |
| 5 | **Security** | Do some parts of the service need higher security levels than others? |
| 6 | **Extensibility** | Is the service always expanding to add new contexts? |

## 1. Service scope and function

The most common — and most abused — driver. It has two sub-dimensions: **[[cohesion]]** (how related the operations are) and **size** (statements per service, public entry points, or both).

The Notification Service worked example: a single service that sends SMS, email, and postal-letter notifications. Tempting to split into three single-purpose services, but cohesion is already strong — *all three notify the customer*. Functional cohesion alone is not enough justification (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md).

Contrast: a Customer Service that manages **profile, preferences, and website comments** — three operations on a broader scope (the customer). Cohesion is weak; the service is doing too much; this *is* a good candidate for splitting.

This driver is the Single Responsibility Principle applied at service level. The chapter is sharp on the trap: "single responsibility" is in the eye of the beholder. *Is notifying the customer one thing, or is notifying via email one thing?* Architects who decompose on this driver alone routinely over-decompose. **Use it in combination with the other five.**

## 2. Code volatility

How often the source code changes. See [[code-volatility]] for the full treatment.

The Notification Service revisited with change-rate data: SMS and email change every six months on average, postal-letter code changes weekly. As one service, every postal-letter tweak forces the entire service to be retested and redeployed; SMS and email may be unavailable during deploy windows.

Splitting into Electronic Notification (SMS + email, low change) and Postal Letter Notification (high change) shrinks testing scope, lowers deployment risk, and isolates the chatty code (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md). Note that the split is *not* one-service-per-method — it groups by volatility class, not by function.

This is also called **volatility-based decomposition**. It is one of the few disintegrators that is **objectively measurable** from version-control history.

## 3. Scalability and throughput

Different functions inside one service may have wildly different load profiles. Notification Service throughput numbers from the chapter:

- SMS: 220,000/minute
- Email: 500/minute
- Postal letter: 1/minute

As a single service, email and letter functionality must scale to meet SMS demand — wasted infrastructure cost, worse mean-time-to-startup ([[elasticity|MTTS]]). Splitting into three services lets each scale to its own demand curve (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md).

This driver targets the [[architectural-modularity]] split between [[scalability]] (modularity-driven) and [[elasticity]] (granularity-driven) made in Chapter 3.

## 4. Fault tolerance

If one function inside a service crashes fatally (e.g., out-of-memory), the whole service comes down — including all unrelated functions. Isolating the unstable function in its own service contains the blast radius (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md).

The Notification example: only **email** has fatal-crash issues; SMS and postal letter are stable. So the natural fault-tolerance split is `Email Service` + `Other Notification Service`. But this immediately runs into the **service naming test** (see below) — *"Other Notification"* is a bad name. Pulling SMS and postal letter together produces only weak cohesion. The honest split, accounting for cohesion *and* fault tolerance, is three services: SMS, Email, Letter.

This driver interacts with #1 (scope) and #2 (volatility): the right number of resulting services is the one where each leftover service still has a *good name*. See "Service naming test" below.

Note the irony: fault tolerance is *also* a [[granularity-integrators|granularity integrator]]. If the resulting services then call each other synchronously to do their work, none of the fault-tolerance benefit is realised — the call chain fails together. Always check whether the split functions are tightly coupled before claiming a fault-tolerance win.

## 5. Security

Sensitive data needs to be isolated not just at rest (separate schemas, separate regions) but also **at the access boundary**. A consolidated service that handles both customer profile and customer credit-card maintenance puts both behind the same set of API entry points. Even if the credit-card *data* is encrypted, anyone with access to the service has access to the credit-card *operations* (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md).

Splitting credit-card maintenance into its own single-purpose service narrows the attack surface: only that service has the operations that touch credit-card data. Authentication and authorisation can be tightened around the smaller service.

The trade-off (often appearing as an [[granularity-integrators|integrator]]): the original consolidated service supported an ACID transaction across profile and credit-card writes. Splitting forfeits that transaction. The chapter's worked decision example: *"better data consistency or better security?"* — the CIO chose security and accepted the cost of resolving consistency elsewhere.

## 6. Extensibility

If the service's domain is one where new operations are routinely added — payment methods, integrations, file formats — keeping everything in one service means each new addition forces the whole service to be retested and redeployed. Splitting along the dimension that grows lets new entries be added in isolation (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md).

The chapter's example: a payment service handling credit cards, gift cards, and PayPal. Splitting by payment method means adding ApplePay or store credit only requires writing, testing, and deploying one new service.

The caveat — the chapter is unusually cautious here: **only apply this driver when the extension pattern is known or strongly expected.** With notification, the methods (SMS/email/letter) are unlikely to keep growing. With payments, new methods are an industry constant. *"Wait on this driver as a primary means of justifying a granular disintegration until a pattern can be established or confirmation of continued extensibility can be confirmed."*

This is the only disintegrator the chapter recommends *not* using speculatively.

## The service naming test

Throughout the disintegrator analysis, Ford and Richards return to a heuristic that comes up especially in driver #4 (fault tolerance):

> If a service is too hard to name because it's doing multiple things, then consider breaking apart the service. Whenever breaking apart a service, regardless of the disintegration driver, always check to see if strong cohesion can be formed with the "leftover" functionality. (source: raw/software-architecture-the-hard-parts/chapter-07-service-granularity.md)

Worked through for the Notification example:

- Notification Service → Email + **Other Notification Service** (poor name)
- Notification Service → Email + **Non-Email Service** (poor name)
- Notification Service → Email + **SMS-Letter Service** (poor name)
- Notification Service → Email + **SMS** + **Letter** (good names)

If you can't name the leftover service cleanly, you have not finished decomposing.

## How disintegrators interact with integrators

Disintegrators don't decide granularity on their own — they're one half of a balanced trade-off with [[granularity-integrators]]. The book's stance: *most architects over-decompose because they focus only on disintegrators*. The discipline is to enumerate **both** sets of forces and resolve the trade-off explicitly, often through ADRs and direct conversation with business stakeholders. See [[service-granularity]] for the worked balance.

## Relationship to other decomposition rubrics

Many of the same forces appear at the **data** layer in [[data-decomposition-drivers-and-integrators]] (Hard Parts Ch 6) — change control, scalability, fault tolerance, security, and database-type optimisation are the data-side analogues. The conceptual symmetry is intentional: the same trade-off framework runs across the architecture (services, data, components) — only the units change.

[[architectural-modularity]] (Hard Parts Ch 3) catalogs the *technical drivers* that justify modularity at all (maintainability, testability, deployability, scalability, elasticity, fault tolerance). Granularity disintegrators are the next level down: *given* you've decided to be modular, *which* services to split *which* way is what these six drivers answer.

## Related pages

- [[service-granularity]]
- [[granularity-integrators]]
- [[code-volatility]]
- [[cohesion]]
- [[scalability]]
- [[elasticity]]
- [[fault-tolerance]]
- [[architectural-modularity]]
- [[architectural-quantum]]
- [[microservices]]
- [[bounded-context]]
- [[data-decomposition-drivers-and-integrators]]
- [[trade-off-analysis]]
- [[architecture-decision-record]]
- [[software-architecture-the-hard-parts]]
