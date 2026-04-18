# Configuration Management (SRE)

**Summary**: Configuration changes are a leading source of instability, and the [[release-engineering]] chapter develops four models for distributing configuration files. All four share two rules: configuration lives in the primary source code repository, and changes go through a strict code-review gate like any other change. Project owners pick the model case-by-case.

**Sources**: `raw/site-reliability-engineering/chapter-08-release-engineering.md`, `raw/site-reliability-engineering/chapter-17-testing-for-reliability.md`

**Last updated**: 2026-04-17

---

## Why configuration is a first-class concern

> Configuration management is one area of particularly close collaboration between release engineers and SREs. Although configuration management may initially seem a deceptively simple problem, configuration changes are a potential source of instability. As a result, our approach to releasing and managing system and service configurations has evolved substantially over time. (source: chapter-08-release-engineering.md)

Configuration cuts across both the release engineers' domain (packaging, versioning, distribution) and SREs' domain (runtime behaviour, incident causes). It is the area where the two disciplines most need to agree.

## The two universal rules

All four patterns share:

- **Config lives in the primary source repository** ([[google-monorepo]]).
- **Strict code review requirement** — same gate as application code.

## The four models

### 1. Mainline configuration

Developers and SREs modify configuration files at the head of the main branch. Changes are reviewed and applied to the running system (source: chapter-08-release-engineering.md).

- **Advantage**: conceptually simple; binary releases and configuration changes are decoupled.
- **Problem**: skew between the checked-in config and the running config, because jobs must be updated to pick up changes.

This was the first method used for Borg and its predecessors.

### 2. Config bundled in the binary's MPM package

For projects with few config files, or where the files change every release cycle, the configuration is included in the [[midas-package-manager|MPM]] package alongside the binaries.

- **Advantage**: simple deployment — one package.
- **Disadvantage**: binary and config are tightly bound, limiting flexibility.

### 3. Separate MPM "configuration packages" tied by label

Apply the [[hermetic-builds|hermetic principle]] to configuration itself. Generate two MPM packages — one for the binary, one for the configuration — and link them with a shared MPM label (the chapter's example is `much_ado`).

> We can leverage MPM's labeling feature to indicate which versions of MPM packages should be installed together. A label of much_ado can be applied to the MPM packages... When a new version of the project is built, the much_ado label will be applied to the new packages. Because these tags are unique within the namespace for an MPM package, only the latest package with that tag will be used. (source: chapter-08-release-engineering.md)

This is the most flexible pattern:

- Bind each version of the config to a specific binary for reproducibility.
- But still change each package independently when only one needs to move.
- The worked example: a feature rolls out with a flag `first_folio`; after discovery it should be `bad_quarto`; cherry-pick the config change, rebuild the config package, deploy. **No new binary build required.**

### 4. Read configuration from an external store

Some projects have configuration that needs to change frequently or dynamically — while the binary is running. These files live in external stores (source: chapter-08-release-engineering.md):

- [[chubby]]
- [[bigtable]]
- Google's source-based filesystem

This is the runtime-reconfigurable model: the binary subscribes to config updates and adapts without a restart.

## The decision rule

> In summary, project owners consider the different options for distributing and managing configuration files and decide which works best on a case-by-case basis. (source: chapter-08-release-engineering.md)

The chapter is deliberate in *not* prescribing one answer. The choice depends on:

- How tightly config and binary are coupled semantically.
- How often config changes relative to binary changes.
- Whether config changes need to propagate within a running binary.
- The blast radius of a bad config change.

## Testing-side treatment (Chapter 17)

Chapter 17 picks up where Chapter 8 leaves off and develops the testing disciplines that protect each of the four distribution models:

- [[configuration-test]] — production test that diffs the checked-in configuration against how the binary is **actually configured in production**; inherently non-hermetic; pattern of passes/fails is itself a monitoring input.
- [[configuration-integration-testing]] — the "config content is potentially hostile input to an interpreter" framing; protocol buffers > YAML with safe_load > interpreted-language config, because of bounded load time and built-in schema validation.
- [[mttr-and-mttf|MTTR-based categorisation]] — config files either exist to keep MTTR low (edited only during failures, release cadence slower than MTBF) or hold release state (must have testing and monitoring coverage at least as strong as the user application); the two categories have opposite treatment.
- [[break-glass-push]] — the emergency override for hurried config edits; don't disable tests, let them run and back-annotate the push.

The Chapter 8 rule ("config in repo + strict code review") is necessary but not sufficient; Chapter 17's testing disciplines are what make configuration changes actually safe.

## Cross-book connections

- [[feature-toggle]] (Newman) — the separate-configuration-package pattern is a feature-toggle delivery mechanism: change the flag, rebuild only the config package, promote the label
- [[deployment-vs-release]] (Newman) — the external-store pattern is the purest form of separating deployment (config file checked in) from release (flag flipped at runtime)
- [[dynamic-worker-scaling]] / [[operator-pattern]] (Burns) — runtime-reconfigurable patterns parallel orchestrator-driven scaling and controllers reading declarative config
- [[data-contract]] (Bellemare) — configuration changes need the same compatibility discipline as data schemas; the strict-code-review rule is an enforcement mechanism
- [[architecture-decision-record]] (Richards & Ford) — choosing which of the four config models applies to a given service is an architectural decision worth recording

## Related pages

- [[release-engineering]]
- [[midas-package-manager]]
- [[release-policy-enforcement]]
- [[hermetic-builds]]
- [[google-monorepo]]
- [[feature-toggle]]
- [[deployment-vs-release]]
- [[chubby]]
- [[bigtable]]
- [[configuration-test]]
- [[configuration-integration-testing]]
- [[break-glass-push]]
- [[testing-for-reliability]]
