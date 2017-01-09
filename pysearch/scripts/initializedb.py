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
    {'url': 'https://www.pillsbury.com/recipes/perfect-apple-pie/1fc2b60f-0a4f-441e-ad93-8bbd00fe5334', 'title': 'Perfect Apple Pie', 'body': 'A classic apple pie takes a shortcut with easy Pillsbury® unroll-fill refrigerated pie crust.'},
    {'url': 'http://www.bettycrocker.com/recipes/scrumptious-apple-pie/c9a4acc6-85aa-4128-b0b0-1a17bdbe05e0', 'title': 'Scrumptious Apple Pie recipe from Betty Crocker', 'body': 'This apple pie is a classic, from the scrumptious filling to the flaky pastry crust. It is homemade goodness at its very best.'},
    {'url': 'http://allrecipes.com/recipe/12682/apple-pie-by-grandma-ople/', 'title': 'Apple Pie by Grandma Ople Recipe - Allrecipes.com', 'body': 'This was my grandmother\'s apple pie recipe. I have never seen another one quite like it. It will always be my favorite and has won me several first place prizes in local competitions. I hope it becomes one of your favorites as well!'},
    {'url': 'https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=7&cad=rja&uact=8&ved=0ahUKEwi075PthrbRAhXhsFQKHaS4DoYQFghOMAY&url=http%3A%2F%2Fwww.foodnetwork.com%2Frecipes%2Ffood-network-kitchens%2Fapple-pie-recipe.html&usg=AFQjCNHveggt-3KI58aJcBqDbUgo3b_HRA&sig2=FCCc1VFPsEHKWsfE-tCiuA', 'title': 'Apple Pie Recipe : Food Network Kitchen : Food Network', 'body': 'Get this all-star, easy-to-follow Apple Pie recipe from Food Network Kitchen.'},
    {'url': 'https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=8&cad=rja&uact=8&ved=0ahUKEwi075PthrbRAhXhsFQKHaS4DoYQFghYMAc&url=http%3A%2F%2Fcooking.nytimes.com%2Frecipes%2F12320-apple-pie&usg=AFQjCNGSddXVaW-cqMEBhcxatPfQTAUlYA&sig2=yl6M2CE0GRhJvCbkTvpChA', 'title': 'Apple Pie Recipe - NYT Cooking', 'body': 'This recipe is adapted from hers, for a plain apple pie. It benefits from heeding her advice to pre-cook the filling before baking. “Apple pies that have crunchy, raw ...'}
]
