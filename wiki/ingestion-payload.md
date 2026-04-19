# Ingestion Payload

**Summary**: Reis and Housley's catch-all term for "the dataset you're ingesting." A payload has five characteristics every [[data-ingestion|ingestion]] design must account for: **kind** (type + format), **shape** (dimensions), **size** (bytes), **schema and data types**, and **metadata**. These five properties together determine how the data moves, what can deserialize it, and whether it is usable downstream.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-07-ingestion.md`

**Last updated**: 2026-04-18

---

## The five characteristics

### 1. Kind

Kind is **type plus format** (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Type** — tabular, image, video, text, audio, and so on.
- **Format** — the concrete byte expression of that type: CSV or Parquet for tabular, JPG or PNG for images, JSON or XML for semistructured, and so on.

Format "directly influences" how the data is expressed in bytes, filenames, and extensions — and each format has different byte patterns for serialization and deserialization.

### 2. Shape

Every payload has a shape describing its dimensions (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

| Kind | Shape |
|---|---|
| Tabular | M rows × N columns |
| Semistructured JSON | Key-value pairs and nesting depth |
| Unstructured text | Number of words, characters, or bytes |
| Images | Width, height, colour depth (e.g., 8 bits per RGB pixel) |
| Uncompressed audio | Channels (stereo = 2), sample depth, sample rate, length |

Shape matters because downstream systems have shape expectations. A CSV with more columns than the target table will fail at import. An ML model expecting 256×256 RGB images breaks on 512×512 grayscale.

### 3. Size

Size is the number of bytes — anywhere from single bytes to terabytes or more. Two standard techniques reduce size-related friction (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- **Compression.** ZIP, TAR, gzip, and so on; see [[compression-algorithms]].
- **Chunking.** A single massive payload can be split into smaller pieces, each easier to transmit (especially compressed) over a network, and reassembled at the destination. "When loading a huge file into a cloud object storage or data warehouse, this is common practice."

### 4. Schema and data types

Many payloads have an explicit schema (tabular, semistructured). Others (unstructured text, images, audio) do not have a native schema but do come with technical descriptors — shape, data and file format, encoding, size. Ch 7's point: **connecting to a database is easy; understanding the underlying schema is the great engineering challenge** (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

Two schema hazards Ch 7 calls out:

- **ORM-generated schemas.** Object-relational mapping (Java, Python, etc.) auto-generates database schemas from object structure. Natural class hierarchies often map to something messy in a relational database, and data engineers may need to read the application's class code to interpret the tables.
- **API schemas.** Many vendor APIs are friendly, but plenty are thin wrappers over underlying systems — and engineers need to understand application internals to use their data.

### Detecting and handling schema changes

Schema changes in source systems are "often well out of data engineers' control." Ch 7 enumerates the usual flavours (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md):

- Adding a new column
- Changing a column type
- Creating a new table
- Renaming a column

Modern ingestion tools increasingly **auto-detect schema changes and auto-update target tables.** Ch 7 calls this a mixed blessing: it can still break pipelines downstream of staging and ingestion; even when the change is accommodated automatically, a new schema may adversely affect downstream report or model performance. Communication between producers and consumers remains as important as the automation. See [[schema-evolution]].

For streaming data, a [[schema-registry]] is the standard tool — a metadata repository that maintains schema and data-type integrity, tracks schema versions and history, and allows consistent serialization/deserialization between producers and consumers (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

### 5. Metadata

A payload often carries [[metadata]] — "data about data" — which can be as critical as the data itself. Ch 7 cites the early data-lake failure mode as the counterexample: "one of the significant limitations of the early approach to the data lake — or data swamp, which could become a data superfund site — was a complete lack of attention to metadata. Without a detailed description of the data, it may be of little value" (source: raw/fundamentals-of-data-engineering/chapter-07-ingestion.md).

## Why this decomposition matters

A single word — "payload" — hides a dense set of decisions. Decomposing into these five characteristics forces the engineer to answer concrete questions at design time:

- Does the destination understand this **kind** (deserialization support)?
- Can it handle this **shape**?
- Is this **size** transmissible, or does it need chunking / compression?
- Is the **schema** stable enough for a long-lived pipeline, or do we need schema-registry enforcement?
- Is **metadata** captured somewhere — a [[data-catalog|catalog]], file headers, event headers — or will this become a data swamp?

## Related pages

- [[data-ingestion]]
- [[encoding-formats]]
- [[compression-algorithms]]
- [[schema-evolution]]
- [[schema-registry]]
- [[metadata]]
- [[data-catalog]]
- [[object-relational-mismatch]]
