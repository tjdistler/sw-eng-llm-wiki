# Network Access Security

**Summary**: The practical side of protecting networked data systems: which IPs and ports are open, to whom, and why. Chapter 10's observation is that data engineers routinely get this wrong — public S3 buckets, EC2 instances with SSH open to `0.0.0.0/0`, databases accepting inbound traffic from the whole internet. The cloud pushes these decisions onto the data engineer; they must know the basics even when a network-security team exists.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## The problems Reis & Housley see in the wild

Chapter 10 opens the section with a roll call of common data-engineer mistakes (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

- **Public S3 buckets** with sensitive data, accessible to anyone.
- **EC2 instances with SSH open to `0.0.0.0/0`** — every IP on the internet.
- **Databases accepting all inbound traffic over the public internet** — no VPC, no IP allowlist, no VPN.

These are not exotic attacks — they are routine misconfigurations that show up in breach post-mortems year after year.

## The baseline habit

The chapter's prescription is simple in principle, practised unevenly in reality (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Understand what IPs and ports are open, to whom, and why. Allow the incoming IP addresses of the systems and users that will access these ports and avoid broadly opening connections for any reason.

Practical forms:

- **IP allowlists** — explicit ranges of trusted source addresses (office, VPN exit, partner IPs), not `0.0.0.0/0`.
- **VPC / private networking** — keep database and internal service endpoints off the public internet entirely; reach them only through private network paths.
- **VPN / bastion hosts** — human access to internal infrastructure goes through an authenticated gateway, not direct SSH to production.
- **Encrypted connections** — see [[encryption-in-transit]]. Don't use an unencrypted website or SSH from an untrusted network.

## The hardened perimeter vs [[zero-trust-security|zero trust]]

Chapter 10 returns to the Chapter 3 distinction (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> The cloud is generally closer to zero-trust security — every action requires authentication. We believe that the cloud is a more secure option for most organizations because it imposes zero-trust practices and allows companies to leverage the army of security engineers employed by the public clouds.

But:

> However, sometimes hardened perimeter security still makes sense; we find some solace in the knowledge that nuclear missile silos are air gapped (not connected to any networks). Air-gapped servers are the ultimate example of a hardened security perimeter. Just keep in mind that even on premises, air-gapped servers are vulnerable to human security failings.

So:

- **Most cloud data workloads** — zero-trust by default (every request authenticated), network controls layered on top.
- **Exceptional on-prem workloads** — hardened perimeter, possibly air-gapped, for the rare cases where exposure is categorically unacceptable.
- **Either way** — the human is still the weakest link. An air-gapped system doesn't survive an insider with a USB stick.

## When the data engineer is the network engineer

The chapter acknowledges organisational reality: "In principle, network security should be left to security experts at your company. (In practice, you may need to assume significant responsibility for network security in a small company.)" (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md).

Even in large orgs, the data engineer configures security groups, IAM role network conditions, and S3 bucket policies. The [[shared-responsibility-model]] makes those configurations the customer's problem, and the customer is whoever types the `terraform apply`. This is why basic network hygiene is a data-engineer-level skill, not an abstraction the security team handles away.

## Related pages

- [[data-security]]
- [[zero-trust-security]]
- [[shared-responsibility-model]]
- [[encryption-in-transit]]
- [[least-privilege]]
- [[infrastructure-as-code]]
- [[fundamentals-of-data-engineering]]
