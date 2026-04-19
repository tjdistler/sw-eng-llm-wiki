# Interoperability

**Summary**: How easily one technology or system connects, exchanges information, and interacts with another. Reis and Housley's third [[technology-selection|selection criterion]] — a spectrum ranging from seamless native integration to time-intensive custom glue. The discipline that makes [[reversible-vs-irreversible-decisions|reversible decisions]] practical.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Definition

Chapter 4 defines interoperability as **how various technologies or systems connect, exchange information, and interact** (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md). When evaluating two technologies A and B:

- Is seamless integration already baked in (zero-configuration connectors), or do you need extensive manual configuration?
- Does the tool target the platforms you already use (data warehouses, lakes, CRMs, accounting software)?

## Standards-based vs vendor-specific

Chapter 4 draws an explicit distinction (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Standards that work.** Almost all databases allow connections via **JDBC** (Java Database Connectivity) or **ODBC** (Open Database Connectivity). You can reliably connect to a database by using these standards.
- **Pseudo-standards that don't.** REST "is not truly a standard for APIs; every REST API has its quirks." When no real standard exists, the integration burden falls on the vendor or OSS project.

Always be aware how simple or painful it will be to connect the various technologies in your data stack.

## Why interoperability is architectural

Interoperability is the discipline that makes several Chapter 4 positions practical:

- **[[monolith-vs-modular-data|Modularity]]** — a modular stack only works if each component can actually be swapped. Interoperability is what "swappable" means concretely.
- **[[reversible-vs-irreversible-decisions|Reversible decisions]]** — Reis and Housley advise "designing for modularity and giving yourself the ability to easily swap out technologies as new practices and alternatives become available." That ability *is* interoperability.
- **Open-standard storage formats.** Parquet in a data lake is interoperable by construction — any tool that supports the format can read the data, transform it, and write it back. This is why [[data-lakehouse|lakehouse]] storage formats (Parquet, Iceberg, Delta) are central to the modular-stack story.

## The hidden cost: when interoperability breaks

Chapter 4 warns that inflexible technologies are "bear traps" — easy to get into, extremely painful to escape. Poor interoperability makes the [[total-opportunity-cost-of-ownership|TOCO]] of a tool substantially higher than its list price. Always test interoperability **before** committing.

## Cross-book framing

- [[data-integration]] is the operational name for the same problem at pipeline scope.
- [[data-liberation]] (Bellemare) is the event-driven route to interoperability — emit events everyone can consume rather than building N point-to-point integrations.
- [[loose-coupling]] is the architectural property that makes interoperable systems possible in the first place.

## Related pages

- [[technology-selection]]
- [[modern-data-stack]]
- [[monolith-vs-modular-data]]
- [[reversible-vs-irreversible-decisions]]
- [[loose-coupling]]
- [[data-integration]]
- [[data-liberation]]
- [[principles-of-good-data-architecture]]
