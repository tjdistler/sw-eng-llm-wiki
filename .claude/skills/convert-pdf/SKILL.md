---
name: convert-pdf
description: "A skill to convert a PDF file into Markdown format and save it in the `raw/` directory for further processing."
argument-hint: "[book-title]"
tools: Read, Write, Edit, Bash, Task
disable-model-invocation: true
---


I've added the book "$0" as a PDF to the raw directory and I want to convert it to Markdown. Please run the pdf-extractor to extract the contents into Markdown files under a dedicated directory in raw (similar to other books already present). Don't ingest the book yet; only convert the pdf to markdown. The pdf-extractor project has a README and REQUIREMENTs doc if you need it.

<CRITICAL>If you need to make changes to the pdf-extractor, I need you to verify this won't break the parsing of existing books. You **MUST** test any changes you make using the following steps before proceeding with the conversion of the new book:
1. Create a directory under /tmp specifically to test your changes.
2. Copy extractor.py to extractor.py.bak in the /tmp directoryto preserve the original version
3. Test extracting existing books into the test directory and verify the results match the already-converted markdown files in the raw directory.
</CRITICAL>