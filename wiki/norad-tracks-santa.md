# NORAD Tracks Santa

**Summary**: SRE Chapter 27's opening case study. Google collaborated with NORAD to host a Christmas-themed site tracking Santa around the world, with a "virtual fly-over" backed by Keyhole (the satellite-imagery service for Google Maps and Google Earth). On Christmas Eve 2011 the project received up to one million requests per second — **25 times** Keyhole's normal peak. The launch had every attribute of high risk: a hard deadline, heavy publicity, a worldwide audience, and an extremely steep traffic ramp. It is the chapter's motivating example for why [[launch-coordination-engineering|LCE]] exists as a distinct SRE function.

**Sources**: `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## The project

Google partnered with NORAD (the North American Aerospace Defense Command) for a Christmas-Eve website tracking Santa's progress around the world in real time. Part of the experience was a **virtual fly-over** using satellite imagery to track Santa over a simulated world. The backend for the fly-over was Keyhole — ordinarily serving up to several thousand satellite images per second for Google Maps and Google Earth (source: chapter-27-reliable-product-launches-at-scale.md).

On Christmas Eve 2011, Keyhole received **upward of one million requests per second — 25x its normal peak**.

## Why it was a hard launch

Whimsical-looking but a textbook hard launch (source: chapter-27-reliable-product-launches-at-scale.md):

- **Hard deadline.** Google couldn't ask Santa to come a week later if the site wasn't ready.
- **Heavy publicity.** Millions of children watching.
- **Worldwide audience.** Every time zone hits Christmas Eve in sequence.
- **Steep traffic ramp-up.** Nearly every user arrives in a predictable narrow window.

Combine those and the project had every attribute a launch coordinator is trained to worry about: the failure modes of runaway success, of synchronised client behaviour, of hard-to-predict demand curves, of high-profile outage cost.

## The Make-children-cry switches

SRE prepared infrastructure so Santa could "deliver all his presents on time under the watchful eyes of an expectant audience." The chapter names the various kill switches built into the experience to protect Google's services during the event (source: chapter-27-reliable-product-launches-at-scale.md):

> In fact, we dubbed the various kill switches built into the experience to protect our services "Make-children-cry switches."

The name captures the trade-off the kill switches let SRE make in an incident: degrading the user-facing experience (graceful degradation, disabled features, fallback content) is preferable to taking down the backing services that many other Google products also depend on. The naming is deliberate dark humour — it reminds on-call engineers that using the switch *has a cost* and shouldn't be first-resort. See [[graceful-degradation]] for the general pattern.

## What the case motivates

The chapter uses this as the motivating example for LCE (source: chapter-27-reliable-product-launches-at-scale.md):

> Anticipating the many different ways this launch could go wrong and coordinating between the different engineering groups involved in the launch fell to a special team within Site Reliability Engineering: the Launch Coordination Engineers (LCE).

Individually, Google's teams could each have reasoned about their own piece. The cross-team coordination — mapping Keyhole's load sensitivity to front-end rollout plans to marketing's publicity schedule to the kill-switch choreography — was the distinctively LCE job. A pure product-embedded SRE team wouldn't have the cross-product experience; a pure release-engineering function wouldn't own reliability.

## Cross-references

- [[reliable-product-launches]] — chapter hub
- [[launch-coordination-engineering]] — the team that coordinated the launch
- [[launch-checklist-themes]] — the capacity section explicitly notes launches tied to publicity as higher-risk
- [[graceful-degradation]] — the general name for the Make-children-cry switch pattern

## Related pages

- [[reliable-product-launches]]
- [[launch-coordination-engineering]]
- [[launch-checklist-themes]]
- [[graceful-degradation]]
- [[capacity-planning]]
- [[overload-behavior-launches]]
- [[site-reliability-engineering]]
