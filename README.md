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

## Stats for tripartite graph and derivative graphs

50189 papers. 78901 authors. 13150 institutions.

The author-publication graph has 129090 nodes, 7916 connected components.
Their sizes: [95637, 295, 102, 101, 96, 77, 64, 55, 47, 46], etc.

50639 authors have ONE publication.
11646 authors have TWO publications.
5196 authors have THREE publications.
11420 authors have MORE THAN THREE publications.

8491 papers have ONE author.
10458 papers have TWO authors.
9397 papers have THREE authors.
21843 papers have MORE THAN THREE authors.

The author-institution graph has 92051 nodes, 7493 connected components.
Their sizes: [73729, 67, 53, 47, 45, 38, 36, 35, 35, 29], etc.

58527 authors have ONE institutions.
12546 authors have TWO instututions.
3370 authors have THREE institutions.
4458 authors have MORE THAN THREE institutions.

6850 institutions have ONE author.
1942 institutions have TWO authors.
1022 institutions have THREE authors.
3336 institutions have MORE THAN THREE authors.
