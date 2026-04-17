# Microkernel Architecture

**Summary**: Also known as the **plug-in architecture**. A monolithic style that pairs a minimal **core system** with a set of independent **plug-in components** that extend it. Canonical examples are the Eclipse IDE, Chrome/Firefox, Jira, Jenkins, PMD, and the 1040-driven US tax-preparation application. The style is Richards and Ford's third Part II entry and the *only* one in the book that can be **both technically and domain partitioned simultaneously** — the core is technical, the plug-ins are domain.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-12-microkernel-architecture-style.md`

**Last updated**: 2026-04-16

---

## What it is

The microkernel architecture style was coined several decades ago and is still widely used today (source: chapter-12-microkernel-architecture-style.md). It is a natural fit for **product-based applications** — packaged software made available for download and installed on the customer's site as a third-party product — but it is also widely used for large *custom* business applications whose variability lives along a clean axis (one plug-in per device type, per tax form, per jurisdiction, per payment method).

The style is a **relatively simple monolithic architecture** of exactly two architecture components:

- a **core system** providing the minimum functionality required to run the application, and
- **plug-in components** providing specialized processing, additional features, and custom logic meant to enhance or extend the core.

Application logic is divided between the two so that the core stays small and generic, while domain-specific or customer-specific or regulation-specific variability is pushed out into self-contained plug-ins that can be added, removed, or replaced without touching the core.

## Core system

The core system has two common definitions (source: chapter-12-microkernel-architecture-style.md):

1. **The minimal functionality required to run the system.** Eclipse is the canonical example: the core is just a basic text editor (open a file, change some text, save the file). It isn't until you add plug-ins that Eclipse becomes a usable product.
2. **The happy path.** The general processing flow through the application, with little or no custom processing — custom assessment rules, jurisdictional variations, per-device logic all moved out to plug-ins.

Both definitions converge on the same discipline: **keep the core small** and **pull cyclomatic complexity out**. The chapter's electronics-recycling example makes the point concrete. Before:

```java
public void assessDevice(String deviceID) {
    if (deviceID.equals("iPhone6s")) {
        assessiPhone6s();
    } else if (deviceID.equals("iPad1")) {
        assessiPad1();
    } else if (deviceID.equals("Galaxy5")) {
        assessGalaxy5();
    } else ...
}
```

After, with the device-specific rules in plug-ins:

```java
public void assessDevice(String deviceID) {
    String plugin = pluginRegistry.get(deviceID);
    Class<?> theClass = Class.forName(plugin);
    Constructor<?> constructor = theClass.getConstructor();
    DevicePlugin devicePlugin = (DevicePlugin)constructor.newInstance();
    devicePlugin.assess();
}
```

Pulling the cyclomatic complexity out of the core into independent plug-ins improves extensibility (adding a new device is adding a plug-in plus a registry entry), maintainability, and [[cyclomatic-complexity|testability]] — each device's rules can be tested in isolation.

### Variations of the core

The core itself can be structured several ways (source: chapter-12-microkernel-architecture-style.md):

- **Layered** — a traditional [[layered-architecture]] inside the core.
- **Modular monolith** — a [[modular-monolith]] with internal module boundaries.
- **Split into domain services** — each domain service is its own core with its own plug-ins. The chapter's example is a Payment Processing domain service with plug-ins for credit card, PayPal, store credit, gift card, and purchase order.

Regardless of which shape the core takes, **the whole monolithic application typically shares a single database**.

The presentation layer can be embedded in the core or implemented as a separate UI calling the core as a backend — and that separate UI can itself be a microkernel architecture.

## Plug-in components

Plug-ins are **standalone, independent components** containing specialized processing, additional features, and custom code. They also serve to **isolate highly volatile code** — variability that changes often — for better maintainability and testability (source: chapter-12-microkernel-architecture-style.md).

Two rules of plug-in discipline:

- **Plug-ins should be independent of each other** with no dependencies between them. A plug-in is a leaf in the dependency graph.
- **Communication between a plug-in and the core is typically point-to-point** — a method invocation or function call to the plug-in's entry-point class.

### Compile-based vs runtime-based

Plug-ins are either compile-based or runtime-based (source: chapter-12-microkernel-architecture-style.md):

- **Compile-based** plug-ins are simpler to manage but require the entire monolithic application to be redeployed when a plug-in is modified, added, or removed.
- **Runtime-based** plug-ins can be added or removed at runtime without redeploying the core or other plug-ins. They are typically managed through frameworks: **OSGi** (Open Service Gateway Initiative), **Penrose**, or **Jigsaw** for Java; **Prism** for .NET.

### Point-to-point plug-in packaging

Point-to-point plug-ins are implemented one of two ways (source: chapter-12-microkernel-architecture-style.md):

1. **Shared libraries** — a JAR (Java), DLL (.NET), Gem (Ruby), etc. The name of the library typically matches the domain name of the plug-in (e.g. `iphone6s.jar`).
2. **Namespaces or package names** within the same codebase or IDE project. The chapter recommends the semantic convention `app.plugin.<domain>.<context>` — e.g. `app.plugin.assessment.iphone6s`. The second node (`plugin`) makes it explicit that the component must adhere to plug-in rules (self-contained, no dependencies on other plug-ins); the third node names the domain; the fourth names the specific context.

### Remote plug-in access

Plug-ins don't *have* to be point-to-point. The core can invoke plug-ins remotely — **REST** or **messaging**, with each plug-in implemented as a standalone service or microservice (source: chapter-12-microkernel-architecture-style.md). Remote access buys:

- **Better component decoupling** between core and plug-ins.
- **Better scalability and throughput** at the plug-in tier.
- **Runtime changes** without needing OSGi/Jigsaw/Prism.
- **Asynchronous communication** — the core fires off an assessment request and is notified back when the plug-in completes, allowing the user to continue interacting with the application.

And pays:

- **It turns the architecture into a distributed one**, with everything Chapter 9 catalogues as distribution cost ([[fallacies-of-distributed-computing]], distributed deployment complexity, operational overhead). This makes remote plug-ins **difficult for most third-party on-prem products**, which is the style's sweet spot in the first place.
- **If a plug-in is unreachable (especially over REST), the request cannot complete.** A monolithic deployment does not have this failure mode.
- **The architecture is still a single [[architectural-quantum|quantum]]** despite being distributed — every request must still go through the core to get to the plug-in. The distribution buys throughput, not multiple independently-deployable units with independently-tunable characteristics.

Whether to go point-to-point or remote is a **trade-off analysis** ([[trade-off-analysis]]) driven by specific requirements.

### Data ownership

Plug-ins do *not* typically connect directly to the core's shared database. The core passes whatever data is needed into the plug-in as a parameter. The reason is decoupling: a database change should affect only the core, not the plug-ins (source: chapter-12-microkernel-architecture-style.md).

Plug-ins *can* have their own separate data stores accessible only to them — an in-memory store, an embedded database, or a rules-engine database containing the plug-in's domain-specific rules. Each device-assessment plug-in owning its own rules database is the chapter's worked example.

## Plug-in registry

The core system needs to know **which plug-ins are available** and **how to reach them**. The mechanism is a **plug-in registry** (source: chapter-12-microkernel-architecture-style.md).

A registry entry contains, per plug-in, everything the core needs to invoke it:

- **name** of the plug-in,
- **data contract** (input and output),
- **contract format** (XML, JSON, objects),
- **remote-access protocol details** if the plug-in isn't point-to-point (queue name, URL).

The chapter's tax-software example: a plug-in `AuditChecker` that flags high-risk tax-audit items has a registry entry containing its name, input/output data contract, and contract format (XML).

Implementation can be as simple as an in-memory map inside the core, or as elaborate as an external discovery tool — **Apache ZooKeeper** or **Consul** are the chapter's named examples. The minimal form in Java:

```java
Map<String, String> registry = new HashMap<String, String>();
static {
    // point-to-point access
    registry.put("iPhone6s", "Iphone6sPlugin");
    // messaging
    registry.put("iPhone6s", "iphone6s.queue");
    // REST
    registry.put("iPhone6s", "https://atlas:443/assess/iphone6s");
}
```

Three different remote-access styles, one registry abstraction. The core calls `registry.get(deviceID)` and is shielded from whether the plug-in is a class, a queue, or a URL.

## Plug-in contracts

The **contract** between a plug-in and the core is the interface through which they communicate: **behaviour, input data, output data** (source: chapter-12-microkernel-architecture-style.md).

Contracts are typically **standard across a domain of plug-ins** — every device-assessment plug-in implements the same `AssessmentPlugin` interface, so the core has one code path for all of them. Contracts are implemented as:

- **Language interfaces** (Java `interface`, C# `interface`, abstract base classes).
- **XML or JSON schemas** for out-of-process plug-ins.
- **Plain objects** passed back and forth.

The chapter's example interface:

```java
public interface AssessmentPlugin {
    public AssessmentOutput assess();
    public String register();
    public String deregister();
}

public class AssessmentOutput {
    public String assessmentReport;
    public Boolean resell;
    public Double value;
    public Double resellPrice;
}
```

The plug-in returns a formatted assessment report, a `resell` flag, and — if resellable — the item's value and a recommended resell price. Notice what the contract **does not require**: the core does not know how to format or understand the report. The plug-in owns the report's content; the core just displays or prints it. That division of responsibility between core and plug-in — the core is generic, the plug-in owns the domain detail — is the architectural heart of the style.

### Third-party plug-ins and adapters

The contract discipline breaks when plug-ins come from a third party and use their own contract shape. The standard fix is an **adapter** between the plug-in's contract and the core's standard contract, so the core does not need specialized code per plug-in (source: chapter-12-microkernel-architecture-style.md). This is the [[adapter-pattern]] at the architecture level: a thin translation layer keeps the core's generic invocation path intact.

## Examples and use cases

### Product-based software

Most software development and release tooling is microkernel (source: chapter-12-microkernel-architecture-style.md): **Eclipse IDE, PMD, Jira, Jenkins** — each is a small core with a plug-in marketplace. **Chrome and Firefox** are the consumer-facing version: viewers and add-ons extend the basic browser.

### Large business applications

The chapter is explicit that microkernel also applies to enterprise applications, and gives two extended examples:

- **Insurance claims processing.** Each jurisdiction has different rules. A monolithic rules engine grows into a big ball of mud where changing one rule affects others. The microkernel answer: **per-jurisdiction plug-ins** containing that jurisdiction's claims rules (as source code or as a rules-engine instance). Rules can be added, removed, or changed for one jurisdiction without impacting any other. New jurisdictions can be added without impacting existing ones. The core is the standard claim-filing-and-processing process, which changes rarely.
- **Tax-preparation software.** The US 1040 form is a two-page summary with each line representing a number derived from other forms and worksheets. **The 1040 is the core**; **each supporting form and worksheet is a plug-in**. Tax-law changes get isolated to the affected plug-in. New forms are added as new plug-ins; obsolete forms are unplugged.

The pattern in both: **domain variability on a clean axis** (jurisdiction, form) and a **stable core process**. That is when microkernel earns its keep on a business application.

## Architecture characteristics ratings

The chapter's scorecard (source: chapter-12-microkernel-architecture-style.md).

| Characteristic | Rating | Why |
|---|---|---|
| **Simplicity** | ★★★★★ | Core + plug-ins is an easy mental model |
| **Overall cost** | ★★★★★ | Monolithic; no distribution tax |
| **Modularity** | ★★★ | Plug-ins are independent, self-contained units of modularity |
| **Extensibility** | ★★★ | Add/remove plug-ins without touching the core — the style's signature strength |
| **Testability** | ★★★ | Plug-in isolation reduces the scope of change-induced retesting |
| **Deployability** | ★★★ | Runtime plug-ins can be deployed without redeploying the core; compile-based plug-ins still require a full redeploy |
| **Reliability** | ★★★ | Functional isolation reduces deployment risk |
| **Performance** | ★★★ | Microkernel apps stay small; dodges the layered [[layered-architecture|sinkhole]] antipattern; unneeded features can be unplugged (Wildfly is the chapter's example of unplugging clustering/caching/messaging for speed) |
| **Availability** | ★★ | Monolithic deployment; same MTTR ceiling as other monolithic styles |
| **Scalability** | ★ | Single quantum — the core is the chokepoint |
| **Elasticity** | ★ | Same reason |
| **Fault tolerance** | ★ | A core-system failure takes everything with it |

**Quantum count**: one. All requests must go through the core to reach a plug-in — even the remote-plug-in variant is still one quantum because the core is the mandatory hop.

### The style's distinctive shape

Two things make the microkernel scorecard distinct from the preceding Part II styles ([[layered-architecture]], [[pipeline-architecture]]):

- **Extensibility and modularity are actual strengths**, not just middling ratings. Plug-ins *are* units of modularity; plug-ins are *how* you extend. That's a different profile from layered (where modularity is poor because the layers are technically partitioned) and pipeline (where modularity is good at the filter level but the whole thing is still one deployment unit).
- **Microkernel is the only style that can be both technically and domain partitioned simultaneously**. The core is technically partitioned (it's the happy-path machinery); the plug-ins are domain partitioned (one per device, per form, per jurisdiction). This is what Richards and Ford call a **strong domain-to-architecture isomorphism** — the domain's natural axis of variability (device type, form number, jurisdiction) maps directly onto the plug-in decomposition.

## When to use it

The scorecard and the chapter's examples together imply:

- **Product-based software with user-customizable variability** — IDEs, browsers, project-tracking tools. The whole reason the style exists.
- **Enterprise applications with a clean axis of variability** — per-jurisdiction rules, per-form processing, per-customer customization, per-device logic. If the variability fits on one axis and the core process is stable, microkernel is the right shape.
- **Applications where feature-extensibility is a user-facing value proposition** — a marketplace of plug-ins that third parties can build against a published contract.
- **Third-party on-prem deployment** — monolithic packaging makes install-on-customer-site realistic. Distributed styles do not.
- **Cost and simplicity dominate the characteristic priority list** — same top-of-scorecard shape as layered and pipeline.

## When not to use it

- **Elasticity, scalability, or fault tolerance are critical.** All three are one-star. The core is a single deployment and a single chokepoint.
- **The variability does not fit on a clean axis.** If every "plug-in" ends up needing to call every other plug-in, the discipline has already failed — you have a modular monolith at best, a big ball of mud at worst.
- **The system has many independent business domains, each with their own lifecycle.** That is a [[microservices]]-shaped problem, not a microkernel one.

## Relationship to other concepts

- **[[layered-architecture]]** — monolithic sibling. Microkernel beats layered on extensibility and modularity (plug-in granularity vs layer granularity); the two are close on cost and simplicity. Microkernel's core may *itself be* layered internally.
- **[[pipeline-architecture]]** — monolithic sibling. Pipeline is flow-shaped, microkernel is core-plus-variability-shaped. Both are single-quantum.
- **[[monolithic-vs-distributed]]** — microkernel sits on the monolithic side. The remote-plug-in variant crosses the line into distributed but *remains a single quantum* — the distinction between "physically distributed" and "architecturally distributed" that Chapter 9 introduces.
- **[[technical-vs-domain-partitioning]]** — microkernel is uniquely **both**: core = technical, plug-ins = domain. The only Part II style with this property.
- **[[architectural-quantum]]** — microkernel is a quantum of one. Every request must go through the core.
- **[[components]]** — microkernel has exactly two component types: core and plug-in. The architect's design job is drawing that line correctly: what stays in the core and what becomes a plug-in is the dominant decision.
- **[[modular-monolith]]** — a well-factored microkernel core can *be* a modular monolith internally; they are compatible shapes.
- **[[adapter-pattern]]** — used to bridge third-party plug-ins with non-standard contracts to the core's standard contract.
- **[[zookeeper]]** — named as an external implementation of the plug-in registry when an in-memory map isn't sufficient.
- **[[cyclomatic-complexity]]** — the driving motivation for pulling logic out of the core into plug-ins is to reduce the core's cyclomatic complexity.

## Related pages

- [[layered-architecture]]
- [[pipeline-architecture]]
- [[monolithic-vs-distributed]]
- [[technical-vs-domain-partitioning]]
- [[architectural-quantum]]
- [[components]]
- [[modular-monolith]]
- [[adapter-pattern]]
- [[cyclomatic-complexity]]
- [[fallacies-of-distributed-computing]]
- [[trade-off-analysis]]
- [[fundamentals-of-software-architecture]]
