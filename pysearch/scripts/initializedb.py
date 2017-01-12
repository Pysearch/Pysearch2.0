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
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for result in RESULTS:
            row = Keyword(keyword=result['keyword'], keyword_weight=result['keyword_weight'], title_urls=result['title_urls'], header_urls=result['header_urls'], body_urls=result['body_urls'])
            dbsession.add(row)


RESULTS = [
    {'keyword': 'applepie', 'keyword_weight': '4', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'https://www.pillsbury.com/'},
    {'keyword': 'applepie1', 'keyword_weight': '3', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'https://www.pillsbury.com/'},
    {'keyword': 'applepie2', 'keyword_weight': '2', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'http://allrecipes.com/recipe/12682/'},
    {'keyword': 'applepie3', 'keyword_weight': '2', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'http://allrecipes.com/recipe/12682/', 'body_urls': 'https://www.pillsbury.com/'},
    {'keyword': 'applepie4', 'keyword_weight': '1', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'https://www.applepie.com'},
    {'keyword': 'applepie5', 'keyword_weight': '5', 'title_urls': 'https://www.google.com/apple_pie', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'https://www.pillsbury.com/'},
    {'keyword': 'applepie6', 'keyword_weight': '5', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.google.com/apple_pie', 'body_urls': 'https://www.pillsbury.com/'},
    {'keyword': 'applepie7', 'keyword_weight': '3', 'title_urls': 'http://www.bettycrocker.com/recipes/', 'header_urls': 'https://www.pillsbury.com/', 'body_urls': 'http://www.bettycrocker.com/recipes/'}
]
