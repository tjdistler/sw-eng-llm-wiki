# Unix Philosophy

**Summary**: The Unix philosophy is a set of design principles from the 1970s — make each program do one thing well, use a uniform interface, separate logic from wiring, and favor composability — that remain remarkably relevant to modern distributed data systems.

**Sources**: `raw/designing-data-intensive-applications/chapter-10-batch-processing.md`

**Last updated**: 2026-04-15

---

## The four principles

Doug McIlroy, inventor of Unix pipes, described them in 1964 as "connecting programs like a garden hose." The Unix philosophy was formalized in 1978 (source: designing-data-intensive-applications, chapter 10):

1. **Make each program do one thing well.** Build a new tool rather than adding features to an existing one.
2. **Expect the output of every program to become the input to another.** Don't clutter output; avoid binary or columnar formats; don't require interactive input.
3. **Design and build software to be tried early** — within weeks. Don't hesitate to throw away clumsy parts.
4. **Use tools in preference to unskilled help** to lighten a programming task, even if you have to build the tools.

This approach — automation, rapid prototyping, incremental iteration, friendliness to experimentation — anticipates Agile and DevOps by four decades (source: designing-data-intensive-applications, chapter 10).

## Enabling composability

### Uniform interface

All Unix programs use the same interface: an ordered sequence of bytes (a file descriptor). This same interface represents files, pipes, sockets, device drivers, and TCP connections. By convention, most tools treat the byte stream as ASCII text with newline-separated records (source: designing-data-intensive-applications, chapter 10).

The downside: parsing is ad hoc. Extracting the URL from a log line requires `{print $7}` rather than `{print $request_url}`. There is no schema (source: designing-data-intensive-applications, chapter 10).

In [[mapreduce]] and [[distributed-filesystems]], the uniform interface is files on HDFS. In [[dataflow-engines]], the interface includes pipe-like data transport mechanisms between operators (source: designing-data-intensive-applications, chapter 10).

### Separation of logic and wiring

Unix tools use stdin and stdout by default. A shell user wires inputs and outputs; the program doesn't know or care where data comes from or goes. This is a form of **loose coupling**, **late binding**, or **inversion of control** (source: designing-data-intensive-applications, chapter 10).

MapReduce follows the same principle: input and output directories are configured externally, separating the "what to compute" from the "where to read/write" (source: designing-data-intensive-applications, chapter 10).

### Transparency and experimentation

Unix tools succeed partly because they make it easy to see what's happening (source: designing-data-intensive-applications, chapter 10):

- Input files are treated as immutable — run commands repeatedly without damaging data.
- Pipe output into `less` to inspect intermediate results.
- Write intermediate output to a file and restart later stages without rerunning everything.

These same properties carry over to [[batch-processing]] systems: immutable inputs, replaceable outputs, and the ability to rerun jobs for debugging.

## Carrying the philosophy forward

| Unix | Hadoop/Batch processing |
|---|---|
| stdin/stdout | HDFS files |
| Pipes | Chained MapReduce jobs or dataflow operators |
| Newline-separated text | Structured formats: [[encoding-formats\|Avro]], Parquet |
| `sort` utility | MapReduce shuffle and sort |
| Small single-purpose tools | Map and reduce functions / operators |

Hadoop improves on Unix in one key area: structured file formats like Avro and Parquet eliminate the ad hoc text parsing that Unix tools require, while supporting [[schema-evolution]] (source: designing-data-intensive-applications, chapter 10).

## Limitations

The biggest limitation of Unix tools is that they run on a single machine. [[mapreduce]] and [[distributed-filesystems]] extend the same philosophy to thousands of machines (source: designing-data-intensive-applications, chapter 10).

## Related pages

- [[batch-processing]]
- [[mapreduce]]
- [[dataflow-engines]]
- [[distributed-filesystems]]
- [[declarative-vs-imperative-queries]]
