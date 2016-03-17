from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Entry,
    )


# @view_config(route_name='home', renderer='templates/mytemplate.pt')
# def my_view(request):
#     try:
#         one = DBSession.query(Entry).filter(Entry.name == 'one').first()
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)
#     return {'one': one, 'project': 'learning_journal'}


@view_config(route_name='home', renderer='templates/list.jinja2')
def list(request):
    try:
        articles = DBSession.query(Entry).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'articles': articles}
    # import pdb; pdb.set_trace()
    # return 'Cheesecake is yummy!'


@view_config(route_name='article', renderer='templates/detail.jinja2')
def detail(request):
    try:
        # We can change this commented out code to what has been changed:
        # article_id = '{article_id}'.format(**request.matchdict)
        # It'd be a good idea to import PDB and set a breakpoint here to play around.
        article_id = request.matchdict['article_id']
        #Instead of this code we could do:
        # article = DBSession.query(Entry).filter(Entry.id == article_id).first()
        article = DBSession.query(Entry).get(article_id)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'article': article}

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
