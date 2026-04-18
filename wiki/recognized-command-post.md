# Recognized Command Post

**Summary**: One of the five elements of Chapter 14's [[incident-management-framework]]. Interested parties need to know **where** they can interact with the [[incident-commander]] — a designated war room, an IRC channel, an email thread, or a combination. Google has found IRC particularly valuable because it doubles as a reliable, time-stamped log of communications that's invaluable in postmortem analysis.

**Sources**: `raw/site-reliability-engineering/chapter-14-managing-incidents.md`

**Last updated**: 2026-04-17

---

## What a command post is

> Interested parties need to understand where they can interact with the incident commander. (source: chapter-14-managing-incidents.md)

The command post is the **single known location** where:

- The IC can be found
- Status updates are broadcast
- Volunteers can offer help
- Stakeholders can ask questions
- The incident's communications history accumulates

The form varies. Chapter 14 names two common ones:

- **A central designated "War Room"** — appropriate when the response team can physically co-locate.
- **Desk-based work, with alerts via email and IRC** — preferred by many teams; supports geographically distributed response.

In practice, large modern incidents typically have both: a Zoom/Meet call for synchronous discussion, plus a chat channel that serves as the durable log.

## Why IRC (chat)

> Google has found IRC to be a huge boon in incident response. (source: chapter-14-managing-incidents.md)

Chapter 14's three reasons:

1. **Reliability** — IRC is simple, low-bandwidth, and unlikely to be the thing that breaks during a Google-wide incident. (See the Chapter 13 [[change-induced-emergency|change-induced emergency]] for an incident in which most communications tooling was actually broken; chat survived.)
2. **It's a log** — every message is time-stamped. The transcript is invaluable in keeping detailed state changes in mind during the response, and again later during the postmortem.
3. **Geographic distribution** — chat works as well across continents as across desks; phone bridges and war rooms don't.

Google has also written **bots** that:

- Log incident-related traffic specifically to a known location for postmortem analysis.
- Log alert events into the incident channel so the response team sees them in line with their own discussion.

## Single source of truth, and its shadows

The command post is the *communications* source of truth for the incident; the [[live-incident-state-document|live incident state document]] is the *state* source of truth. They're complementary:

- The command post is a **stream**: chronological, append-only, conversational.
- The document is a **store**: structured, latest-state-on-top, scannable.

Newcomers to the incident can read the document quickly to get oriented; the chat is for ongoing back-and-forth.

## Interactions with the comms lead

The [[incident-communications-lead|comms lead]] doesn't replace the command post — they curate from it and feed updates into the email thread and the live document. Stakeholders who don't want chat-channel detail can read the email thread. The framework supports multiple audiences without forcing the response team to write multiple bespoke updates.

## Cross-book connection

- The command post is structurally a [[log-aggregation|log aggregation]] point applied to human communication: one place all events flow into so everything is durable and searchable.
- The reliability-of-the-tool argument echoes the "depending on the software you are trying to fix is unlikely to end well" warning in [[live-incident-state-document]] — the response infrastructure must be independent of what's broken.

## Related pages

- [[incident-management-framework]]
- [[incident-commander]]
- [[incident-communications-lead]]
- [[live-incident-state-document]]
- [[change-induced-emergency]]
