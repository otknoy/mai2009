#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import nkf
import unicodedata
import json
import os

def load_mai2009(filename):
    text = open(filename).read()
    text = nkf.nkf('-w', text)
    text = text.rstrip()
    return text.decode('utf-8')

def split_mai2009(text):
    text = text.replace(u'＼ＩＤ＼', u'\n＼ＩＤ＼')
    return text.split('\n\n')[1:]

def normalize(s):
    return unicodedata.normalize('NFKC', s)

multiple_tags = ['AA', 'KA', 'AB', 'KB', 'T2']
def parse2dict(text):
    doc = {}
    for line in text.splitlines():
        tag, content = parse_line(line)
        content = content.strip()

        if tag in multiple_tags:
            if not doc.has_key(tag):
                doc[tag] = []
            doc[tag].append(content)
        else:
            if tag in doc:
                print 'error'
            doc[tag] = content
    return doc

line_pattern = re.compile(ur'^\\(..)\\(.*)')
def parse_line(line):
    m = line_pattern.search(line)
    tag = m.group(1)
    content = m.group(2)
    return tag, content

def save_as_json(filename, s):
    j = json.dumps(s, ensure_ascii=False, indent=True)
    f = open(filename, 'w')
    f.write(j.encode('utf-8'))
    f.close()


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]

    print "Loding file: %s" % filename
    text = load_mai2009(filename)

    print "Split loaded file"
    articles = split_mai2009(text)
    del text

    print "Output files as json"
    for article in articles:
        article = normalize(article)
        d = parse2dict(article)
        del article

        output_filename = os.path.join('output', d['ID'] + '.json')
        save_as_json(output_filename, d)

    print "Finish!"
