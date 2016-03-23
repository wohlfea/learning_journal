import os
from pyramid.security import (
    Allow,
    Everyone,
    Authenticated,
)

def check_pw(pw):
    return pw == os.environ.get('AUTH_PASSWORD')

class MyRoot(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, Authenticated, 'edit')]
    def __init__(self, request):
        self.request = request
