# Launch Coordination Engineer (LCE) Role

**Summary**: The individual role inside [[launch-coordination-engineering|LCE]]. Hired directly into the role or transferred from SRE teams with hands-on experience running Google services. LCEs are held to the same technical requirements as any other SRE, plus strong communication and leadership skills: they bring disparate parties together, mediate conflicts, and guide, coach, and educate fellow engineers.

**Sources**: `raw/site-reliability-engineering/chapter-27-reliable-product-launches-at-scale.md`

**Last updated**: 2026-04-17

---

## Who becomes an LCE

Two paths in (source: chapter-27-reliable-product-launches-at-scale.md):

- **Direct hire** into the LCE role.
- **Transfer from an SRE team** with hands-on experience running a Google service.

Technical requirements match any other SRE. Additional requirements:

- Strong **communication** skills
- Strong **leadership** skills — an LCE brings disparate parties together, mediates conflicts, guides, coaches, educates

## What an LCE does day to day

The five consulting-team activities of the team translate into individual LCE work:

- Consulting on launches (the dominant daily activity)
- Auditing products and services against Google's reliability standards
- Mediating across SRE, product dev, PM, marketing
- Signing off on launches as safe (or not)
- Educating developers — writing and curating documentation, training resources

An LCE runs the [[launch-checklist|checklist]] against each launch, asking the questions, recording the answers, pointing at infrastructure to use, and following up on action items. Experienced LCEs adapt the checklist's depth to each launch's risk profile.

## Training

The launch checklist's apparent simplicity hides considerable complexity in *what prompted each question* and *what each answer implies*. A new LCE hire requires about **six months of training** before they can fully weight a checklist response against a specific launch's attributes (source: chapter-27-reliable-product-launches-at-scale.md). One LCE ran 350 launches through the checklist in 3.5 years.

## Incentives

Because LCE is an SRE role, the structural incentive is to **prioritise reliability over other concerns** (source: chapter-27-reliable-product-launches-at-scale.md). This is a deliberate choice that makes LCE a useful counterweight to product-development velocity. A company adopting a similar role without sharing Google's reliability priorities will need to rethink the incentive structure — placing the team inside a different organisational reporting line changes the answer to "when LCE and the launching team disagree, whose view wins?"

## The role as seen by the company

LCEs are simultaneously:

- **Accelerators** of launches — responsible for launches executing quickly without services falling over
- **Quality keepers** — responsible for making sure a failed launch doesn't take down other products
- **Stakeholder informants** — responsible for keeping stakeholders current on the nature and likelihood of failures when corners are cut for time-to-market

The dual accelerator-gatekeeper role is what distinguishes LCE from a pure release-engineering or pure reliability function. The launch-checklist discipline is the artifact that makes the balance reproducible across individuals.

## Related pages

- [[launch-coordination-engineering]]
- [[reliable-product-launches]]
- [[launch-checklist]]
- [[sre-discipline]]
- [[release-engineering]]
- [[site-reliability-engineering]]
