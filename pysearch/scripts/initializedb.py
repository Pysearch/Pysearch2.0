import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Keyword


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for result in RESULTS:
            row = Results(url=result['url'], title=result['title'], body=result['body'])
            dbsession.add(row)


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
