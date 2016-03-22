import datetime
from pyramid.security import (
    Allow,
    Everyone,
)
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
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:authors', 'edit')]
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(128), unique=True, nullable=False)
    text = Column(UnicodeText)
    created = Column(DateTime, default=datetime.datetime.utcnow)
