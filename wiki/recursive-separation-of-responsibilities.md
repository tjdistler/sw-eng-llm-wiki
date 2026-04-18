# Recursive Separation of Responsibilities

**Summary**: Chapter 14's organising principle for the incident management framework. Each participant has a clear role and stays in it; if a role becomes overloaded, the holder asks the planning lead for help and **delegates** — possibly by creating sub-incidents or by handing system components to colleagues who report up. The "recursive" qualifier captures that the structure can subdivide indefinitely as scale demands, using the same delegation pattern at every level.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`

**Last updated**: 2026-04-17

---

## The principle

> It's important to make sure that everybody involved in the incident knows their role and doesn't stray onto someone else's turf. (source: chapter-14-managing-incidents.md)

The counterintuitive claim Chapter 14 makes: a *clear* separation of responsibilities **increases** autonomy rather than constraining it. When you know exactly what is yours, you can act on it without second-guessing your colleagues; when boundaries are fuzzy, every action requires a coordination check.

This is the structural answer to two of the three [[unmanaged-incident-anti-patterns|unmanaged-incident anti-patterns]]: it prevents the freelancing that makes things worse (Malcolm's CPU-affinity change in the opening case study) and surfaces the communication that ad-hoc structures suppress.

## Recursion

The "recursive" in the name is doing real work. Two recursion patterns:

**Vertical**: when a role's holder is overloaded, they delegate. They ask the planning lead for more staff. Then they assign sub-tasks to those staff — possibly by creating *sub-incidents* with their own commanders that report up to the parent IC.

**Horizontal**: a role leader can delegate **system components** to colleagues. Each colleague becomes effectively the "ops lead for component X", reporting high-level information back up to the actual ops lead, who passes the rolled-up state to the IC.

In both cases, the same role vocabulary (commander / ops / comms / planning) applies at every level. The framework scales by *self-similar subdivision*, not by adding new role types.

## The default: IC holds everything not delegated

Chapter 14 names a useful invariant (source: chapter-14-managing-incidents.md):

> De facto, the commander holds all positions that they have not delegated.

This makes the early-incident state simple: one person in charge of everything until they hand pieces off. As the incident grows, delegations accumulate explicitly. This is a different design from "the commander coordinates several independent specialists" — there is never a moment where it's unclear *who* is responsible for, say, communications, even if the IC hasn't actually done any communication yet.

## Why this is hard for engineers

Engineers being engineers, the natural failure mode is the one Chapter 14's opening case illustrates: a colleague who notices a problem dives in to fix it without coordination. Their intent is good; their effect is to introduce uncoordinated changes that the ops lead cannot reason about.

The fix is cultural as much as procedural: the framework is only as effective as the team's discipline in *staying in their role* — including the discipline to **escalate up** rather than expand sideways when overloaded. The Chapter 14 best-practices "Trust" item directs the same point from the other direction: leaders give full autonomy *within* the assigned role, which is the contract that makes staying in role worthwhile.

## The four roles

Each delegated to a specific page:

- [[incident-commander]] — the apex; holds the high-level state; structures the response.
- [[incident-ops-lead]] — applies operational tools; the *only* group permitted to modify the system during an incident.
- [[incident-communications-lead]] — public face; periodic updates to the team and stakeholders.
- [[incident-planning-lead]] — longer-term concerns: bugs filed, dinners ordered, handoffs arranged, divergence from norms tracked for later reversal.

## Cross-book connection

- The pattern is structurally similar to [[modularity]] applied to humans: well-bounded units with explicit interfaces compose better than loosely-bounded ones.
- The "stay in your lane" discipline is the human-scale analogue of [[bulkhead|bulkheading]]: failure (overload) in one role is contained, and the system as a whole stays functional.
- It is also a form of [[architecture-governance]] applied to incident response — the rules of who-does-what are the response-side fitness functions.

## Related pages

- [[incident-management-framework]]
- [[incident-command-system]]
- [[incident-commander]]
- [[incident-ops-lead]]
- [[incident-communications-lead]]
- [[incident-planning-lead]]
- [[unmanaged-incident-anti-patterns]]
