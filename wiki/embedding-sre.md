# Embedding an SRE

**Summary**: Chapter 30's rescue pattern for an SRE team stuck in [[operational-overload]]: temporarily transfer one experienced SRE into the team, not to help empty the ticket queue but to change how the team thinks about its work. The visiting SRE moves the team from reactive ops to the SRE model through three phases — learn the service, share context, and drive change.

**Sources**: `raw/site-reliability-engineering/chapter-30-embedding-an-sre-to-recover-from-operational-overload.md`

**Last updated**: 2026-04-17

---

## The problem

SRE teams are supposed to split time roughly 50/50 between project work and reactive ops. When daily ticket volume spikes for months at a time, that balance breaks: the team burns out, service reliability and scalability suffer, and the team slides into [[ops-mode]] — more tickets answered by more humans, not by more software (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). This is exactly the trajectory the [[toil-and-engineering-balance|50% cap]] is designed to defend against. Chapter 30 is the chapter-specific rescue.

## Why embed rather than help

The instinct when a team is drowning in tickets is to send help to drain the queue. Chapter 30 explicitly rejects that instinct. The visiting SRE's job is **not to help clear tickets**. Their job is to *articulate why processes and habits contribute to, or detract from, the service's scalability* and to make sure the team internalises the reasoning so it stays fixed after the visit ends (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

The consultation framing matters: the team gets a **fresh perspective on routines they can't see themselves**, because from inside, the oppressive routines look like the job.

## One SRE, not two

Send exactly one embedded SRE. *Two SREs don't necessarily produce better results and may actually cause problems if the team reacts defensively* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). The embedded SRE is a visible outside voice; two of them start to look like a takeover.

## Phase 1: Learn the service and get context

The visiting SRE begins by shadowing on-call and observing the team's daily routine. Two deliverables come out of this phase:

- **A picture of the team's stress sources.** Small problems can produce disproportionate stress because of the team's history with them. Rank the sources by actual stress impact, not by engineer intuition about what should hurt.
- **A list of [[identifying-kindling|kindling]]** — emergencies that haven't happened yet but are structurally guaranteed to, surfaced via seven specific warning signals.

The framing for this phase is [[ops-mode|ops mode versus nonlinear scaling]]: is the team spending humans to absorb load growth (ops mode), or are they engineering the load away (SRE)? The answer dictates strategy. A "my service is tiny" response doesn't excuse ops mode — shadow an on-call session and verify.

## Phase 2: Sharing context

Now that the visiting SRE understands the dynamics, they lay groundwork through practices the team can copy:

- **Write a great postmortem for the team.** There will be an outage during the visit. Co-author the postmortem with the on-call SRE and use it as a demonstration of what a [[blameless-postmortem|blameless postmortem]] looks like. Reviewing old postmortems and leaving comments puts the team on the defensive; writing a new one with them models the target behaviour directly.
- **Sort fires by type.** Two categories: fires that shouldn't exist (they are [[toil-and-engineering-balance|toil]]) and fires that are a real part of running the service. Both need tooling to control the burn, but the category determines the response — automate the first; build playbooks and drills for the second. Present the sorted list to the team with reasoning for each assignment (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

This phase also surfaces the **[[bad-apple-theory]]** — the implicit belief that outages are caused by bad individuals — and replaces it with the system-focused framing that the blameless culture requires.

## Phase 3: Driving change

Team health is a process, not a one-time fix. The visiting SRE's job is to *create (or restore) the right initial conditions and teach the small set of principles needed to make healthy choices* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). Humans are good at homeostasis; a team pointed in the right direction with the right reference principles will mostly stay pointed there.

Four moves drive change:

1. **Start with the basics — write an SLO.** If a team has no [[service-level-objective|SLO]], write one. Chapter 30 is explicit: *an SLO is probably the single most important lever for moving a team from reactive ops work to a healthy, long-term SRE focus. If this agreement is missing, no other advice in this chapter will be helpful.* Get tech leads and management in a room and arbitrate. Without an SLO, every later conversation lacks a quantitative ground.
2. **Get help clearing [[identifying-kindling|kindling]] — but don't fix it yourself.** The urge to dive in and fix the visible problems is strong. Resist it; fixing things yourself *bolsters the idea that "making changes is for other people"*. Instead: find a piece of work one team member can do, explain clearly how it addresses a specific issue from the postmortem in a permanent way, serve as reviewer for the code and doc changes, repeat for two or three issues (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). The remaining issues go into bug reports or docs for the team to work through later.
3. **[[explaining-reasoning|Explain your reasoning]] for every decision, whether or not it's asked for.** The team will copy what they observe. Reasoning that isn't verbalised is reasoning that can't be inherited. The goal: after the visit, *the team should be able to predict what your comment on a design or changelist would be.*
4. **Ask [[leading-questions]].** Rather than correcting bad practices, ask questions that guide the team back to first principles. Examples from the chapter: "I see that the TaskFailures alert fires frequently, but the on-call engineers usually don't do anything to respond to the alert. How does this impact the SLO?" and "This turnup procedure looks pretty complicated. Do you know why there are so many config files to update when creating a new instance of the service?" (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

## Exit: the written after-action report

The embedded engagement ends with a written **after-action report** — Chapter 30 names it a *postvitam* in contrast to a postmortem. The report restates the visiting SRE's perspective, examples, and explanations, and leaves action items the team can exercise on the principles they've been taught (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

The embedded SRE should remain available for design and code reviews afterward, and should *keep an eye on the team for the next few months to confirm that they're slowly improving their capacity planning, emergency response, and rollout processes.*

## Relationship to first-SRE-team bootstrap

The chapter makes a parallel claim at the opening: *if you are starting your first SRE team, the approach outlined in this chapter will help you to avoid turning into an operation team solely focused on a ticket rotation* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). The three-phase structure works both for rescuing an existing team from [[operational-overload]] and for building a new team from scratch without sliding into [[sysadmin-approach|the sysadmin approach]] by default.

## Relationship to giving back the pager

The embedded-SRE remedy and [[operational-overload|giving back the pager]] sit at different points on the same escalation ladder. Embedding is the **constructive intervention**: someone comes in and helps the team change its practices from the inside. Giving back the pager is the **structural escape hatch**: the team refuses the work until the product is automatable. Embedding should be tried first; giving back the pager is for when embedding can't land because the product itself is the problem.

## Connection to the SRE hiring promise

Chapter 30's existence is an acknowledgement that the [[toil-and-engineering-balance|50% cap]] isn't self-enforcing. Teams slide into ops mode organically; the cap tells you *when* you've drifted, but an embedded SRE (or equivalent intervention) is often needed to reverse the drift. The cap is the signal; embedding is one of the remedies.

## Related pages

- [[ops-mode]]
- [[identifying-kindling]]
- [[bad-apple-theory]]
- [[explaining-reasoning]]
- [[leading-questions]]
- [[operational-overload]]
- [[toil-and-engineering-balance]]
- [[blameless-postmortem]]
- [[service-level-objective]]
- [[sre-discipline]]
- [[sysadmin-approach]]
- [[dealing-with-interrupts]]
- [[sre-onboarding]]
- [[error-budget]]
