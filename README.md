ZenonASI - author side include processor
========================================

Introduction
------------

ZenonASI is a simple author-side include processor that uses the
well-known SSI syntax. It can be used as a substitute for SSI on
Web hosts that only allow static HTML.

ZenonASI is written in Python 3 and currently requires Python-Markdown.


Supported commands (as of version 20150726):
--------------------------------------------

    <!--include file="file_to_include" -->
    <!--include virtual="file_to_include" -->

Inserts `file_to_include` into the output file. (Both are treated
identically in ZenonASI.)

    <!--include text="markdown_file.md" -->

Converts Markdown file `markdown_file.md` into HTML and inserts
it into the output file.


Command line:
-------------

From `zenonasi -h`:

```
usage: zenonasi [-h] infile [outfile]

Assembles an HTML file and associated includes.

positional arguments:
  infile      file to process
  outfile     output file

optional arguments:
  -h, --help  show this help message and exit

ZenonASI assumes UTF-8 input and produces UTF-8 output.
```
