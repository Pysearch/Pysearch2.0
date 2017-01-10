from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Keyword
# from ..search_engine.analyze_url import analyze_url
# from ..search_engine.add_to_db import add_to_db
# from ..search_engine.compute_results import compute_results
from pyramid.httpexceptions import HTTPFound


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    if request.method == "POST":
        url = request.POST["url"]
        print(url)
        compute_results(url)
        return HTTPFound(request.route_url('results'))
    return {}


### This commented out code is a version of home_view that reroutes to
### /populating_db on POST of url.


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    if request.method == "POST":
        url = request.POST["url"]
        print(url)
        return HTTPFound(request.route_url("populating_db"))
    return {}


### This commented out code is the /populating_db route 'view'
### on POST of url.


@view_config(route_name='populating_db')
def populating_db_view(request):
    """Remove authentication from the user."""
    add_to_db()
    return HTTPFound(request.route_url("results"))


# results = [
#     ['www.msb.com', 'MSB is the BEST', 'Marc, Sera, Ben = Pysearch'],
#     ['www.asdfasdfasdfasf.com', 'asdfasdfasdf is the asdfasdfasdf', 'abcdefghijlkmabcdefghijlkmabcdefghijlkmabcdefghijlkmabcdefghijlkmabcdefghijlkmabcdefghijlkmabcdefghijlkmabcdefghijlkmabcdefghijlkm'],
#     ['www.ohoohohohhhohoh.com', 'HOHOHOHOOOOOO!!!!!!woot', 'awootawootawootawootawootawoot'],
# ]

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
    query = request.dbsession.query(Keyword)
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
