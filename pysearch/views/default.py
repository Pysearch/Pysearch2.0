from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

"""Imports we care about."""
from pyramid.httpexceptions import HTTPFound
from ..models import Match
from subprocess import call
import os
# from pysearch.harvester.spiders.harvester import harvest
# from pysearch.harvester.spiders.crawler import crawl

#
# TODO: Add Form that passes a URL to be crawled + harvested
#     create a route call CRAWL,  POST , url
#
# TODO: Add Form that accepts a query keyword and posts it
#
#


HERE = os.path.dirname(__file__)


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """How view configuration."""
    if request.method == "POST":
        url = request.POST["url"]
        print('home view ', url)
        call(['python3', HERE + "/../harvester/spiders/harvester.py", url])
        return HTTPFound(request.route_url('loading', _query={"url": url}))
    return {}


@view_config(route_name='loading', renderer='../templates/loading.jinja2')
def loading_view(request):
    """Remove authentication from the user."""
    url = request.params["url"]
    print('loading view ', url)
    return HTTPFound(request.route_url('computing_results', _query={"url": url}))


@view_config(route_name='computing_results')
def computing_results_view(request):
    """Remove authentication from the user."""
    url = request.params["url"]
    print('computing results view ', url)
    call(['python3', HERE + "/../harvester/spiders/crawler.py", url])
    return HTTPFound(request.route_url("results"))


@view_config(route_name='results', renderer='../templates/results.jinja2')
def results_view(request):
    """Append result of each unique keyword of each unique url to be passed to be scored."""
    results = []
    try:
        unique_urls = []
        for val in request.dbsession.query(Match.page_url).distinct():
            unique_urls.append(val[0])
        print(unique_urls)

        unique_keywords = []
        for val in request.dbsession.query(Match.keyword).distinct():
            unique_keywords.append(val[0])
        print(unique_keywords)

        for url in unique_urls:
            for kw in unique_keywords:
                url_q = request.dbsession.query(Match).filter_by(keyword=kw).filter_by(page_url = url).first()
                results.append({'keyword': kw, 'weight': url_q.keyword_weight, 'url': url, 'count': url_q.count})

    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)

    return {"RESULTS": results}


RESULTS = [
    {'keyword': 'football', 'weight': 10, 'url': 'url1', 'count': 100},
    {'keyword': 'soccer', 'weight': 5, 'url': 'url1', 'count': 100},

    {'keyword': 'football', 'weight': 10, 'url': 'url2', 'count': 50},
    {'keyword': 'soccer', 'weight': 5, 'url': 'url2', 'count': 25},

    {'keyword': 'football', 'weight': 10, 'url': 'url3', 'count': 5},
    {'keyword': 'soccer', 'weight': 5, 'url': 'url3', 'count': 5}
]


def score_data(lst_results):
    """Score url by accumulative score of count and weight fo reach keyword."""
    set_urls = set()
    for result in lst_results:
        set_urls.add(result['url'])

    ret_data = []
    for url in set_urls:
        score = 0
        for r in lst_results:
            if r['url'] == url:
                score += r['count'] * r['weight']
        ret_data.append({'url': url, 'score': score})

    ret_data = sorted(ret_data, key=lambda x: x['score'], reverse=True)
    return ret_data


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
