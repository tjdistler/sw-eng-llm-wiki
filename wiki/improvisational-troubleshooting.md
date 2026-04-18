# Improvisational Troubleshooting

**Summary**: The third of Chapter 28's three aspirational SRE attributes — the ability to improvise when standard operating procedures break down, by composing defences across multiple tools and "zooming out" when an investigation bogs down. The SRE analogue of defence in depth applied to one's own problem-solving behaviour.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## Why it's necessary

Chapter 28 poses the scenario concretely (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> You try out a fix for the breakage, but it doesn't work. The developer(s) behind the failing system are nowhere to be found. What do you do now? You improvise!

Playbooks and standard procedures cover anticipated cases. Production inevitably produces cases nobody anticipated. The attribute of being able to assemble a response from first principles, when procedure gives out, is what separates SREs who resolve novel incidents from SREs who escalate them.

## Defence in depth in problem-solving behaviour

The chapter's design rule:

> Learning multiple tools that can solve parts of your problem allows you to practice defense in depth in your own problem-solving behaviors. (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md)

Two implications:

- **Multiple tools per job.** Knowing one way to inspect RPC traffic, one way to query metrics, one way to read logs is not enough — when the usual tool is unavailable (the metrics backend is down, the log index is slow), the investigation must continue with the alternatives.
- **Multiple techniques per problem class.** Knowing only one approach to debugging a latency spike (for example) means the SRE is stuck when that approach hits a dead end.

[[reverse-engineering-skills|Reverse engineering]] supplies the toolkit breadth; improvisation is the composition skill that uses the toolkit when the canonical path fails.

## Two named failure modes

Chapter 28 names two specific traps (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

### Being too procedural

> Being too procedural in the face of an outage, thus forgetting your analytical skills, can be the difference between getting stuck and finding the root cause.

The SRE walks through the playbook, finds the playbook's steps don't resolve the issue, and has nothing else to try. The fix is to train analytical improvisation as a separate skill — not to abandon playbooks, but to recognise when to step outside them.

### Too many untested assumptions

> A case of bogged-down troubleshooting can be further compounded when an SRE brings too many untested assumptions about the cause of an outage into their decision making.

The SRE commits early to a theory, confirmation bias kicks in, evidence is interpreted to fit the theory, and the investigation stalls. This is the same failure mode Chapter 11's [[incident-response-mindset|stress-and-cognition section]] and Chapter 12's [[troubleshooting-anti-patterns|latching onto past causes]] describe.

## The "zoom out" manoeuvre

Chapter 28's remedy for a bogged-down investigation is to **zoom out** and take a different approach (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). Widdowson names this as a *valuable lesson for SREs to learn early on* — so it is taught deliberately, not left to be acquired by trial. Recognising "I am stuck; what different angle could I try?" is a metacognitive skill; the practice of naming it makes it available during an incident when cognitive load is otherwise maxed out.

## How it's trained

- **[[disaster-role-playing|Wheel of Misfortune]]** — the game master can deliberately foreclose the obvious path, forcing improvisation
- **[[breaking-real-systems|Hands-on chaos exercises]]** — novel breakages by construction don't have pre-written procedures
- **[[reverse-engineering-class|Reverse-engineering class]]** — presenting the system in ways that require new synthesis rather than memorised answers
- **[[teachable-postmortems|Postmortem reading]]** — exposure to historical cases where the responder improvised successfully; the patterns are absorbed by osmosis

## Connection to the other two attributes

Improvisation depends on both prerequisites:

- Without [[reverse-engineering-skills|reverse engineering]], the SRE does not know the system well enough to improvise meaningfully — the improvisation is guessing
- Without [[statistical-comparative-thinking|statistical-comparative thinking]], improvised attempts can't be evaluated — each new approach is a coin flip

The three attributes compose into a single meta-skill: **under time pressure and with incomplete information, form and test hypotheses against an unfamiliar system using a flexible set of tools**.

## Related pages

- [[sre-onboarding]]
- [[reverse-engineering-skills]]
- [[statistical-comparative-thinking]]
- [[disaster-role-playing]]
- [[breaking-real-systems]]
- [[troubleshooting-anti-patterns]]
- [[incident-response-mindset]]
- [[on-call-playbook]]
