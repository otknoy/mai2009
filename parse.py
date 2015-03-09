#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unicodedata
import json

import nkf
import re

class ArticleBuilder:
    def __init__(self):
        self.id = 0


def load_mai2009(filename):
    f = open(filename)
    for line in f:
        line =  nkf.nkf('-w', line).decode('utf-8')

        tag, content = parse_line(line)

        tag = normalize(tag)
        content = normalize(content)

        print tag, content

line_pattern = re.compile(ur'^＼(..)＼(.+)')
def parse_line(line):
    m = line_pattern.search(line)
    tag = m.group(1)
    content = m.group(2)
    return tag, content


def split(s):
    s = s.replace(u'＼ＩＤ＼', u'\n＼ＩＤ＼')
    return s.split('\n\n')[1:]

def normalize(s):
    return unicodedata.normalize('NFKC', s)

def format_to_csv(s):
    temp = []
    for l in s.split('\n'):
        match = re.search(r'^\\(.+)\\(.+)', l)
        if not match:
            continue

        k = match.group(1)
        v = match.group(2).strip()
        temp.append(k + ',' + v)
    return '\n'.join(temp)

def parse(s):
    doc = {}
    for l in s.split('\n'):
        match = re.search(r'^\\(.+)\\(.+)', l)
        if not match:
            continue
        k = match.group(1)
        v = match.group(2)
        if not doc.has_key(k):
            doc[k] = []
        doc[k].append(v)
    return doc

def format(d):
    # d = json.dumps(d, indent=True, sort_keys=True)
    s = ''
    for k, v in d.items():
        for e in v:
            s += '%s,%s\n' % (k, e)
    return s.encode('utf-8')

def output_to_file(doc):
    out_dir = 'output'
    # fname = doc['ID'][0] + '_' + doc['T1'][0] + '.txt'
    fname = doc['ID'][0] + '.txt'    
    filename = os.path.join(out_dir, fname)

    f = open(filename, 'w')
    f.write(format(d))
    f.close()


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]

    text_file = load_mai2009(filename)



    # text = open(filename).read().decode('utf-8')
    # articles = split(text)

    # for article in articles:
    #     a = normalize(article)
    #     d = parse(a)
    #     output_to_file(d)
