# Change-Induced Emergency

**Summary**: Chapter 13's second case study: a Friday configuration push to Google's abuse-protection infrastructure triggered a crash-loop bug in essentially all external-facing systems and cascaded into internal systems that depended on them. The incident illustrates that "low-risk" changes deserve full canary discipline, that rate-limiting inside the affected system can buy the response team minutes to react, and that out-of-band communication and CLI tooling are load-bearing when the normal stack is unavailable.

**Sources**: `raw/site-reliability-engineering/chapter-13-emergency-response.md`

**Last updated**: 2026-04-17

---

## The change

A configuration change to the infrastructure that protects Google's services from abuse was pushed globally on a Friday (source: chapter-13-emergency-response.md). This infrastructure sits in front of essentially every externally-facing Google service. An earlier push of the same new feature had gone through a thorough canary without incident — but the earlier push did not exercise the **rare and specific configuration keyword** that, combined with the new feature, triggered a crash-loop bug.

Because the global push used the untested keyword/feature combination, external-facing systems began to crash-loop almost simultaneously. Google's internal infrastructure depends on its own services, so many internal applications became unavailable as well.

## What went wrong

- The specific change wasn't considered risky, so it **followed a less stringent canary process** than an earlier, nominally bigger push of the same feature.
- Crash-looping affected internal tools, including the ones SRE normally uses for troubleshooting and communication.
- Some on-call engineers, experiencing corporate-network symptoms, initially believed the **corporate network** had failed rather than the production fleet. They relocated to dedicated secure rooms ("panic rooms") with backup access to production.

## The response

- Monitoring detected the problem within seconds and alerts began firing. The alerting was over-vocal — alerts fired repeatedly, overwhelming the on-calls and spamming emergency communication channels — but the detection itself was immediate.
- **Within five minutes** of the first push, the engineer who performed the push noticed a large volume of complaints about corporate access in real-time chat channels. Unaware of the broader outage but suspecting the push, they **rolled back the configuration change**. Services began to recover almost immediately.
- Within ten minutes of the first push, on-call engineers declared an incident and began following the formal incident-response protocol.
- Some downstream services hit **unrelated bugs or misconfigurations** triggered by the original event and took up to an hour to fully recover.

## What went well

- **Monitoring detected the problem immediately.** Whatever the noise problems, the signal was there within seconds.
- **Incident management, once declared, went well.** Updates were communicated often and clearly.
- **Out-of-band communication systems** — the backup systems SRE deliberately retains for exactly this situation — kept everyone connected when the normal software stacks were unusable.
- **Command-line tools and alternative access methods** let engineers perform updates and rollbacks when the UI was inaccessible. Chapter 13 notes the caveat that engineers needed to be more familiar with these tools and test them more routinely.
- **Infrastructure-level rate limiting** on how quickly the affected system delivered full updates to new clients may have throttled the crash-loop, allowing jobs to service a few requests in between crashes and preventing a complete outage.
- **Luck plus diligence.** The push engineer happened to be watching real-time chat channels — not a normal part of the release process — and initiated the rollback themselves within minutes, before a formal incident declaration would have routed the same decision through slower channels.

## What was learned

- **A thorough canary on a nominally similar change is not a substitute for a thorough canary on this change.** The untested keyword/feature combination is the textbook example of a low-probability input that matters. Canary coverage must be tied to the **actual combinatorial surface**, not to the apparent risk level.
- **Improvements to canarying and automation were slated for the next quarter**; the incident made them immediate. "We were going to get to it" is a recurring theme in outage postmortems.
- **Alert spam during an outage is itself an incident factor.** Vocal alerting disrupted the on-call engineers' real work and made internal communication harder. This is the [[operational-overload|operational-overload]] failure mode manifesting during an acute incident rather than as a chronic condition.
- **The troubleshooting stack lives on the system under test.** Google relies on its own tools; much of the software used for troubleshooting and communication was behind jobs that were crash-looping. Had the outage lasted any longer, debugging would have been severely hindered.

## The load-bearing lesson: don't depend only on the system under test

The running thread of the case is: when the production stack is broken, your **recovery tools must not themselves depend on the production stack**. SRE retains:

- **Out-of-band communication** (backup chat, phone bridges, physical panic rooms with independent access).
- **CLI tools and alternative access methods** that work without the normal UI layer.
- **A push engineer in real-time communication channels** during risky pushes — a social redundancy over the automated detection.

Any of these being unavailable would have lengthened the outage.

## Connections

- [[emergency-response]] — Chapter 13's second case study; the response pattern (rapid rollback by the push engineer, incident declared, staged recovery) is a textbook execution.
- [[change-management-sre]] — the specific change followed an insufficient canary for its actual combinatorial surface. The **quick-and-accurate detection** leg of the automation trio worked (alerts within seconds); the **progressive-rollout** leg did not, because the canary did not exercise the failure mode.
- [[rate-limiting]] — the affected system's internal rate-limit on full-client-update delivery acted as an accidental throttle on the crash-loop propagation, buying the response team time. A general principle: **rate limits on change distribution are a reliability asset**, not only a capacity one.
- [[release-policy-enforcement]] — the chapter's implicit recommendation (and the team's follow-up) was to raise the bar for what counts as a "risky change" requiring full canary.
- [[alert-philosophy]] — the alert-spam observation is Chapter 6's noise/signal discipline failing under acute load. The same alert firing thousands of times is no longer an alert; it's a denial-of-service on the responders.

## Cross-book connection

- [[progressive-delivery]] (Newman / Burns) — the canary was insufficient precisely because it didn't exercise the true configuration surface. The open-source canary frameworks have the same failure mode when canary traffic doesn't include the rare input.
- [[feature-toggle]] (Newman) — the rollback here was a configuration-flip, which is what a feature toggle is. The cheapness of the rollback (flip the bit) is why the push engineer could act inside five minutes.

## Related pages

- [[emergency-response]]
- [[test-induced-emergency]]
- [[process-induced-emergency]]
- [[learning-from-outages]]
- [[change-management-sre]]
- [[rate-limiting]]
- [[alert-philosophy]]
- [[operational-overload]]
- [[release-policy-enforcement]]
