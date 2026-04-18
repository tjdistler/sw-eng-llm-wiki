# Identifying Kindling

**Summary**: Chapter 30's term for **emergencies waiting to happen** — the structural weaknesses that will produce incidents at some point but haven't yet. An embedded SRE's Phase 1 job, after cataloguing existing stress sources, is to catalogue kindling. Chapter 30 gives seven specific warning signals to look for.

**Sources**: `raw/site-reliability-engineering/chapter-30-embedding-an-sre-to-recover-from-operational-overload.md`

**Last updated**: 2026-04-17

---

## The concept

Most operational-load analysis focuses on current pain: what's breaking now, which alerts fire most, which runbooks run hot. Kindling is the **complement**: the things that aren't burning but are structurally positioned to catch fire. A team drowning in current ops work rarely has the slack to look for kindling; the visiting SRE does, because they arrive with fresh eyes and no queue to drain.

Chapter 30's opening framing: *once you identify a team's largest existing problems, move on to emergencies waiting to happen* (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

## Seven warning signals

Chapter 30 gives a specific list of kindling sources (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

1. **New subsystems not designed to be self-managing.** Something just shipped that is going to require manual intervention to keep running. Predict the operational load before the first incident makes it obvious.

2. **Knowledge gaps from over-specialisation.** In large teams, people specialise without immediate consequence. The specialisation becomes visible only when the specialist is on vacation during an incident, or when teammates ignore the component they don't own. Either half of the pattern is kindling.

3. **SRE-developed services quietly increasing in importance.** These services often don't get the careful attention of a new feature launch because they're smaller in scale and implicitly endorsed by at least one SRE. The implicit endorsement is the problem: nobody reviewed the operational characteristics the way they would have reviewed an external team's launch.

4. **Strong dependence on "the next big thing".** People ignore problems for months because they believe a coming solution will make the fix unnecessary. The coming solution slips, and the ignored problems are the ones that fire.

5. **Common alerts not diagnosed by either dev or SRE.** Alerts triaged as "transient" without investigation are a double problem: they distract the team *and* they hide real faults. Either investigate the alerts fully, or fix the alerting rules. There is no acceptable middle state (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

6. **Services that generate client complaints but lack an SLI/SLO/SLA.** The absence of a [[service-level-objective|formal SLO]] means there is no quantitative ground for prioritising the fix. The complaint is the symptom; the missing SLO is why nothing happens about it.

7. **Capacity plans that are effectively "add more servers: our servers were running out of memory last night".** Reactive capacity planning with no forward-looking model. A load test that passes in the short term (1.99 GB measured against a 2 GB limit) does *not* mean capacity is adequate — it means you are about to hit the wall.

8. **Postmortems whose action items only roll back the specific change that caused the outage.** The chapter's example: *"Change the streaming timeout back to 60 seconds," instead of "Figure out why it sometimes takes 60 seconds to fetch the first megabyte of our promo videos."* The shallow action item papers over the structural cause and guarantees the same class of incident will recur (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md).

9. **Serving-critical components whose SREs say "we don't know anything about that; the devs own it".** Chapter 30's standard: *to give acceptable on-call support for a component, you should at least know the consequences when it breaks and the urgency needed to fix problems.* Not owning the code is fine; not understanding the failure mode is not.

The list is not exhaustive — it is a starter kit for the kinds of patterns a visiting SRE should actively hunt for in the first few weeks.

## Kindling vs existing stress sources

Chapter 30 keeps these two lists separate deliberately (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

- **Existing stress sources** come from the team's lived experience. Rank them by the stress they actually produce, which may disagree with the objective impact — small problems with long histories can dominate team morale.
- **Kindling** comes from the visiting SRE's diagnostic eye. It won't show up on the team's own list because the team doesn't have the perspective to see it.

Both lists feed into Phase 2 and Phase 3 of the [[embedding-sre|embedded engagement]]. The stress-source list tells you what the team most wants fixed. The kindling list tells you what most needs fixing whether they know it or not.

## What to do with the kindling list

In Phase 3, Chapter 30 prescribes a *specific* way to work through kindling (source: chapter-30-embedding-an-sre-to-recover-from-operational-overload.md):

- Pick two or three items.
- For each, find useful work a single team member can do.
- Clearly explain how the work addresses a postmortem issue in a **permanent** way — not a shallow rollback action item, but a root-cause fix.
- Serve as the code and documentation reviewer.
- Put remaining items in bug reports or docs for the team to work through after the embedded SRE leaves.

The discipline is *don't fix it yourself*. Fixing kindling personally teaches the team that fixes come from outside; walking a team member through two or three fixes teaches them to do the next dozen themselves. See [[embedding-sre]] for the full framing.

## Relationship to proactive testing

Chapter 13's [[learning-from-outages|"encourage proactive testing"]] directive is a cousin of kindling identification. Both surface failures before they happen: proactive testing by **simulating** the failure in a drill; kindling identification by **reasoning** about what will fail next. They compose — a kindling item ("this capacity plan is reactive") is a natural candidate for a DiRT scenario.

## Related pages

- [[embedding-sre]]
- [[ops-mode]]
- [[operational-overload]]
- [[blameless-postmortem]]
- [[service-level-objective]]
- [[capacity-planning]]
- [[learning-from-outages]]
- [[alert-philosophy]]
- [[on-call-playbook]]
