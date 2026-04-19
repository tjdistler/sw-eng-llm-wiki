# Backward and Forward Compatibility

**Summary**: Backward compatibility means new code can read old data; forward compatibility means old code can read new data. Both are required whenever old and new versions of code coexist in production simultaneously.

**Sources**: `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`, `raw/building-event-driven-microservices/chapter-03-communication-and-data-contracts.md`, `raw/software-architecture-the-hard-parts/chapter-13-contracts.md`

**Last updated**: 2026-04-19

---

## The Two Directions

**Backward compatibility**: Newer code can read data written by older code. This is usually straightforward — the author of new code knows what the old format looks like and can handle it explicitly.

**Forward compatibility**: Older code can read data written by newer code. This is trickier, because old code must gracefully ignore additions it doesn't understand.

Both directions matter because in practice, old and new versions of code always coexist. You cannot flip a switch and instantly upgrade every node, every client, and every stored record at once.

## Why Both Are Needed: Rolling Upgrades

Rolling upgrades are the primary driver. In a server-side application, a new version is deployed to a few nodes at a time — some nodes run old code, some run new code, and they exchange data and share databases throughout the transition. This means:

- A new node may write a record that an old node reads.
- An old node may write a record that a new node reads.

Both directions must work. Neither is optional.

With client-side applications the window is even longer: users may not update for months, so servers must maintain compatibility with old clients indefinitely.

## What "Compatibility" Requires in Practice

For **forward compatibility** (old code reads new data):
- Old code must ignore unknown fields it doesn't recognize, rather than crashing.
- It must be able to determine how many bytes to skip for unknown fields.
- It must not corrupt data it doesn't understand when re-writing it.

For **backward compatibility** (new code reads old data):
- New code must know the defaults for fields that old data doesn't include.
- New required fields break backward compatibility — every new field must be optional or have a default.

## Compatibility and Encoding Format Choice

The [[encoding-formats]] you choose determines how easily compatibility can be maintained:

- **Language-specific formats** (Java serialization, pickle): compatibility is an afterthought. Avoid for anything long-lived.
- **Textual formats** (JSON, XML): compatibility depends entirely on discipline — there are no automatic rules. You must handle missing fields, type ambiguities, and unknown keys manually.
- **Binary schema-driven formats** (Thrift, Protocol Buffers, Avro): compatibility rules are explicit and enforced by the format. See [[schema-evolution]].

## Compatibility Across Dataflow Modes

Compatibility is required everywhere data crosses a boundary:

- **Databases**: old and new code access the same rows. See [[data-outlives-code]].
- **REST/RPC**: clients and servers are deployed independently. See [[rpc]].
- **Message brokers**: publishers and consumers are deployed independently. See [[message-brokers]].

## Full compatibility as the EDM default

Bellemare's Chapter 3 of *Building Event-Driven Microservices* names the union of forward and backward compatibility as **full compatibility** and recommends it as the default for event-driven [[data-contract|data contracts]] (source: chapter-03-communication-and-data-contracts.md):

> "Full compatibility — the union of forward compatibility and backward compatibility — is the strongest guarantee and the one you should use whenever possible. You can always loosen the compatibility requirements at a later date, but it is often far more difficult to tighten them."

Under full compatibility, producer and consumer can be on different schema versions in either direction indefinitely, which is the precondition for the [[independent-deployability]] that [[event-driven-microservices]] rely on. See [[schema-evolution]] for the mechanics and [[schema-registry]] for the enforcement point.

Bellemare is also explicit that JSON fails this bar — JSON has no full-compatibility schema evolution story — which is why he recommends [[avro]] or Protobuf for EDM event formats (source: chapter-03-communication-and-data-contracts.md).

## Hard Parts framing: compatibility is a strict-contract survival mechanism

*Software Architecture: The Hard Parts* Chapter 13 frames backward and forward compatibility as the mechanism that lets [[strict-contract|strict contracts]] remain workable over time (source: raw/software-architecture-the-hard-parts/chapter-13-contracts.md). The alternative — lock-step upgrades across every consumer — is the failure mode that makes strict contracts "create brittleness in integration architecture" and makes architects reach for [[loose-contract|loose contracts]] or [[consumer-driven-contracts|CDCs]].

Compatibility doesn't eliminate the versioning burden of strict contracts; it **defers** it. Each new compatible version prolongs the time before consumers must upgrade. Chapter 13 names versioning as simultaneously an advantage (precise evolution) and a disadvantage (integration nightmare without deprecation discipline) of strict contracts — and compatibility rules are what separates the advantage case from the disadvantage case.

## Related pages

- [[schema-evolution]]
- [[encoding-formats]]
- [[data-outlives-code]]
- [[rpc]]
- [[message-brokers]]
- [[avro]]
- [[data-contract]]
- [[schema-registry]]
- [[event-driven-microservices]]
- [[contracts]]
- [[strict-contract]]
- [[software-architecture-the-hard-parts]]
