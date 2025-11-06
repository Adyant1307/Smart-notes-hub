from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    tags = Column(String)  # Comma-separated
    upvotes = Column(Integer, default=0)
    file_url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)