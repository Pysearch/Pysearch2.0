from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

"""Imports we care about."""
from pyramid.httpexceptions import HTTPFound
from ..models import Keyword
from pysearch.harvester.spiders.harvester import harvest


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    if request.method == "POST":
        url = request.POST["url"]
        harvest()
        print(url)
        return HTTPFound(request.route_url('computing_results'))
    return {}


@view_config(route_name='computing_results')
def computing_results_view(request):
    """Remove authentication from the user."""
    # import pdb; pdb.set_trace()
    return HTTPFound(request.route_url("results"))


RESULTS = [
    {'keyword': 'applepie', 'keyword_weight': 4, 'title_urls': '', 'header_url': '', 'body_url': 'https://www.pillsbury.com/'},
    {'keyword': 'applepie', 'keyword_weight': 3, 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_url': '', 'body_url': ''},
    {'keyword': 'applepie', 'keyword_weight': 2, 'title_urls': '', 'header_url': '', 'body_url': 'http://allrecipes.com/recipe/12682/'},
    {'keyword': 'applepie', 'keyword_weight': 2, 'title_urls': '', 'header_url': 'http://allrecipes.com/recipe/12682/', 'body_url': ''},
    {'keyword': 'applepie', 'keyword_weight': 1, 'title_urls': '', 'header_url': '', 'body_url': 'https://www.applepie.com'},
    {'keyword': 'applepie', 'keyword_weight': 5, 'title_urls': 'https://www.google.com/apple_pie', 'header_url': '', 'body_url': ''},
    {'keyword': 'applepie', 'keyword_weight': 5, 'title_urls': '', 'header_url': 'https://www.google.com/apple_pie', 'body_url': ''},
    {'keyword': 'applepie', 'keyword_weight': 3, 'title_urls': '', 'header_url': '', 'body_url': 'http://www.bettycrocker.com/recipes/'}
]


@view_config(route_name='results', renderer='../templates/results.jinja2')
def results_view(request):
    # query = request.dbsession.query(Keyword)
    # try:
        # results = query.filter(Keyword.keyword == 'baseball')
        # entries = query.all()
    # except DBAPIError:
    #     return Response(db_err_msg, content_type='text/plain', status=500)
    return {"RESULTS": RESULTS}

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
