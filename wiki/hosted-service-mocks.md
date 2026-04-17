# Hosted-Service Mocks and Emulators

**Summary**: How to do [[local-integration-testing]] when a production component is a closed-source hosted service (AWS Kinesis, Google PubSub, Azure Event Hubs, managed FaaS). Some vendors ship local emulators; third-party open-source projects fill some gaps; and for the remainder there is no good option short of [[remote-integration-testing]].

**Sources**: `raw/building-event-driven-microservices/chapter-15-testing-event-driven-microservices.md`

**Last updated**: 2026-04-17

---

## The problem

An EDM that runs on a managed hosted broker or FaaS platform in production cannot necessarily be tested locally — proprietary services usually have no open-source implementation you can download and run (source: chapter-15-testing-event-driven-microservices.md).

## Three tiers of what to expect

**Vendor-shipped emulators.** The best case. The vendor ships a local binary that implements enough of the service's API for testing. Example: **Google PubSub** has an emulator adequate for local testing (source: chapter-15-testing-event-driven-microservices.md).

**Open-source emulators.** Third-party projects reimplement the service's API. Example: **LocalStack** provides open-source local implementations of Amazon Kinesis and many other AWS services.

**Nothing.** At time of writing, **Azure Event Hubs** had neither a vendor emulator nor an open-source implementation. The recommended workaround was the Event Hubs clients' Apache Kafka compatibility mode — talk to a local [[log-based-message-brokers|Kafka]] instance instead — but not all features are supported (source: chapter-15-testing-event-driven-microservices.md).

When no local option exists, developers must each provision a remote staging environment, incurring provisioning cost, security concerns around connecting local code to remote resources, and cleanup overhead. Bellemare's advice: **pick services with this trajectory in mind** — most closed-source providers are adding local options over time, but right now the pain is real.

## FaaS platforms

[[functions-as-a-service|FaaS]] platforms all ship local testing libraries: Google Cloud Functions, AWS Lambda, Azure Functions, and the open-source OpenWhisk / OpenFaaS / Kubeless. These can establish a complete local FaaS environment configured to approximate production (source: chapter-15-testing-event-driven-microservices.md).

## Heavyweight frameworks

[[heavyweight-framework-microservice|Heavyweight frameworks]] install into the same kind of single-container local environment as FaaS — run the master and worker instances side-by-side in the container along with the [[event-broker]] and other dependencies; the application submits its job to the master and reads output from the output streams (source: chapter-15-testing-event-driven-microservices.md).

## When there's nothing

Bellemare is blunt about the fallback when no emulator exists (source: chapter-15-testing-event-driven-microservices.md):

- Either tightly-controlled per-developer remote staging environments (access-controlled), or
- A single shared remote environment used by all (with its own [[remote-integration-testing|shared-environment pathologies]]).

Either way you are effectively doing [[remote-integration-testing]] for what ought to have been a local concern. The long-term answer is to bias service selection toward products that have a story for local development.

## Related pages

- [[local-integration-testing]]
- [[remote-integration-testing]]
- [[functions-as-a-service]]
- [[heavyweight-framework-microservice]]
- [[event-broker]]
- [[log-based-message-brokers]]
