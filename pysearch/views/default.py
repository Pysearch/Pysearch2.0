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

#  This commented out code is a version of home_view that reroutes to
# /populating_db on POST of url.


# @view_config(route_name='home', renderer='../templates/home.jinja2')
# def home_view(request):
#  if request.method == "POST":
#       url = request.POST["url"]
#        print(url)
#        return HTTPFound(request.route_url("populating_db"))
#    return {}


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
    {'url': 'https://www.pillsbury.com/recipes/perfect-apple-pie/1fc2b60f-0a4f-441e-ad93-8bbd00fe5334', 'title': 'Perfect Apple Pie', 'body': 'A classic apple pie takes a shortcut with easy Pillsbury unroll-fill refrigerated pie crust.'},
    {'url': 'http://www.bettycrocker.com/recipes/', 'title': 'Scrumptious Apple Pie recipe from Betty Crocker', 'body': 'This apple pie is a classic, from the scrumptious filling to the flaky pastry crust. It is homemade goodness at its very best.'},
    {'url': 'http://allrecipes.com/recipe/12682/apple-pie-by-grandma-ople/', 'title': 'Apple Pie by Grandma Ople Recipe - Allrecipes.com', 'body': 'This was my grandmother\'s apple pie recipe. I have never seen another one quite like it. It will always be my favorite and has won me several first place prizes in local competitions. I hope it becomes one of your favorites as well!'},
    {'url': 'https://www.applepie.com', 'title': 'Apple Pie Recipe : Food Network Kitchen : Food Network', 'body': 'Get this all-star, easy-to-follow Apple Pie recipe from Food Network Kitchen.'},
    {'url': 'https://www.google.com', 'title': 'Apple Pie Recipe - NYT Cooking', 'body': 'This recipe is adapted from hers, for a plain apple pie. It benefits from heeding her advice to pre-cook the filling before baking. Apple pies that have crunchy, raw'}
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
