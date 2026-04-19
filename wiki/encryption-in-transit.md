# Encryption in Transit

**Summary**: Encrypting data on the wire — between client and service, between services, between services and storage. Chapter 10 treats it as **default** for modern cloud APIs: HTTPS is generally required. It protects against network interception and man-in-the-middle attacks but is routinely undermined by key mishandling, open bucket permissions, and legacy unencrypted protocols (FTP the canonical example).

**Sources**: `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## The modern default

Reis & Housley's framing (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Encryption over the wire is now the default for current protocols. For instance, HTTPS is generally required for modern cloud APIs.

That is: HTTPS / TLS is no longer optional optimisation — it is baseline assumption in any serious cloud environment. Unencrypted HTTP to a cloud API is almost certainly a misconfiguration.

## What encryption in transit does

- Prevents **network eavesdropping** (passive interception on wifi, ISPs, intermediate routers).
- Prevents **man-in-the-middle modification** — an attacker intercepting your download cannot silently modify the bytes before they arrive at the client.
- Authenticates the server (TLS certificate chain) so clients know they are talking to the real service.

## What it does not do

Chapter 10 flags two common failure modes where encryption in transit is in place but irrelevant (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

1. **Key mishandling.** "Bad key handling is a significant source of data leaks." TLS keys, API keys, signing keys — if they leak, the encrypted channel is compromised. Store keys in a [[secrets-management|secrets manager]].
2. **Open bucket permissions.** "HTTPS does nothing to protect data if bucket permissions are left open to the public." The canonical cause of the last decade's S3 scandals — the channel is encrypted, but anyone can use it. Network encryption is orthogonal to authorisation.

## The FTP anti-example

Chapter 10 singles out FTP as the archetypal unencrypted protocol to avoid (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> FTP is simply not secure on a public network. While this may not appear to be a problem when data is already public, FTP is vulnerable to man-in-the-middle attacks, whereby an attacker intercepts downloaded data and changes it before it arrives at the client. It is best to simply avoid FTP.

The general rule: **encrypt everything on the wire, even legacy protocols** — or replace the legacy protocol. If you must use FTP, use FTPS or SFTP. If you must use telnet, don't.

## At the engineer's daily scale

Chapter 10's practical-habit examples:

- Don't use an unencrypted website from a coffee shop when accessing cloud consoles or SaaS tools.
- Prefer VPN or HTTPS-everywhere tooling when on public wifi.
- Check that legacy pipeline endpoints (partner SFTP drops, third-party APIs) actually negotiate TLS and aren't silently falling back to plaintext.

## Relationship to [[encryption-at-rest]]

Encryption at rest and in transit are complementary, not substitutes. Data is encrypted on disk, decrypted on read, encrypted on the wire, decrypted by the client, possibly re-encrypted at application level. Each layer protects a different attack surface; weakness in any one undermines the whole chain.

## Related pages

- [[data-security]]
- [[encryption-at-rest]]
- [[secrets-management]]
- [[network-access-security]]
- [[zero-trust-security]]
- [[fundamentals-of-data-engineering]]
