# Safety Integrity Level (SIL)

**Summary**: Chapter 33's named regulatory-engineering vocabulary from nuclear power, military aircraft, and railway signaling — a four-level discrete scale (SIL 1-4) that classifies safety-related software systems by the reliability they must achieve. Standards Chapter 33 names: UK Defence Standard 00-56, IEC 61508, IEC513, US DO-178B/C, DO-254. Together they specify acceptable approaches to delivering a product where failure has safety consequences.

**Sources**: `raw/site-reliability-engineering/chapter-33-lessons-learned-from-other-industries.md`

**Last updated**: 2026-04-17

---

## What SIL is

Chapter 33 names SIL specifically as the way safety-critical software industries make reliability targets externally checkable (source: chapter-33-lessons-learned-from-other-industries.md):

> Safety standards for software are well detailed (e.g., UK Defence Standard 00-56, IEC 61508, IEC513, US DO-178B/C, and DO-254) and levels of reliability for such systems are clearly identified (e.g., Safety Integrity Level (SIL) 1-4), with the aim of specifying acceptable approaches to delivering a product.

The four-level scale is a discretised reliability classification: SIL 1 is the lowest safety integrity, SIL 4 the highest. Each level is associated with permitted *probability of dangerous failure per hour* — an external regulator can say *this system must be SIL 3* and the implementation has to demonstrably achieve the corresponding failure-rate ceiling.

The chapter doesn't expand the scale numerically. The page footnote points to the Wikipedia article on Safety Integrity Level for the detail.

## How this contrasts with SRE's SLO

The SLO/SLI/SLA vocabulary covered at [[service-level-objective]] occupies the same conceptual slot as SIL — *what reliability are we committing to* — but with a few structural differences:

- **Continuous vs discrete.** SLOs are arbitrary fractions (99.9%, 99.95%, 99.99%); SIL is four levels. SIL discreteness exists because external regulatory verification needs a small set of named buckets to certify against.
- **Self-set vs externally imposed.** SLOs are picked by the product owner based on user expectations and business needs (see [[service-level-objective]]); SIL is set by the regulator based on the consequence of failure.
- **Per-service vs per-component.** SLOs are mostly defined at the service boundary visible to users; SIL is applied at the component level to elements whose failure could lead to hazard.
- **Renegotiable vs fixed.** SLOs adjust as the product evolves; SIL doesn't move because the consequence of failure doesn't move.

Both are mechanisms for *making reliability quantifiable enough to engineer to* — they are the same intellectual move, picked from opposite ends of the regulatory-vs-self-determined axis.

## Why this matters for SRE

Chapter 33's catalogue of safety standards is a reminder that *what reliability target are we engineering to* is not a question Google invented. The decades-older regulatory framework treats it as a precondition for the design conversation. SRE's contribution is mostly about how to **measure and operate** reliability, not about how to **set the target** — for the latter, the regulated industries have a longer track record.

The practical takeaway: when an SRE team is engaging with a safety-critical domain (medical, automotive, financial) the SLO conversation has to coexist with the regulatory-SIL conversation. The two answer overlapping questions in different vocabularies; the engineering work is to make the SLO compatible with the SIL rather than to substitute one for the other.

## Cross-book connections

- [[service-level-objective]] (SRE Ch 1, 4) — the SRE-side reliability-target vocabulary; SIL occupies the same conceptual slot from the regulator side
- [[risk-management-sre]] (SRE Ch 3) — Chapter 3's framing of risk as a continuum is what produces the SLO; SIL is the discretised version of the same continuum
- [[architecture-decisions-vs-design-principles]] (Richards & Ford) — SIL operates as an externally imposed architecture decision; SRE's equivalent is the SLO ADR
- [[lessons-from-other-industries]] / [[preparedness-and-disaster-testing]] — Chapter 33's umbrella

## Related pages

- [[lessons-from-other-industries]]
- [[preparedness-and-disaster-testing]]
- [[organizational-safety-culture]]
- [[service-level-objective]]
- [[risk-management-sre]]
