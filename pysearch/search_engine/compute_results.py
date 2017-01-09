from analyze_url import analyze_url
from add_to_db import add_to_db

def compute_results(url):
    add_to_db(analyze_url(url))
    