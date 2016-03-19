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


def test_edit_entry_view_get(loaded_db_item):
    """Test if the edit entry view returns the expected dict on get request."""
    from learning_journal.views import edit_entry_view
    req = DummyRequest()
    req.matchdict = {'article_id': str(loaded_db_item.id)}
    response = edit_entry_view(req)
    assert response['article'].title == 'jill'


# def test_edit_entry_view(loaded_db_item):
#     """Test if the expected dict is returned on Post request."""
#     from learning_journal.views import edit_entry_view
#     req = DummyRequest()
#     req.matchdict = {'article_id': str(loaded_db_item.id)}
#     req.POST['title'] = 'New Title'
#     req.POST['text'] = 'New text for a new entry'
#     response = edit_entry_view(req)
#     assert response['article'].title == 'New Title'
