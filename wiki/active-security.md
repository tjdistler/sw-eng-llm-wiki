# Active Security

**Summary**: Reis & Housley's Chapter 10 counterpart to [[security-theater]]: rather than deploying scheduled simulated phishing drills and standard compliance checklists, actively research current threats and think through organisation-specific vulnerabilities. Applies to both process (researching real-world attacks) and technology (every engineer treating their systems' security holes as their own responsibility).

**Sources**: `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## The stance

Active security is **the power of negative thinking applied operationally** (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Active security entails thinking about and researching security threats in a dynamic and changing world.

The contrast Chapter 10 draws:

| Passive security | Active security |
|---|---|
| Deploy scheduled simulated phishing attacks | Research actual recent successful phishing attacks and think through how your org would fall for them |
| Adopt a standard compliance checklist | Reason about internal vulnerabilities specific to your org |
| Ask "do we meet the standard?" | Ask "where are our unique attack surfaces?" |
| React to standards bodies | Anticipate emerging threats |

Active security does not *replace* compliance — it layers reasoning about real adversaries on top of it.

## Applied to process

On the process side, active security means the team regularly asks:

- What phishing attacks have hit similar organisations recently? Would we fall for them?
- What incentives might our own employees have to leak or misuse private data? Are we mitigating them?
- What are our specific vulnerabilities — the combinations of systems, roles, and data that are unique to us and wouldn't show up on a generic checklist?

This is not [[threat-modeling]] as a one-time exercise; it is a continuous habit.

## Applied to technology — internal security research

Chapter 10's technology section makes a structural argument for why every engineer should think about security (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Every technology employee should think about security problems. Why is this important? Every technology contributor develops a domain of technical expertise. Even if your company employs an army of security researchers, data engineers will become intimately familiar with specific data systems and cloud services in their purview. Experts in a particular technology are well positioned to identify security holes in this technology.

The implication: security is **not exclusively the security team's job**. A dedicated security team can't be as deeply familiar with the data engineer's Kafka cluster, warehouse partition scheme, or pipeline orchestrator as the data engineer is. The engineer who knows the technology best is also best positioned to find its flaws.

The prescription: "Encourage every data engineer to be actively involved in security. When they identify potential security risks in their systems, they should think through mitigations and take an active role in deploying these."

## Connection to [[shared-responsibility-model|shared responsibility]]

The [[shared-responsibility-model]] puts security accountability on the application engineer. Active security is the **behavioural stance** that matches that accountability structure — once the cloud has made you a security engineer, passively waiting for a central security team to find your vulnerabilities is organisationally incoherent.

## Related pages

- [[data-security]]
- [[security-theater]]
- [[threat-modeling]]
- [[shared-responsibility-model]]
- [[zero-trust-security]]
- [[security-monitoring]]
- [[fundamentals-of-data-engineering]]
