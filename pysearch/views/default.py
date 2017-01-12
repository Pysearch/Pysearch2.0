from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

"""Imports we care about."""
from pyramid.httpexceptions import HTTPFound
from ..models import Keyword
from subprocess import call
import os
# from pysearch.harvester.spiders.harvester import harvest
# from pysearch.harvester.spiders.crawler import crawl


"""Test Params."""
RESULTS = [
    {'keyword': 'applepie', 'keyword_weight': '4', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'https://www.pillsbury.com/'},
    {'keyword': 'applepiea', 'keyword_weight': '3', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'https://www.pillsbury.com/'},
    {'keyword': 'applepieb', 'keyword_weight': '2', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'http://allrecipes.com/recipe/12682/'},
    {'keyword': 'applepiec', 'keyword_weight': '2', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'http://allrecipes.com/recipe/12682/', 'body_urls': 'https://www.pillsbury.com/'},
    {'keyword': 'applepied', 'keyword_weight': '1', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'https://www.applepie.com'},
    {'keyword': 'applepiee', 'keyword_weight': '5', 'title_urls': 'https://www.google.com/apple_pie', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'https://www.pillsbury.com/'},
    {'keyword': 'applepief', 'keyword_weight': '5', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.google.com/apple_pie', 'body_urls': 'https://www.pillsbury.com/'},
    {'keyword': 'applepieg', 'keyword_weight': '3', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'http://www.bettycrocker.com/recipes/'}
]

HERE = os.path.dirname(__file__)


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    if request.method == "POST":
        url = request.POST["url"]
        call(['python3', HERE + "/../harvester/spiders/harvester.py", url])
        return HTTPFound(request.route_url('computing_results', _query={"url": url}))
    return {}


@view_config(route_name='computing_results')
def computing_results_view(request):
    """Remove authentication from the user."""

    url = request.params["url"]
    call(['python3', HERE + "/../harvester/spiders/crawler.py", url])
    return HTTPFound(request.route_url("results"))


@view_config(route_name='results', renderer='../templates/results.jinja2')
def results_view(request):
    query = request.dbsession.query(Keyword)
    try:
        # results = query.filter(Keyword.keyword == 'applepie1')

        """
        Set results to query.all() to render Keyword model data on results page.
        """
        keywords = query.all()
        print(keywords)
        results = []
        for each in keywords:
            results.append(each.keyword)
        print(results)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {"RESULTS": results}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
