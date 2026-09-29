from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey
from sqlalchemy.sql.expression import text
from datetime import datetime
from .database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String(500), nullable=False)
    published = Column(Boolean, server_default='true')
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"
    email = Column(String,nullable=False, unique=True)
    password = Column(String,nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))


