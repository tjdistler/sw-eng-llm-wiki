# Negative Lines of Code

**Summary**: Chapter 9 of *Site Reliability Engineering*'s framing that **every line of code in a 24/7 service is a liability**, and that deleting code is often the highest-value change an engineer can make. "Software bloat" — the tendency of software to grow slower and bigger through accumulated features — is measurable as defect surface area; shrinking the project is shrinking the defect surface. The chapter also catalogues the common objections to deleting code and answers each.

**Sources**: `raw/site-reliability-engineering/chapter-09-simplicity.md`

**Last updated**: 2026-04-17

---

## The core claim

Chapter 9 puts it bluntly (source: chapter-09-simplicity.md):

> At the risk of sounding extreme, when you consider a web service that's expected to be available 24/7, to some extent, every new line of code written is a liability.

The SRE value of a project is not proportional to its line count. It is closer to the inverse: a smaller project is easier to understand, easier to test, and frequently has fewer defects.

From this, the chapter draws three specific SRE practices:

1. **Scrutinise new code** to make sure it actually drives business goals.
2. **Routinely remove dead code.**
3. **Build bloat detection into all levels of testing** — treat bloat as a defect class on par with correctness bugs.

## Software bloat

Chapter 9 notes that the term "software bloat" was coined to describe the tendency of software to grow slower and larger over time as features accumulate. The SRE-specific reframing is that bloat is bad not because users complain about it (they often don't) but because **every line of code changed or added creates the potential for a new defect** (source: chapter-09-simplicity.md).

This makes the arithmetic uncomfortable: adding features is the core activity of product development, but the aggregate effect on reliability of unexamined feature accumulation is negative. The countermeasure is selective addition combined with active removal.

## The satisfying-to-delete observation

Luebbe's aside (source: chapter-09-simplicity.md):

> Some of the most satisfying coding I've ever done was deleting thousands of lines of code at a time when it was no longer useful.

This is the origin of the "negative lines of code" metric as a cultural signal: a team that celebrates deletions has internalised the liability framing. A team that treats line count as a productivity measure has inverted the incentive.

## Objections to deletion, and their answers

Chapter 9 anticipates the emotional response (source: chapter-09-simplicity.md):

> Because engineers are human beings who often form an emotional attachment to their creations, confrontations over large-scale purges of the source tree are not uncommon.

The three common objections and the chapter's answers:

### "What if we need that code later?"

Source control already solves this. Git, Perforce, or any other versioning system keeps the history indefinitely. "Need it later" is an argument for preserving history, not for keeping dead code in the current tree.

### "Why don't we just comment the code out?"

Commented-out code creates distractions and confusion — especially as the surrounding file evolves. Other engineers have to decide, for every commented-out block they encounter, whether it is (a) a reference comment they should read, (b) broken code someone will restore, or (c) abandoned code they can delete. That cognitive overhead is paid on every future read.

### "Why don't we gate the code with a flag?"

Code gated by a flag that is always disabled is a **time bomb**. It is untested in production, unnoticed in refactoring, and re-activatable by mistake.

The chapter's canonical cautionary tale: the 2012 Knight Capital incident (SEC 2013, *Order In the Matter of Knight Capital Americas LLC*). A permanent-never-used code path was re-activated when a new deployment reused an old feature flag name. The code behaved the way the eight-year-old version had behaved, placing orders the current system could not cancel. The loss was approximately $440 million in 45 minutes, and Knight Capital effectively ceased to exist as an independent firm.

The lesson is not that feature flags are bad. It is that **flags that are never toggled are dead code with extra setup**, and dead code should be deleted, not disguised.

## Relationship to the positive metric

"Negative lines of code" is sometimes used as a half-serious performance metric at Google: an engineer who removes 1,000 lines while preserving functionality has done more for reliability than one who added 10,000 lines of new features. The metric is obviously imperfect (deletion can also introduce bugs; not all code is equal in liability), but the *sign* is the point: deletion is production, not destruction.

## Cross-book connections

- [[accidental-complexity]] (Richards & Ford / Brooks) — dead code is accumulated accidental complexity; negative-lines-of-code is the operational remedy
- [[virtue-of-boring]] — the chapter's companion section: less code, more predictable behaviour
- [[minimal-apis]] — the same "take away, don't just add" principle applied to the API surface
- [[change-management-sre]] — 70% of outages come from changes, but dead code is a *latent* change (like Knight Capital's flag) waiting for a trigger
- [[toil-and-engineering-balance]] — every line of code carries a small amount of maintenance toil; cumulative bloat degrades the engineering/toil ratio
- [[monitoring-simplicity]] (Ch 6) — the Ch 6 pruning rules ("rules never exercised are candidates for removal", "metrics never viewed are candidates for removal") are the monitoring-specific version of this discipline

## Related pages

- [[simplicity-sre]]
- [[virtue-of-boring]]
- [[minimal-apis]]
- [[accidental-complexity]]
- [[monitoring-simplicity]]
- [[change-management-sre]]
- [[site-reliability-engineering]]
