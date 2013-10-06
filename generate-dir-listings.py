#!/usr/bin/env python
#coding: utf8
"""
Creates a static HTML page listing the contents of a directory.
"""

import os
import os.path
import codecs
import zipfile

header = \
u"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Index of {thisdir}</title>
  <link href='http://fonts.googleapis.com/css?family=Open+Sans:400' rel='stylesheet' type='text/css'>
  <link href='http://fonts.googleapis.com/css?family=Droid+Serif:700' rel='stylesheet' type='text/css'>
  <style type="text/css">
body {{
	font-family: "Open Sans", Calibri, sans-serif;
	max-width: 600px;
	margin: 0 auto;
	padding-top: 1em;
}}
a {{
	text-decoration: none;
	color: #1f609f;
}}
a:visited {{
	color: #1f609f;
}}
a:hover {{ 
	text-decoration: underline; 
}}
h1 {{
	font-family: "Droid Serif", georgia, times, serif;
	color: #204a87;
	border-bottom: 3px solid #729fcf;
	display: inline;
	text-align: center;
}}
p.linkup::before {{
	content: '\N{black up-pointing triangle} ';
}}
p.download::before {{
	content: '\N{downwards arrow} ';
}}
li.dir::before {{
	content: '\N{black right-pointing triangle} ';
}}
ul {{
	list-style-type: none;
}}
  </style>
</head>
<body>
  <h1>Index of {thisdir}</h1>
  {linkup}
  <p class="download">
    <a href="{zipfile}">Download all files</a>
  </p>
  <ul>
"""

linkup = \
"""  <p class="linkup">
    <a href="{updir}">Up to higher level directory</a>
  </p>
"""

item = \
"""<li class="{cls}">
  <a href="{link}">{name}</a>
</li>
"""

footer = """
</ul>
</body>
</html>"""

def output_html(topdir, subdir=False):
	files = os.listdir(topdir)
	dirnames = [n for n in files if os.path.isdir(os.path.join(topdir, n))]
	filenames = list(set(files) - set(dirnames))
	dirnames.sort()
	filenames.remove('index.html')
	filenames.remove('contents.zip')
	filenames.sort()

	for dirname in dirnames:
		output_html(os.path.join(topdir, dirname), subdir=True)

	html_outfile = os.path.join(topdir, 'index.html')
	zip_outfile = os.path.join(topdir, 'contents.zip')

	with codecs.open(html_outfile, 'w', encoding='utf-8') as fp:
		linkup_text = linkup.format(updir='../index.html') if subdir else ''
		fp.write(header.format(thisdir=topdir, linkup=linkup_text,
			zipfile='contents.zip'))
		for name in dirnames:
			fp.write(item.format(name=name, link=name + '/index.html', 
				cls="dir"))
		for name in filenames:
			if name.startswith('.'):
				continue
			fp.write(item.format(name=name, link=name, cls="file"))
		fp.write(footer)
	
	with zipfile.ZipFile(zip_outfile, 'w') as zp:
		for root, dirs, files in os.walk(topdir):
			files.remove('index.html')
			files.remove('contents.zip')
			for name in dirs + files:
				zp.write(os.path.join(root, name))

if __name__ == '__main__':
	for name in os.listdir('.'):
		if os.path.isdir(name) and name != 'html' and not name.startswith('.'):
			output_html(name)
