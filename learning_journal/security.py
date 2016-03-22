USERS = {'author': 'author'}
GROUPS = {'author': ['group:authors']}

def groupfinder(userid, request):
    if userid in USERS:
        return GROUPS.get(userid, [])
