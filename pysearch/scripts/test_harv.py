"""From pysearch dir. Same level as routes.py.'python scripts/test_harv.py'."""
# from pysearch.harvester.spiders.harvester import harvest
from pysearch.harvester.spiders.crawler import crawl

# harvest('http://www.espn.com')
crawl()