# -*- coding: utf-8 -*-
from learning_journal.models import Entry, DBSession
from pyramid.testing import DummyRequest


def test_list_view(loaded_db):
    """Test if the list_view returns the expected dict."""
    from learning_journal.views import list_view
    response = list_view(DummyRequest())
    assert response['articles'][0].title == "jill"
