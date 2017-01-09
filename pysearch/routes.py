def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('results', '/results')
    config.add_route('populating_db', '/populating_db')
