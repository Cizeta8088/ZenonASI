#!/usr/bin/env python3
# ZenonASI 20150726
# Author-side include processor

import sys
import os
import re
import argparse
try:
  import markdown
except ImportError as err:
  print("fatal: Markdown import failed: try \"pip install markdown\"",file=sys.stderr)
  sys.exit(1)

# processInclude(m: regex match)
# Processes #include directives.
# Returns output of include function.

def processInclude(m):
  incmode=m.group(1).upper()
  incfile=m.group(2)
  if incmode in ["FILE","VIRTUAL"]:
    output=includeHTML(incfile)
  elif incmode == "TEXT":
    output=includeMarkdown(incfile)
  else:
    # This shouldn't happen normally
    print("warning: invalid include mode: "+incmode,file=sys.stderr)
    output="[invalid include mode: "+incmode+"]"
  return output

# includeHTML (f: file to include)
# Returns contents of include file.

def includeHTML(f):
  try:
    with open(f,encoding="utf8") as h:
      html=h.read()
  except IOError as err:
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
  except IOError as err:
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
except IOError as err:
  print("fatal: open infile failed ["+str(err.errno)+"]: "+err.strerror,file=sys.stderr)
  sys.exit(1)

#process input file
page=re.sub(r'(?i)<!-- *#include *(virtual|file|text)=[\'"]([^\'"]+)[\'"] *-->',processInclude,page)

#produce output file
try:
  with open(outfile,"w",encoding="utf8") as f:
    f.write(page)
except IOError as err:
  print("fatal: open outfile failed ["+str(err.errno)+"]: "+err.strerror,file=sys.stderr)
  sys.exit(1)
