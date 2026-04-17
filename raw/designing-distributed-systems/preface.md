# Preface

## Who Should Read This Book

At this point, nearly every developer is a developer or consumer (or both) of distributed systems. Even relatively simple mobile applications are backed with cloud APIs so that their data can be present on whatever device the customer happens to be using. Whether you are new to developing distributed systems or an expert with scars on your hands to prove it, the patterns and components described in this book can transform your development of distributed systems from art to science. Reusable components and patterns for distributed systems will enable you to focus on the core details of your application. This book will help any developer become better, faster, and more efficient at building distributed systems.

## Why I Wrote This Book

Throughout my career as a developer of a variety of software systems from web search to the cloud, I have built a large number of scalable, reliable distributed systems. Each of these systems was, by and large, built from scratch. In general, this is true of all distributed applications. Despite having many of the same concepts and even at times nearly identical logic, the ability to apply patterns or reuse components is often very, very challenging. This forced me to waste time reimplementing systems, and each system ended up less polished than it might have otherwise been. The recent introduction of containers and container orchestrators fundamentally changed the landscape of distributed system development. Suddenly we have an object and interface for expressing core distributed system patterns and building reusable containerized components. I wrote this book to bring together all of the practitioners of distributed systems, giving us a shared language and common standard library so that we can all build better systems more quickly.

## The World of Distributed Systems Today

Once upon a time, people wrote programs that ran on one machine and were also accessed from that machine. The world has changed. Now, nearly every application is a distributed system running on multiple machines and accessed by multiple users from all over the world. Despite their prevalence, the design and development of these systems is often a black art practiced by a select group of wizards. But as with everything in technology, the world of distributed systems is advancing, regularizing, and abstracting. In this book I capture a collection of repeatable, generic patterns that can make the development of reliable distributed systems more approachable and efficient. The adoption of patterns and reusable components frees developers from reimplementing the same systems over and over again. This time is then freed to focus on building the core application itself.

## Navigating This Book

This book is organized into a 4 parts as follows: Chapter 1, Introduction Introduces distributed systems and explains why patterns and reusable components can make such a difference in the rapid development of reliable distributed systems. Part I, Single-Node Patterns Chapters 2 through 4 discuss reusable patterns and components that occur on individual nodes within a distributed system. It covers the side-car, adapter, and ambassador single-node patterns. Part II, Serving Patterns Chapters 8 and 9 cover multi-node distributed patterns for long-running serving systems like web applications. Patterns for replicating, scaling, and master election are discussed. Part III, Batch Computational Patterns Chapters 10 through 12 cover distributed system patterns for large-scale batch data processing covering work queues, event-based processing, and coordinated workflows. If you are an experienced distributed systems engineer, you can likely skip the first couple of chapters, though you may want to skim them to understand how we expect these patterns to be applied and why we think the general notion of distributed system patterns is so important. Everyone will likely find utility in the single-node patterns as they are the most generic and most reusable patterns in the book. Depending on your goals and the systems you are interested in developing, you can choose to focus on either large-scale big data patterns, or patterns for long-running servers (or both). The two parts are largely independent from each other and can be read in any order. Likewise, if you have extensive distributed system experience, you may find that some of the early patterns chapters (e.g., Part II on naming, discovery, and load balancing) are redundant with what you already know, so feel free to skim through to gain the high-level insights—but don’t forget to look at all of the pretty pictures!

## Conventions Used in This Book

The following typographical conventions are used in this book: Italic Indicates new terms, URLs, email addresses, filenames, and file extensions.

```
Constant width
```

Used for program listings, as well as within paragraphs to refer to program elements such as variable or function names, databases, data types, environment variables, statements, and keywords.

```
Constant width bold
```

Shows commands or other text that should be typed literally by the user.

```
Constant width italic
```

Shows text that should be replaced with user-supplied values or by values determined by context. This icon signifies a tip, suggestion, or general note. This icon indicates a warning or caution.

## Online Resources

Though this book describes generally applicable distributed system patterns, it expects that readers are familiar with containers and container orchestration systems. If you don’t have a lot of pre-existing knowledge about these things, we recommend the following resources: • https://docker.io • https://kubernetes.io • https://dcos.io

## Using Code Examples

Supplemental material (code examples, exercises, etc.) is available for download at https://github.com/brendandburns/designing-distributed-systems. This book is here to help you get your job done. In general, if example code is offered with this book, you may use it in your programs and documentation. You do not need to contact us for permission unless you’re reproducing a significant portion of the code. For example, writing a program that uses several chunks of code from this book does not require permission. Selling or distributing a CD-ROM of examples from O’Reilly books does require permission. Answering a question by citing this book and quoting example code does not require permission. Incorporating a significant amount of example code from this book into your product’s documentation does require permission. We appreciate, but do not require, attribution. An attribution usually includes the title, author, publisher, and ISBN. For example: “Designing Distributed Systems by Brendan Burns (O’Reilly). Copyright 2018 Brendan Burns, 978-1-491-98364-5.” If you feel your use of code examples falls outside fair use or the permission given above, feel free to contact us at permissions@oreilly.com.

## O’Reilly Safari

Safari (formerly Safari Books Online) is a membership-based training and reference platform for enterprise, government, educators, and individuals. Members have access to thousands of books, training videos, Learning Paths, interactive tutorials, and curated playlists from over 250 publishers, including O’Reilly Media, Harvard Business Review, Prentice Hall Professional, Addison-Wesley Professional, Microsoft Press, Sams, Que, Peachpit Press, Adobe, Focal Press, Cisco Press, John Wiley & Sons, Syngress, Morgan Kaufmann, IBM Redbooks, Packt, Adobe Press, FT Press, Apress, Manning, New Riders, McGraw-Hill, Jones & Bartlett, and Course Technology, among others. For more information, please visit http://oreilly.com/safari.

## How to Contact Us

Please address comments and questions concerning this book to the publisher: O’Reilly Media, Inc. 1005 Gravenstein Highway North Sebastopol, CA 95472 800-998-9938 (in the United States or Canada) 707-829-0515 (international or local) 707-829-0104 (fax) We have a web page for this book, where we list errata, examples, and any additional information. You can access this page at http://bit.ly/designing-distributed-systems. To comment or ask technical questions about this book, send email to bookquestions@oreilly.com. For more information about our books, courses, conferences, and news, see our website at http://www.oreilly.com. Find us on Facebook: http://facebook.com/oreilly Follow us on Twitter: http://twitter.com/oreillymedia Watch us on YouTube: http://www.youtube.com/oreillymedia

## Acknowledgments

I’d like to thank my wife Robin and my children for everything they do to keep me happy and sane. To all of the people along the way who took the time to help me learn all of these things, many thanks! Also thanks to my parents for that first SE/30.
