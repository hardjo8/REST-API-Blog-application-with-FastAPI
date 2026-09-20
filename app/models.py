from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.expression import text
from datetime import datetime
from .database import Base


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String(500), nullable=False)
    published = Column(Boolean, server_default='true')
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))