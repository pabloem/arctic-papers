#!/usr/bin/env python
import sys

import networkx as nx

def section():
  print('')

G = nx.read_graphml(sys.argv[1])

paper_ids = [p for p in G.nodes() if 'p' in p]
author_ids = [p for p in G.nodes() if 'a' in p]
institution_ids = [p for p in G.nodes() if 'i' in p]

print('{} papers. {} authors. {} institutions.'.format(len(paper_ids),
                                                       len(author_ids),
                                                       len(institution_ids)))

# Removing all institutions
[G.remove_node(p) for p in institution_ids]

section()
connected_components_sizes = sorted(
    [len(a) for a in nx.connected_components(G)],
    key=lambda x: -x)
print(
    'The author-publication graph has {} nodes, {} connected components.'
    .format(len(G.nodes()), len(connected_components_sizes)))
print('Their sizes: {}, etc.'.format(connected_components_sizes[0:10]))

from collections import Counter
author_publications_distribution = Counter(G.degree(a) for a in author_ids)

section()
print('{} authors have ONE publication.'.format(
    author_publications_distribution[1]))
print('{} authors have TWO publications.'.format(
    author_publications_distribution[2]))
print('{} authors have THREE publications.'.format(
    author_publications_distribution[3]))
low_count = sum(author_publications_distribution[i] for i in range(1,4))
print('{} authors have MORE THAN THREE publications.'.format(
    len(author_ids) - low_count))

section()
publication_authors_distribution = Counter(G.degree(a) for a in paper_ids)
print('{} papers have ONE author.'.format(
    publication_authors_distribution[1]))
print('{} papers have TWO authors.'.format(
    publication_authors_distribution[2]))
print('{} papers have THREE authors.'.format(
    publication_authors_distribution[3]))
low_count = sum(publication_authors_distribution[i] for i in range(1,4))
print('{} papers have MORE THAN THREE authors.'.format(
    len(paper_ids) - low_count))

G = nx.read_graphml(sys.argv[1])
# Removing all papers
[G.remove_node(p) for p in paper_ids]

section()
connected_components_sizes = sorted(
    [len(a) for a in nx.connected_components(G)],
    key=lambda x: -x)
print(
    'The author-institution graph has {} nodes, {} connected components.'
    .format(len(G.nodes()), len(connected_components_sizes)))
print('Their sizes: {}, etc.'.format(connected_components_sizes[0:10]))



author_institutions_distribution = Counter(G.degree(a) for a in author_ids)
section()
print('{} authors have ONE institutions.'.format(
    author_institutions_distribution[1]))
print('{} authors have TWO instututions.'.format(
    author_institutions_distribution[2]))
print('{} authors have THREE institutions.'.format(
    author_institutions_distribution[3]))
low_count = sum(author_institutions_distribution[i] for i in range(1,4))
print('{} authors have MORE THAN THREE institutions.'.format(
    len(author_ids) - low_count))


institution_authors_distribution = Counter(G.degree(a) for a in institution_ids)
section()
print('{} institutions have ONE author.'.format(
    institution_authors_distribution[1]))
print('{} institutions have TWO authors.'.format(
    institution_authors_distribution[2]))
print('{} institutions have THREE authors.'.format(
    institution_authors_distribution[3]))
low_count = sum(institution_authors_distribution[i] for i in range(1,4))
print('{} institutions have MORE THAN THREE authors.'.format(
    len(institution_ids) - low_count))
