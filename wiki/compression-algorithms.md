# Compression Algorithms

**Summary**: Compression shrinks data on disk and on the wire, trading CPU time for storage and bandwidth. For data engineering, the common algorithms — **gzip, bzip2, Snappy, LZ4, LZMA, zstd** — sit on a spectrum from fast-and-weak to slow-and-strong, and the right choice depends on whether the workload is storage-bound, network-bound, or CPU-bound.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-06-storage.md`

**Last updated**: 2026-04-18

---

## Why compression matters in data storage

Chapter 6 frames compression as one of the **raw storage ingredients** and names three distinct wins (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md):

1. **Smaller on disk.** Direct storage-cost reduction.
2. **Higher effective scan speed.** A 10:1 compression ratio turns a 300 MB/s HDD into a 3 GB/s logical pipe.
3. **Higher effective network bandwidth.** A 10 Gbps EC2-to-S3 link delivers 100 Gbps of logical payload at 10:1.

The cost is CPU cycles to compress and decompress. Choice of algorithm is a three-way trade among ratio, speed, and compatibility.

## The common algorithms

Chapter 6 names the shortlist every data engineer sees (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). A rough positioning:

| Algorithm | Compression ratio | Speed | Typical role |
|---|---|---|---|
| **gzip** | Medium | Medium | Ubiquitous; HTTP, Parquet, OS tooling |
| **bzip2** | Higher than gzip | Slow | Archival; splittable in MapReduce |
| **Snappy** | Low | Very fast | Columnar files (Parquet default), RPC |
| **LZ4** | Low | Fastest | In-memory compression, streaming, caches |
| **LZMA** | Very high | Very slow | Archival (.xz), software distribution |
| **zstd** | High; tunable | Fast; tunable | Modern replacement for gzip; widely adopted in 2020s (Kafka, Parquet) |

(Reis and Housley defer detailed algorithm commentary to Appendix A; the characterisations above reflect standard industry usage.)

## How to choose

The decision reduces to what is scarce in the workload:

- **CPU-bound processing** (fast query engines, streaming) — prefer **Snappy** or **LZ4**: minimal CPU overhead, willing to trade compression ratio.
- **Storage-bound long-term retention** — prefer **zstd** (modern) or **gzip** (legacy compatibility): higher ratios matter more than decompression speed when accesses are rare.
- **Archival / cold storage** — **LZMA** or **bzip2**: best ratio, speed is irrelevant.
- **Network-bound cross-region transfer** — **zstd** has become the default sweet spot; high ratio at reasonable speed.

Columnar formats like [[column-oriented-storage|Parquet]] compose these with per-column encoding (bitmap, run-length, dictionary). The outer compression algorithm is applied *after* the columnar encoding, which is already highly compressible — so the algorithmic choice matters less than the codec configuration.

## Splittability

A subtle concern for [[batch-processing]]: frameworks like MapReduce and Spark want to split input files into independent chunks for parallel processing. **gzip is not splittable**; **bzip2 is**. **Snappy and LZ4 inside container formats like Parquet are effectively splittable** because the container handles chunking. Choosing a non-splittable compressor on a multi-hundred-GB file can force sequential processing of the whole thing.

## The overhead

Chapter 6 is explicit that compression is not free: "Compressing and decompressing data entails extra time and resource consumption to read or write data" (source: raw/fundamentals-of-data-engineering/chapter-06-storage.md). The engineer should benchmark against the specific workload — synthetic benchmarks understate real-world decompression cost on highly repetitive data.

## Related pages

- [[storage-raw-ingredients]]
- [[column-oriented-storage]]
- [[encoding-formats]]
- [[data-storage-stage]]
- [[object-storage]]
