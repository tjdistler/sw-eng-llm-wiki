# Encryption at Rest

**Summary**: Encrypting data on storage devices — disks, filesystems, databases, object storage, backups. Chapter 10 calls it a **baseline requirement** for any organisation that respects security and privacy. It protects against stolen devices and compromised storage media, but does *nothing* against a human breach that grants legitimate credentials. Pair with [[encryption-in-transit]] and [[secrets-management]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## What to encrypt

Chapter 10's shopping list (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

- **Laptops** — full-disk encryption, so a stolen or lost device does not become a data leak.
- **Servers and filesystems** — server-side encryption for on-prem or managed.
- **Databases** — managed cloud databases almost always offer this as a checkbox.
- **Object storage** ([[object-storage]]) — S3 / GCS / Azure Blob all provide server-side encryption with provider-managed or customer-managed keys.
- **Backups** — "All data backups for archival purposes should also be encrypted." A surprisingly common gap: production data is encrypted but the backup tapes/snapshots are not. See [[backups-vs-archives]].
- **Application-level encryption** — encrypt specific fields inside the application before they ever reach storage, useful for the most sensitive data (passwords should be hashed, not just encrypted).

## What encryption at rest does not do

The chapter is explicit (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Encryption is not a magic bullet. It will do little to protect you in the event of a human security breach that grants access to credentials.

If the attacker has valid credentials, the storage system decrypts the data for them on the way out — that is exactly what encryption at rest is designed to do for legitimate users. Encryption protects against:

- **Physical theft of storage media** — stolen laptop, hard drive, backup tape.
- **Provider-level mis-access** — a cloud employee with physical disk access cannot read your data (if you use customer-managed keys).
- **Misconfigured permissions on underlying storage** — if a bucket is accidentally made public but encrypted with customer-managed keys, attackers still need the keys.

It does *not* protect against:

- Phished credentials (attacker logs in, storage hands them the decrypted data).
- Misconfigured application-level permissions that grant broad access.
- Database queries from a legitimate user with too much privilege — see [[least-privilege]].

## Keys are the weak point

Encryption just moves the problem from "protect the data" to "protect the keys." Chapter 10 explicitly flags key handling as a major leak vector: "bad key handling is a significant source of data leaks." Keys belong in a dedicated [[secrets-management|secrets manager]], not in code, not in environment-variable defaults, not in a shared wiki.

## Encryption and [[defense-in-depth-data|defense in depth]]

Encryption at rest is one of the baseline layers in a defence-in-depth stack. On its own it is weak; combined with [[least-privilege]], [[network-access-security|network access controls]], [[encryption-in-transit]], and [[security-monitoring|monitoring]], it raises the cost of every plausible attack.

## Related pages

- [[data-security]]
- [[encryption-in-transit]]
- [[secrets-management]]
- [[least-privilege]]
- [[backups-vs-archives]]
- [[object-storage]]
- [[fundamentals-of-data-engineering]]
