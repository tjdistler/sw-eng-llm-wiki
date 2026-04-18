# Hypothetico-Deductive Debugging

**Summary**: The epistemological framing Chapter 12 gives to troubleshooting — iterate between observations, candidate hypotheses, and tests designed to confirm or disconfirm those hypotheses. Debugging is a scientific activity: what we know, what we don't know, and what we need to know drives the next action.

**Sources**: `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`

**Last updated**: 2026-04-17

---

## Debugging as a scientific method

Chapter 12 names the method explicitly (source: chapter-12-effective-troubleshooting.md, citing Wikipedia's [hypothetico-deductive model](https://en.wikipedia.org/wiki/Hypothetico-deductive_model)):

> Formally, we can think of the troubleshooting process as an application of the hypothetico-deductive method: given a set of observations about a system and a theoretical basis for understanding system behavior, we iteratively hypothesize potential causes for the failure and try to test those hypotheses.

The three ingredients:

- **Observations** — telemetry, logs, probes, user reports. The raw data.
- **Theoretical basis** — knowledge of how the system *should* work and its known failure modes. Without this, hypotheses are just guesses.
- **Iteration** — test one hypothesis, update beliefs, form the next hypothesis. A binary search through the hypothesis space.

## What knowing-what-you-know looks like

Chapter 12 closes its theory section with a meta-epistemic directive (source: chapter-12-effective-troubleshooting.md):

> A methodical approach to knowing what we do know, what we don't know, and what we need to know, makes it simpler and more straightforward to figure out what's gone wrong and how to fix it.

This is a three-way decomposition of the troubleshooter's mental state at any point in an incident:

- **Known** — facts confirmed by observation or test.
- **Unknown but known-unknown** — gaps you are aware of; the next experiments are designed to fill these.
- **Unknown and unknown-unknown** — the ones that bite you; the reason postmortems exist.

## Two kinds of hypothesis test

Chapter 12 distinguishes passive from active tests (source: chapter-12-effective-troubleshooting.md):

- **Compare observed state against theory.** Look at what you already have (metrics, logs, probe results). If the theory predicts X and you see not-X, disconfirmed. Cheap; no side effects.
- **Treat the system.** Make a controlled change and observe the result. Stronger evidence but may alter state, risk further harm, or create confounds.

Passive first, active when passive isn't conclusive. The [[test-and-treat]] page catalogues Chapter 12's full list of considerations when designing an active test.

## System knowledge is the accelerator

The chapter is emphatic that generic troubleshooting works, but it is slow (source: chapter-12-effective-troubleshooting.md):

> While you can investigate a problem using only the generic process and derivation from first principles, we usually find this approach to be less efficient and less effective than understanding how things are supposed to work. Knowledge of the system typically limits the effectiveness of an SRE new to a system; there's little substitute to learning how the system is designed and built.

The footnote adds that first-principles troubleshooting is itself one of the best ways to *learn* a system — the chapter cross-references Chapter 28 on this.

Expertise in troubleshooting is the product of two competencies:

1. The generic hypothetico-deductive process (transferable).
2. Deep model of the specific system (non-transferable; has to be built per service).

A generalist SRE can troubleshoot any system eventually. A specialist SRE can troubleshoot their service quickly. The 50% [[toil-and-engineering-balance|engineering cap]] exists partly so that SREs have the bandwidth to build and maintain the system model that makes fast troubleshooting possible.

## Pitfalls at the hypothesis-generation step

Chapter 12's [[troubleshooting-anti-patterns|common pitfalls]] include two that are hypothesis-generation failures specifically:

- **Wildly improbable theories.** "When you hear hoofbeats, think of horses not zebras" — not all failures are equally probable; prior likelihoods matter.
- **Latching onto past causes.** If it failed this way before, it must be failing this way again — confirmation bias in hypothesis form.

The antidote is Occam (prefer simpler explanations) balanced against Hickam (one symptom cluster may have multiple low-grade causes rather than a single rare one). Both are footnoted in Chapter 12.

## The five-whys connection

Chapter 12's "ask what, where, and why" technique (see [[divide-and-conquer-debugging]]) is explicitly compared to Taiichi Ohno's **Five Whys** method for manufacturing root-cause analysis (source: chapter-12-effective-troubleshooting.md, citing [Ohn88]). The iterative nature is the same: each answer generates the next question, and the chain terminates at a structural cause rather than a superficial symptom.

## Cross-book connection

- [[unknown-unknowns]] (Richards & Ford) — Rumsfeld's taxonomy applied to architecture. Chapter 12's "knowing what we know, what we don't know, and what we need to know" is the operational discipline Richards & Ford's epistemic framing motivates. Debugging *produces* the knowledge that moves items from unknown-unknown to known-unknown to known.
- [[blameless-postmortem]] — postmortems are where the learnings from a debugging session are captured and fed back into the team's system model, so the next incident starts with more knowledge.
- [[on-call-playbook]] — playbooks encode the hypothesis-generation step for known incident classes; they let the on-call engineer skip straight to the most likely hypotheses.

## Related pages

- [[troubleshooting-model]]
- [[troubleshooting-anti-patterns]]
- [[divide-and-conquer-debugging]]
- [[test-and-treat]]
- [[negative-results]]
- [[incident-response-mindset]]
- [[unknown-unknowns]]
- [[site-reliability-engineering]]
