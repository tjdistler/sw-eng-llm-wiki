# FaaS Decorator Pattern

**Summary**: A composition pattern for [[functions-as-a-service]] in which a small stateless function sits between a caller and a backend API, transforming the request on the way in or the response on the way out. Named after Python's decorator syntax because it attaches behaviour without modifying the underlying callable. Ideal for lightweight, stateless augmentations bolted onto existing services after the fact.

**Sources**: `raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md`

**Last updated**: 2026-04-16

---

## The shape of the pattern

Burns's first canonical FaaS pattern. A function takes an input, transforms it into an output, and passes it on to a different service — typically augmenting or decorating an HTTP request or response (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

```
Client  ─► Decorator FaaS ─► Backend service
                │                    │
                │◄── transformed ◄───┘
```

The decorator is stateless: it reads the incoming payload, applies some transformation rule, and forwards. The function does not own any data that needs to persist across invocations, so the forced statelessness of [[functions-as-a-service]] is not a constraint.

## Why the Python analogy

Burns explicitly draws the analogy to Python's decorator syntax — a wrapper that adds behaviour to a callable without modifying its source (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md). The shape lines up: the backend API is the underlying function; the decorator FaaS is the wrapper that augments its inputs or outputs. The value proposition is the same too — decoration transformations are "generally stateless, and also because they are often added after the fact to existing code as the service evolves, they are ideal services to implement via FaaS."

## Why FaaS suits decoration

Two reasons, both from the chapter (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md):

1. **Decorators are stateless.** They transform one payload at a time without reference to prior invocations, which matches FaaS's forced statelessness exactly.
2. **Decorators are added after the fact.** New defaulting, validation, logging, or auth rules accumulate as an API evolves. The "lightness of FaaS means that you can experiment with a variety of different decorators before finally adopting one and pulling it more completely into the implementation of the service." Deployment cost is low enough that temporary or experimental decorators are cheap.

## Worked example: request defaulting

Burns's chapter example is adding default values to a RESTful JSON API when the caller omits fields. The problem is that `null` in JSON is conventionally "false," so the API can't tell "caller explicitly set false" apart from "caller didn't set anything." Rather than entangle defaulting logic with the business logic of the backend, a decorator FaaS can fill in defaults before the request reaches the backend (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md).

The chapter's Python handler, deployed as a Kubeless function:

```python
def handler(context):
    obj = context.json
    if obj.get("name", None) is None:
        obj["name"] = random_name()
    if obj.get("color", None) is None:
        obj["color"] = "blue"
    return call_my_api(obj)
```

Deployed with:

```
kubeless function deploy add-defaults \
    --runtime python27 \
    --handler defaults.handler \
    --from-file defaults.py \
    --trigger-http
```

The backend is untouched. The defaulting rule is a separate deployable, scalable, and evolvable unit. The backend team can own the business logic; a smaller group (or a platform team) can own defaulting rules across many APIs.

## FaaS decorator vs adapter container

Burns anticipates the overlap with the [[adapter-pattern]] and handles it head-on: "Given the previous discussion of the adapter pattern in the single-node section, you may be wondering why we don't simply package this defaulting as an adapter container. And this is a totally reasonable approach, but it does mean that we are going to couple the scale of the defaulting service with the API service itself" (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md).

The trade-off:

| Dimension | FaaS decorator | Adapter container |
|---|---|---|
| **Scaling** | Independent of backend; scales on decorator load alone | Coscheduled with backend; scales with each backend pod |
| **Deploy granularity** | Deploy decorator independently | Deploy alongside the backend pod |
| **Best when** | Decorator is much lighter than backend; varying decorator usage; experimental | Decorator must be per-backend-instance; one-to-one lifecycle |
| **Fleet-wide reuse** | Harder — one FaaS per transformation kind | Easier — drop the adapter next to any matching app |

The rule of thumb: use a FaaS decorator when the transformation should scale on its own axis, and an adapter container when it should scale in lockstep with the application.

## FaaS decorator vs gateway/proxy middleware

The same functional role can be played by middleware in an API gateway (Kong, nginx Lua, Envoy filter). The trade-off there is "decorator as configuration of a long-running proxy" vs "decorator as independently-deployable function." Gateway middleware is cheaper for very high request volumes (no cold start, one process serving all traffic) but more coupled operationally (one middleware bug affects the whole gateway). FaaS decorators are cheaper for experimentation and for decorators that are naturally per-customer or per-route.

## Common applications

The pattern generalises to any stateless request/response transformation, including (source: raw/designing-distributed-systems/chapter-08-functions-and-event-driven-processing.md and natural extensions):

- **Input defaulting** — Burns's worked example.
- **Input validation and normalisation** — reject malformed payloads before they reach the backend; normalise units or formats.
- **Output shaping** — project, enrich, or redact fields for specific clients.
- **Authentication and authorisation** — inject or validate JWTs, apply rate limits per principal.
- **Backward-compatibility shims** — translate old client requests into the new backend contract during a [[branch-by-abstraction]] or [[strangler-fig-pattern]] migration.

The last use case connects the FaaS decorator directly to Newman's migration-pattern catalogue — a FaaS is a cheap, throwaway way to implement a [[decorating-collaborator-pattern]]-style wrapper during a microservice extraction.

## Not to be confused with the decorating collaborator

Newman's [[decorating-collaborator-pattern]] sounds superficially similar but is a different beast. The FaaS decorator is a **stateless request/response transformer**, implemented as a function, that augments or reshapes traffic to a backend — it lives indefinitely as a piece of the production architecture. The decorating collaborator is a **migration-time proxy** in front of the monolith that triggers calls to a new microservice based on the monolith's outcome, and it exists specifically to add new behaviour to a legacy system you cannot modify. One is an architectural composition primitive; the other is a migration tactic. A FaaS decorator is sometimes a convenient *implementation substrate* for a decorating collaborator (see below), but they are not the same pattern.

## Relationship to other patterns

### To the adapter pattern

The [[adapter-pattern]] solves the same structural problem — transform an application's interface without modifying the application — at the container-scheduling level. FaaS decorators solve it at the request level, with independent scaling. Both are interface-transformation patterns; the choice between them is about coupling the transformation's lifecycle to the backend (adapter) or not (FaaS).

### To the ambassador pattern

A client-side [[ambassador-pattern]] intercepts outbound calls from the application. A FaaS decorator intercepts inbound calls to a backend. The two are mirror images — where ambassador wraps the *caller*, the FaaS decorator wraps the *callee*. Some systems use both, composing a client-side ambassador, a FaaS decorator, and an adapter container into one request path.

### To the decorating collaborator

Newman's [[decorating-collaborator-pattern]] is the migration-specific form of the same idea: wrap the monolith with something that triggers new behaviour based on the monolith's request or response. A FaaS is a convenient implementation substrate for that wrapper.

### To the decorator design pattern

Burns's naming honours the Gang of Four / Python decorator lineage. The structural shape is the same as any OOP decorator, adapted for HTTP request/response instead of method calls. Using FaaS as the implementation gives decoration **deployment-layer independent lifecycle** — something no in-process decorator can.

## Related pages

- [[functions-as-a-service]]
- [[event-pipeline-pattern]]
- [[adapter-pattern]]
- [[ambassador-pattern]]
- [[sidecar-pattern]]
- [[decorating-collaborator-pattern]]
- [[strangler-fig-pattern]]
- [[branch-by-abstraction]]
- [[coupling]]
- [[information-hiding]]
- [[designing-distributed-systems]]
