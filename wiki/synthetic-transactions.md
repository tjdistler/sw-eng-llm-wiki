# Synthetic Transactions

**Summary**: Scripted fake user behaviour run continuously against the production system to verify that key flows still work. The "test in production" complement to pre-deployment functional tests — and a faster signal than waiting for a real user to hit a broken flow.

**Sources**: `raw/monolith-to-microservices/chapter-05-growing-pains.md`

**Last updated**: 2026-04-16

---

## The idea

Pre-deployment functional tests give us confidence that software is fit to ship. But once the software is in production, we want the same kind of feedback continuously — environmental drift, downstream service changes, or new releases can break a flow that worked at deploy time (source: chapter-05-growing-pains.md).

Synthetic transactions inject fake user behaviour into the live system to exercise key flows. We define the expected behaviour and alert if reality diverges.

## Newman's Atomist example

At Atomist, customer onboarding required authorising the product against both GitHub and Slack accounts — enough moving parts that early on it would hit issues (rate limiting against GitHub, etc.). Sylvain Hellegouarch scripted enrolment of fake customers; the script would trigger the full sign-up process on a regular basis. When it failed, the team caught the problem with a fake user instead of a real one (source: chapter-05-growing-pains.md).

Notably, Atomist created GitHub and Slack accounts they controlled for the synthetics, and the script cleaned up after itself. No real human was ever involved.

## The 200-washing-machines warning

Synthetic transactions exercise *real* services. If those services have side effects in the real world, you must isolate the synthetics from those side effects.

> "I did hear reports of a company that ended up accidentally ordering 200 washing machines to be delivered to their head office because they hadn't properly accounted for the fact that the test orders would actually end up getting sent out." (source: chapter-05-growing-pains.md)

A "test customer" account in your production database is not enough if your fulfilment system doesn't distinguish test from real. Either:

- Make the synthetic flows actually distinguishable downstream (test product SKUs, test customer flag honoured by every step including fulfilment), or
- Run synthetics only against flows whose side effects are reversible or contained.

## A starting point

Newman suggests reworking existing end-to-end test cases for use against production (source: chapter-05-growing-pains.md). If you already have a test that drives a user through key flows, the same script — pointed at production with the side-effect concerns above sorted out — can become your synthetic.

## Where this fits in observability

Synthetic transactions complement reactive [[monitoring-and-observability]]: instead of waiting for a real user to hit a problem and then asking "what just happened?", you continuously verify the flows you most care about. The first signal of a broken flow is your own alert, not a customer ticket.

## Related pages

- [[monitoring-and-observability]]
- [[end-to-end-testing]]
- [[progressive-delivery]]
- [[consumer-driven-contracts]]
