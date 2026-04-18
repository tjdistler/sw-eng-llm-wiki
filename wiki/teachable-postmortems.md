# Teachable Postmortems

**Summary**: Chapter 28's framing of postmortems as a primary educational resource for new SREs — the first of the chapter's five practices for aspiring on-callers. Teachable postmortems are the subset that, with small editing, can become durable training material; reading clubs and "tales of fail" are the social formats for putting them to work.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The framing

Chapter 28's opening Santayana epigraph (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Those who cannot remember the past are condemned to repeat it.

Widdowson's operational read: *when writing a [[blameless-postmortem|postmortem]], keep in mind that its most appreciative audience might be an engineer who hasn't yet been hired.* That reframes what a postmortem is for. Chapter 15 treats the postmortem primarily as the [[postmortem-philosophy|learning instrument for the team that experienced the incident]]; Chapter 28 treats it as the **institutional memory that teaches future teammates**.

## "Teachable" postmortems as a subset

Not all postmortems are equally useful as training material. Chapter 28 distinguishes (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- **Rote postmortems** — routine incidents, useful to the team at the time but not pedagogically rich
- **Teachable postmortems** — "structural or novel failures of large-scale systems" that are "as good as gold for new students"

The transformation from one to the other is usually small. Widdowson claims subtle edits to the best existing postmortems are enough to make them teachable — no rewriting required. The work is curation, not authoring.

## Ownership and cross-team sharing

Two organisational moves (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- **Pride of survival.** Many teams take pride in having survived and documented their largest outages; authorship is not the only ownership — hosting and curating the postmortem collection matters too
- **Cross-team sourcing.** Teams should ask related and integrating teams to publish their best postmortems where they can be accessed. The best teaching material often comes from outside the responder's own team

This pairs naturally with Chapter 15's [[postmortem-culture-activities#the-google-postmortem-group|cross-org postmortem group]], which collects material from across (and outside) Google for exactly this reason.

## Reading clubs

Chapter 28 (echoing and elaborating on Chapter 15) names **postmortem reading clubs** as the canonical format for putting teachable postmortems to work (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Some SRE teams at Google run "postmortem reading clubs" where fascinating and insightful postmortems are circulated, pre-read, and then discussed. The original author(s) of the postmortem can be the guest(s) of honor at the meeting.

The mechanics:

- **Pre-read.** The postmortem is distributed in advance — discussion starts with shared context
- **Guest of honour.** The original authors attend. They bring the informal knowledge that never made it into the written document
- **Mixed audience.** Participants, non-participants, and new Googlers all attend (Chapter 15's framing applies). See [[postmortem-culture-activities]]

## "Tales of fail"

An alternative Chapter 28 format (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md): rather than pre-reading, the postmortem's author(s) **semiformally present** the outage themselves — recounting it, driving the discussion. This trades the discussion-breadth of reading clubs for the narrative richness of a first-person telling. Both formats coexist at Google; each targets a different learning style.

## What reading groups actually build

Chapter 28's concrete claim:

> Regular readings or presentations on outages, including trigger conditions and mitigation steps, do wonders for building a new SRE's mental map and understanding of production and on-call response.

Three specific things the repeated exposure develops:

- **Pattern library.** Over time, readers accumulate a catalogue of "incidents that look like X" — the pattern matching that [[statistical-comparative-thinking]] requires
- **Vocabulary and norms.** The way the team *writes* about incidents shapes the way readers will eventually *respond* to them
- **Realistic calibration.** Exposure to real incidents (rather than imagined ones) calibrates expectations about how long outages take, how many false leads they produce, and how messy the response is

## Feedstock for Wheel of Misfortune

Chapter 28's closing observation on teachable postmortems: they are "excellent fuel for future abstract disaster scenarios." That is the bridge to the next practice — [[disaster-role-playing|Wheel of Misfortune]]. A well-documented historical incident is precisely the material a game master needs to build a realistic scenario. Teachable postmortems and disaster role playing therefore compose: the first builds the library, the second uses it.

## Relationship to Chapter 15

Chapter 15's [[postmortem-culture-activities|social activities]] (postmortem of the month, reading clubs, Wheel of Misfortune reenactments) and Chapter 28's teachable-postmortems section describe the same practices from different angles:

- Chapter 15 frames them as how an organisation **keeps its postmortem culture alive**
- Chapter 28 frames them as how an individual newbie **becomes a competent on-caller faster**

Both framings are correct; they compound because the same activity serves both goals.

## Related pages

- [[sre-onboarding]]
- [[blameless-postmortem]]
- [[postmortem-philosophy]]
- [[postmortem-culture-activities]]
- [[disaster-role-playing]]
- [[statistical-comparative-thinking]]
- [[learning-from-outages]]
- [[on-call-playbook]]
