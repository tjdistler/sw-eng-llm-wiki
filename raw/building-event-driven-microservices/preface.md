# Preface

I wrote this book to be the book that I wish I’d had when I started out on my journey into the world of event-driven microservices. This book is a culmination of my own personal experiences, discussions with others, and the countless blogs, books, posts, talks, conferences, and documentation related to one part or another of the event-driven microservice world. I found that many of the works I read mentioned event-driven architectures either only in passing or with insufficient depth. Some covered only a specific aspect of the architecture and, while helpful, provided only a small piece of the puzzle. Other works proved to be reductive and dismissive, asserting that event-driven systems are really only useful for one system to send an asynchronous message directly to another as a replacement for synchronous request-response systems. As this book details, there is far more to event-driven architectures than this. The tools that we use shape and influence our inventions significantly. Event-driven microservice architectures are made possible by a whole host of technologies that have only recently become readily accessible. Distributed, fault-tolerant, high-capacity, and high-speed event brokers underpin the architectures and design patterns in this book. These technological solutions are based on the convergence of big data with the need for near-real-time event processing. Microservices are facilitated by the ease of containerization and the requisitioning of compute resources, allowing for simplified hosting, scaling, and management of hundreds of thousands of microservices. The technologies that support event-driven microservices have a significant impact on how we think about and solve problems, as well as on how our businesses and organizations are structured. Event-driven microservices change how a business works, how problems can be solved, and how teams, people, and business units communicate. These tools give you a truly new way of doing things that has not been possible until only recently.

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

Shows text that should be replaced with user-supplied values or by values determined by context.

### TIP

This element signifies a tip or suggestion.

### NOTE

This element signifies a general note.

### WARNING

This element indicates a warning or caution.

## O’Reilly Online Learning

### NOTE

For more than 40 years, O’Reilly Media has provided technology and business training, knowledge, and insight to help companies succeed. Our unique network of experts and innovators share their knowledge and expertise through books, articles, and our online learning platform. O’Reilly’s online learning platform gives you on-demand access to live training courses, in-depth learning paths, interactive coding environments, and a vast collection of text and video from O’Reilly and 200+ other publishers. For more information, visit http://oreilly.com.

## How to Contact Us

Please address comments and questions concerning this book to the publisher: O’Reilly Media, Inc. 1005 Gravenstein Highway North Sebastopol, CA 95472 800-998-9938 (in the United States or Canada) 707-829-0515 (international or local) 707-829-0104 (fax) We have a web page for this book, where we list errata, examples, and any additional information. You can access this page at https://oreil.ly/building-event-driven-microservices. Email bookquestions@oreilly.com to comment or ask technical questions about this book. For news and information about our books and courses, visit http://oreilly.com. Find us on Facebook: http://facebook.com/oreilly Follow us on Twitter: http://twitter.com/oreillymedia Watch us on YouTube: http://youtube.com/oreillymedia

## Acknowledgments

I’d like to express my respect and gratitude for the people at Confluent, who, along with inventing Apache Kafka, are some of the first people who particularly “get it” when it comes to event-driven architectures. I have been fortunate enough to have one of their members, Ben Stopford (lead technologist, Office of the CTO), provide ample and valuable feedback. Scott Morrison, CTO of PHEMI Systems, has also provided me with valuable insights, feedback, and recommendations. I offer my thanks and gratitude to both Scott and Ben for helping make this book what it is today. As primary proofreaders and technical experts, they have helped me refine ideas, challenged me to improve the content quality, prevented me from promoting incorrect information, and helped me tell the story of event-driven architectures. I would also like to extend my thanks to my friends Justin Tokarchuk, Gary Graham, and Nick Green, who proofread and edited a number of my drafts. Along with Scott and Ben, they helped me to identify the most significant weak points in my narrative, suggested ways to improve them, and provided their insights and personal experience in relation to the material. My thanks also goes out to the folks at O’Reilly for helping me in innumerable ways. I have worked with a number of excellent people during this experience, but in particular I would like to thank my editor, Corbin Collins, for supporting me through some difficult times and helping keep me on track. He has been a great collaborator during this endeavor, and I appreciate the efforts he has put into supporting me. Rachel Monaghan, my copyeditor, reminded me of my high school days, when my essays would be returned colored with red highlights. I am extremely grateful for her sharp eye and knowledge of the English language—she helped make this book far easier to read and understand. Thank you, Rachel. Christopher Faucher has been very patient with me, providing me with excellent feedback and allowing me to make a number of nontrivial, last-minute changes to the book without blinking an eye. Thank you, Chris. Mike Loukides, VP of Content Strategy, was one of my first contacts at O’Reilly. When I approached him with my exceptionally verbose and lengthy proposal, he patiently worked with me to refocus it and refine it into the basis of the book before you today. I am grateful that he took the time to work with me and eventually move forward with this work. I have tried my best to heed his caution to avoid producing a tome that rivals the dictionary in length. To my mother and father, I thank you for giving me appreciation for the written word. I am grateful for their love and support. My father introduced me to Marshall McLuhan, and though I have largely failed to read most of his works, I have gained an immense appreciation for his evaluation on how the medium affects the message. This has transformed the way that I view and evaluate system architectures. Finally, thanks to everyone else who contributed in some way large or small to supporting me and this work. There are so many people who have contributed in their own way—through conversations, blog posts, presentations, open source code, anecdotes, personal experiences, stories, and impromptu rants. Thank you, each and every one of you. It has been both a pleasure and a frustration to work on this book. There have been many times where I cursed myself for starting it, but thankfully there were many more times that I was glad I did. I hope that this book helps you, dear reader, in some way to learn and grow.
