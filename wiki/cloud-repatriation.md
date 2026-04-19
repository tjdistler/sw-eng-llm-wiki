# Cloud Repatriation

**Summary**: Moving workloads back from public cloud to owned hardware. Popularised by Andreessen Horowitz's Sarah Wang and Martin Casado in "The Cost of Cloud, A Trillion Dollar Paradox" (2021). Reis and Housley push back: the case studies (Dropbox, Cloudflare) are genuine but don't generalise — "you are not Dropbox, nor are you Cloudflare."

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## The origin of the debate

Chapter 4 cites Wang and Casado's 2021 article, which generated significant noise (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Readers widely interpreted the article as a call for the repatriation of cloud workloads to on-premises servers. They make a somewhat more subtle argument that companies should expend significant resources to control cloud spending and should consider repatriation as a possible option.

The cited case study — Dropbox moving significant workloads from AWS to its own servers — became a talking point in the industry.

## Chapter 4's pushback: false equivalence

Reis and Housley argue the case studies are **frequently used without appropriate context** and constitute a false-equivalence fallacy (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

### Why Dropbox is not a template

1. **Scale.** Dropbox stores "many exabytes" of data and keeps growing.
2. **Network traffic.** Dropbox added "hundreds of gigabits of internet connectivity" in 2017 alone. Egress costs in a public cloud would be extraordinary.
3. **Highly specialised product.** Dropbox is essentially a cloud storage vendor. Its core competence is a **differential file-update system** that efficiently synchronises actively edited files — not a good fit for off-the-shelf object or block storage. The custom hardware+software stack is a competitive advantage.
4. **Selective repatriation.** Dropbox moved its core storage product on-prem but continued building other AWS workloads. They repatriated one highly tuned service, not the whole company.

### Other cited examples (same lesson)

- **Backblaze** began as personal cloud backup, launched B2 (S3-compatible). Now stores over an exabyte.
- **Cloudflare** provides services for over 25 million internet properties with 51 Tbps of total network capacity — that scale requires owning the edge.
- **Netflix** runs most things on AWS (~70% of 2017 compute for video transcoding, plus application backend and data analytics) but **built a custom CDN** for video distribution because that is where its scale demands custom hardware.

## The criterion: cloud-scale operations

Chapter 4's rule of thumb for when repatriation makes sense (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Consider continuing to run workloads on premises or repatriating cloud workloads if you run a truly cloud-scale service. What is cloud scale? You might be at cloud scale if you are storing an exabyte of data or handling terabits per second of traffic to and from the internet.

Also: consider owning your servers **if data egress costs are a major factor** for your business.

Concrete candidate example from the book: Apple's iCloud storage. Apple could likely gain significant financial and performance advantage by migrating to its own servers.

## The slogan

Chapter 4's memorable framing:

> You are not Dropbox, nor are you Cloudflare.

For the vast majority of companies — not storing exabytes, not pushing terabits per second, without a highly integrated hardware/software differentiator — cloud is still the right default, and repatriation is not.

## Connection to TOCO

Cloud repatriation is an expensive form of [[total-opportunity-cost-of-ownership|TOCO]] being paid **back** — data-gravity made the original cloud decision sticky, and migrating off is the price of that stickiness. Chapter 4's advice to "have an escape plan" is aimed at keeping this price bounded.

## Related pages

- [[cloud]]
- [[on-premises]]
- [[hybrid-cloud]]
- [[data-gravity]]
- [[total-opportunity-cost-of-ownership]]
- [[opex-vs-capex]]
- [[technology-selection]]
- [[finops]]
