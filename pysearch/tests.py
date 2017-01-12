import pytest
import transaction

from pyramid import testing

from sqlalchemy.exc import DBAPIError

from pysearch.models import Match, get_tm_session
from pysearch.models.meta import Base

RESULTS = [
    {'keyword': 'football', 'weight': 10, 'url': 'url1', 'count': 100},
    {'keyword': 'soccer', 'weight': 5, 'url': 'url1', 'count': 100},
    {'keyword': 'football', 'weight': 10, 'url': 'url2', 'count': 50},
    {'keyword': 'soccer', 'weight': 5, 'url': 'url2', 'count': 25},
    {'keyword': 'football', 'weight': 10, 'url': 'url3', 'count': 5},
    {'keyword': 'soccer', 'weight': 5, 'url': 'url3', 'count': 5}
]


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a COnfigurator instance."""
    settings = {
        'sqlalchemy.url': 'sqlite:///:memory:'}
    config = testing.setUp(settings=settings)
    config.include('pysearch.models')

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


@pytest.fixture()
def add_models(dummy_request):
    """."""
    for result in RESULTS:
        row = Match(keyword=result['keyword'], keyword_weight=result['weight'], page_url=result['url'], count=result['count'])
        dummy_request.dbsession.add(row)


# =================== UNIT TESTS =========================


def test_new_models_added(db_session, add_models):
    """Test that models gets added to db."""
    query = db_session.query(Match).all()
    assert len(query) == len(RESULTS)


# def results_view(request):
#     """Append result of each unique keyword of each unique url to be passed to be scored."""
#     results = []
#     try:
#         unique_urls = []
#         for val in request.dbsession.query(Keyword.page_url).distinct():
#             unique_urls.append(val[0])
#         print(unique_urls)

#         unique_keywords = []
#         for val in request.dbsession.query(Keyword.keyword).distinct():
#             unique_keywords.append(val[0])
#         print(unique_keywords)

#         for url in unique_urls:
#             for kw in unique_keywords:
#                 url_q = request.dbsession.query(Keyword).filter_by(keyword=kw).filter_by(page_url = url).first()
#                 results.append({'keyword': kw, 'weight': int(url_q.keyword_weight), 'url': url, 'count': int(url_q.count)})

#     except DBAPIError:
#         return Response(db_err_msg, content_type='text/plain', status=500)

#     return {"RESULTS": score_data(results)}
#     # [{'score': 1500, 'url': 'url1'}, {'score': 625, 'url': 'url2'}, {'score': 75, 'url': 'url3'}]


# def score_data(lst_results):
#     """Score url by accumulative score of count and weight fo reach keyword."""
#     set_urls = set()
#     for result in lst_results:
#         set_urls.add(result['url'])

#     ret_data = []
#     for url in set_urls:
#         score = 0
#         for r in lst_results:
#             if r['url'] == url:
#                 score += r['count'] * r['weight']
#         ret_data.append({'url': url, 'score': score})

#     ret_data = sorted(ret_data, key=lambda x: x['score'], reverse=True)
#     return ret_data


# def test_results_view(dummy_request, add_models):
#     """Test results view."""
#     res = results_view(dummy_request)
#     print(score_data(res))
#     assert 1 == 0
