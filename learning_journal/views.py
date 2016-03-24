# -*- coding: utf-8 -*-
import markdown
from pyramid.httpexceptions import HTTPFound
from pyramid.view import (
    view_config,
    forbidden_view_config,
)
from pyramid.security import (
    remember,
    forget,
)
from .models import (
    DBSession,
    Entry,
)
from learning_journal.forms import EntryForm
from learning_journal.security import check_pw
import os


@view_config(route_name='home', renderer='templates/list.jinja2',
             permission='view')
def list_view(request):
    """List view."""
    articles = DBSession.query(Entry).all()
    return {'articles': articles}


@view_config(route_name='article', renderer='templates/detail.jinja2',
             permission='view')
def detail_view(request):
    """Detail view."""
    md = markdown.Markdown(safe_mode='replace', html_replacement_text='NO')
    article_id = request.matchdict['article_id']
    article = DBSession.query(Entry).get(article_id)
    text = md.convert(article.text)
    return {'article': article, 'text': text}


@view_config(route_name='add_entry', renderer='templates/add_entry.jinja2',
             permission='edit')
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


@view_config(route_name='edit_entry', renderer='templates/edit_entry.jinja2',
             permission='edit')
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


@view_config(route_name='delete_entry', permission='edit')
def delete_entry(request):
    article_id = request.matchdict['article_id']
    article = DBSession.query(Entry).get(article_id)
    DBSession.delete(article)
    DBSession.flush()
    return HTTPFound(location='/')


@view_config(context='learning_journal.security.MyRoot', name='login',
             renderer='templates/login.jinja2')
@forbidden_view_config(renderer='templates/login.jinja2')
def login(request):
    referrer = request.url
    if 'login' in referrer:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    message = ''
    login = ''
    password = ''
    if 'login' in request.params and 'password' in request.params:
        login = request.params['login']
        password = request.params['password']
        if check_pw(password) and login == os.environ.get('AUTH_USERNAME'):
            headers = remember(request, login)
            return HTTPFound(location=came_from,
                             headers=headers)
        message = 'Incorrect Username or Password.'
    return dict(
        message=message,
        url=request.application_url + '/login',
        came_from=came_from,
        login=login,
        password=password,
    )


@view_config(context='learning_journal.security.MyRoot', name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)
