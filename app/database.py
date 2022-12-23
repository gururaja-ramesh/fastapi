'''
This is basic connection setup between a DB and Sqlalchemy. Most of the code remain the
same except for the url which changes depending on the type of the database.
This code is from Fastapi documentation.
Link : https://fastapi.tiangolo.com/tutorial/sql-databases/
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:anuguru@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()