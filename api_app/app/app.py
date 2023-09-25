"""Backend API for nature block website

For testing in dev, seed db with:
docker exec -it db bash

psql -U ${POSTGRES_USER} nature_blog

INSERT INTO blog_posts(id, title, body, slog) VALUES(1, 'Blog post 1', 'Body content', 'bp1'), (2, 'Blog post 2', 'Body content post 2', 'bp2');

"""

from fastapi import FastAPI
from model import init_db, BlogPost, engine
from sqlalchemy.orm import sessionmaker

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware settings
origins = [
    "http://localhost:3000",
    # TODO: ADD FOR PROD - THROUGH ENV
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SessionLocal = sessionmaker(bind=engine)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get('/')
def home():
    return {'title': 'Nature Blog', 'content': 'This is the blog of Vernon'}


@app.get("/api/posts")
async def list_posts():
    session = SessionLocal()
    posts = session.query(BlogPost).all()
    session.close()
    return posts


@app.post("/api/post/")
def create_post(title: str, body: str):
    db_session = SessionLocal()
    blog_post = BlogPost(title=title, body=body)
    db_session.add(blog_post)
    db_session.commit()
    db_session.refresh(blog_post)
    db_session.close()
    return {"id": blog_post.id,
            "title": blog_post.title,
            "slug": blog_post.slug,
            "body": blog_post.body}
