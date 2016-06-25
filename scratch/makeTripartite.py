import networkx as nx
import json

f = open('scratch/firstPapers.json')
papers = json.load(f)
f.close()

f = open('scratch/journalData.json')
journals = json.load(f)
f.close()

journalDic = {j['issn']:j for j in journals}
institutionDic = {}

for pp in papers:
    if 'affiliations' not in pp: continue
    for j, aff in enumerate(pp['affiliations']):
        if 'id' not in aff or aff['id'] is None or aff['id'] == '': continue
        if not isinstance(aff,str) and len(aff['names']) > 0: 
            aff['name'] = aff['names'][0]
            aff['names'] = ', '.join([nm for nm in aff['names'] if nm is not None])
        newAff = {}
        for k,e in aff.items():
            if e is None: continue
            newAff[k] = e
        aff = newAff
        institutionDic[aff['id']] = aff

G = nx.Graph()


seenAuths = set()
seenAffs = set()
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
    pp['type'] = 'paper'
    G.add_node(ppId,pp)

    if affiliations is not None:
        for j, aff in enumerate(affiliations):
            if 'id' not in aff or aff['id'] is None or aff['id'] == '': continue
            if aff['id'] not in institutionDic: continue
            affId = 'i'+aff['id']
            aff = institutionDic[aff['id']]
            if affId in seenAffs: continue
            seenAffs.add(affId)
            aff['type'] = 'inst'
            G.add_node(affId,aff)
            G.add_edge(ppId,affId) # These might not be useful

    if authors is None: continue
    for j, auth in enumerate(authors):
        athId = 'a{}'.format(auth['id'])
        newAuth = {}
        for k,e in auth.items():
            if e is None: continue
            newAuth[k] = e
        auth = newAuth
        authAffs = []
        if 'affiliations' in auth:
            authAffs = auth['affiliations']
            auth['affiliations'] = ', '.join(auth['affiliations'])
        if athId not in seenAuths:
            seenAuths.add(athId)
            auth['type'] = 'author'
            G.add_node(athId,auth)
        G.add_edge(ppId,athId)
        for aff in authAffs:
            affId = 'i'+aff
            G.add_edge(athId,affId)

nx.write_graphml(G,'tripartite.graphml')
