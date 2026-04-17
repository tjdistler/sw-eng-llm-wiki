# Architect Career Path

**Summary**: Chapter 24's practical advice on how an architect sustains a career after reaching the role — the **20-minute rule** for daily learning, the **personal developer radar** adapted from ThoughtWorks, using social media to seed the radar, and architecture katas as deliberate practice. The chapter's through-line is the operational form of [[architect-expectations|Expectation #3]] ("keep current"): without a deliberate, calendared discipline for learning, [[technical-breadth-vs-depth|technical breadth]] silently atrophies and the architect becomes the "stale expertise" failure mode Chapter 2 warned about.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-24-developing-a-career-path.md`

**Last updated**: 2026-04-16

---

## Why this chapter exists

Becoming an architect takes years; *managing a career* as an architect is a separate, equally tricky problem (source: chapter-24-developing-a-career-path.md). The book opens the chapter with Neal Ford's colleague, a world-renowned Clipper expert — a rapid-application-development tool for DOS-on-dBASE applications — who watched the entire body of his expertise evaporate when Windows arrived. Ford's open question: "has any group in history learned and thrown away so much detailed knowledge within their lifetimes as software developers?" (source: chapter-24-developing-a-career-path.md).

The prescription is not "read more blogs." It is a calendared discipline with three components: a daily learning slot (the 20-minute rule), a structured filter for what to spend that slot on (the personal developer radar), and a practice loop for the architecture skill itself (katas and related exercises). The chapter deliberately does not list resources — "resources come and go all too quickly" (source: chapter-24-developing-a-career-path.md). Talking to colleagues and trusted experts about what *they* read is the recommended way to find the current set.

## The 20-minute rule

Technology breadth matters more to architects than depth (source: chapter-24-developing-a-career-path.md) — the [[technical-breadth-vs-depth|knowledge-pyramid]] argument from Chapter 2. But maintaining breadth takes time, and the competing demands on an architect's calendar (day job, family, hobbies, career development, trend-tracking) make "read more" a losing strategy without structure.

The rule: **spend at least 20 minutes a day on your architect career** by learning something new or going deeper into a specific topic (source: chapter-24-developing-a-career-path.md). Two modes map to the three layers of the [[technical-breadth-vs-depth|knowledge pyramid]]:

- **Breadth mode** — Google an unfamiliar buzzword to convert a "thing you don't know you don't know" into a "thing you know you don't know" (source: chapter-24-developing-a-career-path.md). This is the pyramid's middle layer growing at the expense of the unknown bottom.
- **Depth mode** — go deeper on a topic you already partially know. Useful, but the chapter is explicit that breadth is the primary target.

### Timing: first thing in the morning, before email

Many architects plan to do their 20 minutes at lunch or after work. The chapter is blunt that this "rarely works" (source: chapter-24-developing-a-career-path.md):

> Lunchtime gets shorter and shorter, becoming more of a catch-up time at work rather than a time to take a break and eat. Evenings are even worse — situations change, plans get made, family time becomes more important, and the 20-minute rule never happens.

The strong recommendation is **first thing in the morning, after getting coffee/tea, before checking email** (source: chapter-24-developing-a-career-path.md). Email is the diversion the chapter names explicitly: once it's open, responses get written, and the day is over. Go in a little early. Getting 20 minutes in before the rest of the day lands is the only reliable schedule.

### Relationship to other architect-time techniques

This is the same problem that [[balancing-architecture-and-coding]] solves for technical depth: the architect's calendar is under continuous pressure, and the only way to preserve something that isn't urgent this week is to bake it into the schedule. The 20-minute rule is the breadth-side counterpart to Chapter 2's "code one-to-three iterations out" prescription for staying hands-on.

## Personal developer radar

The chapter's origin story for the radar is another cautionary tale. Neal Ford was CTO of a training-and-consulting company whose primary platform was Clipper. "Until one day it vanished" (source: chapter-24-developing-a-career-path.md). The business market was DOS until it abruptly wasn't. The lesson is the **technology bubble** problem: architects heavily invested in a technology live inside a memetic echo chamber and don't notice the bubble collapsing until it is too late.

A **technology radar** is the defence: a living document that assesses the risks and rewards of existing and nascent technologies (source: chapter-24-developing-a-career-path.md).

### The ThoughtWorks origin

The radar concept comes from ThoughtWorks's **Technology Advisory Board** (TAB) — a group of senior technology leaders chaired by CTO Dr. Rebecca Parsons that meets twice a year to steer the company's and clients' technology direction. One meeting's output was the **Technology Radar**, which settled into a biannual cadence (source: chapter-24-developing-a-career-path.md). The side effect Ford noticed: companies started producing their own internal radars, and "how do you keep up with technology?" — the pervasive speaker-panel question at conferences — was really asking whether the panelists had some form of internal radar. They all did.

### Quadrants and rings

The radar has two axes — **four quadrants** for what's on the radar and **four rings** for how seriously to take it (source: chapter-24-developing-a-career-path.md).

**Quadrants** (what kind of thing):

| Quadrant | Contents |
|---|---|
| **Tools** | Everything from IDEs to enterprise integration tools |
| **Languages and frameworks** | Computer languages, libraries, frameworks; typically open source |
| **Techniques** | Any practice that assists software development: processes, engineering practices, advice |
| **Platforms** | Databases, cloud vendors, operating systems |

**Rings** (from outer to inner — how close to adoption):

| Ring | Original ThoughtWorks meaning |
|---|---|
| **Hold** | "Don't start anything new with this." No harm using it on existing projects; think twice for new development. (Originally "too new to assess"; the meaning evolved.) |
| **Assess** | Worth exploring to understand its impact — spikes, research projects, conference sessions. The mobile-strategy example from the large-company cohort. |
| **Trial** | Worth piloting on a low-risk project to really understand it. |
| **Adopt** | Industry should adopt this. |

### Adapting the radar for personal use

The chapter's most actionable teaching point is the personal adaptation — the same four-ring structure, but with slightly shifted semantics for an individual architect (source: chapter-24-developing-a-career-path.md):

| Ring | Personal meaning |
|---|---|
| **Hold** | Technologies and techniques to avoid **and habits to break**. Example: a .NET architect who compulsively reads low-value team-internals gossip on forums puts that in Hold as a self-reminder. |
| **Assess** | Promising technologies you've heard good things about but haven't had time to assess. A staging area for serious research later. |
| **Trial** | Active research and development — running spike experiments in a larger codebase to do a proper [[trade-off-analysis]]. |
| **Adopt** | The new things you're most excited about, and best practices for particular problems. |

The critical framing: treat a technology portfolio like a **financial portfolio** (source: chapter-24-developing-a-career-path.md). A financial planner's first advice is *diversify* — pick some technologies/skills that are in broad demand and track that demand, and also take some gambits (open source, mobile, etc.). The anecdotes about developers freeing themselves from cubicle servitude by contributing to an open-source project that became a career destination are the gambit pay-off.

The chapter is also explicit that **the exercise is more important than the outcome** (source: chapter-24-developing-a-career-path.md). Drawing the radar forces the conversation; the drawing itself is secondary.

### Tooling

In November 2016, ThoughtWorks open-sourced a tool for building your own radar visualisation. It takes a Google spreadsheet (one sheet per quadrant) as input and renders the radar on an HTML 5 canvas (source: chapter-24-developing-a-career-path.md). The chapter re-emphasises: the conversations that the exercise generates are the real product; the visualisation is a useful by-product.

## Using social media

Where does the **Assess** ring get populated from? The chapter leans on Andrew McAfee's *Enterprise 2.0* for the social-network argument (source: chapter-24-developing-a-career-path.md). McAfee identifies three categories of personal connections:

- **Strong links** — family, coworkers, regular contacts. The litmus test: you know what they had for lunch last week.
- **Weak links** — casual acquaintances, distant relatives, people seen a few times a year. Hard to maintain before social media; much easier now.
- **Potential links** — people you haven't met yet.

McAfee's observation: **someone's next job is more likely to come from a weak link than a strong one** (source: chapter-24-developing-a-career-path.md). Strong links all know the same things — they see each other constantly. Weak links offer advice from outside the echo chamber.

Applied to architect development: use social media professionally to follow technologists whose advice you respect. That's the input stream that feeds the **Assess** ring and keeps the radar from recycling the same ideas everyone in your strong-link circle already shares. This is the specific defence against the technology-bubble failure that opened the chapter.

## Practising architecture

The chapter closes with Fred Brooks's line and Ted Neward's counter (source: chapter-24-developing-a-career-path.md):

> How do we get great designers? Great designers design, of course. — *Fred Brooks*
>
> So how are we supposed to get great architects, if they only get the chance to architect fewer than a half-dozen times in their career? — *Ted Neward*

The answer is **deliberate practice**. The chapter points at [[architecture-katas]] — Neward's 45-minute team exercise, first introduced in Chapter 5 as the drill for [[identifying-architecture-characteristics|identifying characteristics]], and now re-framed in Chapter 24 as the ongoing practice loop for the architecture skill itself. The chapter fields the common question — "is there an answer guide?" — with Neal Ford's answer:

> There are no right or wrong answers in architecture — only trade-offs.

The authors started saving student designs from live trainings, intending to build an answer repository; they abandoned the effort because the artefacts were incomplete. The teams had captured the *how* (topology and decisions) but didn't have time to build [[architecture-decision-record|ADRs]] capturing the *why*, and "the why is much more interesting because it contains the trade-offs they considered" (source: chapter-24-developing-a-career-path.md). This is the book's [[laws-of-software-architecture|Second Law]] ("why beats how") applied to the practice loop itself — an answer without the trade-off reasoning that produced it is half the story.

The parting words of the book: **always learn, always practice, and go do some architecture.**

## How the three techniques compose

The chapter's three techniques are not independent — they form a daily/weekly/career-long stack:

1. **Every day (20 minutes)** — read, watch, or listen to something that either grows breadth or goes deeper. The slot is scheduled, not found.
2. **Weekly-ish (the radar)** — reclassify what you just learned. Does it move from *Assess* to *Trial*? Has something on *Trial* either graduated to *Adopt* or fallen back to *Hold*? The radar is a living document, not a one-shot exercise.
3. **Over a career (katas and production work)** — practise the skill of architecture itself on timeboxed exercises when real opportunities are rare, and capture the trade-offs when they are not.

The three techniques map onto the [[architect-expectations|eight expectations]] as follows: the 20-minute rule operationalises Expectation #3 (keep current); the radar is the Expectation #3 tool and also how Expectation #5 (diverse exposure) grows over time; and deliberate practice via katas keeps Expectations #1, #2, and #5 sharp between rare greenfield opportunities.

## Related pages

- [[architect-expectations]] — Expectation #3 (keep current) and Expectation #5 (diverse exposure) are what this chapter operationalises
- [[technical-breadth-vs-depth]] — the knowledge-pyramid model the 20-minute rule feeds; the two dysfunctions (trying to maintain expertise everywhere; stale expertise) the radar is a defence against
- [[architecture-katas]] — Neward's 45-minute exercise; the deliberate-practice tool the chapter's parting words point at
- [[architecture-decision-record]] — the missing half of the katas-as-answer-key problem; why the *why* matters more than the *how*
- [[laws-of-software-architecture]] — the Second Law ("why beats how") applied to the practice loop itself
- [[trade-off-analysis]] — what the radar's Trial ring is really for; what katas are practising
- [[balancing-architecture-and-coding]] — the depth-side counterpart to the 20-minute rule's breadth-side discipline
- [[architectural-thinking]] — the cognitive stance the whole chapter is trying to sustain across a career
- [[fundamentals-of-software-architecture]]
