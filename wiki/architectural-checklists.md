# Architectural Checklists

**Summary**: Richards & Ford's treatment of checklists as a team-effectiveness tool, drawing on Atul Gawande's *The Checklist Manifesto*. Checklists work — but only for the right kind of process: infrequent, non-procedural tasks where errors of omission dominate. Three canonical checklists (code completion, unit/functional testing, software release) are the ones the authors have found worth maintaining.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-22-making-teams-effective.md`, `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## Why checklists work

Airline pilots use checklists on every flight — even seasoned veterans. One missed setting (flaps at 10 degrees, clearance into a terminal control area) can be the difference between a safe flight and a disaster (source: chapter-22-making-teams-effective.md). Atul Gawande's *The Checklist Manifesto* demonstrated the same effect for surgery: hospitals using surgical checklists drove staph-infection rates to near zero, while control hospitals' rates continued to rise.

Checklists work because high-repetition expert work makes details easy to miss. A succinct checklist is a reminder that doesn't depend on vigilance. See [[architecture-fitness-function]] and [[architecture-governance]] for the same framing applied to automated governance — the Checklist Manifesto is already the governing analogy there, and this page extends it from *automated* checks to *manual* ones that resist automation.

## When to use a checklist — and when not to

Software developers don't need a checklist for everything — and an architect who makes everything a checklist invokes the **law of diminishing returns**. The more checklists an architect creates, the less chance developers will use them (source: chapter-22-making-teams-effective.md).

| Good checklist candidate | Bad checklist candidate |
|---|---|
| No procedural order among tasks | Procedural flow with dependent steps |
| Error-prone; frequently missed or skipped | Simple, well-known, frequent, error-free |
| Infrequently executed | High-frequency routine |

The chapter's explicit anti-example (Figure 22-11): a "checklist" for creating a new database table that lists *submit form* → *verify table* → *confirm columns* in dependent order. That's a procedure, not a checklist — the verification can't happen before the submission. Procedural flows belong in documentation or automation, not checklists.

### Keep them small

Developers won't follow checklists that are too big. Pull out anything that can be automated (unit tests, static analysis, code crawlers) and delete it from the list. But **don't worry about stating the obvious** — obvious steps are the ones that actually get skipped. Gawande found the same pattern in surgical checklists: it's the routine items, not the exotic ones, that get missed when someone is in a hurry.

## The three canonical checklists

### Developer code-completion checklist

Used when a developer says they're "done" — also useful as the team's **definition of done** (source: chapter-22-making-teams-effective.md). Good contents:

- Coding and formatting standards not included in automated tools
- Frequently overlooked items (such as absorbed exceptions — `catch (Exception e) { /* ... */ }`)
- Project-specific standards
- Special team instructions or procedures

Example items from the chapter's Figure 22-12 include "Run code cleanup and formatting", "Make sure there are no absorbed exceptions", and project-specific items like "Include `@ServiceEntrypoint` on service API class" and "Verify that only public methods are calling `setFailure()`". The latter is a good candidate for automation (a straightforward code-crawling rule) and should be removed from the checklist once automated.

### Unit and functional testing checklist

The largest of the three, because there are so many kinds of tests. Purpose: ensure the most complete testing possible so that when the developer is done with the checklist, the code is essentially production-ready (source: chapter-22-making-teams-effective.md). Typical contents:

- Special characters in text and numeric fields
- Minimum and maximum value ranges
- Unusual and extreme test cases
- Missing fields

Whenever QA finds a bug tied to a test case, the case goes on the checklist. Again: anything automatable (a unit test for negative-share stock trades) should become an automated test and leave the checklist.

This checklist is also the bridge between developers and dedicated testers — the more developers cover via the list, the more testers can focus on harder business scenarios not in the list.

### Software release checklist

Releasing to production is one of the most error-prone parts of the SDLC, which makes it the best checklist candidate of all (source: chapter-22-making-teams-effective.md). This checklist is the most **volatile** of the three — it continuously grows as new deployment failures surface. Typical contents:

- Configuration changes on servers or in external configuration servers
- Third-party libraries added to the project (JAR, DLL, etc.)
- Database updates and corresponding migration scripts

The discipline: **every time a build or deployment fails, the architect analyses the root cause and adds a corresponding entry**. The item gets checked on the next release, and that failure mode doesn't recur.

## Getting developers to actually use them

The core risk: a developer in a hurry simply marks all items as completed without performing them. Richards and Ford's escalating tactics (source: chapter-22-making-teams-effective.md):

1. **Talk about the importance.** Have team members read *The Checklist Manifesto*. Make sure each person understands the reasoning behind each checklist.
2. **Collaborate on contents.** Developers who helped decide what goes on the checklist are more likely to follow it.
3. **When all else fails, invoke the Hawthorne effect.**

### The Hawthorne effect

When people know they are being observed or monitored, their behaviour changes — they tend to do the right thing. The chapter's everyday examples: highly visible security cameras that don't actually record, website-monitoring reports that nobody reads.

Applied to checklists: tell the team that every checklist will be verified, then **spot-check occasionally**. Developers behave as if every item is being checked, and the omission rate drops sharply. The deception is mild and the payoff is real — but the first two tactics (buy-in via the book; collaboration on contents) should be tried before this one.

## The SRE launch-checklist counterpart

Google SRE's [[launch-checklist|launch checklist]] is a sustained-scale instance of the same pattern (source: chapter-27-reliable-product-launches-at-scale.md). A [[launch-coordination-engineering|dedicated LCE team]] curates the checklist across hundreds of launches per year. Three specific disciplines from that experience align with Richards & Ford's framing and sharpen it:

- **Every question must be substantiated — ideally by a previous launch disaster.** Items earn a place by having already caused a problem that is worth preventing next time. This is the operational form of "the case backlog grows the checklist" that Richards & Ford describe for the release checklist.
- **Every instruction must be concrete, practical, and reasonable for developers to accomplish.** The question/action-item/pointer-to-infrastructure shape gives developers an explicit next step.
- **Continuous curation with a full review 1-2 times per year.** Items deprecate as systems are replaced and new policies land; an uncurated checklist drifts into irrelevance and then into disuse.

Chapter 27 also names the **law of diminishing returns** that Richards & Ford warn about, from the same operational angle: at one point, adding a new question to the checklist required VP approval. The shared rule: developers sidestep processes they view as too burdensome, especially under deadline pressure. LCE's answer is aggressive use of **fast common paths** (low-risk launches get a nearly trivial checklist) and **convergence on shared infrastructure** (one line "use X for rate limiting" replaces pages of rate-limiting requirements) to keep the cost per item low.

## Relationship to fitness functions

Checklists and [[architecture-fitness-function|fitness functions]] are complementary tools for the same underlying problem: ensuring expert work doesn't drop important details. The split is automation:

- **Fitness functions** automate the checks. Code-crawlers, ArchUnit tests, cyclomatic-complexity thresholds, smoke tests, chaos experiments — all of these live in CI and fail loudly without developer attention.
- **Architectural checklists** cover what fitness functions can't automate — subjective steps, judgement calls, process items tied to deployment or release choreography.

The discipline is to continuously move items *from* the checklist *to* the fitness-function suite as automation becomes feasible. See [[architecture-fitness-function]] and [[architecture-governance]] for the other side of this.

## Related pages

- [[architect-control-spectrum]]
- [[architect-providing-guidance]]
- [[architecture-fitness-function]]
- [[architecture-governance]]
- [[architecture-decisions-vs-design-principles]]
- [[fundamentals-of-software-architecture]]
- [[launch-checklist]]
- [[launch-coordination-engineering]]
- [[reliable-product-launches]]
