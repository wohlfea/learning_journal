# -*- coding: utf-8 -*-
from pyramid.testing import DummyRequest


def test_list_view(loaded_db):
    """Test if the list_view returns the expected dict."""
    from learning_journal.views import list_view
    response = list_view(DummyRequest())
    assert response['articles'][0].title == "jill"


def test_detail_view(loaded_db):
    """Test if the detail_view returns the expected dict."""
    from learning_journal.views import detail_view
    article_id = str(loaded_db.id)
    req = DummyRequest()
    req.matchdict = {'article_id': article_id}
    response = detail_view(req)
    assert response['article'].title == "jill"
