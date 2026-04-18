# Live Incident State Document

**Summary**: The [[incident-commander|IC]]'s most important responsibility, per Chapter 14: a living document that captures the current state of the incident, edited concurrently by multiple people. It's the structured complement to the chronological [[recognized-command-post|command-post chat log]] — newcomers get oriented in seconds, and the document survives to feed the postmortem.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`, `raw/site-reliability-engineering/chapter-15-postmortem-culture-learning-from-failure.md`

**Last updated**: 2026-04-17

---

## What it is

> The incident commander's most important responsibility is to keep a living incident document. This can live in a wiki, but should ideally be editable by several people concurrently. (source: chapter-14-managing-incidents.md)

A single document — usually a Google Doc — that holds the up-to-date state of the incident: what's happening, what's been tried, what's working, who's doing what, what the next steps are. Both the IC and the comms lead may edit it; for large incidents, anyone in the response can. Most Google teams use Google Docs; Google Docs SRE itself uses Google Sites (more on that below).

## What's in it

Chapter 14 doesn't enumerate the fields, but the managed-incident narrative shows the shape:

- **Current impact** — what users see, which systems are affected
- **What's been tried** — including what didn't work (Mary's failed binary rollback)
- **Working hypotheses**
- **Active mitigations and temporary deviations from the norm** (so [[incident-planning-lead|planning]] can revert them later)
- **Who holds which role**, and the handoff schedule
- **Timeline of significant events**

> This living doc can be messy, but must be functional. Using a template makes generating this documentation easier, and keeping the most important information at the top makes it more usable. (source: chapter-14-managing-incidents.md)

The "messy but functional" guidance is permission to skip prose polishing during the incident. The information layout — important things at the top — is what makes the document scannable for someone joining mid-incident.

A sample incident document is referenced in the book's Appendix C.

## Why concurrent editing matters

Single-writer documents create a serialisation bottleneck: the IC stops paying attention to the response in order to type. Concurrent editing means:

- The comms lead pastes the latest IRC update directly while the IC keeps coordinating.
- The ops lead annotates a hypothesis as they're forming it.
- Sister-office responders read the document during a handoff call and add clarifying questions inline.

This is why a wiki page is *acceptable* but a concurrently-editable document is **preferred** — Google Docs' real-time multi-user editing is the load-bearing capability.

## Don't depend on the system you're fixing

> Most of our teams use Google Docs, though Google Docs SRE use Google Sites: after all, depending on the software you are trying to fix as part of your incident management system is unlikely to end well. (source: chapter-14-managing-incidents.md)

This is the response-infrastructure-independence rule. Your incident-management tool must not be in the failure domain of the thing you're managing the incident for. The general principle: the **response infrastructure** (chat, doc, paging, dashboards) needs an availability story independent of the production system. The Chapter 13 [[change-induced-emergency|change-induced emergency]] is the worked example — most internal Google tools were affected by the same push that took down external services, so the response had to fall back to chat (independent), CLI tools (independent), and out-of-band communication.

## Lifecycle

The document is created when the incident is declared and **retained for postmortem analysis** and, if necessary, meta-analysis (source: chapter-14-managing-incidents.md). Chapter 12 makes the same point from the other side — see [[blameless-postmortem]] — that the postmortem timeline is built from the notes the response team kept during the incident. The live incident document is one of the primary inputs.

## Input to automated postmortem creation (Chapter 15)

Chapter 15's [[postmortems-at-google-working-group|Postmortems at Google working group]] explicitly names *automating postmortem creation with data from tools used during an incident* as one of its workstreams (source: chapter-15-postmortem-culture-learning-from-failure.md). The live incident document is one of the primary data sources being targeted — alongside the [[recognized-command-post|command-post chat log]], monitoring dashboards, and alert records.

The implication for the document's structure: Chapter 14's "messy but functional" guidance has to be balanced against the emerging need for **machine-readability**. Messy is fine; structured-enough-to-extract-timestamps-and-actions-from is better. Chapter 15's metadata-enrichment trend on the [[postmortem-template|postmortem template]] is the same pressure applied at the template end; the live document is where the raw material originates.

## Cross-book connection

- The independence-from-the-system-being-fixed rule mirrors the Ch 13 [[change-induced-emergency|out-of-band communication]] lesson and Burns's general "control-plane separate from data-plane" recommendation.
- "Important info at the top" is the [[architecture-presentation|inverse-pyramid]] discipline applied to the incident workspace.
- The document is the in-incident analogue of an [[architecture-decision-record|ADR]] — a structured, append-only record of state and decisions whose value compounds when the incident is over.

## Related pages

- [[incident-management-framework]]
- [[incident-commander]]
- [[incident-communications-lead]]
- [[incident-planning-lead]]
- [[recognized-command-post]]
- [[blameless-postmortem]]
- [[change-induced-emergency]]
