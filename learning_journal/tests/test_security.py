# -*- coding: utf-8 -*-
import os


def test_password_exist(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_username_exist(auth_env):
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_no_access_to_view(app):
    response = app.get('/secure', status=403)
    assert response.status_code == 403


def test_access_to_login(app):
    response = app.get('/login', status=200)
    assert response.status_code == 200


def test_access_to_logout(authenticated_app):
    response = authenticated_app.get('/logout', status=302)
    assert response.status_code == 302


def test_check_password_success(auth_env):
    from learning_journal.security import check_pwd
    password = 'secret'
    assert check_pwd(password)


def stored_password_is_encrypted(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) != 'secret'


def test_check_pwd_fails(auth_env):
    from learning_journal.security import check_pwd
    password = 'not it'
    assert not check_pwd(password)
