from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
    Authenticated
    )

from .models import (
    DBSession,
    Base,
    )


class DefaultRoot(object):
    """I Hope this is the right place for an acl."""
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, Authenticated, ALL_PERMISSIONS)]

    def __init__(self, request):
        """Init."""
        self.request = request


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    # This is a new way to do this with the environment variables instead.
    # database_url = os.environ.get('DATABASE_URL', None)
    # if database_url is not None:
    #     settings['sqlalchemy.url'] = database_url

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy(
        'sosecret', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
                          root_factory=DefaultRoot,)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_jinja2')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('article', '/article/{article_id}')
    config.add_route('add_entry', '/add_entry')
    config.add_route('edit_entry', '/edit_entry/{article_id}')
    config.scan()
    return config.make_wsgi_app()
