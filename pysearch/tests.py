
"""Test Params."""
import pytest

from pyramid import testing

from pysearch.models import Keyword, Match, get_tm_session
from pysearch.models.meta import Base
from pyramid.config import Configurator

RESULTS = [
    {'keyword': 'football', 'weight': 10, 'url': 'url1', 'count': 100},
    {'keyword': 'soccer', 'weight': 5, 'url': 'url1', 'count': 100},
    {'keyword': 'football', 'weight': 10, 'url': 'url2', 'count': 50},
    {'keyword': 'soccer', 'weight': 5, 'url': 'url2', 'count': 25},
    {'keyword': 'football', 'weight': 10, 'url': 'url3', 'count': 5},
    {'keyword': 'soccer', 'weight': 5, 'url': 'url3', 'count': 5}
]


TEST_FILE = '<!doctype html>\n<html>\n<head>\n    <title>Example Domain</title>\n\n    <meta charset="utf-8" />\n    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1" />\n    <style type="text/css">\n    body {\n<h2>this is h2</h2>        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;\n        \n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n  <h3>h3</h3>      padding: 50px;\n        background-color: #fff;\n        border-radius: 1em;\n    }\n    a:link, a:visited {\n        color: #38488f;\n <h2>this is h2</h2>       text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        body {\n            background-color: #fff;\n        }\n        div {\n            width: auto;\n            margin: 0 auto;\n            border-radius: 0;\n            padding: 1em;\n        }\n    }\n    </style>    \n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n<h3>h3</h3><h4>h4</h4><h5>h5</h5><h6>h6</h6>    <p>This domain is established to be used for illustrative examples in documents. You may use this\n    domain in examples without prior coordination or asking for permission.</p>\n    <p><a href="http://www.iana.org/domains/example">More information...</a></p>\n</div>\n</body>\n</html>\n'

TEST_FILE_2 = '<!doctype html><html><head><title>Free Example Domain</title><meta charset="utf-8" /><meta http-equiv="Content-type" content="text/html; charset=utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" /><style type="text/css">body {background-color: #f0f0f2;margin: 0;padding: 0;font-family: "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;}h1 {color: red}h2 {color: red;}h3 {color: red;}h4 {color: red;}h5 {color: red;}h6 {color: red;}p {color: red;}div {width: 600px;margin: 5em auto;padding: 50px;background-color: #fff;border-radius: 1em;}a:link, a:visited {color: #38488f;text-decoration: none;}@media (max-width: 700px) {body {background-color: #fff;}div {width: auto;margin: 0 auto;border-radius: 0;padding: 1em;}}</style>    </head><body><div><h1>Example Domain</h1><p> the the the the the the the the marc marc marc marc marc marc pie pie pie pie pie pie pie glad glad glad glad free free free free free free only appear once </p><p><a href="http://www.iana.org/domains/example">More information...</a></p><h1>Header 1</h1><h2>marc Header 2</h2><h3>Header 3</h3><h4>Header 4</h4><h5>Header 5</h5><h6>Header 6</h6></div></body></html>'


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a COnfigurator instance."""
    config = testing.setUp(settings={
        'sqlalchemy.url': 'postgres://Sera@localhost:5432/test'
        })
    config.include("pysearch.models")
    config.include("pysearch.routes")


    def tearDown():
        testing.tearDown()

    request.addfinalizer(tearDown)
    return config


@pytest.fixture()
def db_session(configuration, request):
    """."""
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture()
def dummy_request(db_session):
    """."""
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def dummy_response():
    """."""
    from scrapy.http import TextResponse, Request
    url = 'http://www.example.com'
    request = Request(url=url)
    response = TextResponse(url=url, request=request, body=TEST_FILE_2, encoding='utf-8')
    return response


@pytest.fixture()
def add_models(dummy_request):
    """Add results to the database, then return scored urls in order of rank."""
    for result in RESULTS:
            row = Match(keyword=result['keyword'], keyword_weight=result['weight'], page_url=result['url'], count=result['count'])
            dummy_request.dbsession.add(row)


# =================== UNIT TESTS =========================


def test_new_models_added(db_session, add_models):
    """Test that models gets added to db."""
    query = db_session.query(Match).all()
    assert len(query) == len(RESULTS)


def test_results_view_scored_data(dummy_request, add_models):
    """Test resulting view."""
    from pysearch.views.default import results_view
    print(results_view(dummy_request))
    assert results_view(dummy_request) == {'RESULTS': [{'score': 1500, 'url': u'url1'}, {'score': 625, 'url': u'url2'}, {'score': 75, 'url': u'url3'}]}


# =================== FUNCTIONAL VIEWS ======================


@pytest.fixture()
def testapp(request):
    """Create an instance of webtests TestApp for testing routes."""
    from webtest import TestApp

    def main(global_config, **settings):
        """Return a Pyramid WSGI application."""
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('pysearch.models')
        config.include('pysearch.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main({}, **{
        'sqlalchemy.url': 'postgres://Sera@localhost:5432/test'
    })

    testapp = TestApp(app)
    session_factory = app.registry["dbsession_factory"]
    session = session_factory()
    engine = session.bind
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(bind=engine)

    def tearDown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(tearDown)

    return testapp


def test_layout_root(testapp):
    """Test that the contents of the root page contains <article>."""
    response = testapp.get('/', status=200)
    html = response.html
    assert 'PySearch' in html.find("footer").text

# =================== TESTING VIEWS =========================


def test_home_view_is_returns_empty_dict(dummy_request):
    """Test there are no listings when db is empty."""
    from pysearch.views.default import home_view
    assert home_view(dummy_request) == {}


def test_home_view_post_returns_a_redirect(dummy_request):
    """Test that search post redirects."""
    from pysearch.views.default import home_view
    from pyramid.httpexceptions import HTTPFound
    dummy_request.method = 'POST'
    dummy_request.POST['url'] = 'https://www.sample.com'
    result = home_view(dummy_request)
    assert isinstance(result, HTTPFound)


def test_computing_results_view_redirects(dummy_request):
    """Test that computing results redirects and has an url attached."""
    from pysearch.views.default import computing_results_view
    from pyramid.httpexceptions import HTTPFound
    dummy_request.params['url'] = 'https://www.sample.com'
    result = computing_results_view(dummy_request)
    assert isinstance(result, HTTPFound)


# =================== HARVESTER =========================


def test_harvest_spider_start_request_returns_generator():
    """Test that start request returns generator."""
    from pysearch.harvester.spiders.harvester import HarvestSpider
    import types
    harvy = HarvestSpider()
    result = harvy.start_requests()
    assert isinstance(result, types.GeneratorType)


# def test_harvest_spider_parse_function_returns_something(dummy_response):
#     """Test that the harvest spider parse function returns something."""
#     from pysearch.harvester.spiders.harvester import HarvestSpider
#     from collections import Counter
#     harvy = HarvestSpider()
#     result = harvy.parse(dummy_response)
#     assert type(result) is Counter


# @patch('pysearch.harvester.spiders.harvester.harvest')
# def test_harvest_calls_other_functions(test_patch):
#     """Test that harvest works."""
#     # from unittest.mock import patch
#     # from pysearch.harvester.spiders.harvester import HarvestSpider
#     # patcher = patch.object(HarvestSpider, 'harvest')
#     # patched = patcher.start()


# =================== CRAWLER =========================


def test_crawler_spider_parse_function_returns_something(dummy_response):
    """Test that the harvest spider parse function returns something."""
    from pysearch.harvester.spiders.crawler import CrawlingSpider
    import types
    crawly = CrawlingSpider()
    result = crawly.parse_items(dummy_response)
    assert isinstance(result, types.GeneratorType)


def test_crawler_spider_to_lower():
    """Test that the harvest spider parse function returns something."""
    from pysearch.harvester.spiders.crawler import lower_list
    to_lower = ['This', 'is', 'A', 'tEsT']
    result = lower_list(to_lower)
    assert result == ['this', 'is', 'a', 'test']
