# Modular, Reusable Containers

**Summary**: The design discipline required to make containers — sidecars, ambassadors, adapters, and other add-on containers — reusable across applications and deployments. Burns identifies three focus areas: parameterize the container, define its API surface deliberately, and document it. Without these, the modularity promise of the [[sidecar-pattern]], [[ambassador-pattern]], and [[adapter-pattern]] does not pay off.

**Sources**: `raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md`, `raw/designing-distributed-systems/chapter-03-ambassadors.md`, `raw/designing-distributed-systems/chapter-04-adapters.md`

**Last updated**: 2026-04-16

---

## Why discipline is needed

Sidecars are only valuable if they can be reused across many applications. A single-use sidecar is often no cheaper than in-process code. Burns's argument is that achieving reuse — "just like achieving modularity in high-quality software development" — requires focus and discipline on three fronts (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

1. Parameterize your containers.
2. Define each container's API surface.
3. Document your containers.

Each is covered below.

## 1. Parameterize the container

Burns's framing: **think of the container as a function, and its parameters as the function's arguments** (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md). Each parameter customizes a generic container for a specific deployment.

For an nginx HTTPS sidecar, reasonable parameters include:

- The path to the TLS certificate.
- The port of the legacy application on localhost.

Without these, the container is hard-coded and unusable for anything else.

### How to pass parameters

Two mechanisms are available: environment variables and command-line arguments. Burns prefers environment variables (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

```
docker run -e=PROXY_PORT=8080 -e=CERTIFICATE_PATH=/path/to/cert.crt ...
```

Inside the container, a small shell entrypoint typically reads the env vars and templates them into a config file (e.g. `nginx.conf`) or passes them to the main binary.

## 2. Define the container's API surface

Parameterizing the container immediately creates an API: every parameter is part of it. But Burns stresses that the API is broader than just parameters (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

> All aspects of how your container interacts with its world are part of the API defined by that reusable container.

That includes:

- Environment variables / CLI flags the container accepts.
- HTTP and other protocol endpoints the container exposes.
- Calls the container makes to other services.
- Files the container expects to find or produces on the shared filesystem.
- Signals the container sends to the application container.

### Breaking changes can be subtle

Burns walks through a configuration-sync sidecar with an `UPDATE_FREQUENCY` parameter to illustrate how easy it is to break consumers without noticing (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

- **Obvious break**: renaming `UPDATE_FREQUENCY` to `UPDATE_PERIOD`. Existing deployments fail to find the parameter.
- **Subtler break**: changing the type from "a number in seconds" to "a string with units like `10m`, `5s`". Old values `10` no longer parse.
- **Subtlest break**: the developer keeps unit-less values parseable, but changes their interpretation from seconds to milliseconds. No error is raised, but the sidecar now polls the config server 1,000× more often, and consumers get no signal that anything is wrong.

The lesson: "breaking" changes to a container's API are not always obvious. Version bumps, deprecation windows, and — as in [[microservices]] generally — [[consumer-driven-contracts]] or equivalents are worth considering for widely-used sidecars.

### API surface and information hiding

This is [[information-hiding]] applied to containers. A container's parameters, endpoints, and side effects are its contract; everything else should remain implementation detail that the maintainer is free to change. The less a container exposes, the easier it is to evolve — exactly the argument Newman makes for microservice interfaces.

## 3. Document the container

Burns observes there are few formal tools for container documentation, but several best practices using the `Dockerfile` itself (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md):

### `EXPOSE` directive with comments

Document the ports the container listens on:

```
# Main web server runs on port 8080
EXPOSE 8080
```

### `ENV` directive for parameter defaults

Document each environment-variable parameter and give it a sensible default:

```
# The PROXY_PORT parameter indicates the port on localhost to redirect
# traffic to.
ENV PROXY_PORT 8000
```

### `LABEL` directive for metadata

Use labels for vendor, URL, and version:

```
LABEL "org.label-schema.vendor"="name@company.com"
LABEL "org.label.url"="http://images.company.com/my-cool-image"
LABEL "org.label-schema.version"="1.0.3"
```

The names come from the **Label Schema project**, a shared taxonomy of well-known labels so multiple tools can rely on the same image metadata for visualization, monitoring, and correct use (source: raw/designing-distributed-systems/chapter-02-the-sidecar-pattern.md).

## The broader point

Burns's three-part discipline mirrors long-standing lessons from reusable library design. A container is a deployable function:

- Its parameters are its signature.
- Its observable behaviours are its contract.
- Its documentation is how others discover it.

Without all three, reuse does not happen — people fork the container or rewrite the functionality in-process, and the modularity benefit of the [[sidecar-pattern]] is lost.

## Applies to ambassadors too

Chapter 3 explicitly invokes the same discipline for ambassador containers (source: raw/designing-distributed-systems/chapter-03-ambassadors.md). A sharding ambassador's shard list, a service-broker ambassador's environment-probe configuration, and a request-splitting ambassador's weight/ratio are all parameters in the sense of this page. The whole value of the [[ambassador-pattern]] — "the ambassador container can be reused with a number of different application containers" — depends on the same three-part discipline being applied to ambassadors as to sidecars.

## Applies to adapters too

Chapter 4's [[adapter-pattern]] containers are the most aggressively reused of the three: one Redis-to-Prometheus exporter can run anywhere Redis runs; one MySQL health-check adapter runs anywhere MySQL runs; community fluentd plugins adapt dozens of different applications' logs to a common format (source: raw/designing-distributed-systems/chapter-04-adapters.md). That broad reach only works if every one of those adapters:

1. Is **parameterised** over everything deployment-specific — listening ports, credentials, probe queries, metric names, log tags. The Chapter 4 health-check adapter does this with command-line flags; the Chapter 4 fluentd examples do it via config snippets.
2. Defines its **API surface** in both directions: the application-facing protocol it consumes (Redis wire protocol, MySQL driver, Storm REST) *and* the fleet-facing interface it produces (Prometheus metrics endpoint, fluentd event stream, HTTP health endpoint). Both sides are part of the contract.
3. Is **documented** so third-party users — who by design don't have deep knowledge of the application the adapter fronts — can adopt it confidently. Burns explicitly flags that adapters become a mechanism for sharing operational expertise across the community, which only works if documentation is good.

## Related pages

- [[sidecar-pattern]]
- [[ambassador-pattern]]
- [[adapter-pattern]]
- [[pod]]
- [[information-hiding]]
- [[coupling]]
- [[breaking-changes]]
- [[consumer-driven-contracts]]
- [[microservices]]
- [[designing-distributed-systems]]
