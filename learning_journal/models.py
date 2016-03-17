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
    # Try varchar here if it doens't work
    title = Column(Unicode(128), unique=True, nullable=False)
    text = Column(UnicodeText)
    # The default value can either take a scaler value OR
    # It can take a callable, such as datetime.datetime.now()
    # We want datetime.datetime.utcnow()
    # When we test this, make sure we get errors for things like entering
    # Too many characters in title should raise an error from sqlalchemy.exc
    created = Column(DateTime, default=datetime.datetime.utcnow())
