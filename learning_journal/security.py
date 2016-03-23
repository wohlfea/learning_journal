import os
from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
)
from passlib.apps import custom_app_context as pwd_context

def check_pw(pw):
    hashed = os.environ.get('AUTH_PASSWORD')
    return pwd_context.verify(pw, hashed)

class MyRoot(object):
    __name__ = '__acl__' #not sure why this was necessary to pass test.
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'edit')]
    def __init__(self, request):
        self.request = request
