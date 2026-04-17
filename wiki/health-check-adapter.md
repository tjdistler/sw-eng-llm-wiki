# Health Check Adapter

**Summary**: The third canonical application of the [[adapter-pattern]]: using an adapter container to expose a rich, application-specific health check to a container orchestrator that otherwise would see only "is the process running." Worked example: a Go adapter that runs a workload-representative SQL query against a sibling MySQL container and exposes the result as an HTTP health endpoint.

**Sources**: `raw/designing-distributed-systems/chapter-04-adapters.md`, `raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md`

**Last updated**: 2026-04-16

---

## The problem

Container orchestrators like Kubernetes health-check pods in standard ways: is the process running, is a given port open, does an HTTP endpoint return 200. These checks tell you the container has not crashed, but not much more (source: raw/designing-distributed-systems/chapter-04-adapters.md).

Deep health — "is this database actually serving queries correctly under a workload representative of our application?" — requires running application-specific diagnostics. For an off-the-shelf database container supplied by the upstream project, there are two unattractive options:

1. **Modify the image** to embed a health-check script. This forks the upstream image and creates a maintenance debt every time a new upstream version comes out.
2. **Ship a shell-script health check inside the orchestrator spec.** Kubernetes does allow this, but now the script lives outside version control with the application, is hard to maintain, and can't easily contain binary dependencies (database drivers, TLS certificates, etc.).

## The adapter solution

Deploy the health check as an **adapter container** alongside the application (source: raw/designing-distributed-systems/chapter-04-adapters.md):

- The application container (e.g. `mysql`) is used unmodified from the upstream image.
- The adapter container contains the health-check logic — arbitrary binary, script, or small service — and exposes a standard probe endpoint (usually HTTP).
- The orchestrator's health check is configured against the adapter's endpoint.
- If the check fails, the orchestrator restarts the (application container, or the pod, per the orchestrator's rules).

Because the two containers share the pod's network namespace, the adapter can reach the database on `localhost` with no extra configuration.

This solves both problems cleanly: the application image is untouched, and the health-check code lives in a proper, versioned, testable, containerised artefact that can be developed and shipped on its own cadence.

## Hands-on: rich MySQL health checks in Go

Chapter 4 walks through a minimal Go adapter that runs a parameterised SQL query against a sibling MySQL container and exposes the result as an HTTP health endpoint (source: raw/designing-distributed-systems/chapter-04-adapters.md):

```go
package main

import (
    "database/sql"
    "flag"
    "fmt"
    "net/http"

    _ "github.com/go-sql-driver/mysql"
)

var (
    user   = flag.String("user", "", "The database user name")
    passwd = flag.String("password", "", "The database password")
    db     = flag.String("database", "", "The database to connect to")
    query  = flag.String("query", "", "The test query")
    addr   = flag.String("address", "localhost:8080", "The address to listen on")
)

func main() {
    flag.Parse()
    db, err := sql.Open("localhost",
        fmt.Sprintf("%s:%s@/%s", *user, *passwd, *db))
    if err != nil {
        fmt.Printf("Error opening database: %v", err)
    }
    http.HandleFunc("", func(res http.ResponseWriter, req *http.Request) {
        _, err := db.Exec(*query)
        if err != nil {
            res.WriteHeader(http.StatusInternalServerError)
            res.Write([]byte(err.Error()))
            return
        }
        res.WriteHeader(http.StatusOK)
        res.Write([]byte("OK"))
    })
    http.ListenAndServe(*addr, nil)
}
```

Wrapped into an image and dropped into a pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: adapter-example-health
  namespace: default
spec:
  containers:
  - image: mysql
    name: mysql
  - image: brendanburns/mysql-adapter
    name: adapter
```

The MySQL container is the unmodified upstream image; the adapter exposes an HTTP endpoint that succeeds only if the representative query runs successfully against the sibling MySQL process. The orchestrator is configured to probe the adapter's endpoint.

The adapter is parameterised (user, password, database, query, listen address), which is the [[modular-reusable-containers]] discipline in action: one adapter image works for any MySQL deployment with any workload-representative query.

## The modularity argument

Burns anticipates the "couldn't we just build one custom image with the health check baked in?" response and answers it with an argument that applies to the whole adapter pattern (source: raw/designing-distributed-systems/chapter-04-adapters.md):

> If every developer implements their own specific container with health checking built in, there are no opportunities for reuse or sharing. In contrast, if we use patterns like the adapter to develop modular solutions comprised of multiple containers, the work is inherently decoupled and more easily shared.

A public `brendanburns/mysql-adapter` image (or any community equivalent) lets anyone add rich MySQL health checks to their deployment without understanding MySQL internals deeply. The pattern becomes a way to package and distribute operational expertise.

## Relationship to existing wiki concepts

### Health checks and the adapter pattern

This is the third of three canonical adapter applications in Chapter 4; the other two are [[unified-monitoring-interface]] and [[log-normalization]]. All three share the adapter-pattern structure.

### Health checks and monitoring

A health check is a narrow, orchestrator-facing view into an application's readiness to serve traffic. Richer application metrics usually go through the [[unified-monitoring-interface]] adapter path — the two adapter kinds complement each other.

### Liveness vs readiness: which probe is this?

Chapter 5 makes an operational distinction that Chapter 4's example leaves implicit: container orchestrators run two different kinds of probes. A **liveness** probe decides when to restart a container; a **readiness** probe decides when to include a replica in the load-balancer pool (source: raw/designing-distributed-systems/chapter-05-replicated-load-balanced-services.md). See [[health-probes]] for the full distinction.

The Chapter 4 Go/MySQL adapter — running a representative SQL query against the sibling MySQL container — can legitimately drive either probe, but the two uses have different failure characteristics:

- As a **readiness** probe, it is exactly right: the replica should not receive traffic until real queries work against the real database.
- As a **liveness** probe, the same check is more aggressive. If the query fails because of a transient database issue rather than a permanent one, the orchestrator restarts the container — throwing away whatever warm state it had. For liveness, a narrower "is the adapter process itself alive" check is usually safer.

The adapter container shape supports either configuration; the orchestrator spec decides which probe points at which endpoint. When in doubt, use richer adapter checks for readiness and cheaper checks for liveness.

### Health checks and desired-state management

Newman's [[desired-state-management]] page describes orchestrators that continuously reconcile observed state with declared state. Health checks are the observability half of that loop: they tell the orchestrator when the observed state has diverged. A deep, application-specific health check is what lets the declarative loop act on meaningful signals rather than just "the process is still alive."

### Health checks and modular reusable containers

Because a single health-check adapter is reused across many deployments of the same application type, the [[modular-reusable-containers]] discipline — parameterize, define the API surface, document — applies especially strongly. The Chapter 4 example already parameterises everything configuration-dependent through command-line flags.

### Health checks and legacy modernization

Bolting rich health checks onto an unmodified legacy application — including vendor-supplied database images — is a [[legacy-modernization]] task. The health-check adapter achieves it without touching the legacy image.

## Related pages

- [[adapter-pattern]]
- [[unified-monitoring-interface]]
- [[log-normalization]]
- [[monitoring-and-observability]]
- [[desired-state-management]]
- [[modular-reusable-containers]]
- [[legacy-modernization]]
- [[pod]]
- [[health-probes]]
- [[replicated-load-balanced-service]]
- [[designing-distributed-systems]]
