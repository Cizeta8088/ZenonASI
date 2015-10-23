#!/usr/bin/env python3
# ZenonASI 20151022
# Author-side include processor
#
# Copyright (c) 2015 by Czq'bqymc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import sys
import os
import re
import argparse
import time
try:
  import markdown
  mdenabled=True
except ImportError as err:
  print("warning: Markdown import failed: try \"pip install markdown\"",file=sys.stderr)
  print("note: Markdown support is disabled.")
  mdenabled=False

# processInclude(m: regex match)
# Processes #include directives.
# Returns output of include function.

def processInclude(m):
  incmode=m.group(1).upper()
  incfile=m.group(2)
  if incmode in ["FILE","VIRTUAL"]:
    output=includeHTML(incfile)
  elif incmode == "TEXT":
    if (mdenabled):
      output=includeMarkdown(incfile)
    else:
      print("warning: Markdown file ignored: "+incfile,file=sys.stderr)
      output="[Markdown file "+incfile+" ignored]"
  else:
    # This shouldn't happen normally
    print("warning: invalid include mode: "+incmode,file=sys.stderr)
    output="[invalid include mode: "+incmode+"]"
  return output

# processEcho(m: regex match)
# Processes #echo directives.

def processEcho(m):
  echovar=m.group(1).upper()
  if echovar == "LAST_MODIFIED":
    mtime=os.path.getmtime(infile)
    output=time.asctime(time.localtime(mtime))
  else:
    output="[invalid echo var: "+echovar+"]"
  return output

# processFDrirectives(m: regex match)
# Processes #flastmod and #fsize directives.

def processFDirectives(m):
  fdirective=m.group(1).upper()
  ffile=m.group(2)
  if fdirective=="FLASTMOD":
    try:
      flastmod=os.path.getmtime(ffile)
      output=time.asctime(time.localtime(flastmod))
    except OSError as err:
      print("warning: getmtime "+ffile+" failed ["+str(err.errno)+"]: "+err.strerror,file=sys.stderr)
      return "[flastmod failed: "+err.strerror+"]"
  elif fdirective=="FSIZE":
    try:
      fsize=os.path.getsize(ffile)
      output=str(fsize)
    except OSError as err:
      print("warning: getsize "+ffile+" failed ["+str(err.errno)+"]: "+err.strerror,file=sys.stderr)
      return "[fsize failed: "+err.strerror+"]"
  else:
    # This shouldn't happen either
    output="[invalid fdirective:"+fdirective+"]"
  return output
  

# includeHTML (f: file to include)
# Returns contents of include file.

def includeHTML(f):
  try:
    with open(f,encoding="utf8") as h:
      html=h.read()
  except OSError as err:
    print("warning: open include "+f+" failed ["+str(err.errno)+"]: "+err.strerror,file=sys.stderr)
    return "[HTML include failed: "+err.strerror+"]"
  return html

# includeMarkdown (f: file to include)
# Returns HTML conversion of include file. 

def includeMarkdown(f):
  try:
    with open(f,encoding="utf8") as m:
      md=m.read()
      html=markdown.markdown(md,output_format="html4")
  except OSError as err:
    print("warning: open include "+f+" failed ["+str(err.errno)+"]: "+err.strerror,file=sys.stderr)
    return "[Markdown include failed: "+err.strerror+"]"
  return html

# init command-line parser
parser = argparse.ArgumentParser(description="Assembles an HTML file and associated includes.",epilog="ZenonASI assumes UTF-8 input and produces UTF-8 output.")
parser.add_argument("infile",help="file to process")
parser.add_argument("outfile",help="output file",nargs="?",default=None)
args=parser.parse_args()

infile=args.infile
if args.outfile==None:
  outfile=os.path.splitext(infile)[0]+".html"
else:
  outfile=args.outfile

#open input file
try:
  page=open(infile,encoding="utf8").read()
except OSError as err:
  print("fatal: open infile failed ["+str(err.errno)+"]: "+err.strerror,file=sys.stderr)
  sys.exit(1)

#process input file
page=re.sub(r'(?i)<!-- *#include *(virtual|file|text)=[\'"]([^\'"]+)[\'"] *-->',processInclude,page)
page=re.sub(r'(?i)<!-- *#echo *var=[\'"]([^\'"]+)[\'"] *-->',processEcho,page)
page=re.sub(r'(?i)<!-- *#(flastmod|fsize) *(?:virtual|file)=[\'"]([^\'"]+)[\'"] *-->',processFDirectives,page)

#produce output file
try:
  with open(outfile,"w",encoding="utf8") as f:
    f.write(page)
except OSError as err:
  print("fatal: open outfile failed ["+str(err.errno)+"]: "+err.strerror,file=sys.stderr)
  sys.exit(1)
