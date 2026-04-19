# Data Security

**Summary**: The first of the six [[data-engineering-lifecycle|lifecycle]] **undercurrents** in Reis and Housley's framing. Security must be top of mind for data engineers — the engineer carries operational responsibility for the [[least-privilege|principle of least privilege]], access control, encryption, and the human-organisational culture that determines whether those technical measures work in practice. Chapter 10 gives the undercurrent its own dedicated treatment, organised around **people, processes, and technology — in that order**.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`, `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## Why security is the first undercurrent

Reis and Housley deliberately put security first among the six undercurrents: "those who ignore it do so at their peril." Data engineers must understand both data and access security, and exercise [[least-privilege|least privilege]] — giving users and systems access to only the essential data and resources needed to perform their function (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

A common antipattern the authors call out: data engineers with little security experience give **admin access to all users**. "This is a catastrophe waiting to happen. Give users only the access they need to do their jobs today, nothing more."

The principle applies to the engineer's own hands, too: don't work from a root shell when standard user access suffices; don't query with the superuser role when a lesser role would do. Self-imposed least privilege prevents accidental damage and keeps the engineer in a security-first mindset.

## People are the biggest vulnerability

"People and organizational structure are always the biggest security vulnerabilities in any company." The authors observe that major breaches covered in the media typically trace back to someone ignoring basic precautions, falling for phishing, or acting irresponsibly (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

The first line of defence is therefore a **culture of security** that permeates the organisation. Everyone who touches data must understand their responsibility to protect it.

## Dimensions of data security

Chapter 2 names the dimensions the engineer must handle (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Timing of access** — provide access only to the people and systems that need it, only for the duration needed.
- **Protection in flight and at rest** — encryption, tokenisation, data masking, obfuscation, robust access controls.
- **Identity and access management (IAM)** — roles, policies, groups; the administrator-level knowledge the engineer must hold.
- **Network security** — who can reach what.
- **Password policies and encryption** — baseline hygiene.

The engineer must be a **competent security administrator**, not just a developer — security "falls in their domain."

## Multi-tenant / embedded-analytics security

Embedded analytics (see [[data-serving]]) sharpens the security problem: businesses may serve analytics to thousands of customers and every customer must see their data and only their data. The chapter's framing: "minimise your blast radius" — apply tenant-level or data-level security in storage and anywhere data could leak. A data leak between customers is a massive breach of trust; an internal leak is a procedural review (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

## People, processes, technology (Chapter 10)

Chapter 10 organises security around three layers in order of importance (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

### People — the weakest link

"The weakest link in security and privacy is you." Most breaches are human compromises, not technical failures. Chapter 10 prescribes two postures:

- **[[threat-modeling|The power of negative thinking]].** Borrowed from Atul Gawande's 2007 op-ed: positive thinking blinds you to disaster scenarios. Think through how pipelines and storage could be attacked or leaked *before* you build them. "The best way to protect private and sensitive data is to avoid ingesting this data in the first place."
- **Always be paranoid.** "Trust nobody at face value when asked for credentials, sensitive data, or confidential information, including from your coworkers." When in doubt, hold off, get a second opinion, call the person back. "A quick chat or phone call is cheaper than a ransomware attack triggered through an email click."

The engineer is also the first line of defence for ethics: uncomfortable with the data being collected? Raise concerns. Ensure the work is both legally compliant *and* ethical. See [[data-ethics]].

### Processes — habits, not theatre

Chapter 10 names [[security-theater]] explicitly as the antipattern — compliance-box-ticking without genuine security. The antidote is habit: simple practices repeated often enough to become automatic.

Key process disciplines:

- **[[security-theater|Security theater vs security habit]]** — short, memorable, frequently-rehearsed practices beat 200-page unread policies.
- **[[active-security]]** — research current real-world attacks and your org's unique vulnerabilities, not just checklist items.
- **[[least-privilege|Principle of least privilege]]** — people and systems get only what they need, only for as long as they need it. Extended in Chapter 10 to include column/row/cell-level access, PII masking, views-over-tables, and **broken-glass processes** for emergency access.
- **[[shared-responsibility-model|Shared responsibility in the cloud]]** — the provider owns the platform, you own the configuration. "Most cloud security breaches continue to be caused by end users, not the cloud."
- **Back up your data** — for ransomware recovery as well as disaster recovery. Test restores regularly. See [[backups-vs-archives]].
- **[[security-policy|A short, practical security policy]]** — credentials, devices, software updates, all on a page people will actually read.

### Technology — the baseline stack

Chapter 10's technology priorities:

- **Patch and update systems.** Automate where possible; alert on CVEs for the rest.
- **[[encryption-at-rest]]** and **[[encryption-in-transit]]** — baseline, not silver bullet. Useless against a human credential breach; essential against interception, theft, and mis-permissioning.
- **[[secrets-management]]** — credentials as configuration, never in code, SSO and MFA everywhere possible.
- **[[security-monitoring|Logging, monitoring, and alerting]]** — access, resource, billing, and excess-permission anomalies. Couple with a rehearsed incident-response plan.
- **[[network-access-security|Network access controls]]** — know what IPs and ports are open, to whom, and why; avoid `0.0.0.0/0`; use VPCs, bastions, VPNs.
- **Security for low-level data engineering.** Every dependency, CPU microarchitecture, and logging library is a potential vulnerability. Apply [[active-security|internal security research]] to your own systems — the engineer who knows the system best is best positioned to find its flaws.

### The closing posture

> Security needs to be a habit of mind and action; treat data like your wallet or smartphone. Although you won't likely be in charge of security for your company, knowing basic security practices and keeping security top of mind will help reduce the risk of data security breaches at your organization. (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md)

## Connection to the other undercurrents

- **[[data-governance]]** — access controls, discoverability with accountability, and classification of sensitive data are shared surface area.
- **[[data-ethics]]** — PII masking, consent, and privacy regulation (GDPR, CCPA) are ethical-and-legal counterparts to purely technical security.
- **[[dataops]]** — observability and incident response extend to security incidents.

## Cross-book connections

- [[defense-in-depth-data]] (DDIA) names the layered-protection pattern at the data-storage level.
- [[event-stream-acls]] (Bellemare) is the event-driven-microservices view of access control for event streams — tied automatically to the [[data-lineage|topology graph]].

## Related pages

- [[least-privilege]]
- [[data-engineering-lifecycle]]
- [[data-governance]]
- [[data-ethics]]
- [[defense-in-depth-data]]
- [[event-stream-acls]]
- [[security-theater]]
- [[active-security]]
- [[threat-modeling]]
- [[encryption-at-rest]]
- [[encryption-in-transit]]
- [[secrets-management]]
- [[security-monitoring]]
- [[network-access-security]]
- [[security-policy]]
- [[zero-trust-security]]
- [[shared-responsibility-model]]
