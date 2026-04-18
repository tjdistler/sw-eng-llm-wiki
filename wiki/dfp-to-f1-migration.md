# DFP-to-F1 Migration

**Summary**: Chapter 31's case study in SRE + product-development collaboration. DoubleClick for Publishers' main ad-serving database was migrated from MySQL to F1 while the serving system stayed untouched and the user experience was continuous. The SRE team drove the infrastructure design (extract-and-process over F1, feeding the unchanged serving system's index format), the product-development team owned the business-logic changes, weekly meetings synchronised the tracks, and the cutover was seamless.

**Sources**: `raw/site-reliability-engineering/chapter-31-communication-and-collaboration-in-sre.md`

**Last updated**: 2026-04-17

---

## The problem

DoubleClick for Publishers (DFP) is Google's tool for publishers to manage ads served on their websites and apps. The migration target was the **main database**, moving from **MySQL** to **F1** (source: chapter-31-communication-and-collaboration-in-sre.md; F1 is [Shu13]).

The chapter authors were responsible for a specific portion of the serving system (Figure 31-1): a pipeline that *"continually extracts and processes data from the database, in order to generate a set of indexed files that are then loaded and served around the world."* Scale:

- Distributed over several datacenters
- ~1,000 CPUs and 8 TB of RAM
- Indexes 100 TB of data per day

Constraints:

- Nontrivial migration — the database schema was significantly refactored and simplified, leveraging F1's ability to store and index protocol buffer data in table columns.
- Goal: the processing system produces output **perfectly identical** to the existing system. This allowed the serving system to remain untouched and the migration to be seamless from the user's perspective.
- Hard requirement: **live migration without any disruption of service to users at any time.**

## The collaboration structure

Chapter 31 uses this migration specifically to illustrate its [[sre-dev-collaboration|SRE-dev collaboration]] thesis. Key structural choices (source: chapter-31-communication-and-collaboration-in-sre.md):

### Early, joint involvement

*"From the start of the migration project, product development and SRE knew they would have to collaborate even more closely, conducting weekly meetings to sync on the project's progress."*

The weekly meeting is Chapter 31's specific recommendation — an ongoing [[production-meetings|production-meeting-style]] sync that keeps both tracks aligned.

### Division of expertise

- **Product development team**: more familiar with Business Logic (BL) and in closer contact with Product Managers / business need.
- **SRE team**: more expertise on infrastructure components (distributed-storage libraries, database libraries) — reuse across services accumulates caveats and nuances that let software run scalably and reliably over time.

### Infrastructure-first sequencing

Because BL changes were partially dependent on infrastructure changes, the project started with **the design of the new infrastructure**. **SREs drove that design** because they had extensive domain knowledge about extracting and processing data at scale. The design work covered:

- Extract tables from F1
- Filter and join data
- Extract only changed data (incremental) rather than the entire database each cycle
- Sustain loss of some machines without impacting the service
- Ensure resource usage grows linearly with the amount of extracted data
- Capacity planning

**Reusing a similar shape** to other services already extracting and processing data from F1 gave confidence in the solution's soundness and allowed reuse of parts of the monitoring and tooling.

### Design document and joint review

Before development, **two SREs produced a detailed design document**. Both teams thoroughly reviewed it, tweaked the solution to handle edge cases, and agreed on a design plan. The plan explicitly identified *what kind of changes the new infrastructure would bring to the BL*.

Example: the new infrastructure extracts only changed data (not the entire database) per run. The BL had to be updated to handle the new incremental-extraction model.

### Interface contract defined early

*"Early on, we defined the new interfaces between infrastructure and BL, and doing so allowed the product development team to work independently on the BL changes."* Similarly, the product development team kept SRE informed of BL changes. Where the two interacted (BL changes dependent on infrastructure), the weekly sync surfaced the dependency so it got handled quickly and correctly.

This is the chapter's concrete demonstration of the [[communication-and-collaboration-in-sre|API-as-contract]] metaphor for inter-team interfaces.

## Implementation and validation

### Test-environment deployment

Later in the project, SREs deployed the new service in a **testing environment that resembled the project's eventual production environment**. This was essential to measure expected service behaviour — in particular, **performance and resource utilisation** — while BL development was still underway.

### Validation by output comparison

Product development used the testing environment to validate the new service: *"the index of the ads produced by the old service (running in production) had to match perfectly the index produced by the new service (running in the testing environment)."*

### Iterative edge-case resolution

Validation highlighted discrepancies between the old and new outputs (due to edge cases in the new data format). The product development team resolved them iteratively: debug the cause of each difference, fix the BL that produced the bad output, repeat.

### Production preparation

In the meantime, the SRE team prepared the production environment (source: chapter-31-communication-and-collaboration-in-sre.md):

- Allocated necessary resources in a different datacenter
- Set up processes and monitoring rules
- Trained the engineers designated to be on-call for the new service
- Set up a basic **release process that included validation** — a task usually handled by product development or Release Engineers, but here owned by SREs to speed up the migration

### Rollout

When the service was ready, SREs prepared a **rollout plan in collaboration with the product development team** and launched the new service. *"The launch was very successful and proceeded smoothly, without any visible user impact"* (source: chapter-31-communication-and-collaboration-in-sre.md).

## What the case study demonstrates

The migration hits every Chapter 31 recommendation for SRE-product-development collaboration:

| Recommendation | Realisation in DFP-to-F1 |
|---|---|
| Collaborate from the design phase onward | SRE drove infrastructure design before BL work began |
| Weekly meetings to sync | Explicit project-long practice |
| Design doc authored and jointly reviewed | Two SREs wrote it, both teams reviewed, solution tweaked |
| Define inter-team interfaces early | Infrastructure-BL interface defined to enable parallel work |
| SRE expertise on infrastructure, dev on BL | Explicit division reflected in ownership |
| Monitoring and tooling reuse | Built on existing F1-adjacent services |
| Release process owned by SRE where speed warranted | SREs ran the release+validation pipeline |
| Rollout plan jointly prepared | Joint effort, seamless cutover |

## Comparison to other large migrations in the wiki

The DFP-to-F1 migration is an example of the joint-SRE-dev shape; it contrasts with:

- **Monolith-to-microservice migrations** ([[incremental-migration]], [[strangler-fig-pattern]], [[parallel-run-pattern]]) — Newman's catalogue for gradually re-homing functionality. The DFP validation approach (output match between old and new) is structurally a [[parallel-run-pattern|parallel run]] over index outputs, validating semantic equivalence before cutover.
- **Database split migrations** ([[split-the-database-first]], [[synchronize-data-in-application]], [[tracer-write]]) — Newman's patterns for splitting one database schema into many. DFP-to-F1 is the opposite direction: migrating to a new (more capable) single database.
- **Stream-based change-data-capture integrations** ([[change-data-capture]], [[outbox-table-pattern]]) — an alternative mechanism that could have fed the indexing pipeline directly from F1 changes. The chapter doesn't use the term CDC, but the "extract only changed data" discipline is structurally the same idea.

## Related pages

- [[sre-dev-collaboration]]
- [[communication-and-collaboration-in-sre]]
- [[production-meetings]]
- [[spanner]]
- [[parallel-run-pattern]]
- [[change-data-capture]]
- [[release-engineering]]
- [[launch-coordination-engineering]]
- [[capacity-planning]]
