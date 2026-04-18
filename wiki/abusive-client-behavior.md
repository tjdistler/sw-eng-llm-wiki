# Dealing with Abusive Client Behavior

**Summary**: SRE Chapter 27's treatment of the non-user-initiated-request problem. On a traditional website every request is triggered by a user action (a click), so request rate is bounded by user throughput. Apps that sync periodically, sites that auto-refresh, offline-retry protocols, and retry loops all break this assumption — inadvertent client design choices can easily threaten a service's stability. Defences: server-controlled client configuration, exponential backoff with jitter, random scheduling of periodic work, and dormant functionality shipped ahead of activation.

**Sources**: `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## The axiom that no longer holds

Traditional website design (source: chapter-27-reliable-product-launches-at-scale.md):

> On a traditional website, there is rarely a need to take abusive behavior from legitimate users into account. When every request is triggered by a user action such as a click on a link, the request rates are limited by how quickly users can click. To double the load, the number of users would have to double.

This axiom breaks for apps that sync periodically, websites that auto-refresh, and any other client that initiates action on its own schedule. In these cases abusive client behaviour can threaten stability even from first-party clients the service operator supposedly controls. This is a distinct problem from defending against abusive **external** traffic (scrapers, DoS attacks).

## Misjudged update rates

The simplest failure mode: a client that syncs every 60 seconds instead of every 600 seconds causes **ten times** the load on the service. The decision looks harmless at the client-development stage and catastrophic at the service scale.

## Retry pitfalls

Retry behaviour has two well-known pitfalls (source: chapter-27-reliable-product-launches-at-scale.md):

### Retry amplification

A service that is overloaded and therefore failing some requests: if clients retry the failed requests, they add load to an already overloaded service, producing more retries and more requests. See [[retry-amplification]] for the SRE Chapter 22 development of this mechanism.

The chapter prescribes:

- **Reduce retry frequency** via exponentially increasing delay between retries
- **Be careful about which errors warrant retries** — a network error usually does; a 4xx HTTP error (client-side problem) usually does not

### Thundering herd

Intentional or inadvertent synchronisation of automated requests produces a thundering herd. The chapter's canonical example: an app developer decides 2 a.m. is a good download time because users are asleep. Every client download-updates at 2 a.m., producing a nightly spike at the download server and almost no requests at any other time.

The fix: **every client should choose the time randomly**. This applies broadly — retries also need jitter:

> Take the example of a client that sends a request, and when it encounters a failure, retries after 1 second, then 2 seconds, then 4 seconds, and so on. Without randomness, a brief request spike that leads to an increased error rate could repeat itself due to retries after 1 second, then 2 seconds, then 4 seconds. In order to even out these synchronized events, each delay needs to be jittered (that is, adjusted by a random amount).

See also [[cron-thundering-herd]] for the server-side analogue in Google's Cron scheduler.

## Server-controlled client configuration

Chapter 27's foundational defence for any client fleet not controlled by the server (source: chapter-27-reliable-product-launches-at-scale.md):

> The ability to control the behavior of a client from the server side has proven an important tool in the past.

For an app on a device, this might mean instructing the client to check in periodically and download a configuration file that can:

- Enable or disable specific features
- Set parameters such as sync frequency or retry policy
- Enable completely new user-facing functionality

Configuration delivery decouples **release** from **activation** — code is shipped, then activated (or not) by a config change. This is [[deployment-vs-release]] applied to clients.

## Dormant functionality

The more sophisticated realisation of server-controlled clients: **host code supporting new functionality in the client application before activating the feature** (source: chapter-27-reliable-product-launches-at-scale.md).

Benefits:

- **Reduces launch risk** — activating is cheaper and lower-risk than shipping new client code to every user's device
- **Simplifies release trains** — no parallel release tracks for "version with feature X" vs "version without feature X"; one binary supports both states
- **Avoids combinatorial version explosion** — a set of independent features on different schedules would otherwise require maintaining many version combinations
- **Makes aborting launches easy** — if a rollout shows problems, flip the feature off, iterate, release an updated version

The alternative (no dormant functionality) requires providing a new app without the feature and forcing an update on all users' phones — slow, costly, and high-friction.

This is the client-side form of [[feature-flag-framework|feature flag frameworks]]. The server-side flag activates code that was already shipped.

## Relationship to the launch checklist

This problem area maps to the **client behavior** section of the [[launch-checklist-themes|launch checklist]]:

> Example question: Do you have auto-save / auto-complete / heartbeat functionality?
>
> Example action items: Make sure that your client backs off exponentially on failure. Make sure that you jitter automatic requests.

The three action-bucket defences are: (1) exponential backoff with jitter on failure retries, (2) random scheduling of periodic work, (3) server-controlled configuration for emergency adjustment.

## Related pages

- [[retry-amplification]]
- [[retry-budget]]
- [[cron-thundering-herd]]
- [[feature-flag-framework]]
- [[deployment-vs-release]]
- [[rate-limiting]]
- [[request-criticality]]
- [[launch-checklist-themes]]
- [[reliable-product-launches]]
- [[site-reliability-engineering]]
