# Process-Induced Emergency

**Summary**: Chapter 13's third case study: Google's Diskerase decommission automation, on a duplicate turndown request, sent every machine in a class of small CDN installations to the disk-wipe queue globally. The incident is Chapter 13's operational read of the same failure Chapter 7 catalogues structurally — a sentinel-value bug amplified by highly efficient automation. The response chapter emphasises the recovery arc: traffic diversion, damage containment via freezing all team automation, a three-day phased manual rebuild, and the organisational maturity (mature incident-response, cross-team collaboration, large-installation fallback capacity) that made a fleet-wide destructive bug a capacity headache instead of a user-visible catastrophe.

**Sources**: `raw/site-reliability-engineering/chapter-13-emergency-response.md`, `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`

**Last updated**: 2026-04-17

---

## The trigger

As part of routine automation testing, two consecutive turndown requests were submitted for the same soon-to-be-decommissioned server installation (source: chapter-13-emergency-response.md). A subtle bug in the automation, handling the **second** (redundant) request, sent all machines in all such installations globally to the [[automation-gone-wrong|Diskerase queue]] — their disks destined to be wiped.

Soon after, the on-call engineers received a page as the first small server installation was taken offline.

## The response — stopping the bleeding

Chapter 13's response narrative is a tight example of [[triage-sre|triage-before-diagnose]]:

1. **Identify the wrong-state.** Investigation determined the machines had been transferred to the Diskerase queue. The outage was not a routine failure — destructive automation was running ahead of them.
2. **Drain traffic to healthy capacity.** Because the wiped machines could not respond, the on-call engineers drained traffic from the affected locations to locations that could respond. Users saw elevated latency, not failed requests.
3. **Freeze the blast radius.** As pagers fired globally for similar server installations, the on-call engineers **disabled all team automation** to prevent further damage, then stopped or froze additional automation and production maintenance.
4. **Declare the outage over at the user-facing level.** Within an hour, traffic was diverted to other locations and requests were being fulfilled.

The key move is step 3. The destructive automation was still running; the **only** way to stop it was to kill the automation surface wholesale rather than chase individual actions. Chapter 13's lesson: when automation is the aggressor, the circuit breaker is at the automation layer, not at the machine layer.

## The response — recovery

With the outage bounded, the real work began:

- **Network link congestion** surfaced as traffic was rerouted. Network engineers implemented mitigations as choke points appeared. On-call engineers prioritised congested networks over other restoration work.
- **First installation rebuilt within three hours** by a small team, thanks to "the tenacity of several engineers" — a reminder that production-engineering heroics still matter inside a process-driven culture.
- **US teams handed off to European counterparts** in the standard follow-the-sun pattern.
- SRE hatched a **streamlined but manual reinstall process**, dividing the team into three parts, each responsible for one step of the process (a pipelined manual workflow under time pressure).
- **Within three days** the vast majority of capacity was back online; stragglers trickled in over the next month or two.

## What went well

- **Architectural blast-radius asymmetry.** Reverse proxies in large server installations are managed differently from those in small installations; large installations were unaffected and had been capacity-planned to handle a full load without difficulty. The small installations got traffic-drained into them.
- **Monitoring reversal.** Turndown automation had torn down monitoring for the small installations. On-call engineers were able to promptly revert those monitoring changes, restoring visibility so they could assess damage extent.
- **Mature incident-response protocol.** In the year since the first case study in the chapter, the incident-management program had matured considerably. Communication and cross-team collaboration were "superb — a real testament to the incident management program and training."
- **Broad engineering participation.** All hands within respective teams chipped in; vast experience was brought to bear. Chapter 13 frames this as a cultural achievement, not a scheduling one.

## What was learned — the root cause (matches Chapter 7)

The turndown automation server lacked appropriate sanity checks on commands it sent to the machine database. On the second (redundant) run, the server received an empty response for the rack machine set. Instead of filtering the empty response, it **passed the empty filter to the machine database** — which interpreted the empty filter as "all machines." The machine database complied and churned through every matching machine as fast as possible.

Chapter 13's one-line summary: **yes, sometimes zero does mean all**. See [[automation-gone-wrong]] for the structural treatment (sentinel-value overloading, no blast-radius cap, restart-from-beginning without state).

## What was learned — recovery-path fragility

Chapter 13's post-incident section emphasises recovery-path problems that don't appear in Chapter 7's telling:

- **Reinstallations were slow and unreliable** because the lowest-priority QoS class was used for the kernel-delivery TFTP traffic from distant locations. The BIOS of affected machines handled TFTP failures poorly — halting, or entering a constant reboot cycle while failing to transfer boot files, further taxing the installers.
- **The mitigation** was to reclassify installation traffic at higher QoS and use automation to restart stuck machines.
- **The reinstall infrastructure couldn't handle simultaneous setup of thousands of machines** due to a regression that capped per-worker setup tasks, improper QoS settings, and poorly tuned timeouts; it also **forced kernel reinstallation on machines that still had the correct kernel and had not yet been wiped**. On-call engineers escalated to the infrastructure owners who retuned it under load.

The structural lesson: **recovery infrastructure is a system in its own right**, with capacity, QoS, and regression surfaces. It must be exercised at the scale it will be needed at — not just at normal single-machine scale. A mass-reinstall flow that has never been tested at 1000× its normal load will have problems at 1000× its normal load.

## Why it's in the chapter

Chapter 13 uses the story to make three points beyond Chapter 7's structural critique:

1. **The response template works even for destructive automation.** Traffic drain, automation freeze, traffic absorbed by fallback capacity — the steps are the same as for any other outage. The difference is the **speed** required on step 3.
2. **Recovery capacity is not the same as serving capacity.** Google's reinstall infrastructure was sized for steady-state machine replacement, not for rebuilding a CDN. Capacity-plan both.
3. **Organisational maturity compounds.** The response in this case was visibly better than the Chapter 13 configuration-push case a year earlier. Disciplined incident-response, repeated, gets sharper.

## Connections

- [[emergency-response]] — Chapter 13's third case study. The arc (mitigate → freeze → divert → rebuild) is the fullest example of the chapter's response model.
- [[automation-gone-wrong]] — Chapter 7's structural root-cause treatment of the same incident. Two chapters, two framings: mechanism (Ch 7) and response (Ch 13).
- [[triage-sre]] — the **stop the bleeding** rule operationalised. Drain traffic, freeze automation, assess, only then start rebuilding.
- [[change-management-sre]] — the mitigations (rate limiting, audit trails, workflow-level idempotence) are progressive delivery applied to automation itself.
- [[n-plus-2-redundancy]] / [[capacity-planning]] — the large-installation fallback capacity that absorbed the small-installation outage is why this was a capacity-and-latency event rather than a user-visible outage.
- [[fault-tolerance]] — architectural diversity (large installations ≠ small installations) is the thing that kept a fleet-wide automation bug from being a total outage.
- [[learning-from-outages]] — the post-incident follow-up on recovery capacity, QoS, and reinstall regressions is a direct example of the chapter's closing discipline.

## Cross-book connection

- Chaos engineering (industry practice; Chaos Monkey and similar) — this is what happens when a destructive-automation drill escapes from the drill. Chaos engineering's blast-radius discipline (start small, verify, expand) is the exact practice Diskerase was missing.
- [[idempotence]] (Bellemare / Kleppmann) — the workflow was not idempotent at the **workflow** level; a second identical turndown request produced dramatically different behaviour from the first. The retrofit made the workflow idempotent.

## Related pages

- [[emergency-response]]
- [[test-induced-emergency]]
- [[change-induced-emergency]]
- [[learning-from-outages]]
- [[automation-gone-wrong]]
- [[triage-sre]]
- [[change-management-sre]]
- [[capacity-planning]]
- [[n-plus-2-redundancy]]
- [[fault-tolerance]]
- [[idempotence]]
