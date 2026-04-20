# Remove Google-specific pages and inbound links

## Context

The wiki is intended to be cloud-platform and company-agnostic. Twenty-four concept pages describe Google-internal systems (Borg/Borgmon, Stubby, Blaze, BNS, GFE, Jupiter, B4, Auxon, Midas, Sisyphus, Outalator, Viceroy, etc.) that don't generalise. They were left out of the MOC layer in Phase 13, but remain on disk and are still cited by ~124 other wiki pages.

This plan removes those 24 pages *and* all inbound `[[wikilinks]]` to them. The general concepts they sit next to (monitoring, RPCs, release engineering, load balancing, etc.) already have dedicated non-Google pages and MOC coverage, so no generalisation work is required — the Google citations are worked-example scaffolding that can be dropped.

**Raw book chapters stay untouched.** `raw/site-reliability-engineering/*.md` still discusses Borg, Borgmon, Stubby, etc. because those are the book's own worked examples and `raw/` is immutable.

## Scope

### Pages to delete (24)

| Page | Subject | Inbound links |
|---|---|---|
| `auxon.md` | Google's intent-based capacity-planning system | 17 |
| `b4-network.md` | Google's private WAN backbone | 5 |
| `blaze-bazel.md` | Blaze (internal) / Bazel (open-sourced) build system | 9 |
| `bns.md` | Borg Naming Service | 9 |
| `borgmon.md` | Google's monitoring system | 23 |
| `borgmon-rules.md` | Borgmon's rules language | 14 |
| `dfp-to-f1-migration.md` | DoubleClick-to-F1 migration case study | 4 |
| `escalator.md` | Google's alert-escalation tool | 7 |
| `google-frontend.md` | Google Frontend (GFE) | 9 |
| `google-monorepo.md` | Google's Piper/internal monorepo | 11 |
| `google-music-runaway-deletion.md` | Google Music incident | 11 |
| `jupiter-network.md` | Google datacenter network fabric | 6 |
| `midas-package-manager.md` | Google's MPM | 9 |
| `mysql-on-borg.md` | Running MySQL on Borg case study | 9 |
| `outalator.md` | Google's outage-aggregator tool | 13 |
| `postvitam.md` | Google's incident/retrospective tool | 6 |
| `prodtest.md` | Google's production-testing framework | 7 |
| `production-guide.md` | Internal production-guide artifact | 6 |
| `shakespeare-example-prr.md` | Shakespeare-service PRR worked example | 4 |
| `sisyphus.md` | Google's release-push tool | 14 |
| `stubby.md` | Google's internal RPC system | 21 |
| `time-series-arena.md` | Borgmon time-series storage | 10 |
| `varz-endpoints.md` | Google's `/varz` metrics handler | 10 |
| `viceroy-case-study.md` | Viceroy internal case study | 5 |

Total inbound wikilinks across the 24 pages: **~230**.

### Linking pages to edit (~124 unique)

Every page that contains a `[[google-page]]` or `[[google-page#anchor]]` wikilink needs review. The full set is the union of all `grep`-listed pages per target; representative high-density linkers include:

- `site-reliability-engineering.md` — the book summary; cites nearly every one of the 24 pages across its chapter summaries.
- Monitoring cluster: `monitoring-and-observability.md`, `monitoring-topology-sharding.md`, `alertmanager.md`, `alert-philosophy.md`, `four-golden-signals.md`, `black-box-vs-white-box-monitoring.md`, `sre-monitoring-outputs.md`, `making-troubleshooting-easier.md`, `prometheus-connection.md`.
- Release/build cluster: `release-engineering.md`, `release-simplicity.md`, `release-policy-enforcement.md`, `release-branching-and-cherry-picking.md`, `rapid-release-system.md`, `push-on-green.md`, `hermetic-builds.md`, `configuration-management-sre.md`, `change-management-sre.md`, `continuous-integration-delivery-deployment.md`.
- Load balancing / networking cluster: `frontend-load-balancing.md`, `datacenter-load-balancing.md`, `network-load-balancer.md`, `gslb.md`, `virtual-ip-address.md`, `packet-encapsulation-load-balancer.md`, `life-of-a-request.md`, `service-discovery.md`, `service-framework.md`, `connection-level-load.md`, `google-datacenter-topology.md`, `software-defined-networking.md`.
- RPC / backend cluster: `rpc.md`, `protocol-buffers.md`, `encoding-formats.md`, `backend-task-states.md`, `lame-duck-state.md`, `deadline-propagation.md`, `latency-and-deadlines.md`, `request-criticality.md`, `handling-overload.md`, `subsetting.md`, `health-probes.md`.
- Incident / outage cluster: `incident-aggregation.md`, `incident-tagging.md`, `learning-from-outages.md`, `outage-tracking.md`, `outage-analysis.md`, `postmortem-philosophy.md`, `cascading-failure-triggers.md`, `recovery-testing.md`.
- Capacity / automation cluster: `capacity-planning.md`, `intent-based-capacity-planning.md`, `traditional-capacity-planning.md`, `automation-at-google.md`, `autonomous-systems.md`, `hierarchy-of-automation-classes.md`, `cluster-turnup-automation.md`.
- Data-integrity cluster: `data-integrity-sre.md`, `data-integrity-principles.md`, `gmail-gtape-restore.md`, `testing-disaster-recovery.md`, `tiered-backup-strategy.md`, `soft-deletion.md`, `replication.md`.
- SRE-practice cluster: `sre-tenets.md`, `sre-discipline.md`, `sre-product-adoption.md`, `sre-alternative-support.md`, `sre-dev-collaboration.md`, `sre-software-development-lessons.md`, `sre-monitoring-outputs.md`, `software-engineering-in-sre.md`, `fostering-software-engineering-in-sre.md`, `communication-and-collaboration-in-sre.md`, `cross-site-project-recommendations.md`, `cross-sre-collaboration.md`, `embedding-sre.md`, `engineering-work-categories.md`, `operational-overload.md`, `toil-and-engineering-balance.md`.
- PRR cluster: `prr-analysis-phase.md`, `prr-continuous-improvement.md`, `prr-onboarding-phase.md`, `simple-prr-model.md`, `launch-checklist-themes.md`.
- Miscellaneous: `chubby.md`, `borg.md`, `mttr-and-mttf.md`, `pipeline-monitoring-problems.md`, `pipeline-batch-scheduling-drawbacks.md`, `queries-per-second-pitfalls.md`, `service-level-indicator.md`, `time-series-database.md`, `canary-test.md`, `gradual-rollout.md`, `reliable-product-launches.md`, `network-access-security.md`, `leading-questions.md`, `explaining-reasoning.md`, `weighted-round-robin.md`, `simple-round-robin.md`.
- `wiki/index.md` — A–Z appendix entries for all 24 pages.

Pages that link Google-pages-to-each-other (e.g. `borgmon.md` links to `borgmon-rules.md`) will be deleted in the same pass, so their internal links don't need separate editing.

## Approach

Each inbound reference is one of three shapes. The editing action differs per shape.

1. **Worked-example scaffolding.** The sentence says *"X. Google's implementation is [[stubby]]."* The action is to delete the second sentence outright.
2. **Example-in-parenthesis.** The sentence says *"X is implemented via RPC ([[stubby]], gRPC)."* The action is to drop the `[[stubby]]` token and keep the rest.
3. **Load-bearing citation.** The sentence uses the Google page as the referent, not just an example: *"[[outalator]] is the tool for aggregating alerts."* The action is to rewrite the sentence to use the general concept (e.g. *"An alert aggregator"* or drop the sentence if the surrounding prose already makes the point).

The `site-reliability-engineering.md` book summary is the one page likely to need a structural rewrite rather than sentence-level edits — it currently sequences chapter summaries via Google-example citations. Expect a handful of chapter summaries to shrink; the book summary's job is to point readers at chapters, not to re-tell the chapters.

## Phasing (~6 commits)

Group edits by the cluster that cites the Google pages, so a reviewer can evaluate each cluster's prose coherence after the rewrite.

### Phase 1 — Delete the 24 pages

**Files**: the 24 pages in *Pages to delete* above.  
Rename-free `rm`. The wiki immediately has ~230 broken `[[wikilinks]]`, which the linter turns into errors. Phases 2–5 fix them.  
**Do not ship Phase 1 alone** — the linter is red until Phase 5 lands.  
**Commit**: 1.

### Phase 2 — Fix `site-reliability-engineering.md`

**Files**: `wiki/site-reliability-engineering.md`.  
By far the densest linker. Rewrite chapter summaries that over-indexed on Google examples so they foreground the general concepts. Cross-check against `raw/site-reliability-engineering/` chapter files to confirm nothing load-bearing is lost; the general concepts are preserved elsewhere (e.g. `monitoring-and-observability`, `release-engineering`, `handling-overload`).  
**Review**: the book summary still reads as a serviceable overview, not a thinned-out shell.  
**Commit**: 1.

### Phase 3 — Fix cluster linkers in batches

**Files**: the linking-page clusters listed under *Linking pages to edit* above. Group edits by cluster so the reviewer can read prose coherence per commit.

Suggested batching (one commit per cluster):

- **3a**: Monitoring cluster (~10 pages).
- **3b**: Release/build cluster (~10 pages).
- **3c**: Load-balancing + RPC clusters (~15 pages).
- **3d**: Incident/outage + capacity/automation + data-integrity clusters (~20 pages).
- **3e**: SRE-practice + PRR + miscellaneous (~25 pages).

Per-page editing rule: apply the three-shape rule from *Approach*. Keep prose terse; most Google references will cleanly compress to a zero-width removal.  
**Commits**: 5.

### Phase 4 — Fix `wiki/index.md` appendix

**Files**: `wiki/index.md`.  
Delete the 24 A–Z appendix entries for the removed pages.  
**Commit**: 1 (can be rolled into Phase 5 commit if trivial).

### Phase 5 — Verification gate

Run `cd wiki-linter && uv run python lint.py ../wiki` — zero errors, zero orphan warnings.  
Spot-check 3–4 concept pages whose prose was edited to confirm it still reads cleanly.  
Append an entry to `wiki/log.md` summarising the removal.  
**Commit**: log entry only.

## Risks and edge cases

- **Broken builds mid-series.** Phases 1–4 must land together or as adjacent commits on the same branch. The linter is red between them. Avoid pushing to `main` until Phase 5 is green.
- **Raw-file pointers.** Some Google concept pages are cited via `[[book-name#chapter-N-title]]` *anchors* that resolve against book summary headings, not against the Google page. These are anchor links and won't break when the 24 pages are deleted. No action needed.
- **Hollowed-out concept pages.** A couple of pages whose body is majority Google-example may be worth a second look after deletion — if more than half the prose goes, consider whether the page still earns its keep. Examples to watch: `google-datacenter-topology.md` (links three Google pages), `gmail-gtape-restore.md`, `cluster-turnup-automation.md`. If a page becomes a stub, delete it too and extend the phase.
- **No new content is required.** The general concepts (RPCs, monitoring, capacity planning, build systems, naming services, release tooling) already have their own concept pages in the wiki. Nothing needs to be written to replace the removed pages.

## Not in scope

- **Rewriting `raw/` files.** Immutable per the wiki convention.
- **Generalising any Google page into a replacement concept page.** The 24 pages are redundant with existing concept pages; no "outage aggregator" or "protobuf-over-generic-RPC" page needs to be written.
- **Removing Google-*examples* embedded inside general concept pages.** This plan removes only the 24 Google-specific *pages* and links *to* them. Inline prose like *"e.g. Google uses Borg"* inside a general page is out of scope — it's example-grounding, not company-specific scaffolding.
