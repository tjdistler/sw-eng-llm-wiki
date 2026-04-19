# File Exchange (Serving)

**Summary**: The oldest and most ubiquitous data-serving mechanism — generate a file, hand it to a consumer. Chapter 9 treats file exchange as a legitimate serving pattern with specific design considerations: use case, consumer capabilities, file size/count, access control, data type. The emailed Excel file remains a common real-world workflow despite every modern alternative; the DE's job is often to migrate to something more robust without breaking the consumer.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md`

**Last updated**: 2026-04-18

---

## Why files are still everywhere

Chapter 9: "File exchange is ubiquitous in data serving. We process data and generate files to pass to data consumers." A file may be used for many purposes — loaded into a pandas dataframe for sentiment analysis, into Excel for statistical analysis, into a computer-vision pipeline for classification (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

The underlying reason for file exchange's persistence: **the consumer cannot use anything else.** A partner uses Excel; a data scientist's tooling expects files; a SaaS tool exports CSVs. The lowest common denominator is always a file.

## Five design considerations

Chapter 9 enumerates what to consider when serving via files (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md):

1. **Use case** — business analytics, operational analytics, user-facing analytics. Each has different freshness and structure requirements.
2. **Consumer data-handling processes** — can they use a sharing platform? A database connection? If not, files.
3. **File size and count** — one 5MB Excel workbook is very different from 10,000 parquet files.
4. **Who accesses the file** — one named person, a group, an external party. Determines access control shape.
5. **Data type** — structured (CSV, parquet), semi-structured (JSON, XML), unstructured (images, text).

## The emailed-Excel problem

Chapter 9's archetype: emailing a single Excel file. Each recipient gets their own version. If someone edits it, the edit is specific to that recipient's copy. Deviations are inevitable (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

The recommended fix: **use a collaboration platform** (Microsoft 365, Google Docs) so there's a single coherent file everyone references.

## Scaling beyond individual files

As needs outgrow single-file email/collaboration tools, the progression:

1. **Handful of large files** → object-storage bucket (S3, GCS, Azure Blob). See [[object-storage]].
2. **Steady supply of files** → [[data-lake]].

Once you're at the lake stage, Chapter 9 notes a subtle classification point: file exchange through object storage is usually considered [[data-sharing]] rather than "file exchange," because "the process can be significantly more scalable and streamlined than ad hoc file exchange" (source: raw/fundamentals-of-data-engineering/chapter-09-serving-data-for-analytics-machine-learning-and-reverse-etl.md).

So the naming convention Chapter 9 uses:

- **File exchange** — ad-hoc one-off file hand-offs, email, SFTP drops, single-file shares.
- **[[data-sharing]]** — platform-mediated exchange of structured datasets at scale.

## When file exchange is correct

- A one-off extract for a business partner who runs Excel.
- A point-in-time snapshot to a consumer that can't hold a live connection.
- A regulatory filing with required file formats.
- A legacy integration that nothing else can consume.

## When to push for something better

- The same consumer gets the same file every week.
- Multiple consumers disagree because they each have their own copy.
- File sizes push email limits.
- The file needs schema evolution (CSV and Excel will be painful; consider parquet + data sharing).

## Cross-book connections

- **[[file-sources]]** — the source-system counterpart. What you serve as a file is often ingested the same way on the consumer side.
- **[[file-based-ingestion]]** — SFTP, SCP, object-storage file drops as an ingestion pattern; same mechanics seen from the other end.

## Related pages

- [[data-serving]]
- [[data-sharing]]
- [[file-sources]]
- [[object-storage]]
- [[data-lake]]
- [[file-based-ingestion]]
