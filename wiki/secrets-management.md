# Secrets Management

**Summary**: Treating credentials — API keys, database passwords, TLS private keys, OAuth tokens — as **configuration**, loaded at runtime from a dedicated secrets store, never committed to version control, never embedded in code. Chapter 10 lists this under the baseline security policy: "Don't put your credentials in code. Handle secrets as configuration and never commit them to version control. Use a secrets manager where possible."

**Sources**: `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## The baseline rules

Chapter 10's short list for handling credentials (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

- **Use single sign-on (SSO) for everything.** Avoid passwords whenever possible.
- **Use multi-factor authentication** with SSO.
- **Don't share passwords or credentials** — including client passwords and credentials. If in doubt, escalate.
- **Beware of phishing and scam calls.** Never give passwords out; prioritise SSO so there's usually no password to give out in the first place.
- **Disable or delete old credentials.** Preferably delete.
- **Don't put credentials in code.** Handle them as configuration; never commit to version control; use a secrets manager.
- **Apply [[least-privilege|least privilege]] to every credential.** Never give more access than the job requires, on-prem or in the cloud.

## Why "secrets as configuration"

The credential is data, not source. Two separation-of-concerns points:

- **Source code is shared widely.** A credential in a repo is visible to everyone with repo access — and everyone who ever had repo access, forever, through Git history. Even a private repo leaks when a laptop is compromised.
- **Credentials rotate, code doesn't.** Pulling a credential out of a secrets manager at deploy time means a rotation is a secret-store update, not a code change and redeploy.

The practical forms:

- **Cloud-provider secrets managers** — AWS Secrets Manager, Google Secret Manager, Azure Key Vault. IAM-gated, audited, rotatable.
- **Self-hosted** — HashiCorp Vault, CyberArk, Conjur.
- **Kubernetes native** — sealed-secrets patterns, external-secrets operators that pull from the above.

## Why the cloud pushed this up the priority list

The [[shared-responsibility-model]] moves credential protection onto the application engineer. A well-configured secrets manager is how the engineer meets their side of the bargain — the cloud provider secures its control plane, the engineer secures the tokens that let their code talk to it. A leaked token is a zero-trust failure at the application layer.

## Connection to [[encryption-at-rest]] / [[encryption-in-transit]]

Chapter 10's framing: "bad key handling is a significant source of data leaks." Encryption only works if the keys are protected — and keys are just one class of secret. Putting keys in a secrets manager is how encryption stops being a false assurance.

## Anti-patterns to avoid

From the chapter and the general practice it points to:

- Hard-coded credentials in Git, even "temporarily for dev."
- Credentials in `.env` files committed to repos (even private ones).
- Credentials in CI/CD job logs (including stack traces).
- Credentials in Slack messages or email.
- Credentials shared across environments (prod key re-used in staging).
- Long-lived static credentials where short-lived rotated tokens (IAM roles, OIDC federation) would work.

## Related pages

- [[data-security]]
- [[encryption-at-rest]]
- [[encryption-in-transit]]
- [[least-privilege]]
- [[shared-responsibility-model]]
- [[infrastructure-as-code]]
- [[fundamentals-of-data-engineering]]
