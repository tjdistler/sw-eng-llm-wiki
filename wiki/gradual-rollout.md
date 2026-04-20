# Gradual and Staged Rollouts

**Summary**: SRE Chapter 27's canonical launch-safety technique: very few launches at Google are "push-button" — most follow a defined staged process with verification steps between stages. A server is installed on a few machines in one datacenter and observed; then on all machines in one datacenter and observed; then all machines globally. The first stage is a [[canary-test|canary]]. The pattern also applies to Android apps (subset of installs upgrade first) and to invite systems (limited signups per day, often coupled with user-invite quotas).

**Sources**: `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## "Never change a running system"

Chapter 27's framing (source: chapter-27-reliable-product-launches-at-scale.md):

> One adage of system administration is "never change a running system." Any change represents risk, and risk should be minimized in order to assure reliability of a system. What's true for any small system is doubly true for highly replicated, globally distributed systems like those run by Google.

The gradual rollout is the operational response. Very few launches at Google are of the "push-button" variety that exposes a new product to the entire world at one specific time.

## The canonical staged pattern

> A new server might be installed on a few machines in one datacenter and observed for a defined period of time. If all looks well, the server is installed on all machines in one datacenter, observed again, and then installed on all machines globally.

Three stages, each a superset of the prior, each separated by an observation window. The first stage is the [[canary-test|canary]] — named after miners' canaries, which detect dangerous gases before they affect humans. Canary servers detect dangerous behaviour under real user traffic before the rest of the fleet is exposed.

**Canary testing is embedded across Google's tooling.** Tools that manage new-software installation typically observe the newly started server for a period, making sure it doesn't crash or misbehave. If the change doesn't pass the validation window, it's automatically rolled back. The same applies to tools that change configuration files — see [[configuration-test]], [[configuration-integration-testing]].

## Client-side gradual rollout

The pattern extends beyond server software. New versions of Android apps can be rolled out gradually, with the updated version offered to a subset of installs. The upgraded fraction grows over time until it reaches 100%. This is especially useful when the new client version drives additional backend traffic: the backend-side effect is observed and measured as the client fleet migrates.

## Invite systems as rollout

The **invite system** is another form of gradual rollout (source: chapter-27-reliable-product-launches-at-scale.md). Rather than allowing free signups to a new service, only a limited number of users are allowed to sign up per day. Rate-limited signups are often coupled with an invite mechanism, where an existing user can send a limited number of invites to friends. Both the per-day rate limit and the invite-quota cap give the service operator control over the ramp.

## Where this sits in the chapter

The gradual rollout is one of the three techniques Chapter 27 identifies as especially well-suited to launches — alongside [[feature-flag-framework|feature flag frameworks]] and the overload/load-testing discipline in [[overload-behavior-launches]]. Together they give a launch operator the ability to control the exposure curve across time, population, geography, and traffic.

## Cross-references

- [[canary-test]] develops the first-stage-only view with the exponential-rollout mathematics from Ch 17.
- A general-purpose rollout-orchestration framework implements the staged pattern across Google services.
- [[change-management-sre]] is the broader SRE discipline this technique realises.
- [[progressive-delivery]] is Newman's and Burns's umbrella term for the same family of techniques.

## Related pages

- [[canary-test]]
- [[feature-flag-framework]]
- [[change-management-sre]]
- [[progressive-delivery]]
- [[reliable-product-launches]]
- [[launch-checklist-themes]]
- [[site-reliability-engineering]]
