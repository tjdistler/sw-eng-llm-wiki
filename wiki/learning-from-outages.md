# Learning from Outages

**Summary**: Chapter 13's closing discipline: treat every outage as a learning opportunity and deliberately cultivate the practices that turn learning into change. Three specific prescriptions — keep a written history of outages, ask big open-ended "what if" questions, and encourage proactive testing — compound with [[blameless-postmortem|blameless postmortems]] into an organisational memory that makes the same outage harder to repeat.

**Sources**: `raw/site-reliability-engineering/chapter-13-emergency-response.md`, `raw/site-reliability-engineering/chapter-15-postmortem-culture-learning-from-failure.md`, `raw/site-reliability-engineering/chapter-16-tracking-outages.md`, `raw/site-reliability-engineering/chapter-26-data-integrity-what-you-read-is-what-you-wrote.md`

**Last updated**: 2026-04-17

---

## "All problems have solutions"

Chapter 13's penultimate section makes an empirical claim that's easy to underweight (source: chapter-13-emergency-response.md):

> Time and experience have shown that systems will not only break, but will break in ways that one could never previously imagine. One of the greatest lessons Google has learned is that a solution exists, even if it may not be obvious, especially to the person whose pager is screaming.

The prescription that follows is social rather than technical: **if you can't think of a solution, cast your net farther**. Pull in more teammates. Seek help. The highest priority is to resolve the issue at hand, quickly. Often the person with the most relevant state is the one whose action triggered the event — *utilize that person* rather than exclude them.

The deeper point: heroism-by-silent-suffering is a failure mode. A rapid escalation to more eyes is almost always the right move.

## Keep a history of outages

Chapter 13's first prescription for turning outages into learning (source: chapter-13-emergency-response.md):

> There is no better way to learn than to document what has broken in the past. History is about learning from everyone's mistakes.

The operational requirements:

- **Be thorough, be honest.**
- **Ask hard questions** — not just tactical fixes, but strategic ones that address classes of outages.
- **Publish and organise postmortems** so everyone in the company can learn.
- **Hold people accountable for follow-up actions** — incomplete action items are the primary reason incidents recur.

The last point is the one most easily lost. Writing a postmortem with thirty follow-up actions and then not tracking them produces the illusion of learning without the substance. Chapter 13's implicit standard: an incident is not closed when the service recovers; it is closed when the follow-up actions land.

## Ask the big, improbable questions

Chapter 13's second prescription is a brainstorming discipline (source: chapter-13-emergency-response.md):

> What if the building power fails…? What if the network equipment racks are standing in two feet of water…? What if the primary datacenter suddenly goes dark…? What if someone compromises your web server…?

The questions are deliberately open-ended and push outside normal-operations thinking. For each scenario, the chapter lists the sub-questions that expose preparedness gaps:

- What do you do?
- Who do you call?
- Who will write the check?
- Do you have a plan? Do you know how to react?
- Do you know how your systems will react?
- Could you minimize the impact if it were to happen now?
- **Could the person sitting next to you do the same?**

That last sub-question is the one that catches most teams. Knowledge that lives in one head is a reliability liability. See [[on-call-playbook|playbooks]] for the concrete mitigation — *write down what's in your head, before you leave for vacation*.

## Encourage proactive testing

Chapter 13's third prescription is the one the entire rest of the chapter's case studies argue for: **until the system has actually failed, you don't know how it will respond**. Assumptions and untested theories are unreliable evidence (source: chapter-13-emergency-response.md).

The chapter's rhetorical question is the test for when to schedule a failure drill:

> Would you prefer that a failure happen at 2 a.m. Saturday morning when most of the company is still away on a team-building offsite in the Black Forest — or when you have your best and brightest close at hand, monitoring the test that they painstakingly reviewed in the previous weeks?

Proactive testing trades **a small planned incident now** for **a large unplanned incident later**. This is the DiRT (Disaster Recovery Training) rationale and the Wheel of Misfortune rationale. See [[on-call-playbook]] and [[operational-underload]] for the team-level variants.

## The closing thesis

Chapter 13 ends with the unifying observation across the three case studies:

- Responders didn't panic.
- They pulled in others when they thought it necessary.
- They studied and learned from earlier outages, and subsequently built their systems to better respond to those types.
- Each time new failure modes presented themselves, responders documented them, helping other teams troubleshoot and fortify.
- Responders proactively tested their systems, validating fixes and identifying new weaknesses before they became outages.

Chapter 13's last sentence frames the loop as self-reinforcing: *as systems evolve, the cycle continues, with each outage or test resulting in incremental improvements to both processes and systems*.

The practical claim Google is making: **an organisation that does these things consistently will, over years, run better systems than an organisation that treats each incident as isolated**. The compounding happens through organisational memory, not individual expertise.

## Chapter 15 formalises the practice

Chapter 13 prescribed "keep a history of outages"; Chapter 15 is the chapter that specifies **how** (source: chapter-15-postmortem-culture-learning-from-failure.md). The connections:

- Chapter 13's "publish and organise postmortems" becomes Chapter 15's [[postmortem-review-process|review-and-broadcast pipeline]] with regular review sessions, senior-engineer review, and widest-possible-audience sharing.
- Chapter 13's "hold people accountable for follow-up actions" is the close-out discipline embedded in the Chapter 15 review meeting — which is where incomplete action items from previous postmortems get surfaced.
- Chapter 13's "ask the big, improbable questions" directive is what the [[postmortem-culture-activities|reading clubs]] and [[postmortems-at-google-working-group|trend-analysis workstream]] produce at scale: questions that no single incident could have raised.
- Chapter 13's "encourage proactive testing" is reinforced by Wheel of Misfortune reenactments (Chapter 15 positions Wheel of Misfortune as a postmortem-culture activity) and by the DiRT drills Chapter 11 named.
- Chapter 13's "know what's in the person sitting next to you's head" concern is answered by the wide-audience sharing rule and by the structured template that turns implicit knowledge into explicit records.

Chapter 15 also names the **organisational mechanism** that keeps the discipline alive: the [[postmortems-at-google-working-group|Postmortems at Google working group]] coordinates templates, automates data collection, and runs cross-product trend analysis. Chapter 13 leaves the discipline as a set of norms; Chapter 15 makes it infrastructure.

## Chapter 16 adds the aggregate-record machinery

Chapter 15 formalised postmortem practice — the depth-per-incident side of the history. Chapter 16 supplies the **complementary breadth side**: a tool that captures every alert and outage (not just the significant ones) and supports cross-incident analysis (source: chapter-16-tracking-outages.md).

The mapping back to Chapter 13's directives:

- "Keep a history of outages" → Chapter 15's [[postmortem-review-process|postmortem corpus]] **plus** Chapter 16's outage-archive of all notifications. Postmortems carry depth; the archive carries breadth.
- "Ask hard questions" → Chapter 16's [[outage-analysis|three-layer analysis]] is the mechanism that turns questions like "how many alerts per shift?" and "which infrastructure component causes the most incidents?" from guesses into data.
- "Publish and organise" → Chapter 16's weekly-review "report mode" (important annotations inline) and shift-handoff emails are the aggregate-layer counterparts to postmortem publication.
- "Ask big improbable questions" → semantic layer-3 analysis across teams (e.g., "is replication lag silently behind alerts from four different services?") surfaces cross-cutting unknowns that no single postmortem would.

Chapter 16's one-line thesis — *"improving reliability over time is only possible if you start from a known baseline and can track progress"* — is the same compounding argument Chapter 13 makes, made measurable. Without the tracked baseline, you can't tell whether the follow-up actions actually worked.

The full history-of-outages stack as of Chapter 16:

- An ack-tracking layer; every page flows through it.
- An outage-level archive built on top of it; annotation, grouping, tagging, reporting.
- [[outage-tracking]] — the discipline's hub page.
- [[outage-analysis]] — the three analytic layers plus reporting.
- [[incident-aggregation]] — grouping multiple alerts into incidents so "incidents per day" and "alerts per day" are separate computable numbers.
- [[incident-tagging]] — free-form colon-namespaced metadata that enables cross-team semantic queries.

## Chapter 26 reinforces proactive testing for data integrity

Chapter 26's [[recovery-testing|continuous-recovery-testing]] discipline is a direct application of Chapter 13's "encourage proactive testing" directive to the data-integrity domain (source: chapter-26-data-integrity-what-you-read-is-what-you-wrote.md). The 2011 [[gmail-gtape-restore|Gmail restore]] and a 2012 race-condition-deletion recovery both explicitly credit prior DiRT-tested recovery tooling for making their actual restorations tractable. Chapter 13 frames the rule generically; Chapter 26 supplies the worked examples of the payoff at Google scale, with the added prescription that recovery tests must be **continuous and alerted**, not just annual.

## Connections

- [[blameless-postmortem]] — the written artifact that carries organisational memory. Chapter 13's "keep a history of outages" is the institutional form of the postmortem discipline Chapter 15 formalises.
- [[postmortem-philosophy]] — Chapter 15's full hub for the philosophy and best practices.
- [[postmortem-review-process]] — how the "publish and organise" directive is operationalised.
- [[postmortem-culture-activities]] — Chapter 15's catalogue of social mechanisms (postmortem of the month, reading clubs, Wheel of Misfortune) that keep the history alive.
- [[postmortems-at-google-working-group]] — the central group coordinating postmortem practice across Google.
- [[emergency-response]] — Chapter 13 as a whole; the learning-from-outages section is the chapter's payoff.
- [[on-call-playbook]] — where specific, repeatable learnings get encoded; Wheel of Misfortune and DiRT are the hands-on drills.
- [[operational-underload]] — the failure mode of under-exercised systems; proactive testing is the remedy.
- [[incident-response-mindset]] — the "don't panic, pull in more people" directive connects to the cognitive-load argument from Chapter 11.
- [[test-induced-emergency]], [[change-induced-emergency]], [[process-induced-emergency]] — the three Chapter 13 case studies that illustrate the discipline.
- [[outage-tracking]] — Chapter 16's aggregate-record mechanism; the breadth complement to the postmortem corpus's depth.
- [[outage-analysis]] — the three-layer framework for turning the tracked data into decisions.
- Chaos engineering (industry practice) — the proactive-testing prescription, industrialised via Chaos Monkey-style tools.
- [[unknown-unknowns]] (Richards & Ford) — the epistemic argument: the questions worth asking are the ones that surface unknowns.

## Cross-book connection

- [[architecture-fitness-function]] (Richards & Ford) — follow-up actions from postmortems are candidate fitness functions: each captured failure mode is an opportunity to add an automated check preventing its recurrence.
- [[architecture-decision-record]] (Richards & Ford) — the outage history can feed ADR Consequences sections; decisions whose consequences played out in incidents should be linked back.

## Related pages

- [[emergency-response]]
- [[blameless-postmortem]]
- [[on-call-playbook]]
- [[operational-underload]]
- [[incident-response-mindset]]
- [[test-induced-emergency]]
- [[change-induced-emergency]]
- [[process-induced-emergency]]
- [[unknown-unknowns]]
- [[outage-tracking]]
- [[outage-analysis]]
- [[incident-tagging]]
- [[incident-aggregation]]
- [[data-integrity-sre]]
- [[recovery-testing]]
- [[gmail-gtape-restore]]
