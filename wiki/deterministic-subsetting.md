# Deterministic Subsetting

**Summary**: Google's answer to the poor distribution of [[random-subsetting]] (SRE Chapter 20). Clients are divided into *rounds*, where each round contains exactly enough clients to collectively cover every backend once. Within a round, every client starts from the same shuffled backend list (shared seed) and takes a disjoint slice as its subset. Different rounds use different shuffle seeds, so load from a failing backend redistributes across the whole fleet rather than just within one subset. The result is connection counts that differ by at most one between backends — near-perfect [[subsetting|subset]] distribution.

**Sources**: `raw/site-reliability-engineering/chapter-20-load-balancing-in-the-datacenter.md`

**Last updated**: 2026-04-17

---

## The algorithm

Chapter 20 prints the Python implementation inline (source: chapter-20-load-balancing-in-the-datacenter.md):

```python
def Subset(backends, client_id, subset_size):
    subset_count = len(backends) / subset_size
    # Group clients into rounds; each round uses the same shuffled list:
    round = client_id / subset_count
    random.seed(round)
    random.shuffle(backends)
    # The subset id corresponding to the current client:
    subset_id = client_id % subset_count
    start = subset_id * subset_size
    return backends[start:start + subset_size]
```

The structure:

1. **Compute the number of subsets per round.** `subset_count = total_backends / subset_size`.
2. **Decide which round this client is in.** `round = client_id / subset_count` (integer division).
3. **Shuffle the backend list with the round number as seed.** All clients in the same round produce the *same* shuffled list; clients in different rounds produce *different* shuffled lists.
4. **Pick the client's slice.** `subset_id = client_id % subset_count` gives the client's position within the round; it takes the contiguous slice starting at `subset_id × subset_size`.

## A worked example

Chapter 20's example: 12 backends, subset size 3, 10 clients (source: chapter-20-load-balancing-in-the-datacenter.md).

- `subset_count = 12 / 3 = 4` subsets per round.
- Round 0: clients 0, 1, 2, 3 — each takes one of the 4 subsets of the round-0 shuffled list, together covering all 12 backends exactly once.
- Round 1: clients 4, 5, 6, 7 — same structure but with a round-1 shuffled list, again covering all 12 backends.
- Round 2: clients 8, 9 — incomplete round; the last two subsets of the round-2 shuffled list are unused.

Each backend ends up in the subset of two or three clients (out of 10). The difference is at most one.

## The two design choices that make it work

### Shuffling (not just slicing) within a round

Without the shuffle, each round would assign clients to consecutive backend indices. This matters when a whole range of backends becomes simultaneously unavailable — which is *the typical case* during a gradual job update, where tasks go down one after another in index order. With consecutive slices, a rolling update wipes out one client's entire subset at a time. With a shuffled list, the affected backends are scattered across subsets and the client-side pain is spread out (source: chapter-20-load-balancing-in-the-datacenter.md).

### Different seeds for different rounds

The subtle part. If every round used the *same* seed, every round's subset 0 would be the same set of backends; when a backend failed, only the clients whose subset contained it would be affected, and those clients would have to push their load onto the other backends *in that same subset*. If `N` backends in a subset fail, the load concentrates on the remaining `subset_size - N` backends — a cascade that gets worse as more backends fail.

Different seeds per round break the alignment: a failing backend ends up in a different position in every round's shuffle, so its load redistributes across *all* remaining backends, not just the members of one subset (source: chapter-20-load-balancing-in-the-datacenter.md). The chapter's phrasing: *"spread this load over all remaining backends by using a different shuffle for each round."*

## The distribution claim

For the 300 clients × 300 backends × 10% subset case that [[random-subsetting]] handled badly, deterministic subsetting gives each backend *exactly the same* number of connections (source: chapter-20-load-balancing-in-the-datacenter.md, Figure 20-5). When `total_backends` is divisible by `subset_size` and `clients` is a multiple of `subset_count`, the count is exact; when divisibility fails, Chapter 20 notes the algorithm allows a few subsets to be slightly larger and the per-backend count differs by at most 1.

## How it satisfies the three requirements

[[subsetting|Recall the requirements]]:

1. **Uniform load** — *passes*, by construction. Within a round, each subset has the same size; across rounds, each backend appears in exactly one subset per round.
2. **Low churn on restart/failure** — *passes*. When a client restarts, it recomputes its subset from the same `client_id`, `subset_size`, and `backend_list`, producing the same set of backends. When a backend disappears, only the clients whose subsets contain it lose a connection, and they replace it from the same subset logic.
3. **Graceful resizes** — *passes*, in the sense that the algorithm itself is parameter-free with respect to "did the fleet just resize?" — it's just a function of the current inputs. A resize does invalidate some assignments (as it must — some backends now belong to different subsets), but the rotation is bounded and doesn't require coordination.

## What "client_id" has to be

The algorithm needs a stable `client_id` that is the same across restarts — otherwise requirement 2 (low churn on restart) breaks. Google's infrastructure provides this via [[borg]] task IDs: a task keeps the same ID through restarts, even if it lands on a different machine. External systems would need an equivalent (e.g. hostname + slot index, or a Kubernetes StatefulSet pod name).

## The seed choice

The seed is just the round number. This is deliberately boring: it's a deterministic function of `client_id` and `subset_size`, which means every client in every copy of the binary computes the same shuffle for the same round, without needing to coordinate via a shared secret or a time-synchronised source. The RNG is a standard deterministic PRNG with the round number as seed.

## Relationship to existing wiki concepts

### Deterministic subsetting vs random subsetting

Both are *stable* per client — neither changes its subset arbitrarily on every request. The difference is coordination: random subsetting has every client choose independently; deterministic subsetting has each round's clients choose *dependently* from a shared shuffle so the aggregate covers the fleet uniformly. See [[random-subsetting]] for the comparison.

### Deterministic subsetting vs consistent hashing

[[consistent-hashing]] solves a related problem (picking a stable assignment that changes minimally under fleet change) but in a different shape: items hash to backends, and a backend change moves only items near the affected arc. Deterministic subsetting operates on *clients* rather than items, and guarantees *exact* uniformity rather than the probabilistic uniformity of consistent hashing. The two techniques could both appear in the same system — consistent hashing for request routing, deterministic subsetting for connection pooling — and Chapter 20's companion Chapter 19 does use consistent hashing in the packet-level [[network-load-balancer]].

### Deterministic subsetting and progressive rollouts

The key robustness argument — that one-at-a-time backend restarts during a push should cause minimal client-side churn — is exactly the [[change-management-sre|progressive-rollout]] scenario. Deterministic subsetting with shuffled rounds is what makes Google's continuous rollouts cheap on the connection-pool side: the algorithm is invariant to which specific task in the fleet is currently down.

### Deterministic subsetting and the monorepo

The algorithm's simplicity — 8 lines of Python — is a small instance of Chapter 9's [[virtue-of-boring]]: the problem looks like it should require coordination (ZooKeeper, gossip) but a careful choice of the *inputs to a pure function* obviates all of that. Every client runs the same function with its own `client_id` and produces a decision consistent with everyone else's.

## Related pages

- [[subsetting]]
- [[random-subsetting]]
- [[datacenter-load-balancing]]
- [[consistent-hashing]]
- [[borg]]
- [[change-management-sre]]
- [[site-reliability-engineering]]
