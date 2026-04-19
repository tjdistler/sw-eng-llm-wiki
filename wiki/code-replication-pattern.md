# Code Replication Pattern

**Summary**: A [[reuse-patterns|code-reuse pattern]] that copies the shared source into each service's own repository, avoiding any sharing mechanism at all. Preserves bounded context perfectly but makes change propagation painful. Reserved for tiny, truly static code (annotations, marker attributes, one-off utilities).

**Sources**: `raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md`

**Last updated**: 2026-04-19

---

## The pattern

Each service's source repository contains its own copy of the shared code. There is no library artifact, no runtime call, no compile-time dependency — just duplicated source (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md).

The pattern was popular in early microservices days, riding the *"share nothing!"* enthusiasm and the (misread) bounded-context principle. In practice it fell apart fast and is rarely the right choice today.

## When it actually works

Two narrow but legitimate cases (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md):

### Tiny, static, one-off code

The chapter's worked example is a service-entry-point annotation in Java / attribute in C#:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface ServiceEntrypoint {}
```

The annotation has *no* logic — it's a marker class. There are no bugs to fix, no functionality to evolve. Building a shared library for it would be ceremony for nothing. Replication is fine.

The test: **is this code so simple it cannot meaningfully change in the future?** If yes, replication is acceptable. Otherwise, prefer a [[shared-library-pattern|shared library]].

### Migration from a monolith

When carving services out of a monolith, replicating something like a `Utility.cs` class into each new service lets each service then *prune* or *evolve* its own copy to fit its bounded context, removing dead code and avoiding accidental coupling. This is a form of [[tactical-forking]] applied at code-level — replication-as-decoupling, not replication-as-reuse.

## Trade-offs

| Pro | Con |
|---|---|
| Preserves [[bounded-contexts\|bounded context]] perfectly — no shared dependency edge | Bug fixes must be propagated by hand to every copy |
| Zero coupling — neither static nor dynamic | Functional changes likewise — every service team has to act |
| No versioning, no library hygiene, no runtime overhead | Drift is inevitable — over time copies diverge |

The chapter is unambiguous: **approach with extreme caution**. The cost of a single defect found later is paid across every service that copied the buggy version (source: raw/software-architecture-the-hard-parts/chapter-08-reuse-patterns.md).

## When to use

Use replication when **all** of the following are true:

- The code is small (typically a single class or file).
- It contains no logic likely to change due to defects or business reasons.
- A shared library would impose more ceremony than the code itself warrants.
- Or: you are migrating a monolith and want each new service to evolve its copy independently.

Otherwise, default to [[shared-library-pattern]] (homogeneous stack) or [[shared-service-pattern]] (polyglot or fast-changing).

## Position in the reuse-pattern decision matrix

Code replication is the **first** option in the [[reuse-patterns]] decision matrix to *rule out*. It is the simplest mechanism but also the most dangerous when the underlying assumption (the code never changes) breaks.

## Related pages

- [[reuse-patterns]]
- [[shared-library-pattern]]
- [[shared-service-pattern]]
- [[tactical-forking]]
- [[bounded-contexts]]
- [[gather-common-domain-components-pattern]]
- [[software-architecture-the-hard-parts]]
