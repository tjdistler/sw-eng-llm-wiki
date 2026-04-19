# Graph Data Models

**Summary**: Graph databases model data as vertices and edges, making highly interconnected data natural to represent and traverse — where the relational model becomes awkward and the document model breaks down entirely.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`, `raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md`

**Last updated**: 2026-04-18

---

## When to use a graph model

The choice of data model tracks relationship density:
- **No or few relationships** → [[document-model]]
- **Many-to-many relationships** → [[relational-model]]
- **Highly interconnected, everything potentially related to everything** → graph model

Real-world examples: social networks, the web (pages linked by URLs), road networks, knowledge graphs. Facebook's social graph uses a single graph with vertices for people, locations, events, checkins, and comments — and edges for every kind of relationship between them. (source: chapter-02-data-models-and-query-languages.md)

## Property graph model

The dominant graph model, implemented by Neo4j, Titan, and InfiniteGraph.

**Vertex** contains:
- A unique identifier
- A set of outgoing edges
- A set of incoming edges
- A collection of key-value properties

**Edge** contains:
- A unique identifier
- Tail vertex (where the edge starts)
- Head vertex (where the edge ends)
- A label describing the relationship type
- A collection of key-value properties

This can be expressed in relational terms as two tables — `vertices` and `edges` — but the graph model makes traversal natural in a way the relational encoding does not. (source: chapter-02-data-models-and-query-languages.md)

### Key strengths of the property graph model

1. **No schema restrictions**: any vertex can connect to any other vertex
2. **Bidirectional traversal**: indexes on both head and tail vertices enable efficient forward and backward navigation
3. **Multiple relationship types in one graph**: different edge labels keep data clean while allowing heterogeneous relationships
4. **Evolvability**: extending a graph for new features is easy — add vertices, add edge types

### Cypher

Cypher is the declarative query language for property graphs, created for Neo4j. Pattern matching syntax uses arrows:

```cypher
(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (us:Location {name:'United States'})
```

`WITHIN*0..` means "follow zero or more WITHIN edges" — variable-length traversal expressed concisely. The same query in SQL requires recursive common table expressions (`WITH RECURSIVE`) and around 29 lines. (source: chapter-02-data-models-and-query-languages.md)

## Triple-store model

An alternative representation where all data is stored as three-part statements: `(subject, predicate, object)`. Implementations include Datomic and AllegroGraph.

The object is either:
- A **primitive value** — in which case predicate/object act as a key-value property on the subject vertex
- **Another vertex** — in which case the predicate is an edge label

Example in Turtle format:
```
_:lucy a :Person; :name "Lucy"; :bornIn _:idaho.
_:idaho a :Location; :name "Idaho"; :type "state"; :within _:usa.
```

### RDF and the semantic web

RDF (Resource Description Framework) is a triple-store standard designed for internet-wide data exchange. It uses URIs as predicates to avoid naming conflicts when combining data from different sources. The semantic web vision — a machine-readable web of data — was overhyped in the early 2000s and hasn't materialized, but the triple-store model is still valuable for internal application data. (source: chapter-02-data-models-and-query-languages.md)

### SPARQL

SPARQL is the query language for RDF triple-stores. It predates Cypher, and Cypher's pattern matching borrows from it. The same people-who-emigrated query:

```sparql
SELECT ?personName WHERE {
  ?person :name ?personName.
  ?person :bornIn  / :within* / :name "United States".
  ?person :livesIn / :within* / :name "Europe".
}
```

### Datalog

Datalog is older than both Cypher and SPARQL (studied academically in the 1980s), and is the foundation later languages build on. It is the query language of Datomic.

Datalog defines *rules* — derived predicates built from other rules or stored facts. Queries are built up step by step, making it powerful for complex, reusable logic. It requires a different mental model but handles complex data well. (source: chapter-02-data-models-and-query-languages.md)

## Graph databases vs CODASYL

CODASYL (the 1970s network model) superficially resembles graph databases but differs critically:

| CODASYL | Graph DB |
|---|---|
| Schema restricts which records can link | Any vertex can connect to any other |
| Only access via predefined access paths | Direct access by vertex ID or index |
| Children are ordered sets | No ordering (sort at query time) |
| Imperative queries only | Declarative languages (Cypher, SPARQL) |

Graph databases are not CODASYL in disguise. (source: chapter-02-data-models-and-query-languages.md)

## Batch processing on graphs

Beyond OLTP-style graph queries, graphs can be analyzed in batch using offline algorithms like PageRank. The Pregel/BSP (Bulk Synchronous Parallel) model provides an efficient vertex-centric abstraction where vertices exchange messages in synchronized rounds. Implementations include Apache Giraph, Spark's GraphX, and Flink's Gelly. See [[graph-batch-processing]] for details (source: designing-data-intensive-applications, chapter 10).

## As a source system (Reis & Housley)

From the data engineer's perspective, a graph database introduces a modelling gap: most downstream analytics tooling assumes rows-and-columns or nested-JSON data, not vertices and edges. Reis and Housley's Chapter 5 of *Fundamentals of Data Engineering* names three choices when a graph database is a source (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md):

- **Map the graph into an existing paradigm.** Flatten vertices into rows; encode edges in a join table. Works for many analytics use cases but loses the traversal-native advantages of the source.
- **Analyze inside the source.** Run analytics in the graph database directly, either on the OLTP store (risky — may impact production) or on a purpose-built graph-analytics engine.
- **Adopt graph-specific analytics tools.** Use a tool that speaks SPARQL / Cypher / GQL natively and meets graph queries on their own terms.

Reis and Housley anticipate rapid growth in graph-database adoption outside tech companies, so the data engineer's job increasingly includes building extraction and modelling paths for graph sources (source: raw/fundamentals-of-data-engineering/chapter-05-data-generation-in-source-systems.md).

## Related pages

- [[data-models]]
- [[relational-model]]
- [[document-model]]
- [[declarative-vs-imperative-queries]]
- [[graph-batch-processing]]
- [[batch-processing]]
- [[source-systems]]
- [[nosql]]
