# Declaring an Incident

**Summary**: Chapter 14's argument that the threshold for invoking the [[incident-management-framework]] should be **low**, with explicit pre-agreed criteria. Spinning the framework up unnecessarily is cheap; spinning it up too late, after a problem has already grown out of control, is expensive. The chapter offers three trigger questions and a separate recommendation that teams use the framework on planned operations to keep their muscle memory fresh.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`

**Last updated**: 2026-04-17

---

## The bias

> It is better to declare an incident early and then find a simple fix and close out the incident than to have to spin up the incident management framework hours into a burgeoning problem. (source: chapter-14-managing-incidents.md)

The asymmetry is the core argument. Declaring early and resolving quickly costs:

- A few minutes of coordination overhead.
- An email thread that fizzles out.
- A short [[live-incident-state-document|incident document]] that becomes a footnote.

Declaring late costs:

- Hours of uncoordinated debugging.
- A [[unmanaged-incident-anti-patterns|narrow technical focus]] that misses bigger pictures.
- Stakeholders who learn about the outage from customers, not from the response team.
- A postmortem that has to reconstruct what people were doing during the chaotic period.

So Chapter 14's prescription is: **default to declaring**.

## The three questions

> My team follows these broad guidelines — if any of the following is true, the event is an incident: (source: chapter-14-managing-incidents.md)
>
> - Do you need to involve a second team in fixing the problem?
> - Is the outage visible to customers?
> - Is the issue unsolved even after an hour's concentrated analysis?

Each is a tripwire calibrated to a different risk dimension:

- **Second team needed** → coordination is now the bottleneck, not skill. The framework's roles and command post are exactly what you need.
- **Customer-visible** → external stakeholders (PR, support, sales) have legitimate interests; communications need the dedicated [[incident-communications-lead|comms lead]] role.
- **One-hour rule** → the outage has outlived the "I'll have it fixed in a minute" assumption. The response is going to be long enough that coordination overhead amortises across multiple shifts and handoffs.

## Set the criteria in advance

The author phrases this carefully — *my team follows these broad guidelines* — because the right thresholds depend on the service. A consumer-facing search engine and an internal batch pipeline have radically different "customer-visible" tests. The point is not the specific three questions but that **the criteria exist before the incident**, so the on-call engineer doesn't have to negotiate with themselves at 3am about whether this counts.

## Use the framework on non-incidents to stay fluent

> Incident management proficiency atrophies quickly when it's not in constant use. So how can engineers keep their incident management skills up to date — handle more incidents? Fortunately, the incident management framework can apply to other operational changes that need to span time zones and/or teams. (source: chapter-14-managing-incidents.md)

The chapter proposes two ways to stay sharp:

- **Use the framework for planned operational changes** that span teams or time zones. Large rollouts, datacentre migrations, and multi-team config changes are natural fits — the coordination problem is the same shape, even if there's no outage.
- **Disaster-recovery testing** ([Kri12]) — incident management should be part of the test process. Role-play the response to a previously-solved on-call issue (perhaps from another office) so people practise the framework on a known story.

This connects directly to [[operational-underload]]: a quiet system erodes the team's response capabilities. Planned and rehearsed use of the framework is one of the [[operational-underload|antidotes]].

## Cross-book connection

- The "declare early" rule is the incident-management form of [[triage-sre|stop the bleeding first]] applied to the meta-level: declaring is the first triage decision, made about whether the response itself needs structure, before any technical triage happens.
- Pre-agreeing the criteria is the same discipline as setting [[service-level-objective|SLOs]] before they're tested in production: do the policy-making in calm, not in crisis.
- Using the framework on planned operations to stay fluent is the same logic as DiRT exercises in [[operational-underload]] and Wheel of Misfortune in [[on-call-playbook]].

## Related pages

- [[incident-management-framework]]
- [[unmanaged-incident-anti-patterns]]
- [[incident-commander]]
- [[operational-underload]]
- [[on-call-playbook]]
- [[triage-sre]]
