# Zero-Trust Security

**Summary**: A cloud-native security posture that replaces the traditional hardened-perimeter model (trusted inside, untrusted outside) with the assumption that no network location is inherently trustworthy. Reis and Housley treat it as one of the two core ideas inside their [[principles-of-good-data-architecture|security principle]]; the other is the [[shared-responsibility-model]].

**Sources**: `raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md`, `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## The hardened-perimeter model and why it fails

The traditional model: a crude network perimeter, trusted things inside, untrusted things outside (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md). Chapter 3 quotes Google Cloud's framing:

> Traditional architectures place a lot of faith in perimeter security, crudely a hardened network perimeter with "trusted things" inside and "untrusted things" outside. Unfortunately, this approach has always been vulnerable to insider attacks, as well as external threats such as spear phishing.

The cinematic illustration Reis and Housley use: **Mission Impossible (1996)**. The CIA hosts highly sensitive data in a physically secured room; Ethan Hunt compromises a human target inside, gains physical access, and exfiltrates the data. The perimeter was hardened; the person wasn't.

Real-world parallels span at least a decade of security breaches where external threats became internal threats via phishing or human compromise.

## Why the perimeter erodes further in the cloud

Even if you wanted a hard perimeter, the cloud makes it impossible (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md):

- All assets are connected to the outside world to some degree
- VPC networks can be defined with no external connectivity — but **the API control plane that engineers use to configure them still faces the internet**
- Employees work on corporate networks while connected to the world through email and mobile devices

There is no longer a clear boundary between "inside" and "outside."

## The zero-trust posture

The response is to assume **no network location is inherently trustworthy**. Every request is authenticated and authorised regardless of origin. Internal systems do not get implicit trust just because they sit on the same network.

Chapter 3 does not give zero-trust a formal technical treatment — it names the concept as a cloud-native replacement for the hardened perimeter and ties it to the data engineer's new responsibility as a [[data-security|security engineer]] (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

## Chapter 10 — zero-trust vs air-gapped

Chapter 10 revisits the zero-trust framing in its [[network-access-security|network access]] section and offers a pointed concession (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> The cloud is generally closer to zero-trust security — every action requires authentication. We believe that the cloud is a more secure option for most organizations because it imposes zero-trust practices and allows companies to leverage the army of security engineers employed by the public clouds.
>
> However, sometimes hardened perimeter security still makes sense; we find some solace in the knowledge that nuclear missile silos are air gapped (not connected to any networks). Air-gapped servers are the ultimate example of a hardened security perimeter.

Two conclusions fall out of this:

- **Zero trust is the default** for cloud data workloads — the model that reflects how the cloud actually works.
- **Hardened perimeter still wins in narrow cases** — the rare workloads where exposure is categorically unacceptable (nuclear weapons, some military and intelligence systems). The trade-off is usability; an air-gapped system is very hard to work with, which is precisely why its attack surface is small.

And a reminder: "even on premises, air-gapped servers are vulnerable to human security failings." No architecture eliminates the human attack vector — see the [[data-security|people layer]] of security.

## Connection to the data engineer's role

The traditional model also implied an **organisational perimeter**: security and networking teams own all security decisions, and application engineers work behind them. The cloud dissolves this too — the engineer who configures the S3 bucket policy **is** the security engineer in that moment. Misconfigurations like the long string of public S3 bucket breaches are zero-trust failures at the application layer (source: raw/fundamentals-of-data-engineering/chapter-03-designing-good-data-architecture.md).

## Related pages

- [[data-security]]
- [[shared-responsibility-model]]
- [[principles-of-good-data-architecture]]
- [[least-privilege]]
- [[defense-in-depth-data]]
- [[cloud-native-principles]]
