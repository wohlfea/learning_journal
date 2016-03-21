# -*- coding: utf-8 -*-
from pyramid.testing import DummyRequest


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


def test_edit_entry_view_functional(loaded_db_item, app):
    """Test if the db updates upon request."""
    from learning_journal.models import Entry, DBSession
    app.post('/edit_entry/{}'.format(loaded_db_item.id),
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


def test_add_entry_view_functional(app):
    """Test if the db updates upon request."""
    from learning_journal.models import Entry, DBSession
    app.post('/add_entry', {'title': 'fancy title', 'text': 'new text'})
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
