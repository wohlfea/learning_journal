# -*- coding: utf-8 -*-
import pytest
from sqlalchemy import create_engine
from learning_journal.models import DBSession, Base


TEST_DATABASE_URL = 'postgres://wohlfea:password@localhost:5432/lj_test'


@pytest.fixture(scope='session')
def sqlengine(request):
    engine = create_engine(TEST_DATABASE_URL)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture()
def dbtransaction(request, sqlengine):
    connection = sqlengine.connect()
    transaction = connection.begin()
    DBSession.configure(bind=connection)

    def teardown():
        transaction.rollback()
        connection.close()
        DBSession.remove()

    request.addfinalizer(teardown)
    return connection


@pytest.fixture()
def loaded_db_item(dbtransaction):
    """Instantiate a temporary database. Return one entry."""
    from learning_journal.models import Entry, DBSession
    new_model = Entry(title="jill", text='jello')
    DBSession.add(new_model)
    DBSession.flush()
    return new_model


@pytest.fixture()
def app(dbtransaction):
    from learning_journal import main
    from webtest import TestApp
    fake_settings = {'sqlalchemy.url': TEST_DATABASE_URL}
    app = main({}, **fake_settings)
    return TestApp(app)


@pytest.fixture()
def dummy_post(dbtransaction):
    from pyramid.testing import DummyRequest
    from webob.multidict import MultiDict
    req = DummyRequest()
    req.method = 'POST'
    md = MultiDict()
    md.add('title', 'dummy title')
    md.add('text', 'dummy text')
    req.POST = md
    return req


@pytest.fixture(scope='session')
def auth_env():
    from passlib.apps import custom_app_context as pwd_context
    import os
    os.environ['AUTH_PASSWORD'] = pwd_context.encrypt('secret')
    os.environ['AUTH_USERNAME'] = 'admin'


@pytest.fixture()
def authorized_app(auth_env, app):
    data = {'login': 'admin', 'password': 'secret'}
    app.get('/add_entry')
    app.post('/add_entry', data)
    return app
