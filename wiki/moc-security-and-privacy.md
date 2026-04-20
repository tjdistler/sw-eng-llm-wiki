# MOC: Security and Privacy

**Summary**: Entry point for questions about *keeping data, systems, and people safe* — the security mindset (least privilege, defense in depth, zero trust, shared responsibility, active security as practice rather than theater), the technical primitives (encryption at rest and in transit, secrets management, network access controls, security monitoring), the privacy and governance frame (data ethics, lifecycle management, retention, governance, sovereignty), and the operational patterns that close the loop with reliability (defense-in-depth backups, ransomware posture, security incident response). Start here when the question is "who can do what to our data, how do we keep it confidential, and how do we prove it?" rather than "is the service available?" (that's [[moc-reliability-and-operations]]) or "what's the shape of the service itself?" (that's [[moc-container-and-serving-patterns]]).

**Sources**: (meta-page; aggregates concept pages and links to raw chapters)

**Last updated**: 2026-04-19

---

## When to read this

You have data that matters — PII, payment info, healthcare records, proprietary IP — and the question is how to keep it confidential, how to comply with the regulations surrounding it, how to make sure only the right people can access it, and how to respond when something goes wrong. Maybe you're designing a new data platform and need the security controls that will pass a SOC 2 audit. Maybe legal just surfaced a data-retention problem. Maybe a credential leaked and you're figuring out the blast radius. Maybe your backup strategy hasn't accounted for ransomware and you want to know what "defense in depth for data" actually looks like.

The canonical shape of a question that lands here: *"What does least privilege actually look like for this data platform?"*, *"How do we encrypt this dataset such that a key compromise doesn't mean game over?"*, *"What goes into our data retention policy and how do we implement it?"*, *"Is our cloud posture actually zero-trust or is it perimeter-with-a-cloud-label?"*, *"What's the shape of a security incident-response plan for a data platform?"*, *"How do we handle 'right to be forgotten' requests from GDPR/CCPA?"*

Jurisdictional rule for this MOC:

- **This MOC** owns the *security and privacy discipline* as a cross-cutting concern. The security mindset, the technical primitives (encryption, secrets, network controls, access control), the monitoring and response discipline specific to security events, the privacy and governance frame, and the cross-cutting patterns (backups under the ransomware lens, defense in depth across layers).
- [[moc-reliability-and-operations]] owns operational reliability. [[security-monitoring]], [[backups-vs-archives]], and [[defense-in-depth-data]] appear in both MOCs — this MOC owns them under the *confidentiality, integrity, compliance* lens; the reliability MOC owns them under the *availability, integrity, restore-SLO* lens. Read both MOCs for any full-stack data-protection question.
- [[moc-data-engineering]] owns the broader data-engineering discipline, including [[data-security]] as an undercurrent. This MOC deepens the undercurrent; the data-engineering MOC owns its context within the full lifecycle.
- [[moc-distributed-systems]] and [[moc-container-and-serving-patterns]] own the mechanisms (network architecture, service-mesh-based mTLS, sidecar-based authz) that this MOC's controls are implemented on top of. This MOC says "encrypt in transit"; those MOCs say "here's how TLS termination lives in the container stack."
- [[moc-data-models-and-storage]] owns storage-engine internals. This MOC cites [[encryption-at-rest]] and data-lifecycle properties under the confidentiality lens; the storage MOC owns the engine-level mechanics.

Shared pages (backups, defense-in-depth, security-monitoring, data-governance) are linked here under the *security/privacy* lens; sibling MOCs own their *reliability/availability/discipline* lenses.

## The mindset — what "security" actually is

Before any control, the stance. Most security failures are stance failures: policies written for compliance but not practice, perimeters assumed to be impregnable, developers trained to "check the box" rather than to think adversarially. Get the mindset right and the technical controls become obvious; get it wrong and expensive tooling will still leave you breached.

- [[data-security]] — the undercurrent framing from *Fundamentals of Data Engineering*. Security is people, processes, and technology — in that order of weight. Least privilege, data minimisation, multi-tenant blast radius, shared responsibility. The umbrella page every other page in this MOC sits under.
- [[active-security]] — forward-looking research on current threats, not reactive compliance. Every engineer is a security researcher; every team reads threat intel; the posture is "we are being attacked continuously" rather than "we will respond if attacked." The opposite of [[security-theater]].
- [[security-theater]] — compliance box-ticking without real security. The 200-page security policy that no one reads. Unused encryption on unaudited data. The antidote is small, habitual, practiced controls that people actually follow.
- [[threat-modeling]] — enumerate attack scenarios *before* you build. "What could an attacker do with this interface?" "What's the blast radius if this key leaks?" "What does the minimum data to ingest look like?" The practice that feeds every other control.
- [[shared-responsibility-model]] — in the cloud, the provider owns platform security; the customer owns configuration. Public S3 buckets, misconfigured IAM, unrotated credentials — the overwhelming majority of cloud breaches are customer-side. Know the line; know it's drawn differently for IaaS vs PaaS vs SaaS.
- [[zero-trust-security]] — the cloud-native posture. Every request is authenticated; no network is trusted by default; the perimeter is the service, not the datacenter. The architectural response to "the hardened perimeter" being a fiction once the cloud, remote work, and third-party integrations exist.
- [[security-policy]] — short, actionable, *habitual* policies. A one-page "here's how to manage credentials, here's how to handle devices, here's how to respond to a phishing attempt" that people actually follow. Not a 200-page PDF. Policy that fits in a pocket survives; policy that fits in a binder does not.

Deeper reading: [[fundamentals-of-data-engineering#chapter-10-security-and-privacy]] is the foundational chapter for the mindset and primitives in this MOC. Read it end-to-end before touching any of the technical controls below.

## Least privilege — the organising principle

If you only internalise one security idea, make it this one. Every other control is either a variant of it or an implementation of it.

- [[least-privilege]] — access is granted at the smallest scope, for the shortest time, that still lets the person or system do the job. Time-boxed access, role-scoped access, column/row/cell-level masking for PII, broken-glass emergency access with full audit trails. The default stance that keeps most accidents local and most compromises bounded.

Least privilege compounds. Applied to humans (least-privileged user accounts), to services (least-privileged service accounts with scoped permissions), to networks (least-privileged network access — see [[network-access-security]]), to data (least-privileged data access — only columns the query actually needs), and to infrastructure (least-privileged CI/CD credentials). The pattern shows up at every layer.

Deeper reading: [[fundamentals-of-data-engineering#chapter-10-security-and-privacy]] for the foundational treatment; [[fundamentals-of-data-engineering#chapter-2-the-data-engineering-lifecycle]] for its role in the lifecycle.

## Technical primitives — the controls that actually enforce policy

Policy without enforcement is theater. These are the mechanisms that turn "we have a policy" into "the system cannot violate the policy."

### Encryption

- [[encryption-at-rest]] — the baseline. Laptops, servers, databases, object storage, backups all encrypted at rest. Cheap (most platforms do it with a checkbox), catches the low-effort attacker (stolen disk, improperly disposed drive). Useless against a credential breach that gives the attacker *legitimate* API access — the keys are the weak point, not the ciphertext.
- [[encryption-in-transit]] — TLS by default on every link, internal and external. Protects against interception, MITM, and passive sniffing. FTP and plaintext HTTP are the canonical anti-examples. Mutual TLS (mTLS) between services takes this further; see [[moc-container-and-serving-patterns]] for the service-mesh implementation.
- [[secrets-management]] — credentials are configuration, not code. Never in version control, never in container images, never hardcoded. A secrets manager (Vault, AWS Secrets Manager, GCP Secret Manager) is mandatory; SSO + MFA protects access to it; rotation happens on a schedule and on suspected compromise.

### Network access

- [[network-access-security]] — IP allowlists, VPCs, VPN, bastion hosts, private endpoints. The perimeter around data services, even in a zero-trust architecture, because defense in depth means the public internet shouldn't have a direct path to your warehouse. Public S3 buckets are the canonical mistake the pattern prevents.

The data engineer often *is* the network engineer for the data platform: VPC peering, private link, IP allowlists on the warehouse, subnet design for multi-tenant isolation. Not optional background knowledge.

### Monitoring

- [[security-monitoring]] — the security-specific observability: access patterns, resource-use anomalies, billing spikes (often the first signal of compromise), excess-permission grants, unauthorised API calls. A distinct dashboard from the ordinary observability stack; a rehearsed incident-response playbook. See [[moc-reliability-and-operations]] for how this plugs into general observability, but the signals, alert thresholds, and response playbooks are their own discipline.

Deeper reading: [[fundamentals-of-data-engineering#chapter-10-security-and-privacy]].

## Privacy and compliance — the rules the data has to live by

Security protects data from unauthorised access; privacy governs what you're allowed to do with it even when access is authorised. Regulation (GDPR, CCPA, HIPAA, SOX, PCI-DSS) is the external constraint; ethics is the internal one.

- [[data-ethics]] — the engineering-ethics framing. PII masking, consent, bias tracking, surveillance resistance. "Privacy as freedom to choose" — what the person sharing data gets to decide about its use. Kleppmann's DDIA Ch 12 framing plus Reis & Housley's FoDE Ch 2 treatment. The ethical floor under the regulatory ceiling.
- [[data-governance]] — the organising discipline. Three categories: discoverability (who knows this data exists?), security (who can access it?), accountability (who's responsible?). Governance is the answer to every "where did this dataset come from and who owns it?" audit question.
- [[data-lifecycle-management]] — archival, retention, destruction. GDPR "right to be forgotten" is a lifecycle-management problem, not a database problem. The question of "can we delete all traces of this user?" has to be answerable at the platform level, not on a one-off basis.
- [[data-retention]] — how long to keep data. Four inputs: value (does the business still use it?), time (does it get stale?), compliance (do regulations require keeping it, or require deleting it?), and cost (cloud object-store pay-as-you-go changes the economics). Retention policy is where privacy, compliance, and cost all meet.
- [[data-sovereignty]] — the geographic dimension. EU data often can't leave the EU; Chinese data often can't leave China; some healthcare data has country-of-origin constraints. The platform-level architecture has to express this; an "everything in us-east-1" architecture isn't legal for a global service.

### Governance mechanisms

- [[data-catalog]] — where metadata lives; the discoverability half of governance. Every dataset has an owner, a sensitivity classification, a retention policy, a description. The catalog is how those facts become findable rather than tribal.
- [[metadata]] — the DMBOK four categories (business, technical, operational, reference) that the catalog tracks. The substrate under every governance question.
- [[data-quality]] — accuracy, completeness, timeliness. Not strictly security, but governance-adjacent: bad data causes bad decisions, which can cause compliance failures (wrong retention policy applied to wrongly-classified data, etc.).
- [[data-management]] — the umbrella discipline the DAMA DMBOK defines. Governance is one of its facets; lifecycle, quality, and architecture are others. See [[moc-data-engineering]] for the full scope.

Deeper reading: [[fundamentals-of-data-engineering#chapter-10-security-and-privacy]] for the privacy/security cross-cutting frame; [[fundamentals-of-data-engineering#chapter-2-the-data-engineering-lifecycle]] for lifecycle and undercurrents; [[fundamentals-of-data-engineering#chapter-6-storage]] for the storage-side retention discussion.

## Defense in depth — the architectural response to single-point compromise

Any single control can fail. Defense in depth assumes compromise of any one layer and makes sure the next layer still catches the attack. Common for data services because the consequences of any one control failing are catastrophic — not just "request fails," but "data leaks" or "data destroyed."

- [[defense-in-depth-data]] — nuclear-industry-origin concept applied to data. Soft delete before hard delete, backups replicated across media types, validators between layers, air-gapped archives for the worst-case restore. Each layer independently insufficient; collectively, no single failure causes permanent loss. Shared with [[moc-reliability-and-operations]] — this MOC owns the confidentiality/integrity lens; that MOC owns the availability/restore-SLO lens.

The pattern applies at every layer:

- **Network**: VPC + security groups + WAF + application-layer auth, not just one of the four.
- **Data**: encrypted at rest + encrypted in transit + access-controlled at the row level + audit-logged, not just the first.
- **Identity**: MFA + SSO + session timeouts + anomaly-based alerts, not just the first.
- **Backups**: multiple tiers, multiple regions, multiple media, tested restore, not just "we have backups."

### Backups as a security control

- [[backups-vs-archives]] — backups for restore within operational SLO; archives for compliance and long-term discovery. Different retention, different access controls, different restore frequency. Ransomware makes backups a *security* control, not just a reliability control: if the attacker can encrypt your backups along with your primary data, you have no backup. Immutability, separate credentials, and offline or write-once media are the specific mitigations.
- [[tiered-backup-strategy]] — hot/warm/cold tiers with different restore SLOs and different access models. The cold tier often doubles as the ransomware-resistant tier (offline tape, WORM object storage).
- [[data-integrity-failure-modes]] — the taxonomy this MOC intersects with: malicious encryption (ransomware), malicious deletion (disgruntled insider), silent corruption (data-mutation bug), operator error (accidental DROP). Different failure modes need different defense-in-depth layers. Shared with [[moc-reliability-and-operations]].

Deeper reading: [[site-reliability-engineering#chapter-26-data-integrity-what-you-read-is-what-you-wrote]] for the reliability-oriented framing of the same patterns; [[site-reliability-engineering#chapter-33-lessons-learned-from-other-industries]] for the nuclear-industry defense-in-depth origin.

## Security in the data lifecycle — cross-cutting placement

Security and privacy aren't a single stage; they are an *undercurrent* that touches every stage of the data engineering lifecycle.

| Lifecycle stage                  | Security/privacy concerns this MOC owns                                                                                            |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Source systems                   | Authentication to the source; least-privileged extraction credentials; data minimisation (ingest only what's needed).              |
| Ingestion                        | Encryption in transit on the wire; secrets management for source credentials; PII classification at ingest.                         |
| Storage                          | Encryption at rest; retention policy enforcement; backup security; lifecycle-management for deletion and archival.                   |
| Transformation                   | Access control on intermediate tables; column-level masking before transformation widens exposure; audit logs of transformations.   |
| Serving                          | Access control on serving endpoints; least-privileged query permissions; row-level security for multi-tenant serving; rate limits. |
| *(Undercurrents)*                |                                                                                                                                    |
| DataOps                          | Automated policy checks in the pipeline (classification drift, permission drift, retention-compliance audits).                      |
| Data architecture                | Zero-trust defaults; shared-responsibility awareness; sovereignty-compliant region design.                                          |
| Orchestration                    | Pipeline credentials in a secrets manager, not in code; job-level least privilege; audit of what a pipeline *actually* touched.     |
| Software engineering             | SAST/DAST on code; dependency scanning; signed artifacts; review gates on security-sensitive changes.                               |

See [[moc-data-engineering]] for the lifecycle and undercurrents as a whole; this table is the security-specific slice.

## Security incident response

When something goes wrong — a credential leak, a data exfiltration alert, a ransomware signal, a compliance breach — the response is a specialisation of the incident-management discipline in [[moc-reliability-and-operations]], with different roles and different priorities.

Key differences from general incident response:

- **Law and compliance in the loop from minute one.** GDPR has a 72-hour breach-notification window; HIPAA has specific reporting obligations; contract clauses may require immediate customer notification. The Comms Lead coordinates with legal, not just PR.
- **Don't touch the evidence.** Unlike a reliability incident where fast mitigation is the priority, a security incident often requires preserving artifacts for forensics. Snapshot before you rebuild. Keep logs, isolate the compromised host, don't just kill it.
- **Blast-radius assessment is a parallel track.** What else could the compromised credential touch? What other services share the same key management? What data was accessible through this vector? A Planning Lead with security specialisation runs this in parallel to the fix.
- **Recovery is not "restore from backup" alone.** Rotate every credential that could have been exposed. Revoke and reissue tokens. Re-verify integrity of data the attacker might have touched. Forensic sign-off before declaring the incident resolved.

The general incident-response framework applies — [[incident-management-framework]], [[incident-commander]], [[live-incident-state-document]] — but adapted with the above overlays. [[security-monitoring]] feeds the initial detection; the response playbook lives partly in this MOC's domain and partly in [[moc-reliability-and-operations]]'.

## Security at the decomposition and extraction boundary

Decomposing a monolith or extracting a service changes the security posture. What used to be an in-process function call — implicitly trusted, running under a single credential, accessing a shared database — becomes a network call with its own authentication, authorisation, and audit surface.

Key changes to address during any extraction ([[moc-decomposition]] owns the broader extraction playbook; this MOC owns the security overlay):

- **Service identity.** The extracted service needs its own credentials (service account, mTLS cert, OAuth client). Don't share credentials with the monolith.
- **Least-privileged data access.** If the monolith had DBO on everything, the new service gets scoped access to only the tables it needs. [[database-as-a-service-interface]] and views with column-level filtering make this cleaner.
- **Transport security.** What was a local call is now a network call — TLS by default, mTLS for internal service-to-service.
- **Audit surface expansion.** The extraction creates a new API; that API's access logs are now a first-class security-monitoring signal.
- **Sovereignty and multi-tenancy.** The extracted service may now handle data from multiple tenants that the monolith kept cleanly partitioned. Row-level security, per-tenant encryption keys, and per-tenant auditing become explicit rather than implicit.

The rule of thumb: an extraction that doesn't rewrite the security posture alongside the code is a security regression.

## Gaps in this wiki (known)

The source material for this MOC is dominated by *Fundamentals of Data Engineering* Ch 10 plus SRE-adjacent security content. Several security/privacy concept pages that a complete picture needs are not yet authored on disk:

- Identity/access specifics — authentication, authorisation, RBAC/ABAC, MFA, SSO as dedicated pages (currently folded into [[secrets-management]] and [[least-privilege]]).
- Privacy regulation specifics — GDPR, CCPA, HIPAA, SOX as dedicated pages (currently folded into [[data-ethics]] and [[data-lifecycle-management]]).
- Cryptographic specifics — key management service, hashing vs encryption, tokenisation, masking as dedicated pages (currently folded into [[encryption-at-rest]]/[[encryption-in-transit]]/[[secrets-management]]).
- Application security — SAST/DAST, dependency scanning, supply-chain security, SBOM.
- Threat-actor models and attack patterns — OWASP Top 10, MITRE ATT&CK, common web vulnerabilities.

Future ingests (a web-application security book, a privacy engineering book) would fill these. For now, this MOC surfaces the security/privacy content the wiki *does* have and flags what it doesn't.

## Sibling MOCs

- [[moc-reliability-and-operations]] — owns availability, integrity (from the restore-SLO lens), and operational discipline. Shared pages: [[security-monitoring]], [[backups-vs-archives]], [[defense-in-depth-data]], [[data-integrity-failure-modes]]. Read both for any full-stack data-protection question.
- [[moc-data-engineering]] — owns the lifecycle and undercurrents; this MOC is a deeper treatment of one undercurrent. The lifecycle table above is the bridge.
- [[moc-data-models-and-storage]] — owns encryption/retention as storage-engine properties; this MOC owns them as confidentiality controls.
- [[moc-decomposition]] and [[moc-microservices]] — own the architectural changes that expose new security surface area; this MOC owns the security overlay on top.
- [[moc-container-and-serving-patterns]] — owns the network and service-mesh mechanisms (mTLS, ingress control, network policy) that implement the controls in this MOC.

## Related pages

- [[index]]
- [[fundamentals-of-data-engineering]]
- [[site-reliability-engineering]]
- [[data-security]]
- [[active-security]]
- [[security-theater]]
- [[threat-modeling]]
- [[shared-responsibility-model]]
- [[zero-trust-security]]
- [[security-policy]]
- [[least-privilege]]
- [[encryption-at-rest]]
- [[encryption-in-transit]]
- [[secrets-management]]
- [[network-access-security]]
- [[security-monitoring]]
- [[data-ethics]]
- [[data-governance]]
- [[data-lifecycle-management]]
- [[data-retention]]
- [[data-sovereignty]]
- [[data-catalog]]
- [[metadata]]
- [[defense-in-depth-data]]
- [[backups-vs-archives]]
- [[tiered-backup-strategy]]
- [[data-integrity-failure-modes]]
