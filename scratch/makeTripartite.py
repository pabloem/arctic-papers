import networkx as nx
import json
import csv
import itertools

from utilities import (PaperGenerator,
                       OpenRefinePaperGenerator,
                       NamesIdDictionary)


def load_journals(file_name='data/journalData.json'):
  with open(file_name) as f:
    journals = json.load(f)
  journal_dictionary = {j['issn']:j for j in journals}
  return journal_dictionary

def load_important_authors(file_name='data/acia.csv'):
  with open(file_name) as f:
    ids = [a[0] for a in list(csv.reader(f))]
  return ids

acia_auths = set(load_important_authors())


journalDic = load_journals()
#papers = PaperGenerator()
papers = OpenRefinePaperGenerator()

def different_institutions(x, y):
  return (x['names'] != y['names'] and
          all([x[k] != y[k] for k in ['country', 'city']
              if k in y and k in x and None not in [x[k], y[k]]] or [False]))

institution_dictionary = NamesIdDictionary(
                    differentiator=different_institutions)
for pp in papers:
  if 'affiliations' not in pp: continue
  for j, aff in enumerate(pp['affiliations']):
    try:
      institution_dictionary.add(aff)
    except KeyError:
      continue

G = nx.Graph()

def fill_in_publication_data(pp, pub):
    for k,e in pub.items():
        if e is None: continue
        pp['pub_'+k] = e

seenAuths = set()
seenAffs = set()
for i, pp in enumerate(papers):
    addPp = {}

    # First we clean the paper info from None fields
    for k,e in pp.items():
        if e is None: continue
        addPp[k] = e
    pp = addPp

    # The we check that the paper has an ISSN (we ignore books), and that the
    # publication is one that we know.
    if 'pubissn' in pp and pp['pubissn'] in journalDic:
        fill_in_publication_data(pp, journalDic[pp['pubissn']])
    else:
        if 'pubissn' not in pp: continue
        journalDic[pp['pubissn']] = {'issn':pp['pubissn']}
        fill_in_publication_data(pp, journalDic[pp['pubissn']])
        print("Publication with issn {} unavailable or publication of paper \"{}\" unavailable."
              .format(str(pp.get('pubissn')),pp['title']))

    ppId = 'p{}'.format(i+1)

    # Now we retrieve author information from a paper.
    authors = pp.get('authors')
    if 'authors' in pp: del pp['authors']
    if authors is None or len(authors) == 0:
        # If there are no authors in the paper, we ignore it
        continue

    # Now we retrieve affiliation information for a paper
    affiliations = pp.get('affiliations')
    if 'affiliations' in pp: del pp['affiliations']
    if affiliations is None or len(affiliations) == 0:
        # If there are no affiliations in the paper, we ignore it
        continue
    pp['category'] = 'paper'
    G.add_node(ppId,pp)

    if affiliations is not None:
        for j, aff in enumerate(affiliations):
            if not aff.get('id'): continue
            aff = institution_dictionary.get(aff['id'])
            if not aff: continue
            try:
                ids = sorted(list(
                        institution_dictionary.get_ids_from_id(aff['id'])))
            except TypeError:
                print(aff)
            if len(ids) > 1:
                print('Long ids. Good. {}'.format(str(ids)))
            affId = 'i'+ids[0]
            if affId in seenAffs: continue
            seenAffs.add(affId)
            aff['category'] = 'inst'
            G.add_node(affId,aff)
            G.add_edge(ppId,affId) # These might not be useful

    if authors is None: continue
    for j, auth in enumerate(authors):
        if 'id' not in auth:
            continue
        auth['acia'] = auth['id'] in acia_auths
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
            auth['category'] = 'author'
            G.add_node(athId,auth)
        G.add_edge(ppId,athId)
        for aff in authAffs:
            affId = 'i'+aff
            G.add_edge(athId,affId)

nx.write_graphml(G,'tripartite.graphml')
