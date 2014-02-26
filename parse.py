#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import nlp

def loadFile(filename):
    f = open(filename)
    text = nlp.normalize(f.read().decode('utf-8'))
    f.close()

    texts = split(text)
    docs = []
    for text in texts:
        doc = parse(text)
        docs.append(doc)

    return docs

def split(text):
    text = text.replace('\\ID\\', '\n\n\\ID\\')
    return text.split('\n\n')[1:]

def parse(text):
    doc = {}
    for line in text.split('\n'):
        match = re.search(r'^\\(.+)\\(.+)', line)
        if not match:
            continue
        key = match.group(1)
        value = match.group(2)

        if not doc.has_key(key):
            doc[key] = []
        doc[key].append(value)
        
    return doc


if __name__ == '__main__':
    filename = 'data/mai2009_utf8.txt'

    docs = loadFile(filename)

    out_dir = 'output/'
    for doc in docs:
        filename = out_dir + doc['ID'][0] + '.txt'
        article = '\n'.join(doc['T2'])

        f = open(filename, 'w')
        f.write(article.encode('utf-8'))
        f.close()
    
