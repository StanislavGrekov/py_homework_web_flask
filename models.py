from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text
from sqlalchemy_utils import EmailType


engin = create_engine('postgresql://postgres:masterkey@127.0.0.1:5431/my_db')

Session = sessionmaker(bind=engin)

Base = declarative_base(bind=engin)

class Users(Base):

    __tablename__='users'

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, nullable=False, unique=True, index=True)
    registration_date = Column(DateTime, server_default=func.now())
    password = Column(String(60), nullable=False)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))


class Advertisement(Base):

    __tablename__ = 'advertisement'

    id = Column(Integer, primary_key=True)
    id_user=Column(Integer, ForeignKey('users.id'), nullable=False)
    users = relationship(Users, backref='advertisement')
    title = Column(String(length=50))
    description=Column(Text())
    created_fild=Column(DateTime, server_default=func.now())


Base.metadata.create_all()