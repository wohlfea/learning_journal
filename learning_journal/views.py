from pyramid.view import view_config
from .models import (
    DBSession,
    Entry,
)


@view_config(route_name='home', renderer='templates/list.jinja2')
def list(request):
    """List view."""
    articles = DBSession.query(Entry).all()
    return {'articles': articles}


@view_config(route_name='article', renderer='templates/detail.jinja2')
def detail(request):
    """Detail view."""
    article_id = request.matchdict['article_id']
    article = DBSession.query(Entry).get(article_id)
    return {'article': article}
