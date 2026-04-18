# SRE Team Composition

**Summary**: Chapter 31's framing of the formal roles inside an SRE team — tech lead (TL), SRE manager (SRM), and project manager (TPM/PM/PgM) — together with the rigid-vs-fluid responsibility spectrum and the diversity-as-collaboration-multiplier argument. The rigid end makes decisions fast and safe but narrow; the fluid end adapts but requires more communication. Great TLs, SRMs, and TPMs can flex across all three roles.

**Sources**: `raw/site-reliability-engineering/chapter-31-communication-and-collaboration-in-sre.md`

**Last updated**: 2026-04-17

---

## The three formal roles

Chapter 31 names three roles every SRE team has (source: chapter-31-communication-and-collaboration-in-sre.md):

- **Tech Lead (TL)** — responsible for technical direction in the team. Leads in a variety of ways: commenting carefully on code, holding quarterly direction presentations, building consensus. At Google, TLs can do almost all of a manager's job because managers are themselves highly technical.
- **SRE Manager (SRM)** — the manager. Two responsibilities a TL doesn't have: the **performance-management function** (the employment-relationship side of managing people) and a general **catchall for everything no one else handles**.
- **Project Manager (TPM / PM / PgM)** — the organisational catalyst for project work: planning, tracking, coordinating dependencies.

Great TLs, SRMs, and TPMs *"have a complete set of skills and can cheerfully turn their hand to organizing a project, commenting on a design doc, or writing code as necessary"* (source: chapter-31-communication-and-collaboration-in-sre.md). Role labels are useful boundaries, not walls.

## Rigid vs fluid responsibility

Chapter 31 names an explicit spectrum (source: chapter-31-communication-and-collaboration-in-sre.md):

### Rigid end

Well-defined responsibilities per role.

- **Benefit**: people can make in-scope decisions *quickly and safely*. Knowing which decisions are yours and which aren't is itself a force multiplier — no negotiation overhead per decision.
- **Who it suits**: people who operate best with crisp boundaries.

### Fluid end

Shifting responsibilities through dynamic negotiation.

- **Benefit**: adaptability. The team handles new situations better; individuals develop across a wider surface.
- **Cost**: more communication, more often, because less shared background can be assumed. Less can be done implicitly; more has to be said out loud.

### The chapter's observation

*"The more fluid the team is, the more developed it is in terms of the capabilities of the individuals, and the more able the team is to adapt to new situations — but at the cost of having to communicate more and more often"* (source: chapter-31-communication-and-collaboration-in-sre.md). Teams tend to slide toward fluid as they mature and toward rigid when under pressure; neither endpoint is universally correct.

## Diversity as collaboration multiplier

The chapter is blunt: *"your chances of successful collaboration — and indeed just about anything else — are improved by having more diversity in your team"* and cites supporting evidence (Nel14). Running a diverse team demands particular attention to **communication**, **cognitive biases**, and related dynamics, which the chapter doesn't cover in detail but flags as non-optional (source: chapter-31-communication-and-collaboration-in-sre.md).

The SRE-specific form: SRE teams already mix systems engineering, software engineering, project management, leadership instincts, and backgrounds from many industries (source: chapter-31-communication-and-collaboration-in-sre.md). Treating that mix as an asset — actively balancing it rather than homogenising — is how the collaboration premium gets collected.

## Skill-set diversity and where it comes from

Chapter 31 catalogues the kinds of skills an SRE team draws on:

- **Systems engineering** and **architectural skills** (see [[sre-discipline]])
- **Software engineering skills** — the premise behind [[software-engineering-in-sre|running full SE projects inside SRE]]
- **Project management skills**
- **Leadership instincts**
- **Backgrounds in varied industries**

The team's external interface (its "API" in the chapter's metaphor) aggregates this skill mix. Collaboration outside SRE works because SRE combines software engineering skill with production-operational wisdom in a way neither pure developers nor pure ops can match (source: chapter-31-communication-and-collaboration-in-sre.md).

## Why this matters for collaboration

The chapter embeds team composition inside a larger argument about what makes SRE-produced designs better:

> The best designs and the best implementations result from the joint concerns of production and the product being met in an atmosphere of mutual respect. This is the promise of SRE: an organization charged with reliability, *with the same skills as the product development teams*, will improve things measurably. Our experience suggests that simply having someone in charge of reliability, without also having the complete skill set, is not enough. (source: chapter-31-communication-and-collaboration-in-sre.md)

The composition argument is why SRE's collaboration with product development works — SRE brings engineering peer status to the table, not just operational concerns.

## Related pages

- [[communication-and-collaboration-in-sre]]
- [[cross-sre-collaboration]]
- [[sre-discipline]]
- [[software-engineering-in-sre]]
- [[sre-dev-collaboration]]
- [[architect-leadership-skills]]
- [[architect-control-spectrum]]
- [[team-autonomy]]
