# UI Composition

**Summary**: Migrating to [[microservices]] by splicing together a user interface from old and new sources at the page, widget, or component level. Lets you ship vertical slices of functionality served partly by the existing monolith and partly by new services, often with brand-new look-and-feel for the migrated parts.

**Sources**: `raw/monolith-to-microservices/chapter-03-splitting-the-monolith.md`

**Last updated**: 2026-04-16

---

## Why composition matters

Most migration patterns push the work to the server side. UI composition opens a complementary front: it lets you migrate user-visible vertical slices independently, and (especially with widget composition) lets multiple backend services contribute to a single screen (source: chapter-03-splitting-the-monolith.md).

Newman draws on his work helping move The Guardian's website off its old CMS onto a new Java platform — a migration done vertical by vertical (Travel, News, Culture, …). REA Group in Australia uses page composition because each channel (residential, commercial) has its own brand and team.

## Three styles

### Page composition

Each migrated *page* is served from the new system; the rest from the old. URL routing decides which. The Guardian used this approach: visitors saw a different look-and-feel when they navigated to migrated verticals, and old URLs were carefully redirected to new locations. Years later, when migrating away from the Java monolith, The Guardian used the Fastly CDN to do the routing — effectively the CDN played the role of the in-house proxy (source: chapter-03-splitting-the-monolith.md).

Page composition fits well when (source: chapter-03-splitting-the-monolith.md):

- Distinct teams can own whole sections end-to-end.
- The look-and-feel can legitimately differ between sections.
- Routing rules are URL-based and simple.

### Widget composition

A page is assembled from multiple widgets, each potentially served by a different service. The Guardian's first migration step was a *single widget* embedded in the old Travel pages: a Top 10 Destinations component, served by the new system and spliced in via Apache Edge-Side Includes (ESI). This let the team ship something live, learn from production, and limit blast radius (source: chapter-03-splitting-the-monolith.md).

Modern variants do widget composition in the browser rather than at the edge. Each widget loads independently, so a single widget's backend going down only degrades that widget — the rest of the page still renders.

Orbitz (now part of Expedia) had its UI broken into "modules" (search form, booking form, map, etc.) served by a Content Orchestration service. The Orchestration service became a bottleneck of contention across teams. Orbitz migrated module-by-module to dedicated backing services, which was easier because the modules already had clean ownership lines (source: chapter-03-splitting-the-monolith.md). This is a textbook example of the Delivery Contention problem (see [[independent-deployability]]).

### Micro frontends

The newer term for widget composition specifically inside single-page-application frameworks (Vue, React, Angular). The Web Components specification has tried to standardise this but adoption has lagged. Real-world micro-frontend implementations are largely about making different SPA frameworks coexist on one page without dependency clashes (source: chapter-03-splitting-the-monolith.md).

## Mobile

Native iOS and Android apps complicate UI migration: each release must pass app-store review, and the app itself is a deployment monolith. Many organisations work around this by driving UI from the server side — embedded web views, or more sophisticated approaches like Spotify's component-driven UI where layouts are described declaratively on the server and rendered by the native app. This lets Spotify experiment with new layouts without a new app submission (source: chapter-03-splitting-the-monolith.md).

## When to use it

UI composition is highly effective for re-platforming when (source: chapter-03-splitting-the-monolith.md):

- The existing UI can be modified to host new components, or routed away from at the page level.
- The chosen UI technology supports composition (a "good old-fashioned website" makes this easy; SPAs make it harder).
- Vertical slices have clean ownership.

It is *not* a server-side migration substitute — it complements server-side patterns.

## Related pages

- [[strangler-fig-pattern]]
- [[independent-deployability]]
- [[migration-pattern-selection]]
- [[incremental-migration]]
- [[reorganizing-teams]]
