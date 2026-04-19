# Web Scraping

**Summary**: Automatically extracting data from web pages by parsing their HTML. Widespread in practice and a legitimate [[data-ingestion|ingestion]] option when no better source exists — but Reis and Housley frame it as a "murky area where ethical and legal lines are blurry" and one where the maintenance burden (HTML structure changes, rate-limiting, bans) often outweighs the value of the data.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## What it is

"Web scraping automatically extracts data from web pages, often by combing the web page's various HTML elements." Typical use cases (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- Scraping e-commerce sites to extract product pricing information.
- Scraping news sites for a news aggregator.

Ch 7 frames scraping as "widespread" — something the data engineer is likely to encounter — and worth handling carefully rather than dismissively.

## Three cautions before scraping

Reis and Housley's top-level advice has three points (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

### 1. Ask whether you should be scraping at all

"Ask yourself if you should be web scraping or if data is available from a third party." Official data feeds, APIs, and [[data-sharing|data-sharing]] subscriptions are often available and preferable. Scraping is the fallback, not the default.

### 2. Be a good citizen

"Don't inadvertently create a denial-of-service (DoS) attack, and don't get your IP address blocked. Understand how much traffic you generate and pace your web-crawling activities appropriately. Just because you can spin up thousands of simultaneous Lambda functions to scrape doesn't mean you should; excessive web scraping could lead to the disabling of your AWS account."

This is practical as well as ethical — aggressive scraping causes real downtime for the target, and cloud providers will shut down accounts that are behaving badly toward third parties.

### 3. Legal implications

"Actions that violate terms of service may cause headaches for your employer or you personally." DoS-adjacent behaviour can carry legal consequences. The legal landscape around scraping is genuinely unsettled (this book's framing pre-dates recent case law but the caution still stands); get counsel involved before anything at scale.

## The maintenance tax

"Web pages constantly change their HTML element structure, making it tricky to keep your web scraper updated. Ask yourself, is the headache of maintaining these systems worth the effort?" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

A scraper against a site you don't control is **perpetually subject to silent breakage** — a new deploy at the target can move an element or change a class name, and the pipeline starts returning empty or wrong data. Monitoring for this is harder than monitoring an API because the scraper often succeeds at the HTTP level while failing at extraction.

## Architecture implications downstream

Ch 7 highlights that web scraping has interesting implications for what happens **after** ingestion (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Minimal-field pattern.** Pull required fields from the scraped HTML with Python, write them to a database. Cheap, but any new use case may require re-scraping.
- **Full-HTML pattern.** Store the complete HTML of every scraped page and process it later with Spark or similar. Expensive to store, but preserves every field for future reprocessing.

"These decisions may lead to very different architectures downstream of ingestion." In the framing of the [[data-engineering-lifecycle|lifecycle]], this is a Ch 7 example of how ingestion choices force architectural decisions across later stages.

## Connection to the rest of the wiki

- When scraping is unavoidable, the scrape pipeline usually feeds [[object-storage]] with raw HTML pages, then a transformation stage parses and shapes them for the warehouse. This is a concrete form of [[etl-vs-elt|ELT]] — load raw first, transform later.
- The "is this data available via [[data-sharing]] or a third-party API?" check is part of the same discipline FoDE pushes throughout: prefer managed, standard, low-maintenance sources over bespoke plumbing.

## Related pages

- [[data-ingestion]]
- [[third-party-api-integration]]
- [[data-sharing]]
- [[object-storage]]
- [[etl-vs-elt]]
