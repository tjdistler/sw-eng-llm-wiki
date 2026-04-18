---
name: ingest-book
description: "A skill to ingest a Markdown book from `raw/` into the `wiki/` knowledge base."
argument-hint: "[book-title]"
tools: Read, Write, Edit, Bash, Task
disable-model-invocation: true
---

I want to ingest the content of the "$0" book contained in Markdown files under the "raw" directory. I only care about the concepts and ideas of the book, not the structure of the book. I want to create wiki pages for each concept and idea in the book, and link them together in a way that makes sense. I also want to create a summary page for the book that links to all the concept pages. Any concepts that are repeated across chapters should be merged into a single wiki page, and the content from each chapter should be added to that page. If an existing wiki page for a concept already exists, I want to read it carefully and augment it with any new information from the new chapter we are ingesting (including updating the page references). Update wiki/index.md so that the concepts across multiple books are linked together in a way that makes sense. The wiki should be organized in a way that allows me to easily navigate between related concepts and ideas across different books. I want to make sure that the wiki is well-structured and easy to use, with clear links between related concepts and ideas. I don't necessarily care about what concept came from what book; it's the ideas in-general I care about (though every wiki page should reference the source content markdown file it was derived from).

<CRITICAL>Use the Agent tool to ingest the concepts of each chapter one-by-one in a subagent. **DON'T** ingest the chapters in parallel; do it one at a time. Use a subagent to ingest each chapter serially so their content doesn't bloat the main context window and overlapping content will be captured correctly in a serial manner. I only care about **CHAPTERS**, not indexes, prefaces, introductions, or appendices. Focus on the main content of the book. **DON'T** lint the wiki as part of ingestion. I will lint later.</CRITICAL>

## Related files
- `CLAUDE.md`
- `wiki/index.md`
- `wiki/log.md`
