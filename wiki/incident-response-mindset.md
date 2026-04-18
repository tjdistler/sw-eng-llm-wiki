# Incident Response Mindset

**Summary**: Chapter 11's account of how SREs should think during an incident — deliberately, with data, balancing intuition against rational analysis. It draws on Kahneman's System 1 / System 2 framing and the stress-hormone literature to argue that incident response is a cognitive task that degrades under pressure, and that SRE teams should structure the environment (escalation paths, incident-management protocol, blameless postmortems) to keep engineers in the right frame of mind.

**Sources**: `raw/site-reliability-engineering/chapter-11-being-on-call.md`, `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`, `raw/site-reliability-engineering/chapter-13-emergency-response.md`, `raw/site-reliability-engineering/chapter-14-managing-incidents.md`

**Last updated**: 2026-04-17

---

## Two modes of thinking under pressure

Chapter 11 cites Kahneman's dual-process framing (source: chapter-11-being-on-call.md, citing [Kah11]). When faced with a challenge, people choose between two modes:

- **Intuitive, automatic, rapid action** — fast but habitual.
- **Rational, focused, deliberate cognitive function** — slower but supportable by data.

For complex production incidents, the *second* mode produces better outcomes and well-planned incident handling. The challenge is that stress pushes engineers toward the first.

## The stress-hormone trap

Production outages carry real stakes (user-visible failure, revenue-critical systems), which produce cortisol and corticotropin-releasing hormone (CRH) — known to cause behavioural consequences including fear, impaired cognition, and suboptimal decision-making (source: chapter-11-being-on-call.md, citing [Chr09]).

Under these conditions, *deliberate cognitive approach is subsumed by unreflective and unconsidered (but immediate) action*. The engineer abandons analysis for heuristics without realising it.

The named trap is **confirmation bias**: the fourth page in a week looks like the previous three, and the engineer associates it with the same external cause — even when the underlying problem is different. Quick reactions are habit-based, and habits are unconsidered, which makes them disastrous when the situation has actually changed.

## The ideal posture

Chapter 11's prescription (source: chapter-11-being-on-call.md):

> The ideal methodology in incident management strikes the perfect balance of taking steps at the desired pace when enough data is available to make a reasonable decision while simultaneously critically examining your assumptions.

Three verbs: *pace* (don't rush), *examine* (assumptions), *decide* (when data supports it). Intuition isn't banned — it's a useful prior — but it must survive questioning.

## The three supporting resources

Chapter 11 names three resources that reduce the cognitive load on the on-call engineer and make the rational mode easier to sustain (source: chapter-11-being-on-call.md):

### Clear escalation paths

Developer teams of SRE-supported systems typically participate in 24/7 on-call rotations too, so SRE can always escalate. Escalation is the *principled* response to a serious outage with significant unknown dimensions. Knowing an escalation path exists reduces the "I have to solve this alone" pressure that drives poor decisions.

### Well-defined incident-management procedures

When an incident is complex enough to need multiple teams, or when its upper-bound time span is unknowable, Chapter 11 recommends adopting a formal **incident-management protocol** (see Chapter 14). Google's protocol:

- Provides easy-to-follow, well-defined steps.
- Is supported by a web tool that automates role handoffs, status updates, and communication channels.
- Frees the incident manager to focus on the incident instead of formatting emails or updating chat rooms by hand.

The rational mode is expensive; mundane overhead eats the budget for it. Offloading the overhead to tooling preserves the budget for the thinking.

### Blameless postmortem culture

Knowing that post-incident analysis will focus on *events* rather than *people* reduces the fear of making a mistake during the incident itself. See [[blameless-postmortem]].

## Why this matters for SRE engagement

Chapter 11's framing is that on-call is not just an availability problem — it's a **human factors** problem. Systems that optimise only for availability SLO and ignore the mental state of the engineer running them will pay for it in worse decisions under pressure, more broken humans, and eventually more broken systems.

## The cognitive failures Chapter 12 names (Chapter 12)

Chapter 12's [[troubleshooting-anti-patterns|common pitfalls]] section catalogues the specific ways the stress-induced cognitive degradation described above manifests during troubleshooting (source: chapter-12-effective-troubleshooting.md):

- **Latching onto causes of past problems** — "since it happened once, it must be happening again" is confirmation bias in explicit hypothesis form. The fourth page in a week looks like the previous three and the engineer jumps.
- **Wildly improbable theories** — System 1 grabs the first plausible story; the rational System 2 check for base-rate likelihood ("horses not zebras") is skipped.
- **Hunting spurious correlations** — noticing that two things happened at the same time feels like insight; without a *mechanism* connecting them, it is only a hypothesis to test.
- **Misreading metrics** — stress narrows attention to familiar patterns; novel meanings of a metric (e.g. a counter reset) are missed.

Chapter 12's antidote is the same as Chapter 11's: *pace, examine assumptions, decide when data supports it*. Slowing down restores access to deliberate reasoning. Chapter 12 adds the operational tools for doing the examining — [[divide-and-conquer-debugging|what/where/why iteration]], [[test-and-treat|experiment design with five considerations]], and [[hypothetico-deductive-debugging|knowing what you know vs don't know vs need to know]].

Naming the cognitive failures is most of the defence. An SRE who recognises "I'm latching onto the previous cause because I'm stressed" in the moment can catch the error; an SRE who doesn't have the name can't.

## The operational directives (Chapter 13)

Chapter 13's opening gives the practitioner's checklist that the cognitive-load argument above theoretically justifies (source: chapter-13-emergency-response.md):

- **Don't panic.** You're not alone. The sky isn't falling. At the very worst, half of the Internet is down. Take a deep breath.
- **Pull in more people if overwhelmed.** Sometimes paging the entire company is the right move. Chapter 13's [[learning-from-outages|all-problems-have-solutions]] section sharpens this: "if you can't think of a solution, cast your net farther."
- **Follow the incident-response process.** If one exists, use it. If you don't know it, that's the first gap to close — the [[test-induced-emergency|Chapter 13 MySQL case study]] nearly went much worse because the on-call engineers weren't familiar with an incident-response process that had been introduced a few weeks earlier.
- **Utilize the person who triggered the event.** They usually have the most context. Exclusion-by-blame is the opposite of what the situation demands — an explicit connection to the [[blameless-postmortem|blameless]] discipline.

These are the verbs-for-the-first-minute versions of Chapter 11's *pace, examine, decide*. Chapter 13 phrases them for the person who's just been paged.

## The framework as cognitive offload (Chapter 14)

Chapter 11's prescription named "a well-defined incident-management protocol" as one of the three supporting resources for staying rational; Chapter 14 is the protocol it referred to forward. The relationship is direct (source: chapter-14-managing-incidents.md):

- **Defined roles** ([[incident-commander]], [[incident-ops-lead]], [[incident-communications-lead]], [[incident-planning-lead]]) mean the on-call engineer doesn't have to *also* solve the coordination problem while solving the technical problem. The IC holds the bigger picture so the ops lead doesn't have to context-switch out of debugging to think about it.
- **A [[recognized-command-post|recognised command post]]** means stakeholders have one place to look. The on-call engineer is no longer interrupted by VPs demanding ETAs — Chapter 14's opening unmanaged-incident case is exactly the failure mode Chapter 11 predicts under stress hormones.
- **A [[live-incident-state-document|living incident document]]** means newly-arrived responders can self-orient instead of consuming the original responders' attention. This is the offload Chapter 11 referred to as "automating role handoffs and status updates".
- **The [[incident-handoff|explicit handoff]] protocol** removes the "who's in charge?" ambiguity that Chapter 11 warns about — uncertainty about responsibility is itself a stress amplifier.

Chapter 14's best-practice "**Introspect**" item is also a literal reference back to this page: *"Pay attention to your emotional state while responding to an incident. If you start to feel panicky or overwhelmed, solicit more support."* The framework gives the responder a structured *action* to take when they notice the stress signal — pull in more people, escalate the IC role, declare an incident if one hasn't been.

## Cross-book connection

The framing — optimise the environment so humans make better decisions — is the organisational analogue of the [[simplicity-sre|simplicity]] argument: minimise accidental cognitive load so the essential cognitive work has room to happen.

## Related pages

- [[sre-on-call-engagement]]
- [[balanced-on-call]]
- [[blameless-postmortem]]
- [[emergency-response]]
- [[on-call-playbook]]
- [[operational-overload]]
- [[sre-tenets]]
- [[troubleshooting-model]]
- [[troubleshooting-anti-patterns]]
- [[hypothetico-deductive-debugging]]
- [[learning-from-outages]]
- [[test-induced-emergency]]
- [[change-induced-emergency]]
- [[incident-management-framework]]
- [[incident-commander]]
- [[recognized-command-post]]
- [[live-incident-state-document]]
- [[incident-handoff]]
