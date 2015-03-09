#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

if __name__ == '__main__':
    import sys
    filenames = sys.argv[1:]
    
    # filenames = filenames[0:10]

    for filename in filenames:
        # print filename
        f = open(filename)
        article = json.loads(f.read())
            if n != 1:
                print filename, n

# ID, AD, AE, AF, C0, T1, S1, S2


