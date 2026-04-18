# Automation Gone Wrong

**Summary**: Chapter 7's two named cautionary tales — the Bigtable disk-zero wipe and the Diskerase CDN-wide erase — and the general failure modes they illustrate. Automation amplifies both correct and incorrect behaviour; once a dangerous action is automated, "the blast radius of a single bad assumption is the entire fleet." The chapter's mitigations: avoid implicit safety signals, use rate limiting, log every RPC, require audit trails, and make destructive workflows idempotent with sanity checks.

**Sources**: `raw/site-reliability-engineering/chapter-07-the-evolution-of-automation-at-google.md`, `raw/site-reliability-engineering/chapter-13-emergency-response.md`

**Last updated**: 2026-04-17

---

## The Bigtable disk-zero incident

Mid-cluster-turnup narrative, Chapter 7 (source: chapter-07-the-evolution-of-automation-at-google.md):

- A multi-petabyte [[bigtable]] cluster was configured **not** to use the first (logging) disk on 12-disk systems, for latency reasons. The decision was explicit and intentional, documented for the humans who set it up.
- A year later, an unrelated piece of automation assumed: *if a machine's first disk isn't being used, that machine has no storage configured; therefore it's safe to wipe the machine and reinstall it.*
- The automation ran. All of the Bigtable data was wiped instantly.
- Multiple real-time replicas of the dataset saved the service, "but such surprises are unwelcome."

The named lesson: **automation needs to be careful about relying on implicit "safety" signals**. The "disk 0 not used" convention was a safety signal only by convention; it carried no type, no schema, no metadata declaring intent. Different downstream code interpreted it differently and the divergence was invisible until it ran.

### The general failure mode

The incident illustrates what the chapter frames as a structural risk of level-3 / level-4 automation (see [[hierarchy-of-automation-classes]]): automation tends to rely on **observable state** as a proxy for **intent**. When a new consumer of that state interprets it differently from the original producer, the divergence becomes a latent bomb that only explodes under the right conditions.

Mitigations implied by the chapter:

- **Express intent explicitly.** A field or label that says "logging disk intentionally disabled" cannot be mistaken for "no storage configured."
- **Fail closed.** Destructive operations should require positive confirmation, not the absence of a disqualifier.
- **Review consumers of shared signals.** When a convention is established, the set of downstream consumers is not fixed; the convention has to survive being read by code no one has written yet.

## The Diskerase incident

Chapter 7's "Automation: Enabling Failure at Scale" sidebar (source: chapter-07-the-evolution-of-automation-at-google.md):

- Google depends on machines in many third-party colocation facilities (colos), used to terminate incoming connections and as CDN cache nodes.
- Racks are continually installed and decommissioned; both processes are largely automated.
- One step in decommission is **Diskerase**: overwrite the full content of every disk in the rack, then have an independent system verify the erase succeeded.
- **The failure.** On one decommission, the automation failed *after* the Diskerase step completed successfully. The process was restarted from the beginning to debug the failure.
- On restart, the automation computed the set of machines still needing Diskerase. The set was (correctly) empty — Diskerase had already run. But the empty set was used as a special value meaning "everything."
- Within minutes, Diskerase wiped the disks on **all machines in Google's CDN**. The machines could no longer terminate user connections.

The impact was small in user terms — Google's own datacenters absorbed the traffic, with a slight external latency increase — thanks to capacity planning. Internally, "we spent the better part of two days reinstalling the machines in the affected colo racks."

### The general failure mode

Three structural contributors:

- **Sentinel-value overloading.** Empty set meant "nothing to do" at the producer and "everything" at the consumer. The type system didn't distinguish the two.
- **No blast-radius cap.** There was no check asking "wait, are we really about to Diskerase the whole CDN?" The automation did exactly what it was told as fast as possible.
- **Restart-from-beginning without state.** The debug procedure assumed idempotence at the step level but not at the workflow level; the workflow didn't remember which racks had already completed the destructive step.

### The mitigations the chapter added

After the incident, the chapter notes, the team spent "the following weeks":

- **Auditing** the decommission workflow for similar traps.
- **Adding more sanity checks**, including **rate limiting** — so that even if an automation decides to do something destructive, it can't do it to the whole fleet at once.
- **Making the decommission workflow idempotent**, so restarting from the beginning was safe even when a prior destructive step had already succeeded.

These are the concrete techniques the chapter recommends whenever automation's blast radius could exceed a single machine or service.

## The deeper point

Chapter 7 uses these stories to sharpen the final-section argument (see [[autonomous-systems]]): highly effective automation runs fast and with high consistency, which is also the exact combination needed to turn a latent bug into a fleet-wide outage. The remedy is not to retreat to manual operation — which introduces its own errors and doesn't scale — but to build in the governance that destructive operations need:

- Explicit intent, not implicit conventions (from the Bigtable story).
- Rate limiting, audit trails, and workflow-level idempotence (from the Diskerase story).
- Code review on permission-privileged operations (the Local Admin Daemon discipline from the [[cluster-turnup-automation|turnup story]]).
- Drill practice so the humans who need to step in have a working mental model ("Disaster Role Playing" in Ch 33).

Put together these are **progressive delivery applied to automation itself** — canary the automation, verify the effect, cap the blast radius. The same techniques Chapter 1 prescribed for code rollouts ([[change-management-sre]]) apply one level up to the automation that drives the rollouts.

## The Chapter 13 response-side view

Chapter 13 retells the Diskerase incident from the **incident-response** side rather than the **structural-failure** side (source: chapter-13-emergency-response.md). The trigger differs slightly in the retelling — Chapter 13 frames it as *two consecutive turndown requests for the same installation* (the second one is where the empty-set bug fires), while Chapter 7 frames it as *restart-from-scratch after a post-Diskerase failure*. Both are the same sentinel-value bug; the framings emphasise different parts of the causal chain.

The Chapter 13 response narrative adds details that Chapter 7 does not cover:

- **Traffic drain first.** Before investigating, on-call engineers drained traffic from the affected installations to healthy capacity. This is [[triage-sre|stop-the-bleeding-first]] applied to a destructive-automation outage.
- **Automation freeze as the circuit breaker.** As pagers fired for more installations globally, the response team disabled all team automation and froze production maintenance. When automation is the aggressor, the circuit breaker is the automation surface itself, not the machines.
- **A three-day phased manual rebuild.** The team was divided into three parts, each responsible for one step of a pipelined manual reinstall process — heroics inside a process-driven culture.
- **Recovery-capacity problems.** The mass-reinstall infrastructure had never been exercised at the scale needed. A regression capped per-worker setup tasks, QoS settings were wrong, timeouts were poorly tuned, and machines that didn't need kernel reinstallation got one anyway. The lesson: **recovery infrastructure is a system in its own right that needs capacity-planning and testing at the scale it will be used at**.

See [[process-induced-emergency]] for the full response-side narrative and follow-up actions.

## Cross-book connections

- [[change-management-sre]] — Chapter 1's "progressive rollouts, fast detection, safe rollback" trio applies to automation itself, not only to application code. The Diskerase mitigations (rate limiting especially) are a direct fit.
- [[progressive-delivery]] (Newman / Burns) — canary and blast-radius control at the automation layer.
- [[idempotence]] — the property the Diskerase workflow was retrofitted to have.
- [[fault-tolerance]] (Kleppmann / Burns) — replicated Bigtable data absorbed the disk-zero error; capacity-planned datacenters absorbed the CDN loss. Fault tolerance is the load-bearing property that turns these incidents from catastrophes into inconveniences.
- [[blameless-postmortem]] — both stories are written in the blameless style Ch 15 prescribes.

## Related pages

- [[automation-at-google]]
- [[autonomous-systems]]
- [[hierarchy-of-automation-classes]]
- [[cluster-turnup-automation]]
- [[change-management-sre]]
- [[progressive-delivery]]
- [[idempotence]]
- [[blameless-postmortem]]
- [[process-induced-emergency]]
- [[emergency-response]]
