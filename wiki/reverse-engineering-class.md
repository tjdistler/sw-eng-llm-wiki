# Reverse Engineering a Production Service (class)

**Summary**: Chapter 28's flagship Google SRE training class — "Reverse Engineering a Production Service (without help from its owners)." Students are told the Google News team has vanished on a Bermuda Triangle cruise and they must commandeer the stack. The class exercises all three SRE attributes (reverse engineering, statistical-comparative thinking, improvisation) in one session.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The framing scenario

Chapter 28's setup (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> The entire Google News Team — SRE, Software Engineers, Product Management, and so forth — has gone on a company trip: a cruise of the Bermuda Triangle. We haven't heard from the team for 30 days, so our students are the newly appointed Google News SRE Team. They need to figure out how the serving stack works from end-to-end in order to commandeer it and keep it running.

The humorous premise does real pedagogical work: it forecloses the usual "ask a senior engineer" escape route and forces students into the techniques the class is actually teaching.

## The activity

Students are led through interactive, purpose-driven exercises that trace an inbound web-browser query through Google's infrastructure. At each stage the instructor emphasises that **multiple methods exist** to discover the connectivity between production servers, so connections aren't missed (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md).

In the middle of the class a deliberate twist: students are challenged to find **another endpoint** for the incoming traffic, revealing that their initial assumption was too narrowly scoped. Then they are challenged to find **other ways into the stack**. The class exploits Google's heavily instrumented production binaries — which self-report their RPC connectivity — plus white-box and black-box monitoring to determine which paths users' queries take.

Along the way, students assemble a system diagram and discuss components that are **shared infrastructure** likely to recur in the future.

## What it teaches (all three attributes)

The class is designed to develop the three [[sre-onboarding|aspirational SRE attributes]] simultaneously:

- **[[reverse-engineering-skills]]** — the entire activity is reverse engineering by construction; students practise the RPC-follow, log-read, and debugging-surface fluencies as reflexes
- **[[statistical-comparative-thinking]]** — the "find another endpoint" twist forces students to compare expected with actual and revise assumptions
- **[[improvisational-troubleshooting]]** — no single standard procedure solves the problem; students must compose their approach from available tools

Paul Cowan's testimonial in Chapter 28 captures the dynamic (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> When it came time to learn [part of the Google Maps stack], [a new SRE] asked if, rather than passively having someone explain the service, she could do this herself — learning everything via Reverse Engineering class techniques, and having the rest of us correct her / fill in the blanks for whatever she missed or got wrong. The result? Well, it was probably more correct and useful than it would have been if I'd given the talk, and I've been on-call for this for over 5 years!

## The take-home assignment

The class does not end when the classroom session does. Each student is assigned a concrete follow-up (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

1. Return to their home team and ask a senior SRE to **select a stack** (or slice of a stack) for which they'll be on-call
2. Using the skills from class, diagram that stack on their own
3. Present the findings back to the senior SRE

Two things happen:

- The student inevitably **misses a few subtle details**, producing a good discussion and filling in gaps
- The senior SRE **likely learns something too**, because the live-system state has drifted from their mental model

This is the same bidirectional newbie-refreshes-senior dynamic that [[documentation-as-apprenticeship|overhauling the on-call learning checklist]] produces. Widdowson notes explicitly that *because of the rapid change of production systems, it is important that your team welcome any chance to refamiliarise themselves with a system, including by learning from the newest, rather than oldest, members of the team* (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md).

## Generalisable design principles

The class is a Google-specific instantiation of principles that transfer to other organisations:

- **Teach by doing, not by explaining** — the student reverse-engineers the stack themselves rather than being lectured at
- **Plant deliberate surprises** — the "find another endpoint" twist trains the habit of questioning initial assumptions
- **Exploit available introspection surfaces** — the class works because Google's binaries self-report RPC connectivity; if the local environment is less instrumented, the class must adapt
- **Close with a homework transfer** — the class's value compounds because students apply the technique to their *own* stack afterwards

The "follow the RPC" heuristic also generalises to batch/pipeline systems: start with the operation that kicks off the system (arriving data, a transaction to validate, a triggering event) and trace outward.

## Related pages

- [[sre-onboarding]]
- [[reverse-engineering-skills]]
- [[statistical-comparative-thinking]]
- [[improvisational-troubleshooting]]
- [[cumulative-learning-paths]]
- [[documentation-as-apprenticeship]]
- [[life-of-a-request]]
- [[distributed-tracing]]
