# -*- coding: utf-8 -*-
import os
import pytest
from sqlalchemy import create_engine

from learning_journal.models import DBSession, Base
from passlib.apps import custom_app_context as pl
import webtest

from learning_journal import main


TEST_DATABASE_URL = 'postgres://jrockscarr:password@localhost:5432/lj_test'
DATA_SUCCESS = {'username': 'jaredscarr', 'password': 'pirateninja'}


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


@pytest.fixture()
def app():
    settings = {'sqlalchemy.url': 'postgres://jrockscarr:password@localhost:5432/lj_test'}
    app = main({}, **settings)
    return webtest.TestApp(app)


@pytest.fixture()
def auth_env():
    os.environ['AUTH_PASSWORD'] = pl.encrypt('secret')
    os.environ['AUTH_USERNAME'] = 'admin'


@pytest.fixture()
def authenticated_app(app, auth_env):
    app.post('/login', DATA_SUCCESS)
    return app
