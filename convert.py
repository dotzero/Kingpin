#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pdfkit
from glob import glob
from markdown import Markdown

""" Paths """
APP_PATH = os.path.dirname(os.path.realpath(__file__))
CHAPTERS_PATH = os.path.join(APP_PATH, 'chapters/*.md')
HTML_PATH = os.path.join(APP_PATH, 'html')

if not os.path.isdir(HTML_PATH):
    os.mkdir(HTML_PATH)

""" Markdown to HTML """
chapters = sorted([os.path.join(APP_PATH, f) for f in glob(CHAPTERS_PATH)])

template = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title></title>
  <link href="../static/style.css" rel="stylesheet" />
</head>
<body>
%s
</body>
</html>
"""

extension_configs = {
    'markdown.extensions.smarty': {
        'substitutions': {
            'left-single-quote': '&sbquo;',  # sb is not a typo!
            'right-single-quote': '&lsquo;',
            'left-double-quote': '&laquo;',
            'right-double-quote': '&raquo;'
        }
    }
}

md = Markdown(output_format="html5", extensions=['markdown.extensions.smarty'], extension_configs=extension_configs)

for chapter in chapters:
    html = md.reset().convert(open(chapter, 'r').read().decode('utf-8'))
    outhtml = template % html

    filename = os.path.splitext(os.path.basename(chapter))[0] + '.html'
    filepath = os.path.join(HTML_PATH, filename)

    with open(filepath, 'w') as f:
        f.write(outhtml.encode('utf-8'))

""" HTML to PDF """
htmlfiles = [os.path.join(HTML_PATH, f) for f in os.listdir(HTML_PATH) if f.endswith('.html')]

options = {
    'page-size': 'A5',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': 'UTF-8',
    'no-outline': None,
    'no-background': None,
}

pdfkit.from_file(htmlfiles, 'kingpin.pdf', options=options, cover='static/cover.html')
