# -*- coding: utf-8 -*-
import markdown
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from .models import (
    DBSession,
    Entry,
)
from learning_journal.forms import EntryForm


@view_config(route_name='home', renderer='templates/list.jinja2')
def list_view(request):
    """List view."""
    articles = DBSession.query(Entry).all()
    return {'articles': articles}


@view_config(route_name='article', renderer='templates/detail.jinja2')
def detail_view(request):
    """Detail view."""
    md = markdown.Markdown(safe_mode='replace', html_replacement_text='NO')
    article_id = request.matchdict['article_id']
    article = DBSession.query(Entry).get(article_id)
    text = md.convert(article.text)
    return {'article': article, 'text': text}


@view_config(route_name='add_entry', renderer='templates/add_entry.jinja2')
def add_entry_view(request):
    """Add entry view."""
    form = EntryForm(request.POST)
    if request.method == 'POST' and form.validate():
        new_entry = Entry(title=form.title.data, text=form.text.data)
        already_in_db = DBSession.query(Entry).filter(
                        Entry.title == new_entry.title).first()
        if already_in_db:
            error_msg = 'That title has already been used.'
            return {'error_msg': error_msg,
                    'rej_title': new_entry.title,
                    'rej_text': new_entry.text}
        DBSession.add(new_entry)
        DBSession.flush()
        url = '/article/{}'.format(new_entry.id)
        return HTTPFound(location=url)
    return {}


@view_config(route_name='edit_entry', renderer='templates/edit_entry.jinja2')
def edit_entry_view(request):
    """Edit entry view."""
    article_id = request.matchdict['article_id']
    article = DBSession.query(Entry).get(article_id)
    form = EntryForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(article)
        url = '/article/{}'.format(article.id)
        return HTTPFound(location=url)
    return {'article': article}
