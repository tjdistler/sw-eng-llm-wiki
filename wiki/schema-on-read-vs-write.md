# Schema-on-Read vs Schema-on-Write

**Summary**: Schema-on-write (relational) enforces structure when data is stored; schema-on-read (document) interprets structure when data is retrieved — analogous to static vs dynamic type checking, with different trade-offs for flexibility and safety.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`, `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## The distinction

**Schema-on-write** (relational databases): the schema is explicit and enforced at write time. Every row stored must conform to the defined columns and types. The database rejects data that doesn't match.

**Schema-on-read** (document databases): there is no schema enforcement. Data is written freely; the code reading the data imposes structure at read time by assuming fields exist. The database accepts anything.

Neither is "schemaless" in practice — document databases still have an implicit schema assumed by application code. The question is *when and where* that schema is enforced. (source: chapter-02-data-models-and-query-languages.md)

## The programming language analogy

| Database | Language equivalent |
|---|---|
| Schema-on-write | Static typing (compile-time type checking) |
| Schema-on-read | Dynamic typing (runtime type checking) |

The decades-long debate between static and dynamic typing has an exact parallel in the databases world. Neither is universally superior. (source: chapter-02-data-models-and-query-languages.md)

## Schema migration comparison

**Changing a field in a document database** — write new documents with the new structure; handle old documents in application code:

```javascript
if (user && user.name && !user.first_name) {
  user.first_name = user.name.split(" ")[0];
}
```

**Changing a field in a relational database** — run a migration:

```sql
ALTER TABLE users ADD COLUMN first_name text;
UPDATE users SET first_name = split_part(name, ' ', 1);
```

Most relational databases execute `ALTER TABLE` in milliseconds. MySQL is an exception — it copies the entire table, causing downtime on large tables. (source: chapter-02-data-models-and-query-languages.md)

## When schema-on-read is the right choice

- **Heterogeneous records** — collection items don't all have the same structure (e.g., many subtypes of events)
- **External data sources** — the data format is controlled by an external system that may change unpredictably
- **Rapid iteration** — schema changes would be disruptive to the development process

## When schema-on-write is the right choice

- **Uniform structure** — all records are expected to have the same fields
- **Documentation value** — explicit schemas serve as machine-checked documentation
- **Data quality enforcement** — the database should reject bad data, not propagate it

## FoDE Ch 6 — schema at the storage layer

Chapter 6 of *Fundamentals of Data Engineering* reframes the distinction for data engineers working on lakes and lakehouses (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

- **Schema on write** is "essentially the traditional data warehouse pattern: a table has an integrated schema; any writes to the table must conform." For a data lake to support schema on write, it must integrate a **schema metastore** — a central record of what schema each table has.
- **Schema on read** is "the schema is dynamically created when data is written, and a reader must determine the schema when reading the data." Ideally the on-disk file format carries its own schema — Parquet and JSON do, CSV notoriously does not. Chapter 6 is explicit: "CSV files are notorious for schema inconsistency and are not recommended in this setting."

Chapter 6's trade-off framing:

- **Schema on write** enforces data standards — data is easier to consume and utilise downstream.
- **Schema on read** prioritises flexibility — virtually any data can be written — at the cost of making future consumption harder.

### The lakehouse compromise

The emergence of [[data-lakehouse|data lakehouses]] and their [[lakehouse-table-formats|table formats]] (Delta Lake, Iceberg, Hudi) represents a practical merger: the underlying files are Parquet (a schema-bearing columnar format), but the metadata layer **imposes schema-on-write guarantees on tables that opt into them**, while leaving the bucket also open to schema-on-read or even unstructured files.

This is why Chapter 6 describes schema as a "Rosetta stone" — the schema can be more or less strict depending on the consumer's needs, and a lakehouse lets the engineer pick per table rather than per bucket.

### Schema is broader than relational

Chapter 6 emphasises that schema does not mean "relational table" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

> Schema need not be relational. Rather, data becomes more useful when we have as much information about its structure and organization. For images stored in a data lake, this schema information might explain the image format, resolution, and the way the images fit into a larger hierarchy.

A lake of videos has a schema in this sense — codec, resolution, frame rate, the taxonomy of what the videos depict. The catalog records this schema even though no SQL table exists.

## Related pages

- [[document-model]]
- [[relational-model]]
- [[data-models]]
- [[nosql]]
- [[data-lake]]
- [[data-lakehouse]]
- [[lakehouse-table-formats]]
- [[data-catalog]]
- [[schema-evolution]]
- [[encoding-formats]]
- [[column-oriented-storage]]
