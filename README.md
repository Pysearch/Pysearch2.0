# PYSEARCH
==================
**Authors:** Marc Fieser, Sera Smith, and Ben Shields

***Live URL:*** https://vascodagama.herokuapp.com/

## Getting Started:
```
- cd <directory containing this file>

- $VENV/bin/pip install -e .

- $VENV/bin/initialize_db development.ini

- $VENV/bin/pserve development.ini
```

## Global Variables:

harvester.py: 
NUM_OF_OCCURANCES -- number of times a word must appear in order for harvester to add word to database keyword table.

crawler.py:
CRAWL_COUNT -- crawl page count parameter
DEPTH_LEVEL -- depth per page crawled

pipelines.py:
MINIMUM_MATCHES -- minimum number of word matches for url to be sent to database matches table.
