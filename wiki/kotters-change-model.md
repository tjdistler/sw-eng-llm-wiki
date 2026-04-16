# Kotter's Change Model

**Summary**: Dr. John Kotter's eight-step process for organisational change, applied by Newman to the specific case of moving an organisation toward a microservice architecture. Most useful for transitions large enough to need cross-team buy-in.

**Sources**: `raw/monolith-to-microservices/chapter-02-planning-a-migration.md`

**Last updated**: 2026-04-16

---

## When to use it

Kotter's model is designed for large-scale organisational shifts; for a 10-person team it can be overkill (source: chapter-02-planning-a-migration.md). But Newman has found even the early steps useful at smaller scope. The full eight steps:

## 1. Establishing a sense of urgency

Your idea — "we should adopt microservices" — is one of many good ideas competing for attention. The trick is helping people understand that **now** is the time. Look for "teachable moments" — the brief window after a crisis when people are receptive to fixing the underlying issue (source: chapter-02-planning-a-migration.md).

Crucially, the urgency you communicate is about the *outcome*, not the architecture. "We need to ship faster", not "we need microservices". Microservices are not the goal — see [[why-microservices]].

## 2. Creating the guiding coalition

You don't need everyone on board, but you need enough to make it happen. For a team-scale change, your immediate colleagues plus a tech lead or architect may suffice. For a company-scale change, you may need executive sponsorship (CIO, CTO).

Trust is earned. People back ideas from people they've previously worked with on smaller wins. And — important for microservice adoption — the coalition must include people *outside* the IT silo, because the technical changes (caching for latency, accepting stale data, different failure modes) have user-visible consequences that the business needs to weigh in on (source: chapter-02-planning-a-migration.md).

## 3. Developing a vision and strategy

The **vision** is the goal: what you're aiming for. The **strategy** is the how. Microservices belong in the strategy, not the vision.

Visions can be vague ("reduce our bug count!") for small teams; they need more packaging the wider you share them. Be committed to the vision; be willing to change the strategy in the face of contrary evidence — sticking with a strategy because you're already invested is the [[measuring-microservice-transition|sunk cost fallacy]] (source: chapter-02-planning-a-migration.md).

## 4. Communicating the change vision

Newman cites a real-world counterexample: an unnamed CEO who announced "in the next 12 months, we will reduce costs and deliver faster by moving to microservices and embracing cloud-native technologies". Nobody believed it — the goals contradicted each other (a wholesale platform change *increases* short-term cost), and the timeline was implausible for that organisation's pace (source: chapter-02-planning-a-migration.md).

Useful tactics: face-to-face communication first (it surfaces reactions and lets you calibrate), then broader channels. Start small. Newman cites Google's "Testing on the Toilet" — one-page articles pinned to toilet doors — as a successful campaign for socialising automated-testing practices.

## 5. Empowering employees for broad-based action

In management-speak, this means **removing roadblocks**. Most often, people simply don't have the bandwidth — they're too busy doing what they do now to change how they do it. Bringing in extra people (hires or consultants) is a common way to provide that bandwidth (source: chapter-02-planning-a-migration.md).

Concrete example for microservice adoption: if your current process needs hardware orders six months in advance, on-demand virtualised infrastructure (containers, public cloud) is itself a roadblock removal. But Newman warns against the inverse trap — spending a year building "The Perfect Microservice Platform" before anyone uses it. Bring in technology to fix concrete observed problems, not theoretical ones.

## 6. Generating short-term wins

If progress isn't visible, faith in the vision evaporates. For microservice migrations this means picking easy-to-extract functionality — but balanced against actual benefit. See [[extraction-prioritization]].

If your "easy" first extraction turns out to be hard, that's valuable information about your strategy. The point of starting small is to surface this information cheaply.

## 7. Consolidating gains and producing more change

Once you have early wins, the temptation is to coast. Don't. Quick wins might be the only wins if you don't push on. Pause and reflect — *then* push on.

Newman flags one specific consolidation challenge for microservices: database decomposition can be deferred initially but cannot be deferred forever (Chapter 4 covers techniques). And techniques that worked in one part of the monolith may not work in another (source: chapter-02-planning-a-migration.md).

## 8. Anchoring new approaches in the culture

Continued iteration plus continued story-sharing turns the new way into the way things are done. In mature microservice organisations, *whether* to use them has stopped being a question — but Newman warns this creates a meta-problem: the Established Way of Working can crowd out the next better idea.

## Why Newman likes it

He likes Kotter's model partly because it distils the work into discrete, comprehensible steps; many other change models exist. He recommends Kotter's *Leading Change* (1996) for the full treatment.

## Related pages

- [[why-microservices]]
- [[incremental-migration]]
- [[reorganizing-teams]]
- [[measuring-microservice-transition]]
