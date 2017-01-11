"""From pysearch dir. Same level as routes.py.'python scripts/test_harv.py'."""

# from pysearch.harvester.spiders.crawler import crawl

# crawl()

import sys
from pysearch.harvester.spiders.harvester import harvest


if __name__ == '__main__':
    harvest()
    print(sys.argv[1])
