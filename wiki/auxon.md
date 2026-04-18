# Auxon

**Summary**: Google's in-house tool for [[intent-based-capacity-planning|intent-based capacity planning]] and resource allocation — Chapter 18's worked case study of SRE-led software development. Auxon replaces manual spreadsheet bin-packing with an [[intent-based-capacity-planning|intent-based]] mixed-integer linear program; it is used to plan the use of many millions of dollars of machine resources and is a critical component for several of Google's largest divisions.

**Sources**: `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`

**Last updated**: 2026-04-17

---

## Origin

Auxon was conceived by an SRE and a technical program manager who had each been tasked by their respective teams with capacity planning large portions of Google's infrastructure. Both had suffered through manual spreadsheet bin-packing and understood the inefficiencies and automation opportunities firsthand (source: chapter-18-software-engineering-in-sre.md). It was built by a small team of software engineers plus the TPM over the course of two years.

The firsthand-experience origin is not incidental — it's the chapter's thesis. See [[software-engineering-in-sre]].

## What Auxon does

Auxon accepts an **intent-based description** of a set of services — requirements like "my service must be N + 2 per continent" or "frontend servers must be no more than 50 ms away from the backend servers" — and emits an **allocation plan** that prescribes which resources go to which services in which locations (source: chapter-18-software-engineering-in-sre.md).

Input is a mix of human-readable configuration (the Intent Config) and programmatic API. Prioritisation is expressible: if resources are insufficient to meet every requirement, higher-priority ones are satisfied first and the plan records which requirements could not be met.

Internally, the intent is represented as a **giant mixed-integer or linear program**, solved to produce the allocation. The resulting plan is the "computed implementation details" of the intent-based description.

## Architecture

Chapter 18's Figure 18-1 has seven labelled components (source: chapter-18-software-engineering-in-sre.md):

### Performance Data

How a service scales: for every unit of demand X in cluster Y, how many units of dependency Z are used? Derived from load tests for mature services, or inferred from past behaviour for less mature ones. This is the glue between dependencies — it converts one resource type into another.

### Per-Service Demand Forecast Data

The usage trend for each demand signal — for example, queries per second broken down by continent. Not every service has a forecast of its own; storage services like [[colossus|Colossus]] derive their demand purely from the services that depend on them.

### Resource Supply

Base-level resource availability — the number of machines expected to be available at a particular future point. In the linear program, this acts as the **upper bound**: services can be placed and grown only to the extent the supply allows.

### Resource Pricing

Base-level resource cost — machines may be more expensive in some facilities due to space/power charges. In the linear program, pricing feeds the **objective** to be minimised: make the cheapest allocation that meets the intent.

### Intent Config

The human-configurable, human-readable definition of what constitutes a service and how services relate to each other. This is the key coupling layer — it lets all the other components be wired together without requiring any one of them to be the authoritative model.

### Auxon Configuration Language Engine

Translates the Intent Config into a machine-readable **optimisation request** (a protocol buffer) consumable by the solver. Performs light sanity checking. This is the gateway between human-configurable intent and machine-parseable constraint.

### Auxon Solver

The brain. Formulates and solves the mixed-integer or linear program. Designed to be highly scalable — it runs in parallel across hundreds or thousands of machines in Google's clusters. Includes not just MIP toolkits but scheduling, worker-pool management, and decision-tree traversal components.

Auxon's early version used a simplified "Stupid Solver" that applied heuristics rather than real optimisation; the solver interface was abstracted so it could later be swapped. See [[sre-software-development-lessons]] for why.

### Allocation Plan

The output. Prescribes which resources should be allocated to which services in which locations. Includes information about any unmet requirements — unsatisfied due to lack of resources or because competing requirements were too strict.

## The decoupling strategy

Auxon's design is deliberately "agnostic" — the Allocation Plan is universally useful rather than integrated with a specific rollout automation tool, forecasting tool, or performance-data tool. Customers can onboard without switching away from their existing upstream and downstream tools (source: chapter-18-software-engineering-in-sre.md). This is the single most important adoption lever and a recurring theme in the chapter. See [[sre-software-development-lessons]].

Similarly, the machine-performance model was hidden behind an interface so customers could plug in different models of future machine power; later, a simple default library was provided behind the same interface.

## Team dynamics

The Auxon team combined generalists (who could come up to speed quickly on linear programming, an unfamiliar domain) with a TPM, and eventually added specialists in statistics and mathematical optimisation as the project matured (source: chapter-18-software-engineering-in-sre.md). Chapter 18's rule: bring in specialists only after the basic product is working and demonstrably useful; adding them earlier skews design toward finesse before the foundations are solid.

The Auxon team stayed on call for services they supported throughout development — they were both consumer and developer of their own product. This is the embedding discipline Chapter 18 argues is non-negotiable for SRE-developed software.

## Cross-book connections

Auxon is a worked example of several patterns catalogued elsewhere in the wiki:

- [[desired-state-management]] (Newman) — the Allocation Plan is a declarative desired state; the automation systems that enact it are the reconcilers. Auxon is the intent-spec side of the same separation.
- [[architecture-fitness-function]] (Richards & Ford) — the intent-as-linear-program reduces capacity planning to an objective automatable computation; each unsatisfied-requirement report is a fitness-function violation
- [[capacity-planning]] — Auxon is the industrial-scale implementation of the demand-and-load capacity-planning loop
- [[scaling-approaches]] (Kleppmann) — bin-packing across heterogeneous supply is the concrete problem Auxon solves

## Related pages

- [[intent-based-capacity-planning]]
- [[traditional-capacity-planning]]
- [[software-engineering-in-sre]]
- [[sre-software-development-lessons]]
- [[sre-product-adoption]]
- [[capacity-planning]]
- [[desired-state-management]]
