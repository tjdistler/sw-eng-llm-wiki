# Simplicity

Written by Max Luebbe Edited by Tim Harvey The price of reliability is the pursuit of the utmost simplicity. —C.A.R. Hoare, Turing Award lecture Software systems are inherently dynamic and unstable.1 A software system can only be perfectly stable if it exists in a vacuum. If we stop changing the codebase, we stop introducing bugs. If the underlying hardware or libraries never change, neither of these components will introduce bugs. If we freeze the current user base, we’ll never have to scale the system. In fact, a good summary of the SRE approach to managing systems is: “At the end of the day, our job is to keep agility and stability in balance in

> *the system.”2*

## System Stability Versus Agility

It sometimes makes sense to sacrifice stability for the sake of agility. I’ve often approached an unfamiliar problem domain by conducting what I call exploratory coding—setting an explicit shelf life for whatever code I write with the understanding that I’ll need to try and fail once in order to really understand the task I need to accomplish. Code that comes with an expiration date can be much more liberal with test coverage and release management because it will never be shipped to production or be seen by users.

> *1 This is often true of complex systems in general; see [Per99] and [Coo00].*

> *2 Coined by my former manager, Johan Anderson, around the time I became an SRE.*

For the majority of production software systems, we want a balanced mix of stability and agility. SREs work to create procedures, practices, and tools that render software more reliable. At the same time, SREs ensure that this work has as little impact on developer agility as possible. In fact, SRE’s experience has found that reliable processes tend to actually increase developer agility: rapid, reliable production rollouts make changes in production easier to see. As a result, once a bug surfaces, it takes less time to find and fix that bug. Building reliability into development allows developers to focus their attention on what we really do care about—the functionality and performance of their software and systems.

## The Virtue of Boring

Unlike just about everything else in life, “boring” is actually a positive attribute when it comes to software! We don’t want our programs to be spontaneous and interesting; we want them to stick to the script and predictably accomplish their business goals. In the words of Google engineer Robert Muth, “Unlike a detective story, the lack of excitement, suspense, and puzzles is actually a desirable property of source code.” Surprises in production are the nemeses of SRE. As Fred Brooks suggests in his “No Silver Bullet” essay [Bro95], it is very important to consider the difference between essential complexity and accidental complexity. Essential complexity is the complexity inherent in a given situation that cannot be removed from a problem definition, whereas accidental complexity is more fluid and can be resolved with engineering effort. For example, writing a web server entails dealing with the essential complexity of serving web pages quickly. However, if we write a web server in Java, we may introduce accidental complexity when trying to minimize the performance impact of garbage collection. With an eye towards minimizing accidental complexity, SRE teams should: • Push back when accidental complexity is introduced into the systems for which they are responsible • Constantly strive to eliminate complexity in systems they onboard and for which they assume operational responsibility

## I Won’t Give Up My Code!

Because engineers are human beings who often form an emotional attachment to their creations, confrontations over large-scale purges of the source tree are not uncommon. Some might protest, “What if we need that code later?” “Why don’t we just comment the code out so we can easily add it again later?” or “Why don’t we gate the code with a flag instead of deleting it?” These are all terrible suggestions. Source control systems make it easy to reverse changes, whereas hundreds of lines of commented code create distractions and confusion (especially as the source files continue to evolve), and code that is never executed, gated by a flag that is always disabled, is a metaphorical time bomb waiting to explode, as painfully experienced by Knight Capital, for example (see “Order In the Matter of Knight Capital Americas LLC” [Sec13]). At the risk of sounding extreme, when you consider a web service that’s expected to be available 24/7, to some extent, every new line of code written is a liability. SRE promotes practices that make it more likely that all code has an essential purpose, such as scrutinizing code to make sure that it actually drives business goals, routinely removing dead code, and building bloat detection into all levels of testing.

## The “Negative Lines of Code” Metric

The term “software bloat” was coined to describe the tendency of software to become slower and bigger over time as a result of a constant stream of additional features. While bloated software seems intuitively undesirable, its negative aspects become even more clear when considered from the SRE perspective: every line of code changed or added to a project creates the potential for introducing new defects and bugs. A smaller project is easier to understand, easier to test, and frequently has fewer defects. Bearing this perspective in mind, we should perhaps entertain reservations when we have the urge to add new features to a project. Some of the most satisfying coding I’ve ever done was deleting thousands of lines of code at a time when it was no longer useful.

## Minimal APIs

French poet Antoine de Saint Exupery wrote, “perfection is finally attained not when there is no longer more to add, but when there is no longer anything to take away” [Sai39]. This principle is also applicable to the design and construction of software. APIs are a particularly clear expression of why this rule should be followed. Writing clear, minimal APIs is an essential aspect of managing simplicity in a software system. The fewer methods and arguments we provide to consumers of the API, the easier that API will be to understand, and the more effort we can devote to making those methods as good as they can possibly be. Again, a recurring theme appears: the conscious decision to not take on certain problems allows us to focus on our core problem and make the solutions we explicitly set out to create substantially better. In software, less is more! A small, simple API is usually also a hallmark of a wellunderstood problem.

## Modularity

Expanding outward from APIs and single binaries, many of the rules of thumb that apply to object-oriented programming also apply to the design of distributed systems. The ability to make changes to parts of the system in isolation is essential to creating a supportable system. Specifically, loose coupling between binaries, or between binaries and configuration, is a simplicity pattern that simultaneously promotes developer agility and system stability. If a bug is discovered in one program that is a component of a larger system, that bug can be fixed and pushed to production independent of the rest of the system. While the modularity that APIs offer may seem straightforward, it is not so apparent that the notion of modularity also extends to how changes to APIs are introduced. Just a single change to an API can force developers to rebuild their entire system and run the risk of introducing new bugs. Versioning APIs allows developers to continue to use the version that their system depends upon while they upgrade to a newer version in a safe and considered way. The release cadence can vary throughout a system, instead of requiring a full production push of the entire system every time a feature is added or improved. As a system grows more complex, the separation of responsibility between APIs and between binaries becomes increasingly important. This is a direct analogy to objectoriented class design: just as it is understood that it is poor practice to write a “grab bag” class that contains unrelated functions, it is also poor practice to create and put into production a “util” or “misc” binary. A well-designed distributed system consists of collaborators, each of which has a clear and well-scoped purpose. The concept of modularity also applies to data formats. One of the central strengths and design goals of Google’s protocol buffers3 was to create a wire format that was backward and forward compatible.

## Release Simplicity

Simple releases are generally better than complicated releases. It is much easier to measure and understand the impact of a single change rather than a batch of changes released simultaneously. If we release 100 unrelated changes to a system at the same time and performance gets worse, understanding which changes impacted performance, and how they did so, will take considerable effort or additional instrumentation. If the release is performed in smaller batches, we can move faster with more

> *3 Protocol buffers, also referred to as “protobufs,” are a language-neutral, platform-neutral extensible mecha‐*

> *nism for serializing structured data. For more details, see https://developers.google.com/protocol-buffers/docs/*

> *overview#a-bit-of-history.*

confidence because each code change can be understood in isolation in the larger system. This approach to releases can be compared to gradient descent in machine learning, in which we find an optimum solution by taking small steps at a time, and considering if each change results in an improvement or degradation.

## A Simple Conclusion

This chapter has repeated one theme over and over: software simplicity is a prerequisite to reliability. We are not being lazy when we consider how we might simplify each step of a given task. Instead, we are clarifying what it is we actually want to accomplish and how we might most easily do so. Every time we say “no” to a feature, we are not restricting innovation; we are keeping the environment uncluttered of distractions so that focus remains squarely on innovation, and real engineering can proceed.

## PART III

# Practices

Put simply, SREs run services—a set of related systems, operated for users, who may be internal or external—and are ultimately responsible for the health of these services. Successfully operating a service entails a wide range of activities: developing monitoring systems, planning capacity, responding to incidents, ensuring the root causes of outages are addressed, and so on. This section addresses the theory and practice of an SRE’s day-to-day activity: building and operating large distributed computing systems. We can characterize the health of a service—in much the same way that Abraham Maslow categorized human needs [Mas43]—from the most basic requirements needed for a system to function as a service at all to the higher levels of function— permitting self-actualization and taking active control of the direction of the service rather than reactively fighting fires. This understanding is so fundamental to how we evaluate services at Google that it wasn’t explicitly developed until a number of Google SREs, including our former colleague Mikey Dickerson,1 temporarily joined the radically different culture of the United States government to help with the launch of healthcare.gov in late 2013 and early 2014: they needed a way to explain how to increase systems’ reliability. We’ll use this hierarchy, illustrated in Figure III-1, to look at the elements that go into making a service reliable, from most basic to most advanced.

> *1 Mikey left Google in summer 2014 to become the first administrator of the US Digital Service (https://*

> *www.whitehouse.gov/digital/united-states-digital-service), an agency intended (in part) to bring SRE principles*

> *and practices to the US government’s IT systems.*

Figure III-1. Service Reliability Hierarchy

## Monitoring

Without monitoring, you have no way to tell whether the service is even working; absent a thoughtfully designed monitoring infrastructure, you’re flying blind. Maybe everyone who tries to use the website gets an error, maybe not—but you want to be aware of problems before your users notice them. We discuss tools and philosophy in Chapter 10, Practical Alerting from Time-Series Data.

## Incident Response

SREs don’t go on-call merely for the sake of it: rather, on-call support is a tool we use to achieve our larger mission and remain in touch with how distributed computing systems actually work (and fail!). If we could find a way to relieve ourselves of carrying a pager, we would. In Chapter 11, Being On-Call, we explain how we balance oncall duties with our other responsibilities. Once you’re aware that there is a problem, how do you make it go away? That doesn’t necessarily mean fixing it once and for all—maybe you can stop the bleeding by reducing the system’s precision or turning off some features temporarily, allowing it to gracefully degrade, or maybe you can direct traffic to another instance of the service that’s working properly. The details of the solution you choose to implement are necessarily specific to your service and your organization. Responding effectively to incidents, however, is something applicable to all teams. Figuring out what’s wrong is the first step; we offer a structured approach in Chapter 12, Effective Troubleshooting. During an incident, it’s often tempting to give in to adrenalin and start responding ad hoc. We advise against this temptation in Chapter 13, Emergency Response, and counsel in Chapter 14, Managing Incidents, that managing incidents effectively should reduce their impact and limit outage-induced anxiety.

## Postmortem and Root-Cause Analysis

We aim to be alerted on and manually solve only new and exciting problems presented by our service; it’s woefully boring to “fix” the same issue over and over. In fact, this mindset is one of the key differentiators between the SRE philosophy and some more traditional operations-focused environments. This theme is explored in two chapters. Building a blameless postmortem culture is the first step in understanding what went wrong (and what went right!), as described in Chapter 15, Postmortem Culture: Learning from Failure. Related to that discussion, in Chapter 16, Tracking Outages, we briefly describe an internal tool, the outage tracker, that allows SRE teams to keep track of recent production incidents, their causes, and actions taken in response to them.

## Testing

Once we understand what tends to go wrong, our next step is attempting to prevent it, because an ounce of prevention is worth a pound of cure. Test suites offer some assurance that our software isn’t making certain classes of errors before it’s released to production; we talk about how best to use these in Chapter 17, Testing for Reliability.

## Capacity Planning

In Chapter 18, Software Engineering in SRE, we offer a case study of software engineering in SRE with Auxon, a tool for automating capacity planning. Naturally following capacity planning, load balancing ensures we’re properly using the capacity we’ve built. We discuss how requests to our services get sent to datacenters in Chapter 19, Load Balancing at the Frontend. Then we continue the discussion in Chapter 20, Load Balancing in the Datacenter and Chapter 21, Handling Overload, both of which are essential for ensuring service reliability. Finally, in Chapter 22, Addressing Cascading Failures, we offer advice for addressing cascading failures, both in system design and should your service be caught in a cascading failure.

## Development

One of the key aspects of Google’s approach to Site Reliability Engineering is that we do significant large-scale system design and software engineering work within the organization. In Chapter 23, Managing Critical State: Distributed Consensus for Reliability, we explain distributed consensus, which (in the guise of Paxos) is at the core of many of Google’s distributed systems, including our globally distributed Cron system. In Chapter 24, Distributed Periodic Scheduling with Cron, we outline a system that scales to whole datacenters and beyond, which is no easy task. Chapter 25, Data Processing Pipelines, discusses the various forms that data processing pipelines can take: from one-shot MapReduce jobs running periodically to systems that operate in near real-time. Different architectures can lead to surprising and counterintuitive challenges. Making sure that the data you stored is still there when you want to read it is the heart of data integrity; in Chapter 26, Data Integrity: What You Read Is What You Wrote, we explain how to keep data safe.

## Product

Finally, having made our way up the reliability pyramid, we find ourselves at the point of having a workable product. In Chapter 27, Reliable Product Launches at Scale, we write about how Google does reliable product launches at scale to try to give users the best possible experience starting from Day Zero.

## Further Reading from Google SRE

As discussed previously, testing is subtle, and its improper execution can have large effects on overall stability. In an ACM article [Kri12], we explain how Google performs company-wide resilience testing to ensure we’re capable of weathering the unexpected should a zombie apocalypse or other disaster strike. While it’s often thought of as a dark art, full of mystifying spreadsheets divining the future, capacity planning is nonetheless vital, and as [Hix15a] shows, you don’t actually need a crystal ball to do it right. Finally, an interesting and new approach to corporate network security is detailed in [War14], an initiative to replace privileged intranets with device and user credentials. Driven by SREs at the infrastructure level, this is definitely an approach to keep in mind when you’re creating your next network.
