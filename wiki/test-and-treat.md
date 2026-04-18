# Test and Treat

**Summary**: Chapter 12's Test/Treat phase: once the Diagnose phase has produced a short list of candidate causes, design experiments that **rule hypotheses in or out**. Chapter 12 names five considerations for experiment design — mutual exclusivity, decreasing likelihood, confounds, side effects, and non-definitive suggestions — and mandates written notes throughout.

**Sources**: `raw/site-reliability-engineering/chapter-12-effective-troubleshooting.md`

**Last updated**: 2026-04-17

---

## Where Test and Treat sits

Test/Treat is step 5 of the [[troubleshooting-model]], after Diagnose has generated hypotheses and before Cure commits to a fix. Chapter 12's framing (source: chapter-12-effective-troubleshooting.md):

> Once you've come up with a short list of possible causes, it's time to try to find which factor is at the root of the actual problem. Using the experimental method, we can try to rule in or rule out our hypotheses.

Each test is a designed experiment whose outcome *differentially supports* some hypotheses over others.

## The worked pair

Chapter 12's illustration is about a latency problem that could be either a network fault between the application server and the database, or the database refusing connections (source: chapter-12-effective-troubleshooting.md):

- **Connect to the database using the same credentials the application server uses** — if it succeeds, the database is accepting connections, which refutes the "refusing connections" hypothesis.
- **Ping the database server** — if it succeeds, the network is at least partially working, which refutes (modulo topology) the "network fault" hypothesis.

Either test rules out one hypothesis and leaves the other; both tests run together narrow the remaining hypothesis space quickly.

The chapter also notes that **tracing the code path step-by-step** ("following the code and trying to imitate the code flow") is itself a form of test — a mental simulation that often surfaces bugs the instruments missed.

## The five considerations

Chapter 12 lists five things to keep in mind when designing tests (source: chapter-12-effective-troubleshooting.md):

### 1. Mutually exclusive alternatives

> An ideal test should have mutually exclusive alternatives, so that it can rule one group of hypotheses in and rule another set out.

A test whose result is consistent with *both* "this is the bug" and "this isn't the bug" gives you no information. Design tests whose outcomes differentially support hypotheses. In practice, achieving full mutual exclusivity is rare — you do your best.

### 2. Decreasing likelihood, accounting for risk

> Perform the tests in decreasing order of likelihood, considering possible risks to the system from the test. It probably makes more sense to test for network connectivity problems between two machines before looking into whether a recent configuration change removed a user's access to the second machine.

The horses-not-zebras heuristic from [[troubleshooting-anti-patterns]] applies here: likely hypotheses first. But weight by test risk — a cheap low-likelihood test may be worth running before an expensive high-likelihood one.

### 3. Confounding factors

> An experiment may provide misleading results due to confounding factors. For example, a firewall rule might permit access only from a specific IP address, which might make pinging the database from your workstation fail, even if pinging from the application logic server's machine would have succeeded.

The environment you run the test from is part of the experiment. Running the same test from a different vantage point gives a different result; the SRE must be aware of which vantage point matters.

### 4. Side effects that change future results

> Active tests may have side effects that change future test results. For instance, allowing a process to use more CPUs may make operations faster, but might increase the likelihood of encountering data races. Similarly, turning on verbose logging might make a latency problem even worse and confuse your results.

Active tests — "treat" in the chapter's terminology — alter system state. They may:

- Fix the problem accidentally, destroying the evidence you needed.
- Introduce new failure modes (data races under added concurrency, latency spikes under added logging).
- Make the next test harder to interpret because you're no longer in the same state.

The antidote is explicit reversibility: know exactly how to undo each active test, and undo it before the next test.

### 5. Non-definitive suggestive tests

> Some tests may not be definitive, only suggestive. It can be very difficult to make race conditions or deadlocks happen in a timely and reproducible manner, so you may have to settle for less certain evidence that these are the causes.

Not every hypothesis can be proven. Intermittent bugs — races, deadlocks, heisenbugs — resist clean experimental design. You accumulate suggestive evidence, triangulate, and make the best judgement you can. The Cure step may proceed on high-probability-not-proven evidence.

## Take notes

Chapter 12 is emphatic about written notes (source: chapter-12-effective-troubleshooting.md):

> Take clear notes of what ideas you had, which tests you ran, and the results you saw. Particularly when you are dealing with more complicated and drawn-out cases, this documentation may be crucial in helping you remember exactly what happened and prevent having to repeat these steps.

The chapter's footnote adds operational guidance: **a shared document or real-time chat channel** provides three things at once — a timestamp, a shared state for the incident response team so no one has to interrupt the troubleshooter to ask status, and the raw material for the postmortem.

The notes also serve an active-test-hygiene purpose (source: chapter-12-effective-troubleshooting.md):

> If you performed active testing by changing a system — for instance by giving more resources to a process — making changes in a systematic and documented fashion will help you return the system to its pre-test setup, rather than running in an unknown hodge-podge configuration.

Without notes, you cannot revert. Without reverting, the next incident starts in a state nobody understands — which is how incidents compound into outages.

## The "negative results" connection

Chapter 12 cross-references the **Negative Results Are Magic** sidebar (Randall Bosetti) for a longer treatment of why experiments that disconfirm their hypothesis are valuable. A test that refutes a candidate cause has genuinely advanced the investigation; recording and publishing these results matters. See [[negative-results]].

## Cross-book connection

- [[incident-response-mindset]] — the pace-not-rush discipline from Chapter 11 is what enables thoughtful test design under pressure. Rushing produces confounded experiments; pacing produces informative ones.
- [[hermetic-builds]] / [[idempotence]] — an idempotent, repeatable system is one where active tests can be re-run and reverted cleanly. Chapter 12's test discipline presupposes this as a design property.
- [[blameless-postmortem]] — the notes from Test/Treat become the raw material for the postmortem timeline.

## Related pages

- [[troubleshooting-model]]
- [[hypothetico-deductive-debugging]]
- [[divide-and-conquer-debugging]]
- [[negative-results]]
- [[troubleshooting-anti-patterns]]
- [[blameless-postmortem]]
- [[site-reliability-engineering]]
