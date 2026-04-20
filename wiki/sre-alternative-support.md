# SRE Alternative Support

**Summary**: The fallback support modes for services SRE cannot take on as a full engagement. Before the [[frameworks-and-sre-platform|framework]] era, these were documentation and consultation only; together with the framework-based [[shared-responsibility-engagement|shared responsibility]] model they form the spectrum of production support SRE offers services that don't warrant full team ownership.

**Sources**: `raw/site-reliability-engineering/chapter-32-the-evolving-sre-engagement-model.md`

**Last updated**: 2026-04-17

---

## Why alternative support exists

Chapter 32 names two structural reasons not every service gets full SRE engagement (source: chapter-32-the-evolving-sre-engagement-model.md):

- Many services don't need high reliability and availability — other support modes suffice
- By design, the number of development teams that request SRE support exceeds the available bandwidth of SRE teams

Some mechanism has to exist for the services SRE can't take on, and that mechanism is alternative support.

## Documentation

Google maintains development guides for internal technologies and clients of widely used systems. The central artifact is the **Production Guide**, which documents production best practices as determined by the experiences of SRE and development teams. Developers implement the documented solutions and recommendations to improve their services without direct SRE involvement (source: chapter-32-the-evolving-sre-engagement-model.md).

## Consultation

Developers may seek SRE consulting to discuss specific services or problem areas (source: chapter-32-the-evolving-sre-engagement-model.md). Two forms:

- **Launch consultation by LCE.** The [[launch-coordination-engineering|Launch Coordination Engineering]] team spends most of its time consulting with development teams, especially at launch time
- **Ad-hoc SRE consultation.** SRE teams not dedicated to launches also consult with development teams. When a new service or feature is implemented, developers commonly ask SRE for advice about preparing for launch

Launch consultation is relatively light: one or two SREs spend a few hours studying design and implementation at a high level, then meet with the development team to flag risky areas and suggest well-known patterns or solutions (often drawing from the Production Guide).

## When consultation is not enough

Chapter 32 names the two patterns where consultation's breadth-but-not-depth ceiling isn't enough (source: chapter-32-the-evolving-sre-engagement-model.md):

- **Services that have grown by orders of magnitude since they launched.** Now require more time to understand than docs and consultation alone can cover
- **Services upon which many others have come to rely.** Now host significantly more traffic from many different clients

When services in either pattern start encountering significant production difficulties while simultaneously becoming important to users, long-term SRE engagement becomes necessary — that's the trigger for the [[simple-prr-model|Simple PRR Model]].

## Where shared responsibility fits

The [[shared-responsibility-engagement|shared responsibility]] engagement model is a newer mode on the alternative-support spectrum. It's not "alternative support" in the classical sense (the Production Guide / consulting pattern) because SRE is providing active infrastructure-layer support, but it serves the same role: a way to give services production-quality attention without committing a full SRE team to each one.

## Related pages

- [[sre-engagement-model]]
- [[simple-prr-model]]
- [[early-engagement-model]]
- [[frameworks-and-sre-platform]]
- [[shared-responsibility-engagement]]
- [[launch-coordination-engineering]]
- [[site-reliability-engineering]]
