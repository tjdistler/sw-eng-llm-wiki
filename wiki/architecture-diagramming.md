# Architecture Diagramming

**Summary**: The architect's craft of visually representing system topology — tools, standards (UML, C4, ArchiMate), guidelines (titles, lines, shapes, labels, color, keys), and the overarching discipline of *representational consistency* that keeps drill-down views anchored to the whole.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-21-diagramming-and-presenting-architecture.md`

**Last updated**: 2026-04-16

---

Diagramming is one of the two critical soft skills Richards and Ford name for the modern architect. Architecture topology captures how a system fits together and forms the shared understanding the team actually builds against, so architects should hone their diagramming skills "to razor sharpness" (source: chapter-21-diagramming-and-presenting-architecture.md). No matter how brilliant a technical idea, if it cannot be communicated it never ships — diagramming is the primary medium for that communication.

## Representational consistency

The one discipline that ties diagramming and [[architecture-presentation|presenting]] together is **representational consistency**: always show the relationship between parts of an architecture before changing views (source: chapter-21-diagramming-and-presenting-architecture.md). When an architect zooms in from a topology-level diagram to a detail view, the detail view must preserve the vocabulary and orientation of the whole — if it introduces new unrelated shapes, colours, or boxes that have no counterpart upstream, viewers lose track of where they are. The canonical technique is to show the full topology first, then highlight the subregion being expanded and draw the detail alongside or inside that highlight. The book's worked example uses the Silicon Sandwiches plug-in structure: the whole architecture is shown, the plug-in region is marked, and only then is the plug-in's internal structure drilled into.

Representational consistency is the scope guardrail — without it "a common source of confusion" creeps in (source: chapter-21-diagramming-and-presenting-architecture.md). It applies equally to slides: the same convention of locating-before-drilling-in is how a presentation preserves the viewer's map of the system.

## Tools and the Irrational Artifact Attachment anti-pattern

Richards and Ford warn architects not to reach for the nice tool too early. They name the **Irrational Artifact Attachment** anti-pattern: a person's irrational attachment to an artifact is proportional to how long it took to produce (source: chapter-21-diagramming-and-presenting-architecture.md). A two-hour Visio diagram is twice as hard to throw away as a one-hour one; a four-hour diagram is nearly impossible to discard even when the design is wrong. The fix is the Agile-style low-ritual approach — index cards, sticky notes, whiteboards, tablets — early in the design process, so ideas can be thrown away without mourning. Only once the team has iterated the design to stability should the architect invest time in a polished tool-rendered version.

The authors' favorite whiteboard substitute is a tablet-and-projector combination: unlimited canvas, copy/paste for "what if" scenarios, and images that are already digitised and glare-free rather than the "Do Not Erase!" cell-phone-whiteboard-photo pattern.

When the time does come for a proper tool, architects should look for this baseline feature set:

- **Layers** — toggle groups of elements to build up views or to hide overwhelming detail on demand; the foundation for [[architecture-presentation#incremental-builds|incremental builds]] later
- **Stencils / templates** — a library of common composites (the book's microservice shape is one stencil), which keeps diagrams consistent across a team or organisation and speeds new diagram production
- **Magnets** — snap points on shapes where lines attach automatically, producing clean alignment
- **Lines, colours, export formats** — the usual

The authors used OmniGraffle for the book but explicitly decline to advocate any one tool.

## Diagramming standards: UML, C4, ArchiMate

Three formal standards for software-architecture diagrams exist. None wins everywhere; architects should know what each is for.

### UML (Unified Modeling Language)

A 1990s unification of three competing 1980s design philosophies. Like many design-by-committee efforts, UML "failed to create much impact outside organizations that mandated its use" (source: chapter-21-diagramming-and-presenting-architecture.md). The **class** and **sequence** diagrams survived — architects and developers still use them routinely to communicate structure and workflow — but the rest of UML's diagram types have fallen into disuse. UML's main legacy is those two diagram shapes, which other standards now reuse.

### C4 (Simon Brown)

C4 is the modern default — a diagramming technique Simon Brown developed specifically to address UML's deficiencies and replace it for most architecture communication. The four C's are four progressive zoom levels:

- **Context** — the whole system including user roles and external dependencies; the outermost view
- **Container** — the physical (and usually logical) deployment boundaries; a good meeting point for architects and operations
- **Component** — the component view, which aligns most naturally with the architect's mental model (and to the wiki's existing [[components]] page)
- **Class** — the innermost view; C4 deliberately reuses UML's class diagrams here because they work

C4 is best suited to **monolithic / layered** architectures where container and component relationships differ meaningfully. It is **less suited to distributed architectures** like [[microservices]], where the container-vs-component distinction often collapses (source: chapter-21-diagramming-and-presenting-architecture.md). For a company standardising on a single diagramming technique, C4 is the strong default.

### ArchiMate

ArchiMate (*Arch*itecture-Ani*mate*) is an open-source enterprise-architecture modelling language from The Open Group. It is explicitly designed to be "as small as possible" rather than to cover every edge case, which makes it lighter than UML while still supporting description, analysis, and visualisation of architecture across business domains. It is popular in enterprise-architecture shops and offers a genuinely different emphasis from C4 (business-domain-spanning rather than system-focused).

The book's editorial stance is that no standard covers every design adequately; even C4 "suffers from an inability to express every kind of design an architecture might undertake" (source: chapter-21-diagramming-and-presenting-architecture.md). The standards are starting points, not straitjackets.

## Diagram guidelines

Regardless of which standard (or custom vocabulary) an architect uses, the book offers six guidelines that apply to every diagram (source: chapter-21-diagramming-and-presenting-architecture.md):

- **Titles** — every element should have a title or be known to the audience. Use rotation and placement to make titles "sticky" to the thing they label and to save space.
- **Lines** — thick enough to see. Use arrows to show direction; use arrowhead styles consistently to indicate different semantics. The one near-universal convention: **solid lines = synchronous, dotted lines = asynchronous** communication. (This convention ties directly to the [[connascence|synchronous vs asynchronous connascence]] axis introduced in Chapter 7.)
- **Shapes** — no pervasive industry standard exists outside the formal modelling languages. Each architect (or organisation) develops their own. The book's convention: 3D boxes for deployable artifacts, rectangles for containership.
- **Labels** — label every item, especially where ambiguity is possible. Missing labels are a reliable source of misinterpretation.
- **Colour** — architects under-use colour, a historical legacy of black-and-white printing. Use colour when it distinguishes one artefact from another (the book uses it to show that two microservices are *different* services rather than two instances of the same one).
- **Keys** — include a key/legend whenever shapes are ambiguous. "Nothing is worse than a diagram that leads to misinterpretation, which is worse than no diagram" (source: chapter-21-diagramming-and-presenting-architecture.md).

The broader point: build a consistent diagramming style, borrow liberally from representations that work, and be explicit about meaning.

## Relationship to architecture decisions and documentation

Diagrams are one of the two primary forms of architecture documentation; the other is the [[architecture-decision-record]]. The two are complementary: diagrams show *what* the system looks like, ADRs record *why* it looks that way. The Chapter 19 observation that neither C4 nor ArchiMate covers architecture documentation completely — both deliberately stop at visual representation — is why ADRs matter as the narrative companion.

## Related pages

- [[architecture-presentation]] — the companion soft skill: presenting architecture with PowerPoint / Keynote; shares the representational-consistency discipline
- [[components]] — the physical packaging that C4's Component level aligns with
- [[architectural-quantum]] — the unit that distributed diagrams have to represent
- [[connascence]] — the synchronous-vs-asynchronous axis that the solid-vs-dotted line convention encodes
- [[architecture-decision-record]] — the narrative companion to diagrams
- [[microservices]] — the style C4 handles worst; the authors flag it explicitly
- [[layered-architecture]] — the style C4 was designed for
- [[fundamentals-of-software-architecture]]
