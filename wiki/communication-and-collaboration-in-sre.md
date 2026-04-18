# Communication and Collaboration in SRE

**Summary**: Chapter 31 hub on how Google SRE teams communicate and collaborate across two crucial dimensions — internal data flow within an SRE team (the [[production-meetings|production meeting]] is the canonical instrument) and external collaboration with other SRE teams and with product development. The chapter frames the SRE team's external interface as an API: designed deliberately, costly to fix later. Two case studies ground the abstract recommendations: [[viceroy-case-study|Viceroy]] (cross-SRE monitoring-dashboard consolidation) and [[dfp-to-f1-migration|DFP-to-F1]] (joint SRE + product-development database migration).

**Sources**: `raw/site-reliability-engineering/chapter-31-communication-and-collaboration-in-sre.md`

**Last updated**: 2026-04-17

---

## Why the chapter exists

Google SRE is not a command-and-control organisation. Service and infrastructure SRE teams owe allegiance to at least two masters: the product development team whose system they support, and SRE as a whole (source: chapter-31-communication-and-collaboration-in-sre.md). The service relationship is strong — SRE is accountable for production performance — but reporting lines run through SRE. That split, combined with distributed sites, multinational structure, and the diversity of SRE roles (infrastructure, service, horizontal product), makes communication and collaboration a first-class engineering problem.

The chapter uses two metaphors:

- **Data flow**: data (about projects, services, production, people) must flow through an SRE team the way data flows through production — reliably, from interested party to interested party.
- **API as contract**: the SRE team presents an interface to the rest of the organisation. A good API design matters; a bad one is painful to correct later.

## Internal communication: the production meeting

The chapter's main communication instrument is the [[production-meetings|production meeting]]: a weekly 30-60 minute service-oriented gathering where the team articulates the state of its services to itself and to invitees, and connects operational performance back to design, configuration, and implementation decisions. The feedback loop from ops experience to design choice is what makes production meetings worth defending as a practice (source: chapter-31-communication-and-collaboration-in-sre.md).

The default agenda covers upcoming production changes, metrics, outages, paging events, nonpaging events, and prior action items. Attendance is compulsory for team members and includes major stakeholders and partner product development teams.

## Collaboration inside SRE

Because SRE teams are geographically distributed by design (for follow-the-sun pager coverage), most interesting collaboration is cross-site. The chapter lays out:

- **Team composition and roles** — [[sre-team-composition]]: tech lead (TL), SRE manager (SRM), project manager (TPM/PM/PgM); the fluid-vs-rigid trade-off
- **Specialisation as a double-edged tool** — focusing a team on a subset of systems increases technical mastery but risks siloing; a crisp team charter helps
- **Techniques for cross-site work** — [[cross-sre-collaboration]]: good written communication, travel when needed, divide-and-conquer to minimise communication cost

The worked example is [[viceroy-case-study|Viceroy]]: the cross-SRE monitoring-dashboard project that eventually consolidated multiple parallel efforts (including Consoles++) into Google's general SRE monitoring solution. The retrospective generates a set of [[cross-site-project-recommendations|cross-site project recommendations]] the chapter explicitly lists.

## Collaboration outside SRE

The chapter's thesis on SRE-product-development collaboration is simple: **it works best when it starts early, before any code is committed**. SREs can make recommendations about architecture and software behaviour that are nearly impossible to retrofit; getting that voice into the design-phase room changes the outcome (source: chapter-31-communication-and-collaboration-in-sre.md). Work is tracked via the OKR (Objectives & Key Results) process, and for some service SRE teams this kind of consultation is the core of the job.

The worked example is [[dfp-to-f1-migration]]: the migration of DoubleClick for Publishers' main database from MySQL to F1. The SRE team drove the infrastructure design (extract/process/index machinery over F1), the product-development team owned the business-logic changes, weekly meetings synchronised the two tracks, and the cutover was seamless to users — a textbook result for the model the chapter advocates. See [[sre-dev-collaboration]] for the general pattern.

## Pages created or updated by this chapter

New pages:

- [[production-meetings]] — weekly service-oriented meeting: agenda, attendance, rotating chair, Google Docs agenda collaboration
- [[sre-team-composition]] — TL, SRM, TPM roles; the fluid-vs-rigid spectrum; diversity as a collaboration multiplier
- [[cross-sre-collaboration]] — how SRE teams collaborate across sites; specialisation vs siloization; written communication as the primary bridge
- [[viceroy-case-study]] — monitoring-dashboard consolidation across SRE teams; Viceroy + Consoles++ merger; challenges and outcome
- [[cross-site-project-recommendations]] — the chapter's explicit list of recommendations for cross-site engineering projects
- [[sre-dev-collaboration]] — the general model for SRE + product-development collaboration; OKRs; start-early-in-design thesis
- [[dfp-to-f1-migration]] — case study of joint SRE + product-development database migration; infrastructure-first design; seamless cutover

## Related pages

- [[production-meetings]]
- [[sre-team-composition]]
- [[cross-sre-collaboration]]
- [[viceroy-case-study]]
- [[cross-site-project-recommendations]]
- [[sre-dev-collaboration]]
- [[dfp-to-f1-migration]]
- [[sre-discipline]]
- [[conways-law]]
- [[reorganizing-teams]]
- [[team-autonomy]]
- [[architect-leadership-skills]]
