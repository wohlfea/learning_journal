# -*- coding: utf-8 -*-
import markdown
from pyramid.httpexceptions import HTTPFound, HTTPForbidden
from pyramid.view import (
    view_config,
    forbidden_view_config,
    )
from .models import (
    DBSession,
    Entry,
)
from pyramid.security import (
    remember,
    forget,
    )

from learning_journal.forms import EntryForm
from learning_journal.forms import LoginForm
from learning_journal.security import check_pwd


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


@view_config(route_name='add_entry', renderer='templates/add_entry.jinja2', permission='edit')
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


@view_config(route_name='edit_entry', renderer='templates/edit_entry.jinja2', permission='edit')
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


def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return HTTPForbidden()

    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)


@view_config(route_name='secure', renderer='string', permission='chicken')
def secure_view(request):
    return 'I am secure.'


@view_config(route_name='login', renderer='templates/login.jinja2')
def login_view(request):
    form = LoginForm(request.POST)
    username = request.params.get('username', '')
    password = request.params.get('password', '')
    if request.method == 'POST' and form.validate():
        if check_pwd(password):
            headers = remember(request, username)
            return HTTPFound(location='/', headers=headers)
    return {}


@view_config(route_name='logout', renderer='string')
def logout_view(request):
    return 'I am logout.'
