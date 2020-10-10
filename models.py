from sqlalchemy import Column, Integer, String
from database import Base

class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    role = Column(Integer, unique=False)
    token = Column(String(200), unique=True)
    expired = Column(Integer, unique=False)
    name = Column(String(20), unique=False)
    avatar = Column(String(20), unique=False)
    account = Column(String(20), unique=True)
    password = Column(String(200), unique=False)

    def __init__(self, account=None, password=None):
        self.role = role
        self.token = token
        self.expired = expired
        self.name = name
        self.avatar = avatar
        self.account = account
        self.password = password

    # def __repr__(self):
    #     return '<User %r>' % (self.name)