# Life of a Request

**Summary**: The end-to-end trace of a user request through Google's production stack, using the Chapter 2 Shakespeare example as the worked case. Every major piece of Google infrastructure — DNS, [[gslb|GSLB]], [[google-frontend|GFE]], [[stubby|Stubby]]/[[protocol-buffers|protobuf]], [[bigtable]], [[bns|BNS]] — appears in a single call chain.

**Sources**: `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## The scenario

Shakespeare is a hypothetical Google service: given a word, it returns the locations where Shakespeare used it. The system has two parts (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

- A **batch component** — a [[mapreduce|MapReduce]] job that reads Shakespeare's texts, builds an index, and writes rows to [[bigtable]] keyed by word. Runs infrequently.
- An **always-up application frontend** — serves user queries.

The batch component itself is a classic map-sort-reduce pipeline: mapping splits text into words, shuffle sorts by word, reduce produces `(word, list-of-locations)` tuples, each written as a Bigtable row.

## The request trace

When a user asks `shakespeare.google.com` for a word, the trace runs like this (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md):

1. **DNS.** Browser resolves `shakespeare.google.com`. The resolver eventually reaches Google's DNS server, which consults [[gslb|GSLB]]; GSLB picks a frontend IP based on load distribution across regions.
2. **TCP termination.** The browser opens a TCP connection to that IP. A **[[google-frontend|Google Frontend (GFE)]]** terminates it. The GFE is a reverse proxy.
3. **Service routing.** The GFE identifies the service (Shakespeare, in this case), consults [[gslb|GSLB]] again to find an available Shakespeare **frontend** server, and sends it the HTML request as a [[stubby|Stubby]] RPC.
4. **Frontend → backend.** The Shakespeare frontend builds a [[protocol-buffers|protobuf]] request containing the word to look up. It consults [[gslb|GSLB]] for a suitable unloaded Shakespeare **backend** server via [[bns|BNS]].
5. **Backend → Bigtable.** The Shakespeare backend calls a [[bigtable]] server to read the row for that word.
6. **Return.** Bigtable returns the locations → backend packs them into a reply protobuf → frontend assembles the HTML → user's browser renders it.

Whole round trip: hundreds of milliseconds.

## What to notice

- **Every hop goes through [[gslb|GSLB]].** DNS, GFE → frontend, frontend → backend — GSLB chooses a peer at every level. GSLB is therefore a critical dependency; "a failing GSLB would wreak havoc" (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).
- **Addresses are logical, not physical.** [[bns|BNS]] resolves logical names to `IP:port` at call time, so [[borg]] is free to move tasks around underneath.
- **Intra-process modularity crosses the RPC boundary.** "Often, an RPC call is made even when a call to a subroutine in the local program needs to be performed." Frontend-vs-backend is an RPC boundary even within one logical service (source: chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md).
- **Graceful degradation holds it together.** Careful rollouts, rigorous testing, and graceful-degradation defaults are what prevent the many potential failure points in the chain from aggregating into outages.

## Sizing the system: 37 tasks

The chapter follows the trace with a sizing calculation: at 100 QPS per backend and 3,470 QPS peak, you need 35 tasks, and [[n-plus-2-redundancy|N + 2]] rounds that to 37. Regional distribution then breaks the 37 into 17 in the USA, 16 in Europe, 6 in Asia, and 4 in South America (the last using N + 1 to save 20% of hardware cost). [[bigtable]] is replicated per region to keep data-access latency low.

## Cross-book connections

- [[replicated-load-balanced-service]] (Burns) — the container-level pattern for each tier in the trace (frontends and backends are both instances of it).
- [[scatter-gather-pattern]] (Burns) — not used in the Shakespeare trace, but the natural next step when a backend has to query many Bigtable shards in parallel.
- [[tail-latency-amplification]] (Burns) — the hidden tax on a chain this deep; each intermediate hop's tail compounds.
- [[fallacies-of-distributed-computing]] — the trace implicitly respects most of the fallacies; the "latency is zero" one is the most obviously load-bearing here.

## Related pages

- [[gslb]]
- [[google-frontend]]
- [[stubby]]
- [[protocol-buffers]]
- [[bns]]
- [[bigtable]]
- [[borg]]
- [[n-plus-2-redundancy]]
- [[site-reliability-engineering]]
