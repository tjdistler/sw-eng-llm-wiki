# Service Framework

**Summary**: A prescriptive code framework that captures production best practices as reusable infrastructure modules. Each framework module addresses one [[sre-engagement-model|SRE concern]] (instrumentation, request logging, traffic/load management) with a canonical implementation. Developers focus on business logic; the framework handles the infrastructure correctly by construction. Google maintains per-language frameworks (Java, C++, Go) whose implementations differ but whose APIs, behaviour, configuration, and controls are intentionally identical.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## What a framework provides

A service framework is, per Chapter 32, "a prescriptive implementation for using a set of software components and a canonical way of combining these components" (source: chapter-32-the-evolving-sre-engagement-model.md). It also exposes features for controlling those components in a cohesive manner.

Concrete feature set Chapter 32 lists (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Semantic components.** Business logic organised as well-defined components that can be referenced using standard terms
- **Standard instrumentation dimensions.** Uniform monitoring labels that composing tools know how to aggregate across services
- **Standard debug-log format.** Consistent request-trace layout across the fleet
- **Standard load-shedding configuration.** One format teams use to configure [[load-shedding]] and overload behaviour
- **Semantically consistent capacity and overload measure.** Per-server capacity and "overload" expressed the same way across every framework-built service, so downstream control systems can trust the signal

## Why frameworks matter for SRE

Each framework module captures a canonical solution to a problem area that otherwise gets re-solved per service. Before frameworks, differing software practices across services meant production features had to be "reimplemented specifically for each service or, at best, once for each small subset of services sharing code" — the canonical example being functionally similar logging frameworks written repeatedly in the same language (source: chapter-32-the-evolving-sre-engagement-model.md).

With frameworks, one reusable solution serves every framework-based service. When the framework improves, every user improves. When a new lesson is learned, it lands once in the module, not 50 times across 50 services.

## Multi-language, single semantics

Google supports several major application languages, and frameworks are implemented across each of them (Java, C++, Go are Chapter 32's named languages). Though the Java and C++ implementations can't share code, the goal is for both to expose the same (source: chapter-32-the-evolving-sre-engagement-model.md):

- API
- Behaviour
- Configuration
- Controls

That way development teams pick the language that fits their needs and experience, and SRE still gets identical operational behaviour, standard tooling, and predictable management across the fleet.

## What frameworks free developers from

The framework "takes care of correct infrastructure use," so developers can focus on business logic rather than on the cross-cutting infrastructure plumbing (source: chapter-32-the-evolving-sre-engagement-model.md). Chapter 32 is explicit that this is not just a convenience — it's a structural shift. Before frameworks, developers had to "glue together and configure individual components in an ad hoc service-specific manner, in ever-so-slightly incompatible ways, that then have to be manually reviewed by SREs." The reviews were expensive and they scaled linearly with service count. Frameworks move the review from per-service to per-framework-change.

## Relationship to other Google infrastructure

The framework story is a natural progression from the [[stubby|Stubby]] era in which the RPC framework already carried cross-cutting behaviour (connection management, [[backend-task-states|backend states]], [[weighted-round-robin|balancing policies]], [[adaptive-throttling|throttling]]). [[handling-overload|Chapter 21]] already showed the RPC framework pulling overload-handling mechanisms into itself; Chapter 32's frameworks are the generalisation — the same pattern applied to instrumentation, logging, configuration, and the control surface.

## Related pages

- [[frameworks-and-sre-platform]]
- [[sre-engagement-model]]
- [[shared-responsibility-engagement]]
- [[stubby]]
- [[handling-overload]]
- [[load-shedding]]
- [[site-reliability-engineering]]
