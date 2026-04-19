# Electronic Data Interchange (EDI)

**Summary**: A catch-all term for "archaic means of file exchange" — typically email attachments, flash drives, FTP — that some data sources still rely on because of legacy IT systems or entrenched human processes. Data engineers cannot always replace EDI, but they can usually **automate around it** by wiring the drop point (email inbox, file server) to object storage and an orchestration trigger.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## What EDI means in practice

Reis and Housley: "Another practical reality for data engineers is electronic data interchange (EDI). The term is vague enough to refer to any data movement method. It usually refers to somewhat archaic means of file exchange, such as by email or flash drive" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

The point is not that EDI is a technical specification (it historically was — EDIFACT, X12, and others — but Ch 7 uses the term in the loose modern sense). The point is that **some sources only support these old transports**, and the engineer has to deal with it.

## Why it sticks around

"Data engineers will find that some data sources do not support more modern means of data transport, often because of archaic IT systems or human process limitations" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

Typical examples:

- A partner business that emails CSV attachments once a month.
- An on-prem system that can only dump files to a legacy file share.
- A counterparty whose security team won't open an API or grant service-account access.
- A manual workflow where a person exports a report and drops it somewhere.

## The FoDE advice: automate around it

Engineers cannot always replace the transport, but they "can at least enhance EDI through automation." The book's concrete example: set up a cloud-based email server that saves files onto company object storage as soon as they are received. This drop can then **trigger orchestration processes to ingest and process the data** (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

"This is much more robust than an employee downloading the attached file and manually uploading it to an internal system, which we still frequently see" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## Pattern: turn EDI into object-storage-triggered ingestion

The general shape:

```
[email / SFTP / flash-drive sneakernet] --> landing zone (object store)
                                                  |
                                                  v
                                           orchestrator trigger
                                                  |
                                                  v
                                         file-based ingestion pipeline
```

Once the file is in object storage, the pipeline looks identical to any other [[file-based-ingestion]] flow — the "EDI-ness" is confined to the transport.

## Relation to other ingestion patterns

EDI is essentially the most primitive form of [[file-based-ingestion]] — the file transport is whatever ad-hoc human or legacy mechanism exists, rather than a designed pipeline. See [[file-based-ingestion]] for everything that happens once the files land.

## Related pages

- [[data-ingestion]]
- [[file-based-ingestion]]
- [[object-storage]]
- [[orchestration]]
- [[file-sources]]
