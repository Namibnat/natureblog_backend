from datetime import datetime

from decouple import config
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

engine = create_engine(config('DATABASE_URL'))
Base = declarative_base()


class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True)
    slug = Column(String(100), nullable=False, unique=True)
    title = Column(String(100), nullable=False, unique=True)
    body = Column(String(500), nullable=False)
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)
    date_updated = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Blog post: {self.title} created {self.date_created: %d/%m%/Y}"


def init_db():
    Base.metadata.create_all(bind=engine)
