import sys
import requests as r
import urllib.parse as purl
import json

f = open('../scopus.key')
keys = [ln.strip() for ln in f if len(ln) > 5]
key = keys[0]
f.close()

f = open(sys.argv[1])

journalFields = [('dc:title','title'),
                 ('dc:publisher','publisher')]

def formatJournal(jrnl):
    res = {}
    if ('serial-metadata-response' not in jrnl or 
        'entry' not in jrnl['serial-metadata-response'] or
        len(jrnl['serial-metadata-response']['entry']) == 0): 
        return res
    jrnl = jrnl['serial-metadata-response']['entry'][0]
    for jsId, oId in journalFields:
        res[oId] = jrnl[jsId]
    if 'subject-area' in jrnl and len(jrnl['subject-area']) > 0:
        res['subject'] = jrnl['subject-area'][0]['@abbrev']
        res['subjects'] = "; ".join([sb['$'] for sb in jrnl['subject-area']])

    if 'SNIPList' in jrnl and 'SNIP' in jrnl['SNIPList']:
        res['SNIP'] = jrnl['SNIPList']["SNIP"][0]["$"]
        res['SNIPyear'] = jrnl['SNIPList']["SNIP"][0]["@year"]

    if 'SJRList' in jrnl and 'SJR' in jrnl['SJRList']:
        res['SJR'] = jrnl['SJRList']["SJR"][0]["$"]
        res['SJRyear'] = jrnl['SJRList']["SJR"][0]["@year"]

    if 'IPPList' in jrnl and 'IPP' in jrnl['IPPList']:
        res['IPP'] = jrnl['IPPList']["IPP"][0]["$"]
        res['IPPyear'] = jrnl['IPPList']["IPP"][0]["@year"]
    return res

outp = []
baseUrl = "http://api.elsevier.com/content/serial/title/issn/"
for i,ln in enumerate(f):
    ln = ln.strip().replace("\"","")
    url = purl.urlencode({'apiKey':key,
                          'httpAccept':'application/json'})

    resUrl = "{}{}?{}".format(baseUrl,ln,url)
    m = r.get(resUrl)
    itm = formatJournal(m.json())
    itm['issn'] = ln
    outp.append(itm)

f = open('journalData.json','w')
json.dump(outp,f)
f.close()
