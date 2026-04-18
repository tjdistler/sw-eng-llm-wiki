# Postmortem Feedback Surveys

**Summary**: Chapter 15's third named best practice — *ask for feedback on postmortem effectiveness*. Google regularly surveys SRE teams to find out whether the postmortem process is actually serving them, or whether it has drifted into pure [[toil-and-engineering-balance|toil]]. The survey mechanism is what keeps the process continuously improving rather than calcifying.

**Sources**: `raw/site-reliability-engineering/chapter-15-postmortem-culture-learning-from-failure.md`

**Last updated**: 2026-04-17

---

## The practice

Chapter 15's best practice statement (source: chapter-15-postmortem-culture-learning-from-failure.md):

> At Google, we strive to address problems as they arise and share innovations internally. We regularly survey our teams on how the postmortem process is supporting their goals and how the process might be improved.

The surveys aren't one-off exercises; they're a **standing feedback loop** baked into how the postmortem culture is maintained.

## The four survey questions

Chapter 15 lists the specific questions asked (source: chapter-15-postmortem-culture-learning-from-failure.md):

1. **Is the culture supporting your work?** The broadest question — does the postmortem process feel like a genuine learning mechanism, or does it feel like bureaucracy?
2. **Does writing a postmortem entail too much toil** (see Chapter 5)? The explicit cross-reference to [[toil-and-engineering-balance]] is deliberate. Postmortems are supposed to be engineering work — a postmortem process that has become toil (repetitive, tactical, no enduring value) has degenerated.
3. **What best practices does your team recommend for other teams?** Surfaces the on-the-ground innovations that deserve to be shared.
4. **What kinds of tools would you like to see developed?** Feeds the [[postmortems-at-google-working-group]] tooling roadmap directly.

## Why this matters

The survey mechanism is the **defence against process calcification**. A postmortem process that was right for Google in 2010 will not be right in 2016 — services have grown, team sizes have shifted, tooling has evolved, incident types have changed. Without a feedback loop, the process ossifies and eventually stops delivering the value it was designed for.

Chapter 15's framing makes this explicit (source: chapter-15-postmortem-culture-learning-from-failure.md):

> The survey results give the SREs in the trenches the opportunity to ask for improvements that will increase the effectiveness of the postmortem culture.

The surveys are a **governance instrument**: they give the people closest to the work standing to drive changes to the process.

## The toil question in particular

The second question — does writing a postmortem feel like toil? — is the critical one. Chapter 5's [[toil-and-engineering-balance]] definition flags repetitive, manual, automatable work as specifically corrosive. If postmortem authoring has become toil, the organisation has to either:

- Automate the toil portions (data collection from incident tools, timeline reconstruction — see [[postmortems-at-google-working-group]]).
- Reduce the scope of what postmortems require (revisit [[postmortem-triggers|triggers]] or [[postmortem-template|template]] fields).
- Both.

The survey is the mechanism by which this degradation gets detected before it erodes the culture.

## Continuous improvement as a discipline

Chapter 15 ends the best-practice section with a cultural claim (source: chapter-15-postmortem-culture-learning-from-failure.md):

> Beyond the operational aspects of incident management and follow-up, postmortem practice has been woven into the culture at Google: it's now a cultural norm that any significant incident is followed by a comprehensive postmortem.

The survey practice is what keeps that cultural norm *functional*. Cultural norms without continuous maintenance become ritual — things people do because that's how it's done, rather than because it's useful. The survey keeps asking "is this actually working?" and pushes back when the answer is no.

## Connection to the working group

The survey results feed directly into [[postmortems-at-google-working-group|Postmortems at Google]] — the chapter's closing section names template improvements, automation, and trend-analysis tooling as active workstreams, all driven by the kinds of "what tools would you like to see developed" feedback the surveys collect.

## Related pages

- [[postmortem-philosophy]]
- [[postmortem-review-process]]
- [[postmortems-at-google-working-group]]
- [[toil-and-engineering-balance]]
- [[postmortem-template]]
- [[postmortem-triggers]]
