# Divide and Conquer Debugging

**Summary**: Chapter 12's generic techniques for the Diagnose phase when deep system knowledge isn't enough: simplify-and-reduce to get a reproducible test case, divide-and-conquer (or bisect) a multi-layer system, ask **what / where / why** iteratively, and check **what touched it last**. These work without domain knowledge and often surface the problem faster than first-principles reasoning.

**Sources**: `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`

**Last updated**: 2026-04-17

---

## The four Diagnose-phase techniques

Chapter 12 explicitly presents these as "generic practices that will help even without domain knowledge" (source: chapter-12-effective-troubleshooting.md). Deep system understanding beats them; in its absence, they work.

1. **Simplify and reduce.**
2. **Divide and conquer / bisect.**
3. **Ask what, where, why.**
4. **What touched it last.**

## Simplify and reduce

The key insight (source: chapter-12-effective-troubleshooting.md):

> Ideally, components in a system have well-defined interfaces and perform known transformations from their input to their output. It's then possible to look at the connections between components — or, equivalently, at the data flowing between them — to determine whether a given component is working properly.

The technique has two forms:

- **Black-box testing at every step.** Inject known test data at a component boundary and verify the output against the expected transformation. This localises the fault to a specific component.
- **Adversarial data injection.** Inject data specifically designed to probe suspected error modes.

The chapter emphasises the payoff of a **reproducible test case** (source: chapter-12-effective-troubleshooting.md):

> Having a solid reproducible test case makes debugging much faster, and it may be possible to use the case in a nonproduction environment where more invasive or riskier techniques are available than would be possible in production.

A reproducer converts the problem from an observation-only activity (you can only look at production) into an experimental one (you can instrument, modify, re-run).

## Divide and conquer

For a multi-layer stack, Chapter 12 recommends starting at one end and working toward the other (source: chapter-12-effective-troubleshooting.md):

> In a multilayer system where work happens throughout a stack of components, it's often best to start systematically from one end of the stack and work toward the other end, examining each component in turn. This strategy is also well-suited for use with data processing pipelines.

Linear scan is O(n) in the number of components. For very large systems the chapter recommends **bisection**:

> An alternative, bisection, splits the system in half and examines the communication paths between components on one side and the other. After determining whether one half seems to be working properly, repeat the process until you're left with a possibly faulty component.

Bisection is O(log n). The technique is the same one that works for `git bisect`: divide the suspect set in half; test the midpoint; recurse into the half containing the fault.

The prerequisite is **observable communication paths between components** — which Chapter 12 calls out as a design discipline in [[making-troubleshooting-easier]]: well-defined, observable interfaces between components make divide-and-conquer possible at all.

## Ask what, where, why

Chapter 12's formulation (source: chapter-12-effective-troubleshooting.md):

> A malfunctioning system is often still trying to do something — just not the thing you want it to be doing. Finding out what it's doing, then asking why it's doing that and where its resources are being used or where its output is going can help you understand how things have gone wrong.

Three iterative questions:

- **What is it doing?** — not what should it be doing, but what *is* it doing right now.
- **Where are its resources going / where is its output going?** — CPU? Disk? Network? Which output path?
- **Why is it doing that?** — follow the answer back to the code / config / data that produced it.

Chapter 12 explicitly compares this to Taiichi Ohno's **Five Whys** technique (source: chapter-12-effective-troubleshooting.md, citing [Ohn88]). Each answer generates the next question; the chain terminates when the cause is structural enough to fix.

### The Spanner worked example

Chapter 12's illustration (source: chapter-12-effective-troubleshooting.md):

> **Symptom:** A Spanner cluster has high latency and RPCs to its servers are timing out.
> **Why?** The Spanner server tasks are using all their CPU time and can't make progress on all the requests the clients send.
> **Where in the server is the CPU time being used?** Profiling the server shows it's sorting entries in logs checkpointed to disk.
> **Where in the log-sorting code is it being used?** When evaluating a regular expression against paths to log files.
> **Solutions:** Rewrite the regular expression to avoid backtracking. Consider using RE2, which does not backtrack and guarantees linear runtime growth with input size.

Four "where/why" steps from symptom to actionable fix. Each one narrows the suspect scope by an order of magnitude.

## What touched it last

Chapter 12's version of an operational folk wisdom (source: chapter-12-effective-troubleshooting.md):

> Systems have inertia: we've found that a working computer system tends to remain in motion until acted upon by an external force, such as a configuration change or a shift in the type of load served. Recent changes to a system can be a productive place to start identifying what's going wrong.

The chapter's footnote cites Allspaw's observation that this is a frequently-used heuristic in outage resolution. It is also the logic behind the [[change-management-sre|change-management tenet]]: 70% of outages stem from change; therefore the first diagnostic question is always "what changed recently?"

Operationalising the heuristic requires **production logging of changes at every layer of the stack** — server binary versions, configuration pushes, OS package updates on individual nodes. The chapter recommends annotating monitoring dashboards with deployment start/end markers so that performance changes can be visually correlated with deploys.

Having the change timeline ready-to-hand when an incident starts is how "what touched it last" becomes a fast check rather than a half-hour archaeological dig.

## Specific tooling beats general techniques

Chapter 12 closes the Diagnose section by noting that while the generic tools above work broadly, teams should also build **diagnosis tools specific to their services** (source: chapter-12-effective-troubleshooting.md):

> Google SREs spend much of their time building such tools. While many of these tools are necessarily specific to a given system, be sure to look for commonalities between services and teams to avoid duplicating effort.

This is an instance of the [[toil-and-engineering-balance|50% engineering cap]] at work: diagnosis-tool construction is software engineering that reduces future toil and MTTR.

## Cross-book connection

- [[distributed-tracing]] (Newman) — Dapper-style request tracing is divide-and-conquer formalised into infrastructure: each span localises time spent to a specific component, letting you skip straight to the bisected answer.
- [[correlation-ids]] (Newman) — propagated request IDs turn an incident's logs into a reconstructable call tree, which is the precondition for divide-and-conquer on a distributed request.
- [[progressive-delivery]] (Newman / Burns) — canary releases and phased rollouts make "what touched it last" quickly answerable by narrowing the blast radius and the timeline of any new deploy.
- [[modularity]] (Richards & Ford) — well-defined interfaces between components are a precondition for divide-and-conquer debugging; a monolith with implicit coupling resists the technique.

## Related pages

- [[troubleshooting-model]]
- [[hypothetico-deductive-debugging]]
- [[test-and-treat]]
- [[making-troubleshooting-easier]]
- [[change-management-sre]]
- [[distributed-tracing]]
- [[correlation-ids]]
- [[site-reliability-engineering]]
