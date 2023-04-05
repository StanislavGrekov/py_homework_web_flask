from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, func

engin = create_engine('postgresql://postgres:masterkey@127.0.0.1:5431/my_db')

Sessin = sessionmaker(bind=engin)

Base = declarative_base(bind=engin)

class Advertisement(Base):