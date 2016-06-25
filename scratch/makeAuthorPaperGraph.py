import networkx as nx
import json

f = open('scratch/firstPapers.json')
papers = json.load(f)
f.close()

f = open('scratch/journalData.json')
journals = json.load(f)
f.close()

journalDic = {j['issn']:j for j in journals}

G = nx.Graph()


seenAuths = set()
for i,pp in enumerate(papers):
    addPp = {}
    for k,e in pp.items():
        if e is None: continue
        addPp[k] = e
    pp = addPp
    if 'pubissn' in pp and pp['pubissn'] in journalDic:
        for k,e in journalDic[pp['pubissn']].items():
            if e is None: continue
            pp['pub_'+k] = e
    else:
        if 'pubissn' not in pp: continue
        print("Publication with issn {} unavailable or publication of paper \"{}\" unavailable."
              .format(str(pp.get('pubissn')),pp['title']))

    ppId = 'p{}'.format(i+1)
    authors = pp.get('authors')
    if 'authors' in pp: del pp['authors']

    affiliations = pp.get('affiliations')
    if 'affiliations' in pp: del pp['affiliations']
    G.add_node(ppId,pp)
    if authors is None: continue
    for j, auth in enumerate(authors):
        athId = 'a{}'.format(auth['id'])
        newAuth = {}
        for k,e in auth.items():
            if e is None: continue
            newAuth[k] = e
        auth = newAuth
        if 'affiliations' in auth:
            auth['affiliations'] = ', '.join(auth['affiliations'])
        if athId not in seenAuths:
            seenAuths.add(athId)
            G.add_node(athId,auth)
        G.add_edge(ppId,athId)

nx.write_graphml(G,'author_paper.graphml')
