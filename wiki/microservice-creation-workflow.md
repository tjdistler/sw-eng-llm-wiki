# Microservice Creation Workflow

**Summary**: A streamlined, automated process for creating a new microservice repository and plumbing it into all the organizational tooling — CI, ownership, ACLs, schema registry — with a single request. Removes a step that teams repeat many times and ensures every new service inherits the current tooling baseline instead of copying from an outdated template.

**Sources**: `raw/building-event-driven-microservices/chapter-14-supportive-tooling.md`

**Last updated**: 2026-04-17

---

## The steps that get automated

Bellemare's typical workflow (source: chapter-14-supportive-tooling.md):

1. **Create the repository.**
2. **Wire up CI/CD integrations** — test runners, build pipelines, image registry.
3. **Configure webhooks and dependencies** — anything the org's platform expects every repo to have.
4. **Assign ownership** via the [[microservice-to-team-assignment]] system.
5. **Register input-stream ACLs** via [[event-stream-acls]].
6. **Create output streams and apply ownership permissions** — the new service gets `CREATE`/`WRITE` on its outputs, per [[single-writer-principle]].
7. **Optionally apply a template or code generator** that scaffolds a skeleton service using the organization's current best-practice boilerplate.

## Why it matters more than it sounds

The workflow is run dozens or hundreds of times per team-year across a large EDM organization. Each manual repeat is an opportunity for:

- Skipped steps (service without ownership, missing ACL, no CI wiring).
- Stale templates — a developer who copies from a "recent" project gets whatever platform choices that project happened to have. Over a couple of years that drift makes every service look different.
- Time lost per service that compounds across the organization.

A streamlined creator turns all of this into a single durable integration point where platform improvements propagate automatically.

## Template injection as platform leverage

The template step is not cosmetic — it is **where platform teams ship new capabilities**. When platform updates the template, every new service from that day forward inherits the update (source: chapter-14-supportive-tooling.md). Compare with copy-the-last-project: updates reach no one except by manual diffusion.

## Relationship to existing wiki coverage

- **[[microservice-to-team-assignment]]** — ownership is assigned as part of the workflow.
- **[[event-stream-acls]]** — input-stream reads and output-stream writes are granted as part of the workflow.
- **[[code-generation]]** — the template/skeleton step naturally hosts Avro/Protobuf code-gen for data contracts.
- **[[microservice-tax]]** — this tool is a textbook example of centralizing the tax so teams don't repay it per service.

## Related pages

- [[edm-supportive-tooling]]
- [[microservice-to-team-assignment]]
- [[event-stream-acls]]
- [[single-writer-principle]]
- [[microservice-tax]]
- [[code-generation]]
