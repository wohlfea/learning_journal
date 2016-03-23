import pytest
import webtest

from learning_journal import main


@pytest.fixture()
def app():
    settings = {'sqlalchemy.url': 'postgres://jrockscarr:password@localhost:5432/lj_test'}
    app = main({}, **settings)
    return webtest.TestApp(app)


def test_no_access_to_view(app):
    response = app.get('/secure', status=403)
    assert response.status_code == 403


def test_access_to_view(app):
    response = app.get('/login', status=200)
    assert response.status_code == 200
