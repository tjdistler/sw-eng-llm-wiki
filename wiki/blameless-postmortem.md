# Blameless Postmortem

**Summary**: A written investigation of a significant incident whose goal is to expose faults and apply engineering to fix them, not to assign blame. Google writes postmortems for all significant incidents regardless of whether they paged — non-paging ones are arguably more valuable because they reveal monitoring gaps.

**Sources**: `raw/site-reliability-engineering/chapter-01-introduction.md`, `raw/site-reliability-engineering/chapter-11-being-on-call.md`, `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`, `raw/site-reliability-engineering/chapter-13-emergency-response.md`, `raw/site-reliability-engineering/chapter-14-managing-incidents.md`, `raw/site-reliability-engineering/chapter-15-postmortem-culture-learning-from-failure.md`, `raw/site-reliability-engineering/chapter-30-embedding-an-sre-to-recover-from-operational-overload.md`, `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## What a postmortem is for

Postmortems should be written for all significant incidents, and each should (source: chapter-01-introduction.md):

- Establish **what happened, in detail**.
- Find **all root causes** of the event.
- **Assign actions** to correct the problem or improve the response next time.

The output is documented learning and a set of follow-up work items.

## Blameless culture

Google operates under a **blameless postmortem culture**, with the goal of *exposing faults and applying engineering to fix these faults, rather than avoiding or minimising them* (source: chapter-01-introduction.md). The framing matters because blame produces cover-ups, and cover-ups produce repeat incidents.

This is not the same as "no consequences". A blameless culture is one where the conversation stays on the *system* (what made it possible for the human to make the mistake) rather than on the *individual* (why didn't you know better). The former produces structural fixes; the latter produces fear.

## Paged vs non-paged postmortems

Chapter 1 makes a point that is easy to miss (source: chapter-01-introduction.md):

> Postmortems should be written for all significant incidents, regardless of whether or not they paged; postmortems that did not trigger a page are even more valuable, as they likely point to clear monitoring gaps.

An incident that did not page is a signal that the monitoring did not catch something it should have. That's a direct input into the monitoring system's evolution — see [[sre-monitoring-outputs]].

## Relationship to the engineering-focus cap

Postmortems are one of the things the [[toil-and-engineering-balance|50% cap]] is protecting. The two-events-per-shift on-call target exists so that *each event gets handled accurately, service gets restored, and a postmortem gets written* (source: chapter-01-introduction.md). If the shift volume is higher, the first casualty is the postmortem — which is exactly the wrong thing to lose.

## Postmortems as a psychological safety net (Chapter 11)

Chapter 11 adds a second justification that's easy to miss: blameless postmortems are part of what keeps on-call engineers in the deliberate, rational decision-making mode during an incident (source: chapter-11-being-on-call.md). If the engineer knows the post-incident conversation will focus on *what happened* rather than *who screwed up*, the fear that fuels stress hormones is reduced, and with it the confirmation-bias and heuristic-abuse failure modes that [[incident-response-mindset]] catalogues.

The culture serves two roles at once:

- **Post-incident**: structural fixes instead of cover-ups.
- **In-incident**: less fear, better cognition, lower MTTR.

Chapter 11 also reiterates the six-hour-per-incident estimate (source: chapter-11-being-on-call.md) that covers *root-cause analysis, remediation, and follow-up activities like writing a postmortem and fixing bugs*. The postmortem is an accounted-for part of the incident, not an optional extra — which is why [[balanced-on-call|the 2-incidents-per-12-hour-shift limit]] is pegged to a shift length that can actually fit two of them.

## Postmortems as the terminal step of troubleshooting (Chapter 12)

Chapter 12 positions the postmortem as the Cure step's deliverable, not its sequel (source: chapter-12-effective-troubleshooting.md):

> Once you've found the factors that caused the problem, it's time to write up notes on what went wrong with the system, how you tracked down the problem, how you fixed the problem, and how to prevent it from happening again. In other words, you need to write a postmortem.

The postmortem captures four things: the symptom chain, the investigation (including [[negative-results|negative results]]), the fix, and the preventive follow-ups. In practice, the raw material comes from the shared document or chat channel the on-call engineer kept notes in during the incident — the [[test-and-treat|Test and Treat]] notes become the postmortem timeline.

Chapter 12 also notes that in complex real systems, definitively proving causation by reproducing the bug is often impossible (path-dependence, unacceptable downtime). The postmortem documents *probable* causal factors rather than a formally-proven single root cause. This is consistent with the broader "systems have many causes, not one" framing.

## Follow-through is the discipline (Chapter 13)

Chapter 13's closing section on [[learning-from-outages|learning from past outages]] sharpens the postmortem practice with a specific accountability rule (source: chapter-13-emergency-response.md):

> Ensure that everyone within the company can learn what you have learned by publishing and organizing postmortems. Hold yourself and others accountable to following up on the specific actions detailed in these postmortems.

The rule matters because writing a postmortem with thirty action items and then not tracking them produces the **illusion** of learning without the substance. A recurring pattern in the three Chapter 13 case studies is a follow-up that had been slated for "next quarter" and was pending when the incident made it urgent.

Chapter 13's implicit definition: **an incident is not closed when the service recovers; it is closed when the follow-up actions land.**

The postmortem is also the durable institutional memory that answers Chapter 13's "ask the big questions" directive — you can only ask *what if X happens again?* if the record of the first X is findable. See [[learning-from-outages]] for the full framing.

## The live incident document as raw material (Chapter 14)

Chapter 14 reinforces what Chapter 12 said about postmortem inputs: the [[live-incident-state-document|live incident state document]] kept by the [[incident-commander]] during the response is **retained for postmortem analysis** (source: chapter-14-managing-incidents.md). Concurrently editable, kept up to date as the incident unfolds, captured timestamps in the chat log of the [[recognized-command-post|command post]] — together they make postmortem reconstruction straightforward rather than archaeological.

Chapter 14's framing also clarifies which roles produce which postmortem artefacts: [[incident-planning-lead|planning]] tracks the temporary deviations from the norm (which become the "things we did during the incident" timeline), [[incident-communications-lead|communications]] keeps the document current, and the [[incident-commander|IC]] owns the document's overall accuracy.

## The full culture treatment (Chapter 15)

Chapter 15 is where the Chapter 1 one-line tenet gets its full development. The material is large enough that it lives in a dedicated hub ([[postmortem-philosophy]]) with six supporting pages; the Chapter 15 sharpenings most relevant to the blameless-postmortem concept itself (source: chapter-15-postmortem-culture-learning-from-failure.md):

- **Origin story.** Blameless culture originated in the **healthcare and avionics industries** — industries where mistakes can be fatal. Both nurture environments where every mistake is seen as an opportunity to strengthen the system. Google imported the practice; it wasn't invented internally.
- **The operative shift.** Chapter 15 sharpens the blameless framing: from allocating blame, to *investigating the systematic reasons why an individual or team had incomplete or incorrect information*. The shift moves the conversation from "why did you do the wrong thing" to "why was doing the wrong thing possible".
- **The mechanism.** "You can't fix people, but you can fix systems and processes to better support people making the right choices." The argument for blamelessness is therefore not moral but **structural** — you can only effect change on the things you can act on, and individual behaviour isn't one of them.
- **The failure mode.** "If a culture of finger pointing and shaming individuals or teams for doing the 'wrong' thing prevails, people will not bring issues to light for fear of punishment." Cover-ups are the predicted consequence of blame culture.
- **The two-example contrast.** Chapter 15 demonstrates blamelessness concretely: "We need to rewrite the entire complicated backend system! ... if I get paged one more time I'll rewrite it myself" (pointing fingers) vs "An action item to rewrite the entire backend system might actually prevent these annoying pages ... I'm sure our future on-callers will thank us!" (blameless). Both texts identify the same technical issue; only the blameless version produces a constructive action item.
- **Fear removal isn't enough.** Blamelessness removes the negative incentive, but sustained postmortem discipline also requires positive reinforcement — see [[rewarding-postmortems]] for Chapter 15's reward-side best practice.
- **Frequent-production stigma.** Chapter 15 is explicit: teams or individuals that produce many postmortems should not be stigmatised. A team writing many postmortems is, on average, a team that is good at surfacing failures. Penalising postmortem frequency produces the cover-up failure mode blamelessness was designed to prevent.

## Writing a great postmortem *with* the team (Chapter 30)

Chapter 30's [[embedding-sre|embedded-SRE rescue pattern]] gives blameless postmortems a distinctive role in Phase 2 of the engagement: when a team has been stuck in [[operational-overload]] and postmortems have drifted toward ritual or retaliation, the visiting SRE should **not** go back and critique the archive. That puts the team on the defensive and doesn't change anything. Instead, *take ownership of the next postmortem* — co-author it with the on-call SRE during the outage that inevitably happens during the visit — and use that one document as the **live demonstration** of what a blameless postmortem looks like (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

The demonstration approach works because the team sees the practice in action on their own incident, with their own engineer, and on their own timeline. Retrospective commentary on old documents feels like judgement; a collaborative new document feels like training.

Chapter 30 also supplies the specific phrasing to use when an engineer reacts to being asked to write a postmortem with *"why me?"*. That reaction almost always stems from the [[bad-apple-theory|Bad Apple Theory]] — the belief that outages come from flawed individuals who could be removed to make the system fine. The chapter's refutation, verbatim, to be used at the keyboard (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

> Mistakes are inevitable in any system with multiple subtle interactions. You were on-call, and I trust you to make the right decisions with the right information. I'd like you to write down what you were thinking at each point in time, so that we can find out where the system misled you, and where the cognitive demands were too high.

This phrasing operationalises the Chapter 15 *"you can't fix people, but you can fix systems"* thesis at the moment the postmortem process is most at risk of collapsing into blame. See [[bad-apple-theory]] for the full argument and [[embedding-sre]] for the phased rescue it sits inside.

Chapter 30 also makes the broader point that **the quality of a team's postmortems is a strong signal of the team's health**: *postmortems offer much insight into a team's collective reasoning. Postmortems conducted by unhealthy teams are often ineffectual. Some team members might consider postmortems punitive, or even useless* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md). An embedded SRE who finds postmortems treated as optional or punitive has diagnosed a more structural problem than ticket volume.

## The full cross-industry catalogue (Chapter 33)

Chapter 15 names the *origin* of blameless culture (healthcare and avionics). Chapter 33's cross-industry survey expands the catalogue of analogues across non-software fields (source: chapter-33-lessons-learned-from-other-industries.md):

- **Corrective and preventive action (CAPA)** is the formal name for the discipline; it predates SRE and is widely used in regulated industries
- **Lifeguarding** has a deeply embedded culture of post-incident analysis and action planning. Mike Doherty's quip: *"If a lifeguard's feet go in the water, there will be paperwork!"* Detailed write-up after any incident; team end-to-end discussion of serious incidents; operational changes and follow-up training; counselor brought on site for traumatic incidents. Like Google, the field embraces *blameless* incident analysis: *"Incidents are chaotic, and many factors contribute to any given incident. In this field, it's not helpful to place blame on a single individual."*
- **Manufacturing and chemical industries** under regulators (FCC, FAA, OSHA, FDA, EU National Competent Authorities) use postmortems where lives are at stake. Alcoa under Paul O'Neill is the named exemplar; see [[organizational-safety-culture]] for the 24-hour-notification practice and the CEO-distributed-home-phone-number mechanism
- **Manufacturing's [[near-miss-reporting|near-miss reporting]]** is preemptive postmortem: scenarios that *could have* caused serious harm but didn't. The UK's CHIRP (Confidential Reporting Programme for Aviation and Maritime) provides a confidential reporting point with periodic newsletters. *"Latent error, plus an enabling condition, equals things not working quite the way you planned"* (VM Brasseur)

The chapter's framing answers a question the earlier chapters leave implicit: *why does the practice work?* The answer is structural — every industry that has built a sustained reliability record under high consequence cost has converged on a postmortem-shaped mechanism. The convergence is independent evidence that the mechanism produces the outcome.

## Cross-book connection

The SRE framing dovetails with the [[unknown-unknowns]] argument in Richards & Ford: you cannot anticipate every way a system will fail, so the architecture must be iterative and learning-driven. The blameless postmortem is the mechanism by which that learning is captured and fed back into the system.

## Related pages

- [[sre-tenets]]
- [[emergency-response]]
- [[on-call-playbook]]
- [[toil-and-engineering-balance]]
- [[sre-monitoring-outputs]]
- [[monitoring-and-observability]]
- [[incident-response-mindset]]
- [[balanced-on-call]]
- [[troubleshooting-model]]
- [[test-and-treat]]
- [[negative-results]]
- [[learning-from-outages]]
- [[incident-management-framework]]
- [[live-incident-state-document]]
- [[postmortem-philosophy]]
- [[postmortem-triggers]]
- [[postmortem-template]]
- [[postmortem-review-process]]
- [[postmortem-culture-activities]]
- [[rewarding-postmortems]]
- [[postmortem-feedback-surveys]]
- [[postmortems-at-google-working-group]]
- [[bad-apple-theory]]
- [[embedding-sre]]
- [[operational-overload]]
- [[lessons-from-other-industries]]
- [[organizational-safety-culture]]
- [[near-miss-reporting]]
