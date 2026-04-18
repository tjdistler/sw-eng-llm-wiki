# Launch Checklist Themes

**Summary**: The nine themes Google's [[launch-checklist|launch checklist]] organises around, as documented in SRE Chapter 27. Each theme catalogues a category of risk a launch must address: architecture/dependencies, integration, capacity, failure modes, client behavior, processes/automation, development process, external dependencies, and rollout planning. The themes are company-general; the specific questions under each are tailored to the organisation's internal services and infrastructure.

**Sources**: `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## Architecture and dependencies

An architecture review verifies correct use of shared infrastructure and identifies the owners of that infrastructure as additional stakeholders. The list of dependencies feeds [[capacity-planning|capacity planning]] — each one needs correct provisioning (source: chapter-27-reliable-product-launches-at-scale.md).

**Example questions:**
- What is your request flow from user to frontend to backend?
- Are there different types of requests with different latency requirements?

**Example actions:**
- Isolate user-facing requests from non user-facing requests.
- Validate request-volume assumptions: one page view can turn into many requests.

See [[request-criticality]] for the user-facing-vs-batch request isolation discipline.

## Integration

The company's internal ecosystem — how to set up machines, configure new services, set up monitoring, integrate with load balancing, set up DNS — has its own idiosyncrasies. This section varies widely company to company.

**Example actions:**
- Set up a new DNS name for your service.
- Set up load balancers to talk to your service.
- Set up monitoring for your new service.

At Google the internal ecosystem means [[bns]], [[borg]], [[borgmon]], [[gslb]], and [[stubby]].

## Capacity planning

New features may show a **temporary launch spike** that subsides within days. The workload or traffic mix during the spike can differ substantially from steady state, throwing off load-test results. Public interest is notoriously hard to predict — some Google products had to accommodate launch spikes **up to 15 times higher than initially estimated** (source: chapter-27-reliable-product-launches-at-scale.md). Launching initially in one region or country helps build confidence for larger launches.

Capacity interacts with redundancy: three replicated deployments to serve 100% of peak means maintaining four or five to shield users from maintenance and failures. See [[n-plus-2-redundancy]]. Datacenter and network resources have long lead times and need early requests.

**Example questions:**
- Is this launch tied to a press release, ad, blog post, or other promotion?
- How much traffic and growth rate do you expect during and after launch?
- Have you obtained all compute resources needed to support your traffic?

See [[capacity-planning]] and [[intent-based-capacity-planning]].

## Failure modes

A systematic look at the failure modes of a new service ensures reliability from the start. Walk each component and dependency and identify the impact of its failure:

- Can the service deal with individual machine failures? Datacenter outages? Network failures?
- How does it handle bad input data? A DoS attack?
- Can it serve in degraded mode if a dependency fails?
- How does it handle dependency unavailability at startup? At runtime?

**Example actions:**
- Implement request deadlines to avoid running out of resources for long-running requests (see [[deadline-propagation]]).
- Implement load shedding to reject new requests early in overload (see [[load-shedding]]).

See [[fault-tolerance]], [[graceful-degradation]], [[cascading-failure]].

## Client behavior

The checklist's direct treatment of [[abusive-client-behavior|client-induced load]]. On a traditional website every request is user-driven, so request rate is bounded by user clicks. Clients that initiate actions without user input (apps syncing periodically, websites auto-refreshing) break this assumption and can threaten stability on their own.

**Example question:**
- Do you have auto-save / auto-complete / heartbeat functionality?

**Example actions:**
- Make sure your client backs off exponentially on failure (see [[retry-amplification]], [[retry-budget]]).
- Make sure you jitter automatic requests.

## Processes and automation

Google encourages engineers to use standard tools to automate common processes. Automation is never perfect, so every service has residual processes that need human execution: creating a new release, moving the service to a different datacenter, restoring from backups. For reliability, **minimise single points of failure, which include humans.** Document every residual process before launch, while the information is still fresh, so anyone on the team can execute it in an emergency.

**Example question:**
- Are there any manual processes required to keep the service running?

**Example actions:**
- Document all manual processes.
- Document the process for moving your service to a new datacenter.
- Automate the process for building and releasing a new version.

See [[automation-at-google]], [[autonomous-systems]], [[on-call-playbook]].

## Development process

Google is an extensive user of version control, and nearly every development process is integrated with it. Many best practices revolve around using version control effectively:

- Most development on the mainline branch; releases on per-release branches — see [[release-branching-and-cherry-picking]]
- Configuration files in version control too — history tracking, attribution, code review all apply
- In some cases, changes propagate from version control to live servers automatically

**Example actions:**
- Check all code and configuration files into the version control system.
- Cut each release on a new release branch.

See [[google-monorepo]], [[release-engineering]], [[configuration-management-sre]].

## External dependencies

Launches sometimes depend on factors outside company control — a third-party library, a vendor service, external data. Identifying these risks allows mitigation planning.

When a vendor outage, bug, security issue, or unexpected scalability limit hits, prior planning averts or reduces user-visible damage. Google has used filtering/rewriting proxies, data transcoding pipelines, and caches to mitigate such risks.

**Example questions:**
- What third-party code, data, services, or events does the service or launch depend on?
- Do partners depend on your service? If so, do they need to be notified of your launch?
- What happens if you or the vendor can't meet a hard launch deadline?

## Rollout planning

Few events in a large distributed system happen instantaneously. A complicated launch might require enabling features on multiple subsystems, each configuration change taking hours. A working config in a test instance doesn't guarantee rollout to production. Sometimes the components need a complicated dance or special functionality to launch cleanly in the right order.

External requirements from marketing and PR may complicate things further — a feature might need to be available at a conference keynote but invisible before it.

**Contingency measures** are part of rollout planning: what if you don't enable the feature in time? Sometimes a backup slide deck saying "We will be launching this over the next days" rather than "We have launched."

**Example actions:**
- Set up a launch plan identifying actions to launch the service; identify who owns each item.
- Identify risk in each launch step and implement contingency measures.

See [[progressive-delivery]], [[sisyphus]], [[canary-test]], [[feature-flag-framework]].

## Related pages

- [[launch-checklist]]
- [[launch-coordination-engineering]]
- [[reliable-product-launches]]
- [[capacity-planning]]
- [[fault-tolerance]]
- [[abusive-client-behavior]]
- [[feature-flag-framework]]
- [[gradual-rollout]]
- [[site-reliability-engineering]]
