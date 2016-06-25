#!/usr/bin/env python3
from ScopusScrapus import *
from ScopusScrapus.utils import formatScopusEntry
import json

f = open('../scopus.key')
keys = [ln.strip() for ln in f if len(ln) > 5]
f.close()

params = {'query':'TITLE-ABS-KEY(arctic)'}

ppList = []
qExceeded = False
for year in range(2016,1945,-1):
    params['date'] = year
    ssq = StartScopusSearch(keys,params,delay=10)
    for pp in ssq:
        try:
            ppList.append(formatScopusEntry(pp))
        except Exception as e:
            if 'QuotaExceeded' not in str(e):
                raise
            qExceeded = True
            print("Quota Exceeded. Made it to",year)
            break
    if qExceeded: break



outf = open("firstPapers_1.json",'w')
json.dump(ppList,outf)
outf.close()
