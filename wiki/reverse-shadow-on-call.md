# Reverse Shadow On-Call

**Summary**: Chapter 28's optional final onboarding step before full on-call — the newbie becomes the primary on-caller and owns all escalations, while an experienced on-caller "lurks in the shadows" and independently diagnoses the situation without modifying state. Inverts the roles of [[shadow-on-call|shadow on-call]]: the student drives, the mentor validates.

**Sources**: `raw/site-reliability-engineering/chapter-28-accelerating-sres-to-on-call-and-beyond.md`

**Last updated**: 2026-04-17

---

## The mechanic

Chapter 28's description (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

> Some teams will also include a final step: having the experienced on-caller "reverse shadow" the student. The newbie will become primary on-call and own all incoming escalations, but the experienced on-caller will lurk in the shadows, independently diagnosing the situation without modifying any state. The experienced SRE will be available to provide active support, help, validation, and hints as necessary.

Two moves invert the usual arrangement:

- The **newbie is primary** — they receive the page, own the investigation, make the decisions
- The **mentor is the shadow** — watching, independently diagnosing, but not modifying state unless explicitly asked

## What the reversal tests

Regular shadow on-call tests the newbie's **comprehension** — can they follow what is happening? Reverse shadow tests their **agency** — can they drive the response themselves? The two skills are distinct and the second is harder. Comprehension can be passive; driving requires committing to actions under time pressure with uncertain information.

The mentor's parallel diagnosis is the validation channel: if the experienced SRE arrived at the same mitigation the newbie is pursuing, the newbie is on the right track. If they diverge, the mentor can intervene with active support.

## Three supports the mentor provides

Chapter 28's list (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md):

- **Active support** — step in if the situation gets beyond the newbie's capability
- **Help** — answer specific questions in real time
- **Validation and hints** — confirm hypotheses or point out missed evidence

The mentor's default posture is **lurking**, not directing. That is what makes it a reverse shadow rather than a standard pairing — the newbie's judgement is primary; the mentor's role is to prevent actual harm, not to drive.

## The "not modifying state" discipline

The mentor is explicitly prohibited from modifying state. This constraint is load-bearing:

- It forces the newbie to make all the commit points themselves, which is the skill being developed
- It prevents the mentor's instincts from taking over the investigation mid-flight (a real risk under time pressure)
- It creates a clean, observable record of what the newbie did, which supports post-incident review

The mentor's independent diagnosis exists in parallel with the newbie's, but only the newbie's actions touch production.

## Placement in the progression

Reverse shadow is the **final optional gate** in Chapter 28's progression:

1. [[cumulative-learning-paths|Learning paths]] and [[on-call-learning-checklist|checklist]] completion
2. [[targeted-project-work|Starter project]]
3. [[teachable-postmortems|Postmortem reading]], [[disaster-role-playing|Wheel of Misfortune]], [[breaking-real-systems|break-real-things exercises]]
4. [[documentation-as-apprenticeship|Documentation overhaul]]
5. [[shadow-on-call|Shadow on-call]]
6. **Reverse shadow on-call** (optional)
7. Full on-call — [[sre-continuing-education|learning continues]]

Some teams skip step 6 and go straight from shadow to full on-call; Chapter 28 notes that this step is a team choice rather than a universal requirement.

## Relationship to the on-call pairing structure

Reverse shadow pre-figures the normal on-call arrangement at Google. Chapter 11's [[sre-on-call-engagement|engagement model]] has **primary and secondary** on-callers simultaneously. A reverse shadow rotation is essentially the newbie running primary for practice, with an experienced engineer as a non-standard "auxiliary secondary" — similar structure, different purpose.

The transition to full on-call is then a matter of the newbie moving from the practice structure to the standard primary/secondary pairing with another full-rotation SRE. The cognitive model and the tooling are already familiar.

## Relationship to rite-of-passage framing

Chapter 28 treats going on-call as a **rite of passage that should be celebrated as a team** (source: chapter-28-accelerating-sres-to-on-call-and-beyond.md). Reverse shadow is the last-mile practice that makes the celebration earnable on evidence rather than assumption. After enough reverse-shadowed incidents where the newbie's diagnosis converged with the mentor's, the team has concrete grounds to trust the handoff.

## Related pages

- [[sre-onboarding]]
- [[shadow-on-call]]
- [[sre-continuing-education]]
- [[sre-on-call-engagement]]
- [[balanced-on-call]]
- [[on-call-learning-checklist]]
