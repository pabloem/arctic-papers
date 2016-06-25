import json
f = open('firstPapers.json')
papers = json.load(f)
f.close()

authors = []
affiliations = []

author_id = 

for p in papers:
    ath = p['authors']
    for a in ath:
        
