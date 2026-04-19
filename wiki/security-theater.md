# Security Theater

**Summary**: Reis & Housley's named antipattern from Chapter 10: doing security "in the letter of compliance (SOC-2, ISO 27001, and related) without real commitment." The letter of the law is satisfied — audits pass, boxes are ticked — but a few minutes of reflection reveals gaping holes. The antidote is **security habit**: simple practices ingrained into the team's culture until security becomes automatic.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## The symptoms

Chapter 10's tell-tale markers of security theater (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

- **Policies in the hundreds of pages that nobody reads.** Volume as a proxy for thoroughness; dense documents that are impossible to follow in practice.
- **Annual security policy review that people immediately forget.** Training treated as a compliance ritual rather than a cultural investment.
- **Box-ticking for audits** (SOC-2, ISO 27001). The goal becomes passing the audit rather than being secure.
- **Compliance-focused thinking that doesn't consider bad scenarios.** Internal rules, laws, and standards-body recommendations are followed literally, but nobody asks "how could this actually go wrong?"

The chapter's blunt framing: "This creates an illusion of security but often leaves gaping holes that would be evident with a few minutes of reflection."

## Why it happens

Security theater emerges because compliance is **measurable and attributable** — an auditor signs off, a certificate is produced, a checklist is completed. Real security is harder to measure; absence of breaches today doesn't prove the absence of vulnerabilities. Organisations under pressure to demonstrate security gravitate toward the measurable thing regardless of whether it correlates with actual safety.

## The opposite: security habit

Chapter 10 prescribes "the spirit of genuine and habitual security" — baking a security mindset into the culture (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

- **Keep it simple.** Security doesn't need to be complicated. The authors describe running monthly security training and policy reviews at their company — not the 200-page binder, but a short set of practical actions people can take immediately. See [[security-policy]] for their example.
- **Make it a priority, not an afterthought.** "Security must not be an afterthought for your data team. Everyone is responsible and has a role to play."
- **Pair with [[active-security]].** Security theater is passive — it reacts to standards. Active security is forward-looking — it asks "what could actually go wrong here?"

## The connection to people

See [[data-security]]. Security theater fails because the weakest link in every system is the human, and an unread 200-page policy cannot change human behaviour. A short, habitually-rehearsed list of practices can. The chapter's recipe for the cultural shift: small practices, frequent repetition, and leadership modelling the behaviour.

## Related pages

- [[data-security]]
- [[active-security]]
- [[security-policy]]
- [[least-privilege]]
- [[shared-responsibility-model]]
- [[fundamentals-of-data-engineering]]
