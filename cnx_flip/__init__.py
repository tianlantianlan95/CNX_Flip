import sys
from pyramid.config import Configurator
from sqlalchemy import engine_from_config, create_engine
from .db import DBSession, Base

from pyramid.paster import setup_logging, get_appsettings

def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config_uri = sys.argv[1]
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    # engine = create_engine('postgresql+psycopg2://Tim:Qasdew123@localhost/openflip-flashcarddb')
    # DBSession.configure(bind=engine)
    # Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('api_deck', 'api/decks/{userid:.*}/{deckid:.*}')
    config.add_route('api_card', 'api/cards/{userid:.*}/{cardid:.*}')
    config.add_route('api_textbook', 'api/textbook/{userid:.*}')
    
    # config.add_route('add_user', 'addUser')
    config.add_route('test_db', 'test_db')
    config.scan()
    return config.make_wsgi_app()
