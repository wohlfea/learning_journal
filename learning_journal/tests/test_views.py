# -*- coding: utf-8 -*-
from pyramid.testing import DummyRequest
import os


def test_list_view_unit(loaded_db_item):
    """Test if the list_view returns the expected dict."""
    from learning_journal.views import list_view
    response = list_view(DummyRequest())
    assert response['articles'][0].title == "jill"


def test_detail_view_unit(loaded_db_item):
    """Test if the detail_view returns the expected dict."""
    from learning_journal.views import detail_view
    article_id = str(loaded_db_item.id)
    req = DummyRequest()
    req.matchdict = {'article_id': article_id}
    response = detail_view(req)
    assert response['article'].title == 'jill'
    assert response['article'].text == 'jello'


def test_detail_view_functional_0(loaded_db_item, app):
    """Test if the detail_view returns the response upon valid request."""
    response = app.get('/article/{}'.format(loaded_db_item.id))
    assert response.status_code == 200
    assert loaded_db_item.title in response


def test_edit_entry_view_functional(loaded_db_item, authorized_app):
    """Test if the db updates upon request."""
    from learning_journal.models import Entry, DBSession
    authorized_app.post('/edit_entry/{}'.format(loaded_db_item.id),
                        {'title': 'new title', 'text': 'new text'})
    new = DBSession.query(Entry).filter(Entry.id == loaded_db_item.id).first()
    assert new.title == 'new title'
    assert new.text == 'new text'


def test_edit_entry_view_unit(loaded_db_item, dummy_post):
    """Assert redirect upon valid POST Request"""
    from learning_journal.views import edit_entry_view
    article_id = str(loaded_db_item.id)
    dummy_post.matchdict = {'article_id': article_id}
    response = edit_entry_view(dummy_post)
    assert response.status_code == 302


def test_add_entry_view_functional(authorized_app):
    """Test if the db updates upon request."""
    from learning_journal.models import Entry, DBSession
    authorized_app.post('/add_entry', {'title': 'fancy title',
                                       'text': 'new text'})
    new_entry = DBSession.query(Entry).filter(
                Entry.title == 'fancy title').first()
    assert new_entry.id
    assert new_entry.title == 'fancy title'
    assert new_entry.text == 'new text'


def test_add_entry_view_unit_POST_new(dummy_post):
    """Assert redirect upon valid POST Request"""
    from learning_journal.views import add_entry_view
    response = add_entry_view(dummy_post)
    assert response.status_code == 302


def test_add_entry_view_unit_POST_existing(dummy_post):
    """Assert error message exists upon requesting something already in db."""
    from learning_journal.views import add_entry_view
    add_entry_view(dummy_post)
    response = add_entry_view(dummy_post)
    assert response['error_msg']


def test_add_entry_view_unit_GET(dummy_post):
    """Assert empty object is returned upon GET request"""
    from learning_journal.views import add_entry_view
    dummy_post.method = 'GET'
    response = add_entry_view(dummy_post)
    assert response == {}


def test_no_access_to_add_view(app):
    response = app.get('/add_entry')
    assert 'Log Me In!' in response.text


def test_pass_exists():
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_username_exists():
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_hashed_password_check_bad(auth_env):
    from learning_journal.security import check_pw
    assert not check_pw('bad password')


def test_hashed_password_valid(auth_env):
    from learning_journal.security import check_pw
    assert check_pw('secret')


def test_post_login_success_auth_tkt_present(auth_env, app):
    data = {'login': 'admin', 'password': 'secret'}
    response = app.post('/login', data)
    headers = response.headers
    cookies_set = headers.getall('Set-Cookie')
    assert cookies_set
    for cookie in cookies_set:
        if cookie.startswith('auth_tkt'):
            break
    else:
        assert False


def test_assert_login_post_redirect_functional(auth_env, app):
    data = {'login': 'admin', 'password': 'secret'}
    app.get('/add_entry')
    response = app.post('/add_entry', data)
    assert response.status_code == 302


def test_assert_login_post_redirect_from_login_functional(auth_env, app):
    data = {'login': 'admin', 'password': 'secret'}
    response = app.post('/login', data)
    assert response.status_code == 302
    assert '/login' not in response.location


def test_login_displayed_when_logged_out(app):
    response = app.get('/')
    assert 'href="/login"' in response.text
    assert 'href="/logout"' not in response.text


def test_logout_displayed_when_logged_in(authorized_app):
    response = authorized_app.get('/')
    assert 'href="/logout"' in response.text
    assert 'href="/login"' not in response.text


def test_logout_functional(authorized_app):
    response = authorized_app.get('/logout')
    headers = response.headers.getall('Set-Cookie')
    assert 'auth_tkt=;' in headers[0]


def test_logged_out_article_view_no_buttons(app):
    response = app.get('/article/1')
    assert 'href="/edit_entry/1"' not in response.text
    assert 'href="/delete_entry/1"' not in response.text


def test_logged_in_article_view_show_buttons(authorized_app):
    response = authorized_app.get('/article/1')
    assert 'href="/edit_entry/1"' in response.text
    assert 'href="/delete_entry/1"' in response.text


def test_delete_entry(loaded_db_item, authorized_app):
    from learning_journal.models import Entry, DBSession
    check_db = DBSession.query(Entry).filter(
                Entry.title == 'jill').first()
    assert check_db
    authorized_app.get('/delete_entry/{}'.format(loaded_db_item.id))
    check_db = DBSession.query(Entry).filter(
                Entry.title == 'jill').first()
    assert not check_db
