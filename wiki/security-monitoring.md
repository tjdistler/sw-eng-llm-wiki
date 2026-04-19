# Security Monitoring

**Summary**: Logging, monitoring, and alerting applied specifically to security events. Chapter 10 lists it as a core technology practice: hackers don't announce their presence, so you detect them through anomalies in access patterns, resource usage, billing, and permissions. A sibling to general [[monitoring-and-observability]] and [[data-observability]], but oriented around the question "is someone I don't recognise doing something they shouldn't?"

**Sources**: `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## Why security monitoring is distinct

Chapter 10's framing (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Hackers and bad actors typically don't announce that they're infiltrating your systems. Most companies don't find out about security incidents until well after the fact.

Ordinary observability answers "is the system healthy?" Security monitoring answers "is the system being misused?" The signals differ:

| Ordinary observability | Security monitoring |
|---|---|
| Latency, error rate, throughput | Access patterns, permission grants, credential usage |
| Health = matches SLO | Health = matches expected user/system behaviour |
| Alert on service degradation | Alert on behaviour *anomalies*, even when the service is fine |

The chapter places this under [[dataops]] as part of the broader "observe, detect, and alert on incidents" discipline.

## The four areas to monitor

Chapter 10 lists four monitoring surfaces (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

### 1. Access

The core question: **who is accessing what, when, and from where?**

Signals:

- New accesses granted — who granted them, to whom, for what role.
- Strange patterns among current users — accessing systems they don't usually access, or shouldn't have access to at all. Often indicates a compromised account.
- New unrecognised users appearing in the system.

"Be sure to regularly comb through access logs, users, and their roles to ensure that everything looks OK."

### 2. Resources

Sudden changes in disk, CPU, memory, or I/O can indicate a breach — crypto miners running on compromised VMs, bulk data exfiltration, etc. The same metrics used for capacity planning double as security canaries.

### 3. Billing

Especially for [[cloud|cloud]] and SaaS: unexpected cost spikes are often the first observable symptom of a breach. Attackers compromising an AWS account commonly spin up expensive GPU instances to mine cryptocurrency or use compute to attack other targets. **Budget alerts** are a security control.

### 4. Excess permissions

Modern cloud vendors provide tools that monitor for permissions a user or service account hasn't used over some period. The chapter's worked example:

> Suppose that a particular analyst hasn't accessed Redshift for six months. These permissions can be removed, closing a potential security hole. If the analyst needs to access Redshift in the future, they can put in a ticket to restore permissions.

This is [[least-privilege]] operationalised — automated permission decay closes the gap between "needed access two years ago" and "still has access today."

## Automated anomaly detection

Chapter 10 recommends setting up **automatic anomaly detection** where possible — statistical baselines for each of the four surfaces above, with alerts when behaviour deviates. This connects to the broader [[dataops]] statistical-process-control practice.

## The team dashboard

The chapter's concrete recommendation (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> We suggest setting up a dashboard for everyone on the data team to view monitoring and receive alerts when something seems out of the ordinary.

Security monitoring is not a specialist pane of glass for a security team only — every data engineer should have eyes on access and resource patterns for the systems they own. See [[active-security]] for the cultural argument.

## Incident response is the other half

Monitoring without response is passive. The chapter pairs monitoring with:

> An effective incident response plan to manage security breaches when they occur, and run through the plan on a regular basis so you are prepared.

The run-through-on-a-regular-basis piece matches SRE's [[disaster-role-playing]] / [[preparedness-and-disaster-testing]] discipline — a plan that has never been rehearsed has never been tested.

## Cross-book connections

- [[monitoring-and-observability]] — the broader reliability-engineering discipline; security monitoring is a specialisation.
- [[data-observability]] — the data-quality sibling; both monitor for silent failures.
- [[alert-philosophy]] — SRE's framework for what's worth alerting on.
- [[disaster-role-playing]] — the drill-the-response-plan discipline this depends on.

## Related pages

- [[data-security]]
- [[active-security]]
- [[least-privilege]]
- [[dataops]]
- [[monitoring-and-observability]]
- [[data-observability]]
- [[fundamentals-of-data-engineering]]
