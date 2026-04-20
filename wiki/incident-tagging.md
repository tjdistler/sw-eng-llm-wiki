# Incident Tagging

**Summary**: Chapter 16 names **tagging** — free-form single-word metadata attached to notifications at any level — as *probably the Outalator's most useful unique feature*. Tags replace a predetermined list of categories with emergent, team-specific vocabularies that converge on hierarchical namespaces (`cause:network:switch`, `bug:76543`, `customer:132456`, `bogus`) through usage. The resulting metadata is what makes [[outage-analysis|analysis]] and cross-team comparison possible without forcing every team to pre-register every category they'll ever need.

**Sources**: `raw/site-reliability-engineering/chapter-16-tracking-outages.md`

**Last updated**: 2026-04-17

---

## The design choice

Chapter 16 frames tagging as a deliberate choice to *avoid a predetermined list* (source: chapter-16-tracking-outages.md):

> Of course, some tags are typos ("cause:netwrok") and some tags aren't particularly helpful ("problem-went-away"), but avoiding a predetermined list and allowing teams to find their own preferences and standards will result in a more useful tool and better data.

The argument: a centrally-curated tag taxonomy has two costs.

- Teams must argue about the taxonomy before they can use it.
- The taxonomy can't keep up with emergent categories (new failure modes, new customers, new infrastructure).

Free-form tagging trades **typos and noise** for **adoption and adaptability**. The noise is a smaller problem than the adoption friction of a committee-managed tag list would be.

## Colon-namespaced tags

Chapter 16 notes one piece of structure Outalator does enforce: **colons are interpreted as semantic separators**, subtly promoting hierarchical namespaces (source: chapter-16-tracking-outages.md). Examples:

- `cause:network` vs `cause:network:switch` vs `cause:network:cable` — teams pick the depth they need.
- `action:rolled-back`, `action:hotfix`.
- `customer:132456` — for teams with per-customer incident patterns.
- `bug:76543` — parsed as a link into the bug tracker.

The prefixes aren't hardcoded. Outalator maintains a **team-specific suggested-tag list generated from historical usage**; so `customer:` suggestions appear for teams that use customer IDs, but not for teams that don't.

## The suggested-prefix feedback loop

Two prefixes Chapter 16 singles out as primary:

- `cause:` — what triggered the incident.
- `action:` — what was done about it.

These appear across teams because almost every on-call rotation eventually wants to answer "what caused the last N incidents?" and "what did we do about them?" Tags are the data that makes those questions answerable.

Other prefixes emerge per team. The mechanism (suggested prefixes based on historical usage) means that teams that start with no taxonomy converge on one organically, driven by what their own recent incidents have been tagged with.

## Bogus: the false-positive tag

Chapter 16 calls out one specific single-word tag (no namespace) as widely used:

> "bogus" is widely used for false positives.

This pairs with the incident-vs-alert distinction from [[incident-aggregation]]. Alerts that fire but don't correspond to a real incident get tagged `bogus` so they can be excluded from actionable-alert counts and included in noise-ratio counts. Tagging `bogus` is cheaper than deleting the record, and preserving the data enables later analysis of monitoring noise patterns.

## What tagging enables

Even without any formal analysis pipeline, Chapter 16 argues, tagging pays off (source: chapter-16-tracking-outages.md):

> Overall, tags have been a remarkably powerful tool for teams to obtain and provide an overview of a given service's pain points, even without much, or even any, formal analysis. As trivial as tagging appears, it is probably one of the Outalator's most useful unique features.

Concrete uses:

- **Filtered queries** — "show me every incident tagged `cause:network` this quarter" directly answers "is the network a problem?"
- **Weekly review inputs** — the [[outage-analysis|weekly production review]] filters on tags to surface patterns worth discussing.
- **Cross-team comparisons** — if two teams both use `cause:bigtable-replication-delay`, aggregating across them exposes an infrastructure problem neither team alone would have flagged.
- **Automatic link expansion** — `bug:76543` becomes a clickable link into the bug tracker, giving the record navigational affordances without requiring structured fields.

## Why tagging beats structured fields

A common alternative design is **structured metadata fields** — a form with "root cause category," "customer ID," "action taken," each with a dropdown. Tagging wins on three counts:

- **Low friction.** Type a word. No form to fill out.
- **Emergent vocabulary.** The taxonomy is discovered, not pre-specified.
- **Any-level attachment.** Tags can attach to individual notifications, to incidents, to annotations — structured fields would require schema decisions for each level.

The trade-off is data quality: typos (`cause:netwrok`) and unhelpful tags (`problem-went-away`) exist. Chapter 16's position is explicit: the trade is worth it.

## Related pages

- [[outage-tracking]]
- [[incident-aggregation]]
- [[outage-analysis]]
- [[alert-philosophy]]
- [[postmortem-template]]
- [[site-reliability-engineering]]
