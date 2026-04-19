# On-Premises

**Summary**: Running data systems on hardware your company owns, in data centres you own or colocate. Reis and Housley's Chapter 4 treats on-prem as the default for established companies — still a valid choice in specific cases, but increasingly the exception rather than the rule.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## What on-prem means

Chapter 4 frames it concretely (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> Essentially, these companies own their hardware, which may live in data centers they own or in leased colocation space. In either case, companies are operationally responsible for their hardware and the software that runs on it.

Obligations that come with this:

- Repair or replace failed hardware.
- Manage upgrade cycles every few years as hardware ages.
- **Capacity plan for peaks** — an online retailer must have enough capacity to handle Black Friday load.
- For data engineers: buy systems large enough for peak performance and large jobs **without overbuying**.

## Established advantage

Chapter 4 is even-handed about the trade-off. Established companies often have (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Established operational practices** that have served them well — juggling cost, personnel, software environments, code deployment, database/big-data operations.
- **Known cost structure** — the [[opex-vs-capex|capex]] cycle, while inflexible, is predictable.

But they also see their competitors scaling rapidly with cloud-managed services. "Companies in competitive sectors generally don't have the option to stand still."

## Modern on-prem ≠ legacy on-prem

Chapter 4 notes the on-prem world is not frozen (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

> On-premises services are becoming more cloud-like and abstracted.

Companies staying on-prem increasingly adopt newer DevOps practices — containers, Kubernetes, microservices, continuous deployment — so their internal operations resemble cloud operations. A "new generation of managed hybrid cloud service offerings" (e.g., AWS Outposts, Google Cloud Anthos) lets customers locate cloud-managed servers inside their data centres.

## When on-prem is the right answer

Chapter 4's [[cloud-repatriation]] discussion is where the positive case for on-prem lives. Three rough signals (source: raw/fundamentals-of-data-engineering/chapter-04-choosing-technologies-across-the-data-engineering-lifecycle.md):

- **Cloud-scale operations.** Storing an exabyte of data or handling terabits per second of internet traffic. Dropbox, Backblaze, Cloudflare, Netflix's CDN. "You are not Dropbox, nor are you Cloudflare."
- **Data egress costs dominate.** If the bulk of your cost would be moving data out of the cloud, owning the servers can be much cheaper.
- **Highly integrated hardware+software.** When competitive advantage comes from engineering a custom stack (Dropbox's differential file-update system; Netflix's custom CDN), you need to own the hardware.

For normal workloads, Chapter 4 still recommends cloud-first.

## Related pages

- [[cloud]]
- [[hybrid-cloud]]
- [[cloud-repatriation]]
- [[opex-vs-capex]]
- [[technology-selection]]
- [[principles-of-good-data-architecture]]
