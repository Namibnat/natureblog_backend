from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from decouple import config
from datetime import datetime

DATABASE_URL = config('DATABASE_URL')


engine = create_engine(DATABASE_URL)

Base = declarative_base()


class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True)  # This should auto-increment in PostgreSQL
    slug = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    body = Column(String(500), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_updated = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)
