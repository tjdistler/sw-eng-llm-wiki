# Data Ethics

**Summary**: Ethical considerations for engineers building data-intensive applications, covering predictive analytics bias, surveillance, privacy, consent, and the responsibility to design systems that respect human dignity -- argued by Kleppmann as inseparable from the technical design of data systems. Reis and Housley place ethics and privacy inside the [[data-management]] undercurrent of the [[data-engineering-lifecycle]] and frame the data engineer as squarely on the hook for PII masking, bias tracking, and regulatory compliance (GDPR, CCPA).

**Sources**: `raw/designing-data-intensive-applications/chapter-12-the-future-of-data-systems.md`, `raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md`

**Last updated**: 2026-04-18

---

## Why ethics matters for data engineers

Every system is built for a purpose, but its consequences reach beyond that purpose. Many datasets are about people -- their behavior, interests, and identity. Engineers building data systems carry responsibility for how those systems affect people's lives. The ACM Software Engineering Code of Ethics exists but is rarely discussed, applied, or enforced in practice (source: chapter-12-the-future-of-data-systems.md).

## Predictive analytics

Using data to predict weather or disease spread is one thing; predicting whether a person will reoffend, default on a loan, or make expensive insurance claims directly affects individual lives (source: chapter-12-the-future-of-data-systems.md).

### Bias and discrimination

- Algorithms trained on biased historical data learn and amplify that bias. "Machine learning is like money laundering for bias."
- Features correlated with protected traits (ethnicity, gender, etc.) can produce discriminatory outcomes even when those traits are not directly used. A postal code or IP address can be a strong predictor of race.
- Predictive analytics extrapolate from the past; if the past is discriminatory, they codify that discrimination. Moral imagination is required to do better -- something only humans can provide.

### Accountability

- When automated decisions go wrong, it is unclear who is accountable.
- Credit scores are based on actual borrowing history and can be corrected. ML-based scores use wider inputs, are more opaque, and harder to challenge.
- Predictive systems work on "who is similar to you" rather than "how did you behave" -- stereotyping by association.

### Feedback loops

Self-reinforcing cycles arise: a bad credit score reduces employment chances, which worsens financial difficulties, which further lowers the credit score. Systems thinking (considering the entire system including human interactions) is needed to detect and prevent such loops (source: chapter-12-the-future-of-data-systems.md).

## Surveillance

Kleppmann proposes a thought experiment: replace the word "data" with "surveillance" in common industry phrases. "In our surveillance-driven organization we collect real-time surveillance streams and store them in our surveillance warehouse." The reframing highlights the nature of mass data collection (source: chapter-12-the-future-of-data-systems.md).

Key observations:

- We have built the greatest mass surveillance infrastructure in history, largely through smartphones, smart TVs, voice assistants, and IoT devices.
- The difference from state surveillance is that the data is collected by corporations, not governments -- but governments seek access through secret deals, legal compulsion, or theft.
- Data is not just an asset but a **toxic asset**: breaches happen often, companies go bankrupt and sell user data, and future governments may not share current values.

## Privacy

Privacy does not mean keeping everything secret. It means having the **freedom to choose** which things to reveal to whom. It is a decision right and an aspect of personal autonomy. When companies collect data, this decision right transfers from the individual to the company (source: chapter-12-the-future-of-data-systems.md).

### Consent

- Users have little knowledge of what data is collected or how it's processed. Most privacy policies obscure rather than illuminate.
- Data from one user often reveals things about other people who never consented.
- The relationship between service and user is asymmetric: terms are set by the service, not negotiated.
- For popular services that are de facto mandatory for social participation, opting out is not a realistic choice.

## Recommendations

Kleppmann advocates (source: chapter-12-the-future-of-data-systems.md):

- Treat users as humans deserving respect, dignity, and agency -- not metrics to optimize.
- Self-regulate data collection and processing to maintain trust.
- Educate end users about how their data is used.
- Purge data when no longer needed (despite the appeal of immutability).
- Enforce access control through cryptographic protocols, not just policy.
- Draw parallels to the Industrial Revolution: pollution was the dark side of industrialization; data misuse is the dark side of the information age. Regulation eventually improved industrial practices; similar evolution is needed for data.

> "Data is the pollution problem of the information age, and protecting privacy is the environmental challenge." -- Bruce Schneier (source: chapter-12-the-future-of-data-systems.md)

## FoDE perspective — ethics as a lifecycle undercurrent

Reis and Housley treat ethics and privacy as a **facet of [[data-management]]** that cuts across every stage of the [[data-engineering-lifecycle]]. Their framing opens with Aldo Leopold: "Ethical behavior is doing the right thing when no one else is watching" — with their rejoinder that in data, "everyone will be watching someday" (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md).

What Chapter 2 asks the data engineer to do (source: raw/fundamentals-of-data-engineering/chapter-02-the-data-engineering-lifecycle.md):

- **Mask PII and other sensitive information** across datasets.
- **Identify and track bias** in datasets as they are transformed.
- **Ensure compliance** with GDPR, CCPA, and a growing regulatory stack. "Please take this seriously."

The cultural hope: "more organizations will encourage a culture of good data ethics and privacy." Where Kleppmann argues from first principles for why privacy matters, Reis and Housley take that as given and focus on the **operational responsibility** of the data engineer to implement it — connecting to [[data-lifecycle-management]]'s retention and destruction requirements.

## Related pages

- [[data-integration]]
- [[derived-data]]
- [[reliability]]
- [[maintainability]]
- [[data-management]]
- [[data-governance]]
- [[data-security]]
- [[data-lifecycle-management]]
- [[data-engineering-lifecycle]]
