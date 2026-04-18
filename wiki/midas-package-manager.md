# Midas Package Manager (MPM)

**Summary**: The package manager Google uses to distribute software to production machines. MPM assembles packages from [[blaze-bazel|Blaze]] rules (build artifacts, owners, permissions), assigns each package a **name plus unique-hash version**, and signs the result. MPM's distinguishing feature is **movable labels** (dev / canary / production) that point at a particular version — moving a label from an old package to a new one is how promotion works without rebuilding.

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`

**Last updated**: 2026-04-17

---

## What MPM does

> Software is distributed to our production machines via the Midas Package Manager (MPM). MPM assembles packages based on Blaze rules that list the build artifacts to include, along with their owners and permissions. Packages are named (e.g., `search/shakespeare/frontend`), versioned with a unique hash, and signed to ensure authenticity. (source: chapter-08-release-engineering.md)

Four properties:

- **Named** — stable identifier, project-scoped (`search/shakespeare/frontend`).
- **Versioned by hash** — content-addressed, so two packages with the same hash are byte-identical (pairs naturally with [[hermetic-builds]]).
- **Signed** — authenticity is verifiable at deploy time.
- **Labelled** — see below.

## Movable labels

MPM supports applying labels to a particular version of a package. Rapid applies a label containing the build ID, so a package can be uniquely referenced by `(name, build-ID-label)`.

Beyond build-ID labels, MPM labels mark a package's position in the release pipeline (source: chapter-08-release-engineering.md):

- `dev`
- `canary`
- `production`

The key property:

> If you apply an existing label to a new package, the label is automatically moved from the old package to the new package. For example: if a package is labeled as canary, someone subsequently installing the canary version of that package will automatically receive the newest version of the package with the label canary.

This is what makes label-based promotion work: deployers don't need to know the hash, they just install `name:production` and get whatever is currently labelled that way. Promoting a canary to production is a label move, not a rebuild.

## Why it matters: [[deployment-vs-release]] at the package layer

The movable-label model is essentially the Newman deployment-versus-release separation realised in the package manager. A package is *deployed* (present in MPM, installable, signed) as soon as it is built. It is *released* when a label like `production` is moved to it. The two actions are independent and independently auditable.

## Configuration packages

MPM also hosts **configuration packages** — a separate MPM package containing only configuration files. The same labelling and promotion machinery applies. This is the "package configuration files into MPM configuration packages" pattern described in [[configuration-management-sre]]: binary and configuration are versioned separately but can be tied together with a shared label (`much_ado` in the chapter's example).

## Cross-book connections

- [[deployment-vs-release]] (Newman) — MPM's separation of package existence from label state is the same distinction at the artefact layer
- [[feature-toggle]] (Newman) — configuration packages are effectively feature-toggle carriers; the `cherry pick config + rebuild config package + redeploy` flow is a toggle-update flow that doesn't touch the binary
- [[hot-sharding]] / [[rolling-update-pattern]] (Burns / Bellemare) — label moves are the promotion primitive that rolling deploys build on top of
- [[content-addressed-storage]] ideas — unique-hash versioning is content addressing applied to release artefacts

## Related pages

- [[release-engineering]]
- [[hermetic-builds]]
- [[blaze-bazel]]
- [[rapid-release-system]]
- [[sisyphus]]
- [[deployment-vs-release]]
- [[configuration-management-sre]]
