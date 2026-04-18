# Traditional Capacity Planning

**Summary**: The demand-driven, spreadsheet-assisted capacity-planning cycle that prevailed across industry as of Chapter 18's writing — and the four structural problems with it that motivated Google's move to [[intent-based-capacity-planning]]. Understanding this is a precondition for understanding why [[auxon|Auxon]] was worth building.

**Sources**: `raw/site-reliability-engineering/chapter-18-software-engineering-in-sre.md`

**Last updated**: 2026-04-17

---

## The cycle

Traditional capacity planning is a neverending cycle with four phases (source: chapter-18-software-engineering-in-sre.md):

1. **Collect demand forecasts** — how many resources are needed, when, and where? Uses today's best data to predict quarters or years into the future.
2. **Devise build and allocation plans** — given the forecast, what's the best way to meet demand with additional supply? How much supply, and in which locations?
3. **Review and sign off on the plan** — is the forecast reasonable? Does it align with budget, product-level, and technical constraints?
4. **Deploy and configure resources** — once resources arrive (possibly in phases), which services get them? How do lower-level resources (CPU, disk) get turned into something useful for services?

The cycle never ends because assumptions change, deployments slip, and budgets get cut — every revision cascades into every subsequent quarter's plan.

## The four problems

Chapter 18 enumerates four structural weaknesses of this approach (source: chapter-18-software-engineering-in-sre.md).

### Brittle by nature

Traditional planning uses **demand as the key driver** and manually reshapes supply to fit. Any seemingly minor change can invalidate the plan:

- A service gets less efficient and needs more resources for the same demand
- Customer adoption accelerates, raising projected demand
- Delivery of a new cluster slips
- A product decision changes a service's deployment shape

Minor changes force cross-checking the entire allocation plan. Larger changes (delayed resource delivery, product strategy shifts) force rebuilding it from scratch. A slip in one cluster perturbs redundancy and latency planning across multiple services, which perturbs resource allocations in other clusters, which perturbs downstream quarters.

### Laborious

Collecting the data needed for demand forecasts is slow and error-prone for most teams. Mapping constrained resource requests into allocations from available capacity is equally slow — bin-packing by hand is tedious and doesn't yield good solutions.

### Imprecise

Two sources of imprecision compound:

- **Not all resources are equivalent**. If latency rules require North American users to be served from North America, supply in Asia doesn't help a North American shortfall. The mapping from "resources needed" to "resources available that would actually work" has constraints the traditional process handles poorly.
- **Bin-packing is NP-hard**, and humans can't solve it by hand. The result is approximate at best.

### Loses intent

When a service owner asks for "X cores in cluster Y", the *reason* for X and Y — and any flexibility around those numbers — is lost by the time the request reaches someone trying to fit it into available supply. The planner sees an inflexible demand; the requester's degrees of freedom are invisible. This loss is the cornerstone of the argument for intent-based planning.

## Tooling failures

Compounding the four problems, the tools used are typically inadequate (source: chapter-18-software-engineering-in-sre.md):

- **Spreadsheets** — scalability problems, limited error-checking, data goes stale, changes are hard to track
- **Simplification pressure** — teams are forced to simplify requirements and assumptions just to keep the problem tractable, which degrades the plan's quality even before the structural issues bite

The net outcome: massive human effort producing an approximate bin-packing that is brittle to change, with no known bounds on optimality.

## Why this matters

Understanding the four weaknesses is the setup for Chapter 18's move to [[intent-based-capacity-planning]]. Each of the four is directly addressed by the new approach:

| Problem (traditional) | Fix (intent-based) |
|---|---|
| Brittle to change | Regenerate the plan programmatically |
| Laborious | Computers do the bin-packing |
| Imprecise | Solvers reach known-optimal solutions |
| Loses intent | Intent is the input, not the output |

## Cross-book connections

- [[capacity-planning]] — Chapter 1's tenet implicitly assumes one of these two approaches; Chapter 18 makes the choice explicit
- [[architecture-decision-record]] (Richards & Ford) — choosing between traditional and intent-based planning is an architectural decision with quarter-scale consequences; worth recording

## Related pages

- [[intent-based-capacity-planning]]
- [[auxon]]
- [[software-engineering-in-sre]]
- [[capacity-planning]]
