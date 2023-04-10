# This repo contains the methods for generating new key phrases for semantic search on CAPE

- The output will be two csvs:
1. all pairwise combinations of the vocabulary with their cosine similarity
2. The key phrases in descending order of counts frequency in the plans

# Set up
Python 3.9.15
There is a requirements.txt file in semantic_search that contains the packages used.
The pyproject.toml file should hopefully prevent dependency conflicts.

# Re-run ML semantic search to generate key phrases
- The entire process can be run through main.py.This involves:

- Load and preprocess plans with process_plans.py
- Run the keyBERT model to generate key phrase vocabulary with model_keyphrases.py
- Post process the vocabulary with process_keyphrases.py to generate the csvs which can be pulled

The modelling is the most time consuming, and so you may want to separate this from the full flow.

# Notebooks also available if wanting to see pandas outputs at various stages in the process
- html-processing gives some statistics on the corpus of files.
- clustering-keyphrases allows plotting of the dimensionally reduces vocabulary
- graph shows the network graph of the vocabulary and its reduction in size by importance of node (betweenness centrality)






