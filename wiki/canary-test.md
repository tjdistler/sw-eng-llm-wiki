# Canary Test

**Summary**: Chapter 17's "conspicuously absent" entry from the production-test list: a canary test **isn't really a test** — it's structured user acceptance against live traffic. A subset of servers is upgraded, left to "bake" under real production load, then either expanded or rolled back based on observed variance. The chapter adds a precise mathematical treatment of what an exponential rollout reveals about the *order* of an underlying fault.

**Sources**: `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`, `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## Not really a test

> The canary test is conspicuously absent from this list of production tests. (source: chapter-17-testing-for-reliability.md)

The chapter flags this deliberately:

> A canary test isn't really a test; rather, it's structured user acceptance. Whereas configuration and stress tests confirm the existence of a specific condition over deterministic software, a canary test is more ad hoc. It only exposes the code under test to less predictable live production traffic, and thus, it isn't perfect and doesn't always catch newly introduced faults. (source: chapter-17-testing-for-reliability.md)

The distinction matters: [[configuration-test|configuration tests]] and [[stress-tests]] check deterministic properties. A canary watches emergent behaviour in a live production sample. It's a surveillance mechanism, not a pass/fail check.

## The baking metaphor

> To conduct a canary test, a subset of servers is upgraded to a new version or configuration and then left in an incubation period. Should no unexpected variances occur, the release continues and the rest of the servers are upgraded in a progressive fashion. Should anything go awry, the single modified server can be quickly reverted to a known good state. We commonly refer to the incubation period for the upgraded server as "baking the binary." (source: chapter-17-testing-for-reliability.md)

The name is load-bearing: **canary in a coal mine**. The canary dies from toxic gas before humans do. A canary server catches a release defect before it exposes the full fleet.

## The exponential-rollout rule of thumb

Chapter 17's suggested rollout schedule, elaborated in a footnote (source: chapter-17-testing-for-reliability.md):

> A standard rule of thumb is to start by having the release impact 0.1% of user traffic, and then scaling by orders of magnitude every 24 hours while varying the geographic location of servers being upgraded (then on day 2: 1%, day 3: 10%, day 4: 100%).

Exponential growth across orders of magnitude; geographic variation so a geo-specific bug surfaces early; four days to full rollout if nothing goes wrong.

## Order of a fault

The chapter's unique contribution: a mathematical treatment of what the number of variance reports during an exponential rollout tells you about the **order** of an underlying fault.

Given the relationship `C_U = R*K` where *C* is cumulative reports, *R* is the rate of reports, *U* is the order of the fault, and *K* is the period over which traffic grows by a factor of *e* (~172%), the order *U* can be estimated from the rate and cumulative reports before rollback (source: chapter-17-testing-for-reliability.md).

Fault orders:

- **U = 1**: The user's request encountered code that is simply broken. Scales linearly with traffic. Most bugs are order one [Per07].
- **U = 2**: This user's request randomly damages data that a future user's request may see.
- **U = 3**: The randomly damaged data is also a valid identifier to a previous request.

**Order-one bugs can be converted to [[regression-tests]] from logs of unusual responses.** Order-two and order-three bugs cannot, because replaying a request in isolation doesn't reproduce the cross-request interaction. This is the operational reason canaries exist alongside pre-deploy testing.

## Rollout fairness doesn't matter for the estimate

> When you are using an exponential rollout strategy, it isn't necessary to attempt to achieve fairness among fractions of user traffic. As long as each method for establishing a fraction uses the same K interval, the estimate of U will be valid even though you can't yet determine which method was instrumental in illuminating the fault. Using many methods sequentially while permitting some overlap keeps the value of K small. This strategy minimizes the total number of user-visible variances C while still allowing an early estimate of U (hoping for 1, of course). (source: chapter-17-testing-for-reliability.md)

The mathematical implication: **small K is what you want**. Short interval × many overlapping ramp methods = early estimate of fault order with minimum user impact.

## Chapter 27's launch framing

SRE Chapter 27 places the canary inside the broader [[gradual-rollout|gradual and staged rollout]] pattern: "the first stages of a rollout are usually called 'canaries'" (source: chapter-27-reliable-product-launches-at-scale.md). Three Chapter 27 additions:

- **Canary testing is embedded across Google's automated change tools.** Tools that install new software typically observe the newly started server for a period, and automatically roll back if the change doesn't pass the validation window. The canary is infrastructure, not a per-release activity.
- **Configuration-file tools canary too.** The pattern extends beyond binaries to any system making automated changes.
- **Client-side canaries.** Android app rollouts offer the new version to a subset of installs, with the fraction growing over time — the launch-time version of the server-side canary.

Chapter 27 also implicitly motivates the canary's distinctive value at launch: [[overload-behavior-launches|overload behaviour can't be predicted from first principles]], so some fraction of faults will only surface under live production load. The exponential rollout from Chapter 17 and the staged-geographic rollout from Chapter 27 converge on the same answer — expose incrementally so the unobservable becomes observed in time to revert.

## Chapter 13's sharpening

Chapter 13's [[change-induced-emergency|configuration-push case]] found that a "less stringent canary" let a crash-loop bug through. The configuration-keyword/feature interaction that triggered it wasn't present in any previous canary run. The operational rule distilled from that incident: **canary coverage must match the combinatorial surface, not the apparent risk level** (source: `raw/site-reliability-engineering/chapter-13-emergency-response.md` via [[change-management-sre]]).

## Cross-book connections

- [[progressive-delivery]] (Newman / Burns) — canary is the flagship progressive-delivery technique; the rollout arithmetic in Chapter 17 quantifies what Newman and Burns describe qualitatively
- [[change-management-sre]] — canary is the "progressive rollout" leg of the automation trio; Ch 13's sharpening is embedded there
- [[change-induced-emergency]] (Ch 13) — the case study that proved the "combinatorial surface" rule
- [[sisyphus]] (Ch 8) — the general-purpose rollout framework that executes the canary pattern across Google services
- Chaos engineering (industry practice) — the statistical-testing tools Chapter 17 cites ([[statistical-testing-techniques|Chaos Monkey, Jepsen]]) induce variance canaries must then catch

## Related pages

- [[testing-for-reliability]]
- [[change-management-sre]]
- [[change-induced-emergency]]
- [[progressive-delivery]]
- [[sisyphus]]
- [[regression-tests]]
- [[stress-tests]]
- [[statistical-testing-techniques]]
- [[gradual-rollout]]
- [[reliable-product-launches]]
- [[overload-behavior-launches]]
