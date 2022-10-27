from sqlite3 import Timestamp
from time import timezone
from tkinter.tix import COLUMN
from xmlrpc.client import Boolean
from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "Post"

    id = Column(Integer,primary_key = True,nullable = False)
    title = Column(String,nullable = False)
    content = Column(String,nullable = False)
    published = Column(Boolean,server_default ='True',nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False,server_default = text('now()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete = "CASCADE"),nullable = False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    email = Column(String,nullable = False,unique = True)
    password = Column(String,nullable = False)
    id = Column(Integer,primary_key = True,nullable = False)
    created_at = Column(TIMESTAMP(timezone = True),nullable = False,server_default = text('now()'))

class Vote(Base):
    __tablename__ = "vote"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key = True)
    post_id = Column(Integer,ForeignKey("Post.id",ondelete="CASCADE"),primary_key = True)