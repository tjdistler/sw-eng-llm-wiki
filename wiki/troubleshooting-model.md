# Troubleshooting Model

**Summary**: Chapter 12's general-purpose process for diagnosing distributed-system failures: problem report → triage → examine → diagnose → test/treat → cure. The model is an application of the hypothetico-deductive method — observations, hypotheses, tests — that turns troubleshooting from an ingrained intuition into a teachable skill.

**Sources**: `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`

**Last updated**: 2026-04-17

---

## The chapter's thesis

Chapter 12 (Chris Jones) opens by contesting the folk belief that troubleshooting is an innate talent (source: chapter-12-effective-troubleshooting.md):

> Troubleshooting is a critical skill for anyone who operates distributed computing systems — especially SREs — but it's often viewed as an innate skill that some people have and others don't. [...] We believe that troubleshooting is both learnable and teachable.

Effective troubleshooting combines two factors:

- **Generic process** — the method described on this page, derivable from first principles.
- **System knowledge** — how the system is designed, how it should behave, and its known failure modes.

First-principles troubleshooting works, but it is slower and less effective than troubleshooting informed by how the system actually works. Deep system understanding is the thing that separates expert SREs from competent novices.

## The six-step process

The chapter lays out the process as a loop:

1. **Problem report** — an alert or human report of unexpected behaviour.
2. **Triage** — assess severity and stop the bleeding. See [[triage-sre]].
3. **Examine** — gather system state (metrics, logs, traces).
4. **Diagnose** — form hypotheses about possible causes.
5. **Test / treat** — design experiments that rule hypotheses in or out; see [[test-and-treat]].
6. **Cure** — apply the fix, verify it, and write a [[blameless-postmortem|postmortem]].

Diagnose → Test/Treat is a loop: if a test disconfirms a hypothesis, return to diagnosis with the new data. The exit condition is a (probable) root cause.

## The hypothetico-deductive loop

Formally, the process is an application of the hypothetico-deductive method (source: chapter-12-effective-troubleshooting.md):

> Given a set of observations about a system and a theoretical basis for understanding system behavior, we iteratively hypothesize potential causes for the failure and try to test those hypotheses.

See [[hypothetico-deductive-debugging]] for the full framing.

Hypotheses can be tested two ways:

- **Passively** — compare the observed system state against the theory's predictions; confirming or disconfirming evidence arrives from instruments you already have.
- **Actively** — change the system in a controlled way ("treat") and observe the result. Actively testing refines your understanding but risks changing state.

## Stopping the bleeding comes first

A critical detail from the Triage section: the novice instinct in a major outage is to root-cause immediately. **Ignore that instinct** (source: chapter-12-effective-troubleshooting.md).

> Your first response in a major outage may be to start troubleshooting and try to find a root cause as quickly as possible. Ignore that instinct! Instead, your course of action should be to make the system work as well as it can under the circumstances.

Chapter 12's pilot analogy (Atul Gawande via [Gaw09]): novice pilots are taught that their first responsibility in an emergency is to **fly the airplane**. Troubleshooting is secondary to getting the plane safely onto the ground. For SRE, that means diverting traffic, dropping load, disabling subsystems, or freezing the system if corruption is possible — *before* starting root-cause analysis. See [[triage-sre]].

## The model is not clean in practice

Chapter 12 is candid: "in practice, of course, troubleshooting is never as clean as our idealized model suggests it should be." The steps overlap; you bounce between them; you discover mid-diagnosis that the triage decision was wrong. The model is a scaffold, not a recipe.

## Common pitfalls

The Common Pitfalls subsection catalogues four failure modes of the Triage/Examine/Diagnose phases, all rooted in shallow system knowledge:

- Looking at irrelevant symptoms or misunderstanding metrics — produces wild goose chases.
- Misunderstanding how to change the system safely to test hypotheses.
- Coming up with wildly improbable theories, or latching on to previous incident causes.
- Hunting down spurious correlations.

See [[troubleshooting-anti-patterns]] for the full list with the "hear hoofbeats, think horses not zebras" and Occam/Hickam framings.

## The Shakespeare case (worked example)

Chapter 12 illustrates each step with a recurring Shakespeare-search-service example:

1. Problem report: `ShakespeareBlackboxProbe_SearchFailure` alert fires.
2. Triage: severity is moderate (~50% failure on a non-critical path).
3. Examine: `curl` to `/api/search` returns 502; `X-Request-Trace` identifies the backends.
4. Diagnose: the 502 with backend IDs means the request reached the backends — so frontends and load balancers are ruled out. Focus on backends.
5. Test/treat: query backends directly, examine logs and metrics.
6. Cure: (not shown in chapter's narrative arc) fix the underlying backend issue and postmortem.

The App Engine case study later in the chapter is a longer, messier example where the initial hypothesis (`merge_join`/suboptimal indexing) turned out to be a spurious correlation and the real cause was a whitelist-caching antipattern exercised by a security scanner.

## Connections inside the chapter

- [[hypothetico-deductive-debugging]] — the theoretical framing of the loop.
- [[triage-sre]] — the stop-the-bleeding phase.
- [[troubleshooting-anti-patterns]] — the pitfalls to avoid.
- [[divide-and-conquer-debugging]] — the simplify/reduce/bisect/ask-what-where-why toolkit for the Diagnose phase.
- [[test-and-treat]] — the rule-in/rule-out experimental design phase.
- [[negative-results]] — Randall Bosetti's essay on the value of failed experiments; sidebar in Chapter 12.
- [[making-troubleshooting-easier]] — the design disciplines that reduce the need for troubleshooting in the first place.

## Related pages

- [[emergency-response]]
- [[on-call-playbook]]
- [[blameless-postmortem]]
- [[incident-response-mindset]]
- [[symptoms-vs-causes]]
- [[four-golden-signals]]
- [[distributed-tracing]]
- [[site-reliability-engineering]]
