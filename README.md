## Dataset of Arctic-related papers
The dataset contains two main graphs:
* A bipartite graph of authors and papers
* A **tripartite** graph of authors, papers, and institutions. This is the main graph. To operate over 'pairs' of nodesets, it is only necessary to remove nodes of type 'paper', 'inst' or 'author'.

The code to ceate the datasets is in `scratch/`. Their functions are the following:
* `scratch/scrapePapers.py` - It scrapes all papers containing the word 'arctic' in their title, keywords or abstract, every year back to 1945.
* `scratch/scrapeIssn.py` - Takes in a list of ISSNs (for instance in `data/issn.txt`) and downloads data about their publication
* `scratch/makeAuthorPaperGraph.py` - It takes in data from the two previous scripts (check first few lines), and outputs a bipartite graph of authors and papers
* `scratch/makeTripartite.py` - It takes in data from the two previous scripts (check first few lines), and outputs a tripartite graph that includes papers, authors, and institutions.

### Graph conventions
Some data from Scopus was 'corrupted', so there will be a few papers without publication, author or affiliation information.

Node ids capture what entity the node represents by their first letter: an author("a"), paper("p") or institution("i"). For instance, node "a7563051" would represent an author, node "i7563957" would represent an institution, and node "p67865" would represent a paper.

Also, in `tripartite.graphml`, the nodes contain a `type` field which has a value of `'author'`,`'paper'`, or `'inst'`, for each entity.
