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

