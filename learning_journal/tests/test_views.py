# -*- coding: utf-8 -*-
from pyramid.testing import DummyRequest


def test_list_view(loaded_db_item):
    """Test if the list_view returns the expected dict."""
    from learning_journal.views import list_view
    response = list_view(DummyRequest())
    assert response['articles'][0].title == "jill"


def test_detail_view(loaded_db_item):
    """Test if the detail_view returns the expected dict."""
    from learning_journal.views import detail_view
    article_id = str(loaded_db_item.id)
    req = DummyRequest()
    req.matchdict = {'article_id': article_id}
    response = detail_view(req)
    assert response['article'].title == "jill"


def test_detail_view_1(loaded_db_item, app):
    """Test if the detail_view returns the expected dict."""
    response = app.get('/article/{}'.format(loaded_db_item.id))
    assert response.status_code == 200


def test_edit_entry_view(loaded_db_item, app):
    """Test if the response redirects user and db is updated."""
    from collections import OrderedDict
    from learning_journal.models import Entry, DBSession
    response = app.post('/edit_entry/{}'.format(loaded_db_item.id),
                        OrderedDict([('title', 'new title'),
                                    ('text', 'new text')]))
    assert response.status_code == 302
    new = DBSession.query(Entry).filter(Entry.id == loaded_db_item.id).first()
    assert new.title == 'new title'
    assert new.text == 'new text'
