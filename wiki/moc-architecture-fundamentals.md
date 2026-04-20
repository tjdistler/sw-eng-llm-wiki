# MOC: Architecture Fundamentals

**Summary**: Entry point for questions about what software architecture *is* — its definition, its first principles, the architect's stance, the "-ilities" that drive every concrete design decision, and the trade-off discipline that runs through everything else in the wiki. Start here when the question is "how should I think about this design?" rather than "which pattern do I pick?"

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You are about to make an architectural decision and want to ground it in the discipline rather than in the pattern catalogue. Or someone has handed you a green-field design and you need to figure out *what to even decide first*. Or you're trying to articulate why one design beats another and "I just like it better" isn't going to fly.

This MOC is the layer beneath every other MOC. The decomposition MOC tells you *how* to split a monolith; this one tells you *what makes a split a good architectural decision*. The architecture-styles MOC catalogues the canonical shapes; this one tells you what dimensions to score them on. Read this first if you've never had a clear answer to "what is the architect actually responsible for, and how do you tell whether they've done it well?"

The canonical shape of a question that lands here: *"How should I think about X?"*, *"How do I decide between A and B when both 'work'?"*, *"What architectural characteristics matter for this domain?"*, *"How do I tell if my architecture is decaying?"* The answer is rarely a pattern — it's a frame.

## What software architecture even is

Before anything else, get the definition straight. Most disagreements about architecture are disagreements about scope.

- [[software-architecture-definition]] — Richards and Ford's four-part definition: structure (the styles), characteristics (the -ilities), decisions (the rules), design principles (the guidelines). Architecture is *all four* — collapse any one into "design" and the conversation goes sideways. Read this before reading anything else in this MOC.
- [[architecture-versus-design]] — why the architecture-then-design handoff fails (no feedback loop, no shared accountability) and what bidirectional collaboration looks like instead. The structural reason "throw it over the wall" produces worse outcomes than "stay engaged."
- [[laws-of-software-architecture]] — the two laws that frame every later trade-off: (1) everything in software architecture is a trade-off; (2) *why* you did something matters more than *how* you did it. Internalise both before reaching for any pattern.
- [[trade-off-analysis]] — Hickey's "architecture is the stuff you can't Google"; the auction-system worked example showing why the obvious answer is rarely the best answer once you weigh the negatives. The discipline that operationalises Law 1.
- [[least-worst-trade-offs]] — *Hard Parts*'s sharper restatement: don't search for the best architecture, search for the least-worst one. The architect-as-objective-arbiter framing that keeps you out of pattern-evangelism traps.
- [[mece-principle]] — Mutually Exclusive, Collectively Exhaustive option enumeration; the discipline that prevents the trade-off analysis from being a comparison between three flavours of the same idea. Useful any time you catch yourself between exactly two options.
- [[unknown-unknowns]] — Rumsfeld's framing applied to architecture: you cannot know upfront what you will discover the system needs. The argument for *iterative* architecture and against the up-front-perfect mindset.
- [[architectural-thinking]] — the architect's cognitive stance: architecture-vs-design, breadth-over-depth, trade-off framing, business-driver alignment. The four lenses you switch between as you work.

Deeper reading: [[fundamentals-of-software-architecture#chapter-1-introduction]] and [[fundamentals-of-software-architecture#chapter-2-architectural-thinking]].

## The architect's stance and skill profile

Architecture is a role discipline as much as a technical one. The shape of what you spend your day on, what you read, and how you communicate matters as much as what diagrams you draw.

- [[architect-expectations]] — Richards and Ford's eight behavioural expectations placed on any architect regardless of title. The job description that sits behind every "what should I be doing?" question.
- [[technical-breadth-vs-depth]] — the three-tier knowledge pyramid (stuff you know, stuff you know you don't know, stuff you don't know you don't know); why architects optimise for *breadth*, not depth, and how the "frozen caveman" anti-pattern emerges when they don't refresh either side.
- [[architect-role-intersections]] — architecture now intersects engineering practices, ops/DevOps, process, and data. Why "the architect just designs, engineers build" hasn't been true for a decade.
- [[balancing-architecture-and-coding]] — the bottleneck trap (architects who don't code lose touch; architects who write production code become single-points-of-failure) and the techniques for staying hands-on without becoming the bottleneck.
- [[architectural-checklists]] — when checklists work for architecture (high-stakes, high-coverage, infrequent procedures) and when they don't (creative design work). Gawande's *Checklist Manifesto* applied to release / unit-test / code-completion lists; the Hawthorne effect as the governance mechanism.

Deeper reading: [[fundamentals-of-software-architecture#chapter-2-architectural-thinking]] for the stance; [[fundamentals-of-software-architecture#chapter-22-making-teams-effective]] and the wider [[moc-risk-and-communication]] for the people-side practices that don't fit on this MOC.

## Architecture characteristics — the "-ilities" as first-class

Characteristics are the dimension architecture optimises along. Without them, "I picked microservices" is a pattern citation, not a justification.

- [[architecture-characteristics]] — the "-ilities" introduced as a first-class architectural dimension; the three-criteria test (non-domain / structurally influential / critical or important to success); the operational/structural/cross-cutting taxonomy; the *least-worst-architecture principle* that no design maximises every characteristic.
- [[identifying-architecture-characteristics]] — three sources (explicit domain concerns, explicit requirements, implicit domain knowledge); the domain-to-ility translation; the consensus-of-three rule; the *drop-one* sharpening exercise; the Vasa cautionary tale of over-specification.
- [[measuring-architecture-characteristics]] — objective definition as the prerequisite to governance; the three measurement axes (operational, structural, process); performance budgets, K-weight budgets, coverage and pipeline metrics. *If you can't measure it, you can't govern it; if you can't govern it, it isn't really a characteristic — it's an aspiration.*
- [[architectural-quantum]] — the independently-deployable unit with high functional cohesion and synchronous connascence; the *scope* at which a characteristic actually applies. A system can have multiple quanta, each with its own characteristic profile (auction-bidding quantum strict-real-time; bid-history quantum eventually-consistent). Read this before claiming a system "has" any characteristic.
- [[maintainability]] — the ease of adding, changing, and removing features over a system's lifetime. The characteristic that compounds: a system easy to maintain on year one is still evolvable on year five; a system hard to maintain early ossifies into the thing nobody wants to touch. Often an implicit characteristic discovered only when it's missing.
- [[architecture-decisions-vs-design-principles]] — the hard-and-fast-rules vs guidelines distinction; the architecturally-significant test; the five factors that make a decision worth recording. Characteristics drive decisions; design principles guide everything else.

Deeper reading: [[fundamentals-of-software-architecture#chapter-4-architecture-characteristics-defined]], [[fundamentals-of-software-architecture#chapter-5-identifying-architectural-characteristics]], [[fundamentals-of-software-architecture#chapter-6-measuring-and-governing-architecture-characteristics]], and [[fundamentals-of-software-architecture#chapter-7-scope-of-architecture-characteristics]] for the quantum.

## Modularity, complexity, and the structural metrics

Architecture characteristics include the implicit structural ones. They don't appear on a requirements doc; they appear in the costs everyone pays later.

- [[modularity]] — Richards and Ford's umbrella for the logical grouping of related code; the implicit characteristic; the three measurement tools (cohesion, coupling, connascence) that turn "well-organised" from an aesthetic into a measurable property.
- [[cyclomatic-complexity]] — McCabe's 1976 metric (E − N + 2); the under-10 rule of thumb (under-5 preferred); Crap4J as the complexity-plus-coverage product; TDD's emergent effect on CC; CC as a fitness function. The single most actionable structural metric on this list.
- [[accidental-complexity]] — the complexity that comes from implementation choices, not the problem itself; what most "the architecture is too complicated" complaints actually point to. The thing simplicity-minded architects are constantly fighting back.
- [[minimal-apis]] — Saint-Exupéry's "perfection is achieved not when there is nothing more to add but when there is nothing more to take away," turned into an API-design principle. The discipline that resists surface-area creep — every accepted request shape becomes a forever-maintained contract, and the cheapest ones to live with are the ones that were never added.
- [[software-defined-networking]] — the architectural move to pull routing intelligence out of individual switches into a centralised controller; the data-plane / control-plane split applied to networks. The worked example of "architecture is a trade-off": centralised control trades per-device autonomy for fleet-wide policy. Frames a broader lesson about when a characteristic (uniform policy) is worth re-drawing the quantum for.

For the deeper coupling, cohesion, and connascence material — including how they trade off against each other inside service boundaries — see [[moc-components-and-partitioning]].

## Evolution, fitness functions, and architectural decay

Architecture isn't a thing you ship once. It is a thing that decays unless you actively defend it. Fitness functions are the mechanism that keeps the structure honest.

- [[evolutionary-architecture]] — Ford's framing: architecture designed to change gracefully; fitness-function-driven governance as the alternative to prescriptive standards. The conceptual frame for why the next two pages exist.
- [[architecture-fitness-function]] — objective, automatable integrity assessment of an architecture characteristic; the six axes (atomic/holistic, triggered/continual, static/dynamic); JDepend, ArchUnit, NetArchTest, the Simian Army as the canonical implementations. The *Continuous Integration* moment for architectural rules.
- [[architecture-governance]] — steering the project so the declared characteristics actually hold over time; the XP → CI → DevOps → governance progression; the *Checklist Manifesto* framing; fitness functions as the primary mechanism that turns governance from "yelling at code reviews" into "the build fails."
- [[architecture-vitality]] — continuous analysis as the discipline; structural decay as its opposite. Why an architecture that worked a year ago can fail today without anyone changing it.
- [[architecture-katas]] — Ted Neward's 45-minute team exercise for drilling characteristic identification; *Silicon Sandwiches* as the worked kata. The deliberate-practice format for the trade-off muscle this MOC keeps invoking.

Deeper reading: [[fundamentals-of-software-architecture#chapter-6-measuring-and-governing-architecture-characteristics]] for fitness functions; [[fundamentals-of-software-architecture#chapter-19-architecture-decisions]] for the decision and ADR side that fitness functions enforce.

## Architectural decisions — recording, justifying, governing

Once you've made a decision, you have to make it survive — survive turnover, survive future you, survive the team that will inevitably come back and question it.

- [[architecture-decisions-vs-design-principles]] — the hard-and-fast rule vs guideline distinction (re-cited here as the basis for ADRs); the architecturally-significant test that decides which decisions get an ADR at all; the five factors (cost, cross-team impact, security, etc.) that escalate a design call to an architectural one.
- [[architecture-decision-record]] — Nygard's ADR template (Title / Status / Context / Decision / Consequences) plus Compliance and Notes; the RFC Status workflow; cost / cross-team / security as the canonical approval triggers; wiki storage by scope; ADRs as both *documentation* and *standards*. The single highest-leverage artifact for keeping architecture coherent across time.
- [[architecture-decision-anti-patterns]] — the three progressive failure modes: *Covering Your Assets* (no decision), *Groundhog Day* (no justification), *Email-Driven Architecture* (no single system of record). ADRs as the cure for all three.

Deeper reading: [[fundamentals-of-software-architecture#chapter-19-architecture-decisions]].

## The data dimension

The wiki's distilled position — drawn from *Hard Parts* and consistent with *DDIA* — is that data is a first-class architectural concern, not a thing engineers handle after the architect leaves the room.

- [[operational-vs-analytical-data]] — *Hard Parts*'s opening data lens; the OLTP boundary as a primary driver of decomposition; why this distinction must be made before any extraction or split decision.
- [[architecture-versus-design]] (re-cited) — ties the data argument to the architect-engineer collaboration model; data integration is the canonical place where the handoff fails most expensively.

For the deep storage, modeling, and processing material that this section is the entry point *to*, see the data MOCs: [[moc-data-models-and-storage]], [[moc-data-processing]], and [[moc-data-engineering]]. For the consistency and transactional dimension, [[moc-consistency-and-transactions]].

## Sibling MOCs

- [[moc-risk-and-communication]] — owns the *risk* and *communicate* halves of the architect's job (architecture risk matrix, risk storming, diagramming, presentation, soft skills, negotiation, career path). This MOC says *what to think*; that one says *how to surface and convey it*.
- [[moc-components-and-partitioning]] — owns the inside-the-box side: components, the partitioning axis, the identification cycle, modularity in implementation, granularity drivers/integrators, coupling and cohesion as decomposition tools. This MOC introduces modularity as a characteristic; that MOC operationalises it.
- [[moc-architecture-styles]] — owns the catalogue: layered, pipeline, microkernel, service-based, event-driven, space-based, orchestration-driven SOA, microservices. This MOC tells you *how to score* a style; that MOC catalogues *which styles to score*.
- [[moc-decomposition]] — owns the monolith-extraction playbook (decision frame, extraction patterns, database decomposition, correctness, organisational pressure, operational step-up). This MOC's trade-off discipline is the prerequisite frame for any extraction call.
- [[moc-microservices]] — owns the running-microservices view (independence, ownership, organisation, scale-out concerns). This MOC's quantum, characteristics, and fitness-function discipline are the prerequisites for getting microservices right.
- [[moc-domain-driven-design]] — owns the modelling discipline that turns "what does the business care about?" into bounded contexts and aggregates. This MOC names domain alignment as the architecturally-significant axis; the DDD MOC owns the modelling craft.
- [[moc-reliability-and-operations]] — owns the SLO/SLI/error-budget, observability, and incident-response posture. This MOC names reliability as one characteristic among many; the reliability MOC owns the operational playbook for actually delivering it.

## Related pages

- [[index]]
- [[fundamentals-of-software-architecture]]
- [[software-architecture-the-hard-parts]]
- [[software-architecture-definition]]
- [[laws-of-software-architecture]]
- [[trade-off-analysis]]
- [[architecture-characteristics]]
- [[architectural-quantum]]
- [[architecture-fitness-function]]
- [[evolutionary-architecture]]
- [[architecture-decision-record]]
- [[modularity]]
- [[architectural-thinking]]
