from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from decouple import config

DATABASE_URL = config('DATABASE_URL')


engine = create_engine(DATABASE_URL)

Base = declarative_base()


class BlogPost(Base):
    __tablename__ = 'blog_posts'
    id = Column(Integer, Sequence('blog_post_id_seq'), primary_key=True)
    slug = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    body = Column(String(500), nullable=False)


def init_db():
    Base.metadata.create_all(bind=engine)
