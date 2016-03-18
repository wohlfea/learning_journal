# -*- coding: utf-8 -*-
import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from .models import (
    DBSession,
    Entry,
)
from forms import EntryForm


@view_config(route_name='home', renderer='templates/list.jinja2')
def list_view(request):
    """List view."""
    articles = DBSession.query(Entry).all()
    return {'articles': articles}


@view_config(route_name='article', renderer='templates/detail.jinja2')
def detail_view(request):
    """Detail view."""
    article_id = request.matchdict['article_id']
    article = DBSession.query(Entry).get(article_id)
    return {'article': article}


@view_config(route_name='add_entry', renderer='templates/add_entry.jinja2')
def add_entry_view(request):
    """Add entry view."""
    form = EntryForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_entry = Entry(title=form.title.data, text=form.text.data)
        DBSession.add(new_entry)
        DBSession.flush()
        transaction.commit()
        latest = DBSession.query(Entry).order_by(Entry.id.desc()).first()
        url = request.route_url('article', article_id=latest.id)
        return HTTPFound(location=url)
    return {}
