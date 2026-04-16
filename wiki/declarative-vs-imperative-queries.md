# Declarative vs Imperative Queries

**Summary**: Declarative query languages (SQL, CSS) describe *what* result is wanted; imperative code describes *how* to compute it step by step — declarative wins in databases because it enables query optimizers, automatic parallelism, and stable behavior across implementation changes.

**Sources**: `raw/designing-data-intensive-applications/chapter-02-data-models-and-query-languages.md`

**Last updated**: 2026-04-15

---

## The distinction

**Imperative**: specify the exact steps to compute a result. The program must execute in that order.

**Declarative**: specify the *pattern* of the result you want — what conditions must hold, what transformations to apply. The system figures out how to compute it.

SQL is declarative:
```sql
SELECT * FROM animals WHERE family = 'Sharks';
```

The equivalent imperative code:
```javascript
function getSharks() {
  var sharks = [];
  for (var i = 0; i < animals.length; i++) {
    if (animals[i].family === "Sharks") {
      sharks.push(animals[i]);
    }
  }
  return sharks;
}
```

(source: chapter-02-data-models-and-query-languages.md)

## Why declarative wins in databases

### Query optimizer
A declarative language hides how the query is executed. The database engine can choose the best execution plan — which index to use, which join algorithm, in what order to apply filters. This optimization happens automatically, without any changes to the query. The query optimizer needs to be built once; every application benefits forever. (source: chapter-02-data-models-and-query-languages.md)

### Performance improvements without query changes
When the database engine improves internally (better index algorithms, new execution strategies), declarative queries benefit automatically. Imperative code is tightly coupled to the execution strategy — changing the database internals might break it.

### Parallelism
Declarative queries specify only the result pattern, not the algorithm. The database is free to use parallel execution across multiple cores or machines. Imperative code, with its explicit ordering of steps, is difficult to parallelize correctly. (source: chapter-02-data-models-and-query-languages.md)

## The same principle outside databases: CSS

CSS is a declarative language for styling. A CSS rule:

```css
li.selected > p {
  background-color: blue;
}
```

…is far superior to the equivalent imperative JavaScript DOM manipulation — not just shorter, but semantically correct: when the `selected` class is removed, CSS automatically removes the background color. Imperative code that sets a style does not know to remove it when conditions change. Browser vendors can also optimize CSS internally without breaking existing stylesheets. (source: chapter-02-data-models-and-query-languages.md)

## MapReduce: the hybrid

MapReduce is neither fully declarative nor fully imperative. It uses snippets of code (map and reduce functions) embedded in a processing framework. The logic is expressed imperatively, but the framework controls execution order and distribution.

MongoDB's MapReduce support illustrates a practical downside: writing two carefully coordinated functions is harder than writing one SQL query, and the optimizer has less room to improve performance. This is why MongoDB later added a declarative aggregation pipeline — effectively reinventing SQL in JSON syntax. (source: chapter-02-data-models-and-query-languages.md)

## Historical note

IMS and CODASYL (the pre-relational database systems) used imperative query APIs — application code iterated over records one at a time. The relational model's introduction of SQL was a decisive shift to declarative querying, and a key reason it won the "great debate" of the 1970s.

## Batch processing: from imperative to declarative

The evolution of [[batch-processing]] systems recapitulates the declarative-vs-imperative debate. Early [[mapreduce]] required writing imperative callback functions (mappers and reducers). Higher-level frameworks (Pig, Hive, Cascading) added declarative abstractions on top. Modern [[dataflow-engines]] (Spark, Flink) include cost-based query optimizers that automatically choose join algorithms and reorder joins to minimize intermediate state — the same optimization strategy used by relational databases (source: designing-data-intensive-applications, chapter 10).

When simple operations like filtering and field selection are expressed declaratively rather than as callback functions, the engine can take advantage of [[column-oriented-storage]] layouts (reading only needed columns) and vectorized execution (tight CPU-cache-friendly loops). Spark generates JVM bytecode and Impala uses LLVM native code for these inner loops (source: designing-data-intensive-applications, chapter 10).

The result is convergence: batch frameworks gain declarative query languages and optimizers, while MPP databases become more programmable with user-defined functions. See [[hadoop-vs-mpp-databases]] (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[relational-model]]
- [[graph-data-models]]
- [[data-models]]
- [[nosql]]
- [[batch-processing]]
- [[dataflow-engines]]
- [[hadoop-vs-mpp-databases]]
- [[mapreduce]]
