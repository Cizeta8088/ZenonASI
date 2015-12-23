ZenonASI - author side include processor
========================================

Introduction
------------

ZenonASI is a simple author-side include processor that uses the
well-known SSI syntax. It can be used as a substitute for SSI on
Web hosts that only allow static HTML.

ZenonASI is written in Python 3 and uses Python-Markdown to handle
`#include text` directives. If it is not installed, these directives
will be ignored, but ZenonASI will otherwise function.


Supported directives (as of version 20151223):
----------------------------------------------

`file` and `virtual` are treated identically in ZenonASI.

    <!--#include file="file_to_include" -->
    <!--#include virtual="file_to_include" -->

Inserts `file_to_include` into the output file.

    <!--#include text="markdown_file.md" -->

Converts Markdown file `markdown_file.md` into HTML and inserts
it into the output file.

    <!--#echo var="variable_to_echo" -->

Inserts the value of `variable_to_echo` into the output file. Currently,
the only variable supported is `LAST_MODIFIED`.

    <!--#flastmod file="file" -->
    <!--#flastmod virtual="file" -->

Inserts the modification date and time of `file` into the output file.

    <!--#fsize file="file" -->
    <!--#fsize virtual="file" -->

Inserts the size of `file` into the output file.

    <!--#exec cmd="command line" -->

Executes `command line` and inserts the output into the output file.

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
