# Overload Behavior and Load Tests at Launch

**Summary**: SRE Chapter 27's treatment of overload as a distinctive launch risk. Overload has many causes at launch time — runaway success (the most welcome), load-balancing failures, machine outages, synchronised client behaviour, external attacks. A naive model says CPU use scales linearly with load until exhausted; real services rarely behave this way. Caches make lightly-loaded services slower than expected; above the linear region, services often lock up completely. Because first-principles prediction is hard, **load tests are mandatory for most launches**.

**Sources**: `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## Why overload deserves special attention at launch

Overload is a "particularly complex failure mode" and therefore warrants extra attention at launch (source: chapter-27-reliable-product-launches-at-scale.md). The causes at launch time:

- **Runaway success** — the most welcome cause; public interest can exceed estimates by 15x (see [[launch-checklist-themes]] capacity section)
- **Load balancing failures**
- **Machine outages**
- **Synchronized client behavior** — see [[abusive-client-behavior]]
- **External attacks**

Overload defences from [[handling-overload]] and [[cascading-failure]] apply generally. Chapter 27's addition is the **launch-time framing**: the first time overload is real is often the launch, and the first time a service's overload behaviour is observed is often production. Both conditions need addressing before the launch day.

## The naive model and why it's wrong

The naive assumption (source: chapter-27-reliable-product-launches-at-scale.md):

> A naive model assumes that CPU usage on a machine providing a particular service scales linearly with the load (for example, number of requests or amount of data processed), and once available CPU is exhausted, processing simply becomes slower.

Real services don't behave this way. Two deviations:

### Caches make lightly-loaded services slower

CPU caches, JIT caches, service-specific data caches — all of these mean a warmed-up service is faster than a cold one. Request rates below steady-state can show counterintuitively high per-request CPU cost. See [[slow-startup-and-cold-caching]] for the cold-cache cascading-failure trigger; the launch-time version is the same phenomenon showing up at the upper end of the load curve.

### Overload is nonlinear at the top

As load increases, CPU and response time typically track linearly for a while — then hit a nonlinear region. The benign failure mode is rising response times (degraded user experience, possibly dependency timeouts propagating up). The drastic failure mode is **lockup**: the service grinds to a halt.

## The logging-amplification example

The chapter's specific example of overload-triggered lockup (source: chapter-27-reliable-product-launches-at-scale.md):

> A service logged debugging information in response to backend errors. It turned out that logging debugging information was more expensive than handling the backend response in a normal case. Therefore, as the service became overloaded and timed out backend responses inside its own RPC stack, the service spent even more CPU time logging these responses, timing out more requests in the meantime until the service ground to a complete halt.

Overload → more errors → more logging → less CPU available → more timeouts → more errors. A positive feedback loop that the service's operator did not design and could not have predicted from CPU-use-vs-QPS graphs at lower loads. See [[cascading-failure]] for the general form.

## GC thrashing

The JVM-specific version (source: chapter-27-reliable-product-launches-at-scale.md):

> In services running on the Java Virtual Machine (JVM), a similar effect of grinding to a halt is sometimes called "GC (garbage collection) thrashing." In this scenario, the virtual machine's internal memory management runs in increasingly closer cycles, trying to free up memory until most of the CPU time is consumed by memory management.

See [[gc-death-spiral]] for the SRE Chapter 22 development of this mechanism with the full nine-step cascade scenario.

## The load-test requirement

Because first-principles prediction fails (source: chapter-27-reliable-product-launches-at-scale.md):

> Unfortunately, it is very hard to predict from first principles how a service will react to overload. Therefore, load tests are an invaluable tool, both for reliability reasons and capacity planning, and load testing is required for most launches.

Load tests at launch time address two questions:

- **Where does the nonlinear region start?** — feeds capacity planning and saturation thresholds
- **How does the service degrade past that point?** — validates graceful-degradation design, checks that feedback loops (logging, GC, retry) don't produce lockup

See [[stress-tests]] for the SRE Chapter 17 framing of load tests finding the "catastrophic-failure cliff before production does."

## Connection to other chapter sections

The launch-time overload treatment intersects:

- [[launch-checklist-themes]] capacity section — launch spikes up to 15x initial estimates, 1-2 redundant deployments beyond the serving-capacity N, long lead times for compute resources
- [[abusive-client-behavior]] — synchronised client behaviour is one of the cited overload causes
- [[gradual-rollout]] — staged rollout is the mitigation when load prediction is uncertain; a single-datacenter stage lets overload be observed before it becomes global

## Related pages

- [[stress-tests]]
- [[cascading-failure]]
- [[gc-death-spiral]]
- [[slow-startup-and-cold-caching]]
- [[handling-overload]]
- [[load-shedding]]
- [[graceful-degradation]]
- [[capacity-planning]]
- [[launch-checklist-themes]]
- [[abusive-client-behavior]]
- [[gradual-rollout]]
- [[reliable-product-launches]]
- [[site-reliability-engineering]]
