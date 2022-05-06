#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import zipfile
from glob import glob
from markdown import Markdown

""" Paths """
APP_PATH = os.path.dirname(os.path.realpath(__file__))
MARKDOWN_PATH = os.path.join(APP_PATH, 'markdown/*.md')
EPUB_PATH = os.path.join(APP_PATH, 'epub/OPS')
EPUB_FILENAME = 'Kingpin.epub'

if not os.path.isdir(EPUB_PATH):
    os.mkdir(EPUB_PATH)

""" Markdown to XHTML """
CHAPTERS = sorted([os.path.join(APP_PATH, f) for f in glob(MARKDOWN_PATH)])

TEMPLATE = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ru" xmlns:epub="http://www.idpf.org/2007/ops">
<head><link href="epub.css" media="all" rel="stylesheet" type="text/css" /><title></title></head>
<body>
%s
</body>
</html>
"""

md = Markdown(
    output_format="xhtml1",
    extensions=['markdown.extensions.smarty'],
    extension_configs={
        'markdown.extensions.smarty': {
            'substitutions': {
                'left-single-quote': '&sbquo;',  # sb is not a typo!
                'right-single-quote': '&lsquo;',
                'left-double-quote': '&laquo;',
                'right-double-quote': '&raquo;'
            }
        }
    })

for chapter in CHAPTERS:
    bodyhtml = md.reset().convert(open(chapter, 'r').read())
    xhtml = TEMPLATE % bodyhtml

    filename = os.path.splitext(os.path.basename(chapter))[0] + '.xhtml'
    filepath = os.path.join(EPUB_PATH, filename)

    with open(filepath, 'w') as f:
        f.write(xhtml)


""" XHTML to EPUB """
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.startswith('.'):
                fullpath = os.path.join(root, file)
                ziph.write(fullpath, fullpath.replace(path, ''))

with zipfile.ZipFile(os.path.join(APP_PATH, EPUB_FILENAME), 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(os.path.join(APP_PATH, 'epub'), zipf)

print('PDF file {} was generated.'.format(EPUB_FILENAME))
