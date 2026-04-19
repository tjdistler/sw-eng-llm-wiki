# Security Policy

**Summary**: Chapter 10 offers a short, deliberately unelaborate example security policy — three sections (credentials, devices, software updates), a single page of practical rules, written so that real humans might actually follow them. The policy is an antidote to [[security-theater]]: small, memorable, habitual.

**Sources**: `raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md`

**Last updated**: 2026-04-18

---

## Design philosophy: short, practical, habitual

Chapter 10 explicitly frames the example as a counterweight to the 200-page unread policy document (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

> Notice that we don't overcomplicate things; instead, we give people a short list of practical actions they can take immediately.

The premise: a policy people actually remember and follow beats a comprehensive policy that nobody reads. See [[security-theater]] for the broader argument.

## Protect your credentials

- Use single sign-on (SSO) for everything. Avoid passwords whenever possible; SSO is the default. See [[secrets-management]].
- Use **multi-factor authentication** with SSO.
- **Never share** passwords or credentials — including client passwords. If in doubt, escalate until someone in authority confirms.
- Beware of phishing and scam calls. **Never give your passwords out.**
- **Disable or delete old credentials.** Preferably delete.
- **Never put credentials in code.** Handle secrets as configuration; never commit to version control; use a [[secrets-management|secrets manager]].
- Always exercise [[least-privilege|least privilege]]. Never grant more access than the job requires — cloud or on-prem.

## Protect your devices

- **Use device management** for every device used by employees — so that a lost or departed-employee device can be remotely wiped.
- **Use multi-factor authentication** for all devices.
- **Sign in with company email credentials** — the device inherits the org's SSO + MFA.
- Treat the device as an extension of yourself: **don't let it out of your sight**.
- When screen-sharing, share single documents, tabs, or windows — not your full desktop. Use "do not disturb" mode to stop message pop-ups during calls or recordings.

## Software update policy

- **Restart your browser** when you see an update alert.
- **Install minor OS updates** on company and personal devices.
- The company identifies **critical major OS updates** and sends guidance.
- **Don't use OS beta versions.** Wait a week or two before adopting major OS releases.

The policy piece is "humans do the updates on their devices"; the engineering piece (covered in Chapter 10's technology section) is "automation does the updates on the servers" — either by choosing managed services that patch themselves or by setting alerts on new releases and CVEs so the engineer can update manually.

## What makes this policy effective

Structural properties the chapter emphasises (source: raw/fundamentals-of-data-engineering/chapter-10-security-and-privacy.md):

- **Actionable in minutes, not hours.** Every rule can be followed today without a training course.
- **Concrete, not abstract.** "Don't let your device out of your sight" is behavioural; "maintain physical security posture" is not.
- **Short.** The whole policy fits on a page. People can re-read it in a monthly security review.
- **Habit-forming.** Monthly review + leadership modelling + small rule-set = cultural retention.

The authors note: "Based on your company's security profile, you may need to add more requirements for people to follow." The template is deliberately a starting point, not a ceiling.

## The closing reminder

Chapter 10 ends the example policy with the line that frames every section: "People are your weakest link in security." Everything in the policy is designed with that reality in mind — simple enough for tired humans on bad days, specific enough to catch the common failure modes.

## Related pages

- [[data-security]]
- [[security-theater]]
- [[active-security]]
- [[least-privilege]]
- [[secrets-management]]
- [[fundamentals-of-data-engineering]]
