# Disaster Role Playing (Wheel of Misfortune)

**Summary**: Chapter 28's deep treatment of the "Wheel of Misfortune" / "Walk the Plank" tabletop exercise — a weekly scenario-based drill that mixes SREs of different experience levels, impressing the team's problem-solving culture on newbies while keeping veterans current on stack changes. The SRE analogue of a tabletop RPG, with a game master running a carefully prepared scenario.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The purpose

Chapter 28 opens the Disaster Role Playing section with a challenge (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> When you have a group of SREs of wildly different experience levels, what can you do to bring them all together, and enable them to learn from each other? How do you impress the SRE culture and problem-solving nature of your team upon a newbie, while also keeping grizzled veterans apprised of new changes and features in your stack?

The answer: regular disaster role playing. The exercise is bidirectional by design — newbies learn the culture, veterans keep up with changes — and Widdowson notes the humorous titling ("Wheel of Misfortune," "Walk the Plank") deliberately makes it **less intimidating to freshly hired SREs**.

## Robert Kennedy's "SRE Zork"

Chapter 28's source quote (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Once a week we have a meeting where a victim is chosen to be on the spot in front of the group, and a scenario — often a real one taken from the annals of Google history — is thrown at him or her. The victim, whom I think of as a game show contestant, tells the game show host what s/he would do or query to understand or solve the problem, and the host tells the victim what happens with each action or observation. It's like SRE Zork. You are in a maze of twisty monitoring consoles, all alike. You must save innocent users from slipping into the Chasm of Excessive Query Latency, save datacenters from Near-Certain Meltdown, and spare us all the embarrassment of Erroneous Google Doodle Display.

The Zork / text-adventure analogy is apt: the game master is the world simulator, the on-caller issues actions and receives responses, and the game only makes sense when both sides are paying attention.

## The mechanics

Chapter 28's recipe (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- The **game master (GM)** picks two team members to play primary and secondary on-call
- An incoming page is announced; the on-callers respond with what they would do to mitigate and investigate
- The GM has carefully prepared a scenario — often one of:
  - A previous outage newer members weren't around for, or older members have forgotten
  - A hypothetical breakage of a new/soon-to-be-launched feature, leaving everyone equally unprepared
  - An expansion of a new and novel threat a coworker recently found in production
- Over **30–60 minutes**, the primary and secondary try to root-cause the issue
- The GM **provides additional context** as the problem unfolds — what graphs might look like, what other teams would say if paged
- If the scenario involves escalation outside the home team, the GM plays the other team
- When participants stray, the GM steers with red-herring redirection, urgency stimuli, or pointed questions

Two example steering moves from the chapter's footnotes:

- *"You're getting paged by another team that brings you more information. Here's what they say…"*
- *"We're losing money quickly! How could you stop the bleeding in the short term?"*

## What success looks like

Chapter 28's criterion (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> When your disaster RPG is successful, everyone will have learned something: perhaps a new tool or trick, a different perspective on how to solve a problem, or (especially gratifying to new team members) a validation that you could have solved this week's problem if you had been picked.

The *validation* half is load-bearing for culture. New team members get explicit evidence that they could have handled a real incident. That evidence is hard to come by any other way short of an actual page.

The closing observation: with some luck, the exercise inspires teammates to look forward to next week's adventure — or to volunteer to be the game master. Self-sustaining participation is the marker of a healthy drill culture.

## What the exercise trains

Chapter 28 positions Wheel of Misfortune at the intersection of all three [[sre-onboarding|aspirational SRE attributes]]:

- **[[statistical-comparative-thinking]]** — the core of the exercise; the on-caller must articulate hypotheses and the GM provides evidence for and against
- **[[improvisational-troubleshooting]]** — the GM can deliberately close off the canonical path, forcing improvisation
- **[[reverse-engineering-skills]]** — scenarios involving soon-to-launch features mean even the veterans are reasoning about an unfamiliar surface

## Three Chapter cross-references

The same exercise appears in three SRE-book chapters, each giving a different angle:

- **Chapter 1** — mentions it as a complementary practice to [[on-call-playbook|playbooks]]
- **Chapter 11** — positions it as the remedy for [[operational-underload]]: when real incidents are too rare to keep the team current, Wheel of Misfortune fills the gap
- **Chapter 15** — catalogues it under [[postmortem-culture-activities|postmortem culture activities]]: replaying a historical incident with the original [[incident-commander|IC]] in attendance is the format that carries institutional memory forward
- **Chapter 28** — the full operational manual (this page)

The exercise's value is a multi-origin payoff: solving the onboarding problem, the underload problem, and the postmortem-knowledge-decay problem all at once.

## Relationship to [[breaking-real-systems|Break Real Things, Fix Real Things]]

Disaster role playing is purely imagined — the GM describes what graphs look like. [[breaking-real-systems|Breaking real systems]] is the hands-on continuation where the exercise runs against a real (but isolated) production instance. Chapter 28 positions them sequentially: disaster role playing "helps get a newbie's mind into the game," but hands-on experience is "even better" once the mental model is in place.

## Related pages

- [[sre-onboarding]]
- [[on-call-playbook]]
- [[operational-underload]]
- [[postmortem-culture-activities]]
- [[teachable-postmortems]]
- [[breaking-real-systems]]
- [[statistical-comparative-thinking]]
- [[improvisational-troubleshooting]]
- [[incident-commander]]
- [[testing-disaster-recovery]]
