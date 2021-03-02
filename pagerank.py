import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main(): 
    if len(sys.argv) != 2:
       sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])  
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):

    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    p_nod = (1 - damping_factor)/len(corpus)
    
    if len(corpus[page]) != 0:
        p_d = damping_factor/len(corpus[page])
   

    prob = dict()    
    for x,y in corpus.items():
        if len(corpus[page]) == 0:
            prob[x] = 1/len(corpus)  
        elif x not in corpus[page]:
            prob[x] = p_nod
        else:
            prob[x] = p_nod + p_d
    return prob

    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Generate an empty list for samples
    samples = []
    # Peak a random page frmo corpus and add it to samples
    samples.append(random.choice(list(corpus.keys())))
    # Loop over n samples
    for i in range(n):
        tm = transition_model(corpus,samples[i],damping_factor)
        samples.append(random.choices(list(tm.keys()),weights=list(tm.values()))[0])
        
    

    pagerank = dict()    
    for x in corpus.keys():
        pagerank[x] = samples.count(x) / n
    return pagerank
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(list(corpus.keys()))
    
    prank = corpus.copy() # copio corpus para usar la misma estructura del diccionario
    for x,y in prank.items():
        prank.update({x: 1/N})
    suma = 0
    loop = True
    while loop: 
        prank_previous = prank.copy() 
        for x in corpus.keys():
            prob1 = (1 - damping_factor) / N 
            prob2 = 0
            for y,z in corpus.items():
                if x in z:
                    prob2 = prob2 + damping_factor * prank[y]/len(list(z))
            prob = prob1 + prob2
            prank.update({x:prob})
            suma += 1   
            
        dif = []    
        for x in prank.keys():
            dif.append(abs(prank[x]-prank_previous[x]))
        if all([x < 0.001 for x in dif]):
            loop = False
    
    return prank

  


if __name__ == "__main__":
    main()
