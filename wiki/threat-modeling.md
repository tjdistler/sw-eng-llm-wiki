# Threat Modeling

**Summary**: The practice of systematically thinking through who would attack a system, how, and what the consequences would be — before designing defences. In Chapter 10, Reis & Housley don't name it explicitly as "threat modeling" but treat it as the mental habit underneath [[active-security]] and the **power of negative thinking**: enumerate bad scenarios, then design to prevent them.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## The Reis & Housley framing

Chapter 10 argues for threat modeling as the antidote to compliance-driven security (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Data engineers should actively think through the scenarios for data utilization and collect sensitive data only if there is an actual need downstream. The best way to protect private and sensitive data is to avoid ingesting this data in the first place. Data engineers should think about the attack and leak scenarios with any data pipeline or storage system they utilize.

Three habits fall out of this:

- **Minimise data.** The attack that never happens is the one against data you never collected. If a pipeline doesn't need PII to do its job, don't ingest PII.
- **Enumerate attack scenarios** per pipeline and per storage system. What are the plausible ways this specific system is breached?
- **Ask whether defences deliver security or only the illusion of it.** Don't settle for the feeling that "we have encryption"; ask "what attack does that stop, and what attacks remain open?"

## The power of negative thinking

Chapter 10 cites Atul Gawande's 2007 op-ed on negative thinking (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Positive thinking can blind us to the possibility of terrorist attacks or medical emergencies and deter preparation. Negative thinking allows us to consider disastrous scenarios and act to prevent them.

The threat-modeling stance is to deliberately invert the "what's the happy path?" design lens. For each system: what's the worst-case path? Who benefits from it? What's the first sign it's happening?

## Connection to [[active-security]]

Threat modeling is the *process* that makes active security *real*. Without it, "think about security" is a slogan. With it, teams have a concrete artefact — a list of plausible attacks and the mitigations already in place (or missing) — that they review and update.

A common pairing in practice:

- **Every major system** gets a threat model during design.
- **Reviews** happen when the threat landscape changes (new attack classes in the news, new employee incentives, new integrations with third parties).
- **Findings** become tickets: either a new mitigation, an accepted risk with sign-off, or a decision to not build the feature.

## Formal frameworks

Chapter 10 doesn't prescribe a framework, but threat modeling has a long tradition in security engineering:

- **STRIDE** (Microsoft) — categorise threats by Spoofing / Tampering / Repudiation / Information disclosure / Denial of service / Elevation of privilege.
- **PASTA** — Process for Attack Simulation and Threat Analysis; seven-stage risk-centric method.
- **Attack trees** — root goal decomposed into attacker sub-goals and plausible techniques.
- **Data-flow-diagram analysis** — trust boundaries between components, identifying where authentication and validation must happen.

The frameworks differ in rigor and audience; all share the core move Chapter 10 names: **enumerate the ways it could go wrong, then decide what to do about each.**

## Threat-model outputs feed other undercurrents

A good threat-model review produces work for multiple practices:

- **[[least-privilege]]** — "this role has more than it needs because..."
- **[[encryption-at-rest]] / [[encryption-in-transit]]** — "this field has to be encrypted because..."
- **[[network-access-security]]** — "this port needs to close / this IP allowlist needs narrowing..."
- **[[security-monitoring]]** — "this anomaly is worth alerting on..."
- **[[secrets-management]]** — "this credential needs rotation / narrowing of scope..."

## Related pages

- [[data-security]]
- [[active-security]]
- [[security-theater]]
- [[zero-trust-security]]
- [[data-ethics]]
- [[fundamentals-of-data-engineering]]
