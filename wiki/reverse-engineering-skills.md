# Reverse Engineering Skills

**Summary**: The first of Chapter 28's three aspirational SRE attributes — the ability to figure out how a system you've never seen before works, by following RPC boundaries, reading logs, and using the debugging surfaces of production binaries. A baseline reflex, not a specialised skill, because production is always changing.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## Why it's a baseline

Chapter 28's argument:

> In the course of their jobs, [SREs] will come across systems they've never seen before, so they need to have strong reverse engineering skills. (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md)

Widdowson sharpens the claim with a parenthetical: *or, more likely, how the current versions of systems they used to know quite well work.* Production systems change constantly; the system the on-caller last looked at six months ago is not the system they are staring at tonight. Treating every investigation as at least partially a reverse-engineering exercise — rather than assuming remembered mental models still hold — is the only robust stance.

## The required fluencies

The chapter names three concrete skill areas SREs must practice until reflexive (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- **Debugging tools** — the diagnostic surfaces of the company's applications
- **RPC boundaries** — tracing calls between processes to map the live connectivity graph
- **Logs** — the binary's own narrative of what it is doing

Practising these *so they become reflexive* is the explicit goal. The debugging surfaces must be used often enough that the SRE doesn't think about using them — during an incident, consciously remembering how to invoke a tool costs time that isn't available.

## How it's taught

Reverse engineering is not acquired by reading. Chapter 28's approach:

- Teach the diagnostic and debugging surfaces explicitly — don't assume discovery
- Have trainees **practice drawing inferences** from the information those surfaces reveal
- Make the practice repeat until it is reflexive

[[reverse-engineering-class]] is the worked example — a hands-on class where students reverse-engineer a production stack from scratch, tracing a web query through Google's infrastructure.

## The "follow the RPC" heuristic

Chapter 28's footnote about batch/pipeline systems extends the heuristic (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> This "follow the RPC" approach also works well for batch/pipeline systems; start with the operation that kicks off the system. For batch systems, this operation could be data arriving that needs to be processed, a transaction that needs to be validated, or many other events.

The general rule: find the **entry point** (the user query, the arriving data, the trigger event), then trace outward. The SRE's mental model of the system gets built in the direction traffic flows.

## Connection to the other two attributes

Reverse engineering supplies the **mental model** that [[statistical-comparative-thinking]] then operates on. You cannot compare across kernel versions, binary versions, regional traffic mix, etc. unless you already understand how those variables relate. And when standard procedures fail, [[improvisational-troubleshooting]] depends on the same reverse-engineering fluency applied to parts of the system you hadn't planned to touch.

All three attributes therefore share a common substrate: **high comfort with the observability surface of production software**.

## Relationship to monitoring and observability

Reverse engineering is downstream of good observability. Chapter 12's [[making-troubleshooting-easier|design-for-observability disciplines]] — well-defined observable interfaces, consistent request IDs, changes that are logged — are the prerequisites that make reverse engineering tractable. Chapter 28's emphasis on teaching the tools as reflexes is the human-side investment that pays off the observability investment.

## Related pages

- [[sre-onboarding]]
- [[reverse-engineering-class]]
- [[statistical-comparative-thinking]]
- [[improvisational-troubleshooting]]
- [[troubleshooting-model]]
- [[making-troubleshooting-easier]]
- [[distributed-tracing]]
