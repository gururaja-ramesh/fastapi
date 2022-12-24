from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text

'''
This model is used for defining the columns in our table in our database.
This is used to query, create, delete and update entries within our database
'''
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
