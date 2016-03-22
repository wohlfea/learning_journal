USERS = {'author': 'author',
         'viewer': 'viewer'}
GROUPS = {'author': ['group:authors']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
