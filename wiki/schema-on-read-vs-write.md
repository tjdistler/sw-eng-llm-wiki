# Schema-on-Read vs Schema-on-Write

**Summary**: Schema-on-write (relational) enforces structure when data is stored; schema-on-read (document) interprets structure when data is retrieved — analogous to static vs dynamic type checking, with different trade-offs for flexibility and safety.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`

**Last updated**: 2026-04-15

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

## Related pages

- [[document-model]]
- [[relational-model]]
- [[data-models]]
- [[nosql]]
