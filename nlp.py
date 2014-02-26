#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unicodedata
import MeCab


def normalize(text):
    return unicodedata.normalize('NFKC', text)

def tokenize(text, pos=False):
    import MeCab
    uni = text.encode('utf-8')
    tagger = MeCab.Tagger("-Ochasen")
    node = tagger.parseToNode(uni)

    terms = []
    posids = []
    while node:
        surface = node.surface
        features = node.feature.split(',')
        basic_form = features[6]
        if basic_form == '*':
            basic_form = surface
        terms.append(basic_form.decode('utf-8'))
        posids.append(node.posid)
        node = node.next
    if pos:
        return terms[1:-1], posids[1:-1]
    else:
        return terms[1:-1]


def extract_noun(terms, posids):
    return extract(terms, posids, range(36, 67+1))

def extract_verb(terms, posids):
    return extract(terms, posids, range(31, 33+1))

def extract_no_pronoun(terms, posids):
    extract_posids = [posid for posid in range(0, 68+1) if not posid in [59, 60]]
    return extract(terms, posids, extract_posids)

def extract_disindependent(terms, posids):
    extract_posids = [posid for posid in range(0, 68+1) if not posid in [58, 66, 67]]
    return extract(terms, posids, extract_posids)


def term_frequency(terms):
    tf = {}
    for t in terms:
        if not tf.has_key(t):
            tf[t] = 0
        tf[t] += 1
    return tf


if __name__ == '__main__':
    docs = [u'山下さんは山下くんと東京特許許可局へ行った。',
            u'山下さんは山下くんと北海道へ行った。',
            u'山下さんは下山くんと New York へ行った。',
            u'山上さんは山下くんと東京特許許可局へ行った。',]             

    texts = []
    for text in docs:
        terms = tokenize(text)
        texts.append(terms)

    for terms in texts:
        print ' '.join(terms)
        
        tf = term_frequency(terms)
        print ' | '.join(["%s, %d" % (t, f) for t, f in tf.items()])
        
