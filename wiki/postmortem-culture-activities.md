# Postmortem Culture Activities

**Summary**: Chapter 15's catalogue of **social mechanisms** SREs use to disseminate postmortem learning beyond the authoring team. A postmortem that only the authors read is a failed postmortem; the monthly newsletter, discussion groups, reading clubs, and Wheel of Misfortune replays are the channels that turn individual incidents into organisational memory.

**Sources**: `raw/site-reliability-engineering/chapter-15-postmortem-culture-learning-from-failure.md`, `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The why

Introducing a postmortem culture "requires continuous cultivation and reinforcement" (source: chapter-15-postmortem-culture-learning-from-failure.md). The [[postmortem-review-process|review pipeline]] captures learning in writing; the activities below are what keep the learning circulating so it doesn't stagnate in the repository.

Chapter 15 also names the alternative failure mode explicitly: postmortems that are just **written and filed** get forgotten. The activities exist specifically to defeat that outcome.

## Postmortem of the month

Each month, an **interesting and well-written postmortem** is shared with the entire organisation via newsletter (source: chapter-15-postmortem-culture-learning-from-failure.md). This is the curation layer — the signal/noise filter on top of "publish everything."

Two things make it work:

- It's **selective** — not every postmortem is postmortem-of-the-month material, so authors have a target to aspire to.
- It's **well-written** as a criterion in its own right. A deeply-investigated incident that's badly written won't circulate; rewarding good writing is how the prose quality compounds.

This is the visible surface of the [[rewarding-postmortems|reward-the-right-behaviour]] discipline: the authors of featured postmortems are recognised publicly.

## The Google+ postmortem group

An internal group specifically for **sharing and discussing internal and external postmortems, best practices, and commentary** (source: chapter-15-postmortem-culture-learning-from-failure.md). Two notable elements:

- It's cross-org — anyone with an interest participates.
- It includes **external** postmortems (industry outages, published incident writeups from other companies). The implicit argument: learning from other organisations' failures is cheaper than learning from your own.

## Postmortem reading clubs

Teams host regular reading clubs where (source: chapter-15-postmortem-culture-learning-from-failure.md):

> An interesting or impactful postmortem is brought to the table (along with some tasty refreshments) for an open dialogue with participants, nonparticipants, and new Googlers about what happened, what lessons the incident imparted, and the aftermath of the incident. Often, the postmortem being reviewed is months or years old!

Three properties worth calling out:

- **Mix of participants and non-participants.** The original responders provide context; newcomers ask the questions that surface institutional knowledge the old hands forgot they knew.
- **Old postmortems are fair game.** Years-old incidents can still be teaching material — especially when the system they happened on is still running.
- **Low-ceremony format.** Refreshments, open dialogue. The format is deliberately social because sustained culture doesn't come from mandatory training.

Chapter 28 adds a variant: **"tales of fail"** — instead of pre-reading, the postmortem author(s) semiformally present the outage themselves, driving the discussion from first-person narrative (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). The two formats coexist; reading clubs favour breadth of analysis, tales of fail favour narrative richness. Chapter 28 also distinguishes ordinary postmortems from **[[teachable-postmortems]]** — the subset of postmortems whose structural or novel failures make them especially valuable training material for newbies.

## Wheel of Misfortune

The [[on-call-playbook|Wheel of Misfortune]] exercise replays an old incident with engineers playing the roles from the postmortem, with the **original [[incident-commander|incident commander]] attending to keep the reenactment realistic** (source: chapter-15-postmortem-culture-learning-from-failure.md). Chapter 15 positions this as a postmortem-culture activity (not just an [[operational-underload|underload remedy]] from Chapter 11):

- New SREs get to exercise incident-response muscles on a known-resolved incident.
- The old postmortem gets re-opened in the collective memory.
- The original IC's informal knowledge — the bits that never made it into the written doc — gets propagated.

See [[on-call-playbook]] for the full exercise, and [[operational-underload]] for the complementary framing.

## Overcoming resistance

Chapter 15 explicitly names the adoption obstacle (source: chapter-15-postmortem-culture-learning-from-failure.md):

> One of the biggest challenges of introducing postmortems to an organization is that some may question their value given the cost of their preparation.

Three strategies:

1. **Ease postmortems into the workflow.** A trial period with several complete and successful postmortems proves the value and helps calibrate trigger criteria.
2. **Make postmortem-writing a rewarded and celebrated practice** — the activities above plus individual/team performance management. See [[rewarding-postmortems]].
3. **Get senior leadership visibly involved.** Chapter 15 notes that even Larry Page talks about the high value of postmortems; Chapter 15's [[rewarding-postmortems|TGIF story]] is the concrete example.

## The compounding loop

Each activity targets a different failure mode:

- Postmortem of the month → the "filed and forgotten" failure mode.
- Reading clubs → the "authors-only audience" failure mode.
- Google+ group → the "no external learning" failure mode.
- Wheel of Misfortune → the "knowledge dies with the original responder" failure mode.

Together they form the social substrate Chapter 15 says is required: postmortems work as an institution only when the broader organisation actively engages with them.

## Related pages

- [[postmortem-philosophy]]
- [[postmortem-review-process]]
- [[rewarding-postmortems]]
- [[postmortems-at-google-working-group]]
- [[on-call-playbook]]
- [[operational-underload]]
- [[incident-commander]]
- [[learning-from-outages]]
- [[teachable-postmortems]]
- [[disaster-role-playing]]
- [[sre-onboarding]]
