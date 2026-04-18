# Multi-Site On-Call

**Summary**: Google prefers multi-site "follow the sun" on-call rotations over single-site rotations when service load justifies growth. Multi-site rotations eliminate night shifts (which are detrimental to health) and keep on-call rotation sizes small enough that engineers stay in touch with production. The trade-off is coordination and communication overhead.

**Sources**: `raw/site-reliability-engineering/chapter-11-being-on-call.md`

**Last updated**: 2026-04-17

---

## The preference

Chapter 11 states the default: *if a service entails enough work to justify growing a single-site team, we prefer to create a multi-site team* (source: chapter-11-being-on-call.md). The decision is not about team headcount absolutely — it's about whether the team should grow vertically (more people in one site) or horizontally (a second site).

## The two advantages

Chapter 11 gives two reasons (source: chapter-11-being-on-call.md):

### Night shifts are detrimental to health

Night shifts have known adverse effects on health [Dur05 cited by Ch 11]. A multi-site follow-the-sun rotation — typically two sites 8-12 hours apart in timezone — lets each site cover the "business-hours" portion of the 24-hour cycle, so nobody has to sleep with a pager.

### Small rotations keep engineers in touch with production

A large single-site team dilutes each engineer's on-call exposure. The result is operational underload: **knowledge gaps that only surface during an incident, and confidence that has drifted from reality** — see [[operational-underload]]. Chapter 11 uses this as the argument for capping rotation size, not just the 25%-per-engineer upper bound.

The dual-site team is Chapter 11's sweet spot: ≥ 6 engineers per site honours the 25% rule, produces enough exposure to production, and avoids night shifts.

## The cost: coordination overhead

Multi-site teams incur communication and coordination overhead (source: chapter-11-being-on-call.md):

- Handoffs between sites at shift boundaries.
- Context-sharing on in-flight incidents.
- Documentation discipline, because any handover is also a cross-site handover.
- Harder face-to-face decisions on design and prioritisation.

The decision between single-site and multi-site should be based on:

- The trade-offs each option entails.
- The importance of the system.
- The workload the system generates.

## The decision shape

Chapter 11's implicit decision tree:

1. Is the service workload enough to justify a team larger than ~8 at one site?
   - No → single-site team of 8+.
   - Yes → go to 2.
2. Can the organisation absorb multi-site coordination overhead for this service?
   - Yes → multi-site team, ≥ 6 per site, no night shifts.
   - No → single-site team with night shifts (with the health cost accepted explicitly).

The bias is toward multi-site because the health argument is strong and coordination overhead is a cost you can engineer against.

## Related pages

- [[balanced-on-call]]
- [[sre-on-call-engagement]]
- [[operational-underload]]
- [[on-call-compensation]]
- [[toil-and-engineering-balance]]
