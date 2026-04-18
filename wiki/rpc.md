# Remote Procedure Calls (RPC)

**Summary**: Remote Procedure Call (RPC) tries to make a network request look like a local function call. This abstraction is fundamentally leaky — networks behave very differently from local function calls — and the attempt to hide that difference causes subtle bugs. Modern RPC frameworks are more explicit about the difference; REST rejects the abstraction entirely.

**Sources**: `raw/designing-data-intensive-applications/chapter-04-encoding-and-evolution.md`, `raw/site-reliability-engineering/chapter-02-the-production-environment-at-google-from-the-viewpoint-of-an-sre.md`

**Last updated**: 2026-04-17

---

## What RPC Is

RPC has existed since the 1970s. The idea: a client calls a function; the framework transparently encodes the call, sends it over the network to a server, executes the function there, encodes the result, sends it back, and returns it to the caller. This abstraction is called **location transparency** — the caller need not know where the function runs.

Historical examples: Sun RPC/NFS, CORBA, DCOM, Java RMI, EJB.

## Why the Abstraction Leaks

Network calls are fundamentally different from local function calls in ways that cannot be hidden:

| Local function call | Network request |
|---|---|
| Predictable: succeeds or fails based on parameters | Unpredictable: network can lose request, response, or both |
| Returns a result or throws an exception | Can return nothing (timeout) — you don't know if it ran |
| Idempotent by default | Retrying may execute the action twice unless idempotence is explicit |
| Consistent latency | Wildly variable latency — sub-millisecond to many seconds |
| Passes object references (pointers) | Must encode all parameters as bytes — large objects are expensive |
| Single language | Client and server may use different languages with incompatible type systems |

Because of these differences, writing a remote call that looks identical to a local call misleads the programmer. Error handling, retry logic, timeout handling, and idempotence all require explicit attention that the local-call model hides.

## REST: Embracing the Network

REST (Representational State Transfer) is a design philosophy built on HTTP rather than an attempt to abstract it away. Key principles:

- Simple data formats (typically JSON).
- URLs identify resources.
- HTTP features used directly: cache control, authentication, content negotiation.
- HTTP methods carry semantic meaning (GET, POST, PUT, DELETE).

REST does not hide that it's a network protocol. This is the source of its advantages:

- **Debuggable**: any HTTP client (`curl`, browser, Postman) can call a REST API without code generation or special tooling.
- **Universal**: supported by every language and platform.
- **Ecosystem**: caches, load balancers, proxies, firewalls, monitoring tools all understand HTTP.
- **Human-readable**: JSON responses can be inspected directly.

REST is the dominant style for **public APIs** and cross-organizational service integration.

**SOAP** is the opposing approach: an XML-based protocol that aims to be independent of HTTP and defines its own standards (WS-*) for everything. It requires WSDL schema files and code generation. It was popular in large enterprises but has fallen out of favor because of complexity and poor interoperability across vendor implementations.

## Modern RPC Frameworks

Despite the critique, RPC is not dead. Modern frameworks are explicit about the fact that remote calls are different:

- **gRPC**: uses Protocol Buffers for encoding; supports streaming (a call can be a series of requests and responses over time, not just one round trip).
- **Thrift RPC** and **Avro RPC**: encoding and RPC support are bundled together.
- **Finagle** and **Rest.li**: use futures/promises to make the asynchronous, fallible nature of network calls explicit in the type system.
- **gRPC** also supports service discovery.

Custom binary RPC protocols (gRPC, Thrift RPC) can achieve better performance than JSON over REST. The main focus of RPC frameworks is **intra-organization, intra-datacenter service communication**, where the performance advantage matters and the ecosystem support requirement is lower.

## Compatibility for RPC Services

For evolving RPC services without downtime, servers are typically updated before clients. This means:

- Requests need **backward compatibility** (servers must accept old client requests).
- Responses need **forward compatibility** (old clients must tolerate new server responses).

The compatibility properties are inherited from the encoding format:
- **Thrift, gRPC (Protocol Buffers), Avro RPC**: compatibility follows the rules of the respective format. See [[schema-evolution]].
- **REST with JSON**: adding optional request parameters and new response fields is typically safe. No formal schema means compatibility is enforced by convention, not tooling.

**API versioning** is an unsolved problem. Common approaches for REST: version number in the URL (`/v2/users`), or in the HTTP `Accept` header. For APIs using API keys, the preferred version can be stored server-side per client. RPC frameworks generally rely on the schema compatibility rules to avoid explicit versioning.

## Service Compatibility Across Organizations

When a service is public or crosses organizational boundaries, the provider has no control over clients and cannot force upgrades. Compatibility must be maintained for a long time — possibly indefinitely. This often requires maintaining multiple API versions side by side.

## RPC as the default inside Google

The SRE book's Chapter 2 frames RPC use at Google more aggressively than Kleppmann's "when you need it" stance (source: site-reliability-engineering, chapter 2):

> Often, an RPC call is made even when a call to a subroutine in the local program needs to be performed. This makes it easier to refactor the call into a different server if more modularity is needed, or when a server's codebase grows.

All Google services communicate via [[stubby|Stubby]], whose open-source release is gRPC; data on the wire is [[protocol-buffers|protocol-buffer]]-encoded. [[gslb|GSLB]] load-balances RPCs the same way it load-balances externally visible services. The SRE book also inverts the usual RPC vocabulary: inside a service, the caller is the **frontend** (client) and the callee is the **backend** (server), regardless of who is browser-facing.

The Google style is a design stance in favour of [[independent-deployability]]: even in-process modularity gets expressed as an RPC boundary so it can later be moved across machines without refactoring.

SRE Chapter 20 further shows that Stubby is not just a wire protocol: it also implements [[backend-task-states|backend state propagation]] (including [[lame-duck-state|graceful shutdown via lame duck]]), [[subsetting|per-client backend subsetting]], and [[load-balancing-policies|client-side load balancing]] culminating in [[weighted-round-robin]]. These are "RPC framework responsibilities" in Google's stance, not per-service concerns — which is what lets [[change-management-sre|rolling deployments]] be non-disruptive across every Google service by default.

## Related pages

- [[backward-forward-compatibility]]
- [[encoding-formats]]
- [[schema-evolution]]
- [[message-brokers]]
- [[microservices]]
- [[idempotence]]
- [[stubby]]
- [[protocol-buffers]]
- [[gslb]]
