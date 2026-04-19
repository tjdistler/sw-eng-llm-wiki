# Google Cloud's Five Cloud-Native Principles

**Summary**: Google Cloud's compact five-principle architecture framework. Reis and Housley cite it alongside AWS's [[well-architected-framework]] as one of the two primary inspirations for their [[principles-of-good-data-architecture|nine principles of good data architecture]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`

**Last updated**: 2026-04-18

---

## The five principles

Chapter 3 enumerates them (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

1. **Design for automation** — automate everything the system can reasonably automate
2. **Be smart with state** — know where state lives, minimise it where it is not needed
3. **Favor managed services** — use cloud-provided managed services rather than building and operating your own
4. **Practice defense in depth** — multiple layers of security, not one hard perimeter
5. **Always be architecting** — architecture is never finished

## Why it matters

Reis and Housley recommend studying this framework in full alongside AWS's [[well-architected-framework]] (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

The most visible direct borrowing is **Principle 5: Always be architecting** — Reis and Housley lift the name verbatim as [[principles-of-good-data-architecture|their own Principle 5]], naming Google Cloud as the source.

Principle 4 (defense in depth) is the conceptual parent of their security principle and [[zero-trust-security]]'s rejection of the hardened perimeter.

## Related pages

- [[principles-of-good-data-architecture]]
- [[well-architected-framework]]
- [[data-architecture]]
- [[zero-trust-security]]
- [[data-security]]
- [[evolutionary-architecture]]
