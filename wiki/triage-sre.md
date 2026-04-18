# Triage (SRE)

**Summary**: The step immediately after a problem report is acknowledged: assess severity, and — for serious incidents — **stop the bleeding before starting root-cause analysis**. Chapter 12's most counterintuitive directive for new SREs: fly the airplane first; troubleshoot second.

**Sources**: `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`

**Last updated**: 2026-04-17

---

## The triage step in the troubleshooting model

Triage is step 2 of the [[troubleshooting-model]] (after problem report, before examine). It answers: *how bad is this and what do we do first?*

Chapter 12 frames it as a judgement call (source: chapter-12-effective-troubleshooting.md):

> Problems can vary in severity: an issue might affect only one user under very specific circumstances (and might have a workaround), or it might entail a complete global outage for a service. Your response should be appropriate for the problem's impact: it's appropriate to declare an all-hands-on-deck emergency for the latter, but doing so for the former is overkill.

The prerequisite is **good engineering judgement and calm under pressure**. Under [[incident-response-mindset|stress]], both degrade — which is why the triage protocol matters enough to write down.

## The fundamental rule: stop the bleeding first

The chapter's headline directive (source: chapter-12-effective-troubleshooting.md):

> Your first response in a major outage may be to start troubleshooting and try to find a root cause as quickly as possible. Ignore that instinct! Instead, your course of action should be to make the system work as well as it can under the circumstances.

Stopping the bleeding takes precedence over root-cause analysis. The principle: *you aren't helping your users if the system dies while you're root-causing*.

Emergency options the chapter names:

- **Divert traffic** from a broken cluster to others still working.
- **Drop traffic wholesale** to prevent a [[fallacies-of-distributed-computing|cascading failure]].
- **Disable subsystems** to lighten load.
- **Freeze the system** — if a bug is producing possibly unrecoverable data corruption, stopping the system is better than letting the corruption continue.

These are blunt instruments. Triage decides which one to reach for.

## The airplane analogy

Chapter 12 draws from Atul Gawande's writing on aviation training (source: chapter-12-effective-troubleshooting.md, citing [Gaw09]):

> Novice pilots are taught that their first responsibility in an emergency is to fly the airplane; troubleshooting is secondary to getting the plane and everyone on it safely onto the ground. This approach is also applicable to computer systems.

The analogy makes the priority obvious. A pilot who dives into instrument diagnosis while the plane is still in an uncontrolled dive is a dead pilot. An SRE who dives into root-cause analysis while the service is still serving 500s to users is burning the [[error-budget|error budget]] at maximum rate for no reason.

## Counterintuitive for product-development transplants

Chapter 12 notes that this priority ordering is particularly unsettling for SREs coming from a product-development background (source: chapter-12-effective-troubleshooting.md):

> This realization is often quite unsettling and counterintuitive for new SREs, particularly those whose prior experience was in product development organizations.

In product development, understanding the root cause is often the highest-priority action — the bug needs a correct fix, and a correct fix needs an accurate diagnosis. In production operations, a user-visible outage is the emergency, and restoring service is the first-order action even if it means the fix is temporary and imperfect. The correct fix comes later, often in the [[blameless-postmortem|postmortem]] follow-ups.

## Triage does not mean "abandon evidence"

Chapter 12 is careful to note that stopping the bleeding should not come at the cost of losing the data you will need to root-cause afterward (source: chapter-12-effective-troubleshooting.md):

> Of course, an emphasis on rapid triage doesn't preclude taking steps to preserve evidence of what's going wrong, such as logs, to help with subsequent root-cause analysis.

If the mitigation is "restart the service", collect a core dump first. If the mitigation is "divert traffic away from cluster X", snapshot cluster X's metrics and logs before it drains. Evidence is a perishable asset; mitigation often destroys it.

## Triage and the problem-report form

The chapter also notes that triage quality depends on problem-report quality. A well-formed report tells you:

- **Expected behaviour.**
- **Actual behaviour.**
- **How to reproduce** (if possible).

This is why Google's teams build custom report forms and open a bug for every issue — including those received via email or chat (source: chapter-12-effective-troubleshooting.md). A bug in a searchable tracking system provides the record that makes subsequent triage and post-incident analysis possible.

## Cross-book connection

- [[fallacies-of-distributed-computing]] / [[circuit-breaker]] / [[bulkhead]] (Newman / Burns) — the emergency options Chapter 12 names (drop traffic, disable subsystems) are the operational form of the resilience patterns that isolate faults at design time. Triage is when you manually apply the patterns you wish you'd automated.
- [[health-probes]] (Burns) — automated load-balancer deregistration on readiness-probe failure is the automation of the "divert traffic" emergency option.
- [[emergency-response]] — the tenet; triage is the early phase of its execution.

## Related pages

- [[troubleshooting-model]]
- [[emergency-response]]
- [[incident-response-mindset]]
- [[on-call-playbook]]
- [[blameless-postmortem]]
- [[error-budget]]
- [[site-reliability-engineering]]
