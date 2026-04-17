# Architecture Presentation

**Summary**: The architect's second critical soft skill — using presentation tools (PowerPoint, Keynote) well. Manipulating time via transitions and animations, incremental builds, the slides-are-half-of-the-story principle, and invisibility as deliberate refocusing.

**Sources**: `raw/fundamentals-of-software-architecture/chapter-21-diagramming-and-presenting-architecture.md`

**Last updated**: 2026-04-16

---

Presenting is the second critical soft skill Richards and Ford name in Chapter 21, paired with [[architecture-diagramming|diagramming]]. The two share [[architecture-diagramming#representational-consistency|representational consistency]] as their governing discipline but differ in medium. Presentation tools are "the lingua franca of modern organizations" (source: chapter-21-diagramming-and-presenting-architecture.md), yet unlike word processors and spreadsheets, almost no one studies how to use them well. The chapter draws heavily on Neal Ford's earlier book *Presentation Patterns* (Addison-Wesley), which applies the software-patterns/anti-patterns approach to technical presentations.

## The fundamental difference: who controls time

The load-bearing observation: a **document** and a **presentation** differ in who controls the unfolding of an idea. In a document, the reader sets the pace; in a presentation, the presenter does. This makes **manipulating time** the single most important skill an architect can learn in their presentation tool of choice (source: chapter-21-diagramming-and-presenting-architecture.md).

Presentation tools expose two mechanisms for this:

- **Transitions** — move from one slide to the next (usually one per slide)
- **Animations** — create movement *within* a slide. Three kinds: **build in** (appearance), **build out** (disappearance), and **actions** (movement, scale, and other dynamic behaviour)

The skilled use of these mechanisms is not the splashy-effect gallery — dropping anvils and cube-spins — but using subtle transitions (dissolve) and animations to **hide the boundaries between slides**. Many ideas are bigger than one slide; stitching them seamlessly together tells one continuous story. When a thought *does* end, switch to a distinctly different transition (door, cube) to cue the audience that the topic is changing.

The book also names the **Cookie-Cutter** anti-pattern: ideas do not have predetermined word counts, so designers should not artificially pad content to make each idea fill exactly one slide. Content fits the idea; the tool supports the content.

## Incremental builds

The **Bullet-Riddled Corpse** is the canonical corporate-presentation anti-pattern: every slide is the speaker's notes projected for all to see. The audience reads the entire slide as soon as it appears, then sits restlessly while the presenter slowly reads the same bullets aloud for ten minutes (source: chapter-21-diagramming-and-presenting-architecture.md). The cognitive problem is precise: the presenter has two information channels — **verbal** and **visual** — and stuffing the slide with text overloads one and starves the other.

The fix is the **incremental build**: reveal (preferably graphical) information progressively as the narrative reaches it, rather than all at once. The book's worked example: a slide showing the negative consequences of long-lived feature branches, where the "bad thing happens at the end" is initially obscured behind a white box and then revealed at the right moment via a build-out animation. Incremental builds keep the audience's attention with the speaker rather than racing ahead to the end of the slide, and they preserve genuine suspense — making the talk inherently more interesting.

Incremental builds also compose cleanly with the [[architecture-diagramming|diagramming]] practice: the same layered diagram an architect builds in their diagramming tool (using [[architecture-diagramming#tools-and-the-irrational-artifact-attachment-anti-pattern|layers]]) can be re-used as the incremental-build source in the presentation tool.

## Infodecks versus presentations

An **infodeck** is a slide deck that is never actually presented — it is emailed around, read asynchronously at the reader's own pace, and behaves like a magazine article. Infodecks and presentations differ along two axes (source: chapter-21-diagramming-and-presenting-architecture.md):

- **Comprehensiveness of content** — infodecks must stand alone; presentations deliberately do not
- **Use of time mechanisms** — infodecks use no transitions or animations (the reader controls time); presentations use them heavily

The confusion between the two media is the source of most bad corporate presentations. If a slide deck is meant to be projected and presented, it must *not* be comprehensive — because the presenter is half of the presentation.

## Slides are half of the story

The principle behind the infodeck distinction: if the slides contain the full content, the presenter is redundant and everyone's time is wasted — just email the deck. Presenters have two information channels; using them strategically (slides show one thing, speaker says another, the two reinforce rather than duplicate) is what makes the talk land. The Bullet-Riddled Corpse is the failure mode where both channels carry the same content.

## Invisibility

**Invisibility** is a simple pattern: insert a blank black slide at moments when the speaker wants the audience's full attention (source: chapter-21-diagramming-and-presenting-architecture.md). If the audience has two things to look at — slides and speaker — and one of them goes dark, attention automatically shifts to the other. Making the slides invisible makes the speaker the only interesting thing in the room, which is exactly what's needed for the emphasis moments.

This is the sharpest practical expression of the two-channel model: the visual channel is not always on, and deliberate silence in it is a tool.

## Related patterns and anti-patterns from the chapter

Summarised for cross-reference:

- **Cookie-Cutter** — padding content to match a predetermined slide count (anti-pattern)
- **Bullet-Riddled Corpse** — slides as speaker notes (anti-pattern)
- **Incremental Build** — progressive reveal of slide content (pattern)
- **Infodeck** — a slide deck meant to be read, not presented (a distinct medium, not a pattern or anti-pattern)
- **Invisibility** — deliberate blank slide for refocusing (pattern)

## Why this matters for architects

Architecture requires collaboration. To get collaborators, architects must convince people to sign on to their vision — managers to fund it, developers to build it. "The modern corporate soapboxes are presentation tools, so it's worth learning to use them well" (source: chapter-21-diagramming-and-presenting-architecture.md). A great architectural idea that cannot be communicated never gets realised.

## Related pages

- [[architecture-diagramming]] — the companion soft skill; shares the representational-consistency discipline
- [[architecture-decision-record]] — the text form of architecture communication; presentations often motivate and reference ADRs
- [[fundamentals-of-software-architecture]]
