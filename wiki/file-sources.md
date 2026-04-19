# File Sources

**Summary**: Despite decades of better options, **files remain a universal medium of data exchange** between systems — particularly across organizational boundaries. Reis and Housley's Chapter 5 opens the source-system enumeration with files precisely because they are ubiquitous, ugly, and impossible to avoid: a data engineer will receive CSVs by email, download Excel reports from government portals, and pull JSON lines out of cloud object stores for the rest of their career.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## What a file is, in this context

"A file is a sequence of bytes, typically stored on a disk. Applications often write data to files. Files may store local parameters, events, logs, images, and audio" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md). As a [[source-systems|source system]], a file is the output of some upstream process — either directly authored by a human or emitted by a system export — that the data engineer must ingest.

The unavoidable observation from Reis and Housley: "As much as data engineers wish that they could get data programmatically, much of the world still sends and receives files. For example, if you're getting data from a government agency, there's an excellent chance you'll download the data as an Excel or CSV file or receive the file in an email" (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Source-system file formats

The formats that show up at the generation stage (not the warehouse/lake storage formats) (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

| Format | Structure | Source typical |
|---|---|---|
| **Excel** (`.xlsx`, `.xls`) | Structured, tabular | Spreadsheet exports, government data |
| **CSV** | Semi-structured; type-free | Nearly every tabular-data export path |
| **TXT** | Unstructured | Logs, raw dumps |
| **JSON** | Semi-structured, nested | APIs, application exports |
| **XML** | Semi-structured, verbose | Older enterprise and SOAP-era exports |

Reis and Housley explicitly reserve the analytical formats — **Parquet**, **ORC**, **Avro** — for the Chapter 6 storage treatment, not the source-system stage. These formats exist but almost always live as **downstream** representations into which the data engineer transforms the raw file inputs, not as what the source sends. See [[encoding-formats]] for the schema-capable analytical formats.

## Why file-shaped ingestion is hard

- **Implicit schema.** CSV and TXT carry no type information. Numbers parse as strings; booleans parse as `"true"`/`"false"`; dates can be in any of dozens of formats. Every consumer must re-guess the schema.
- **Encoding drift.** A file that "used to work" can break when an upstream process changes the delimiter, the quoting style, the text encoding (UTF-8 vs Latin-1), or the line endings.
- **Partial files.** A file may arrive truncated if the upload is interrupted; atomic publishing (rename-after-upload, sentinel files, manifest files) is often missing.
- **Manual origin.** Spreadsheets frequently have a human editing them; cells are reshaped, rows are inserted, columns are renamed, and nobody tells the data team.
- **Transport path.** Email, SFTP, shared drives, and cloud object stores all have different failure modes for delivery, retention, and access control.

## Landing zones

File-shaped sources typically land in one of:

- **Cloud object storage** (S3, GCS, Azure Blob) — the modern default; durable, versioned, cheaply queryable. Files in object storage are the on-ramp to a [[data-lake]] or [[data-lakehouse]].
- **Shared SFTP servers** — the traditional B2B mechanism; still dominant in finance, healthcare, and government.
- **Email attachments** — rare but real; requires a mail-ingesting process that scrapes attachments and deposits them in object storage.
- **Local shared drives** — the enterprise file share; painful but still present.

The engineer typically layers a standard convention on top: partitioned-by-date paths, manifest files to indicate "this drop is complete," and checksum verification to catch truncation.

## Ingestion approach

- **Pull.** The ingestion system polls the landing zone for new files; when one arrives, it parses, validates, and loads. This is the common path for object-storage-hosted drops.
- **Push.** The source uploads the file directly to an ingestion endpoint. Webhook-style notifications from object-storage services (S3 Event Notifications, GCS Pub/Sub notifications) turn a pull pattern into an effectively-push one.

See [[data-ingestion]] for the broader push-vs-pull framing.

## Connection to the broader lifecycle

Files are the "first" source format in Chapter 5's enumeration but the **last** to benefit from a good [[schema-registry]] or [[data-contract]]. They nearly always lack a machine-checkable schema — the data contract is implicit, and breaking it is easy. Engineers working with file-shaped sources should:

1. Document the expected schema explicitly, even if the source does not.
2. Validate arriving files against that schema before loading downstream.
3. Treat schema violations as incidents, not silent-drop cases — see [[data-quality]].

## Cross-book connections

- [[encoding-formats]] (DDIA) — the deeper treatment of text vs binary vs schema-carrying formats. Chapter 5's Excel/CSV/JSON are the text-format end; Parquet/ORC/Avro are the schema-carrying end used for the Chapter 6 storage stage.
- [[data-liberation]] (Bellemare) — when file-shaped exports are how a legacy monolith exposes its data, liberating that data typically means replacing the file with an event stream over time.
- [[data-lake]] / [[data-lakehouse]] — where raw file-shaped sources most commonly land in a modern architecture.

## Related pages

- [[source-systems]]
- [[source-system-considerations]]
- [[data-ingestion]]
- [[encoding-formats]]
- [[data-lake]]
- [[data-lakehouse]]
- [[schema-on-read-vs-write]]
- [[data-contract]]
- [[data-quality]]
