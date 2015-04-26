import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKeyConstraint
from tombhub.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    passwd = Column(String(50))

    def __init__(self, name=None, passwd = None):
        self.name = name
        self.passwd = passwd

    def __repr__(self):
        return '<User %r>' % (self.name)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Thread(Base):
    __tablename__ = 'threads'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, nullable=False)
    author_name = Column(String(50), nullable=False)
    title = Column(String(50))
    content = Column(Text)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    ForeignKeyConstraint(['author_id','author_name'],['users.id','users.name'])

    def __init__(self, title=None, author_id=None, content = None):
        self.title = title
        self.author_id = author_id
        self.author_name = User.query.get(self.author_id).name
        self.content = content

    def __repr__(self):
        return '<Thread %r>' % (self.title)