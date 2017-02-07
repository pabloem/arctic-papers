""" This script is a sketch of the script that makes the country collaboration
graph for future reference. This was used on Jan 31 2017."""


country_edges = defaultdict(lambda : 0)

for p in all_papers:
  if len(p['affiliations']) < 2:
    continue
  countries = [a['country'] for a in p['affiliations'] if a.get('country')]
  if len(countries) < 2:
    continue
  print('Countries: {}'.format(countries))
  combos = combinations(countries, 2)
  for combo in combos:
    combo = sorted(combo)
    key = tuple(combo)
    country_edges[key] += 1

G = nx.Graph()
for k, v in country_edges.items():
  c1 = k[0]
  c2 = k[1]
  G.add_node(c1)
  G.add_node(c2)
  G.add_edge(c1, c2, weight=v)
