import datetime
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    DateTime
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(128), unique=True, nullable=False)
    text = Column(UnicodeText)
    created = Column(DateTime, default=datetime.datetime.utcnow)


# Maybe switch this to just checking the password. Don't need users or groups
class User(object):
    def __init__(self, login, password, groups=None):
        self.login = login
        self.password = password
        self.groups = groups or []

    def check_password(self, passwd):
        return self.password == passwd
