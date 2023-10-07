"""Backend API for nature block website"""

from typing import Optional
from decouple import config
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slugify import slugify
from sqlalchemy.orm import sessionmaker

from model import init_db, BlogPost, engine

app = FastAPI(
    title="Nature Blog API",
    description="An API for the blog",
    version="0.0.1",
    contact={
        "name": config('NAME'),
        "email": config('EMAIL')
    },
    license_info={
        "name": "MIT"
    }
)

# Add CORS middleware settings
origins = config('URL').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SessionLocal = sessionmaker(bind=engine)


def generate_unique_slug(title: str, session) -> str:
    base_slug = slugify(title)
    slug = base_slug
    counter = 1

    while session.query(BlogPost).filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get('/')
async def home():
    return {'title': 'Nature Blog', 'content': 'This is the blog of Vernon'}


@app.get('/api/contacts/')
async def contact_info():
    contact_details = [
        {'name': 'LinkedIn', 'url': config('LINKEDIN_URL')},
        {'name': 'Twitter', 'url': config('TWITTER_URL')},
        {'name': 'Github', 'url': config('GITHUB_URL')}
    ]
    for key, url_detail in enumerate(contact_details):
        url_detail['key'] = key
    return contact_details


@app.get("/api/posts/")
async def list_posts():
    db_session = SessionLocal()
    posts = db_session.query(BlogPost).all()
    db_session.close()
    return posts


@app.post("/api/post/")
async def create_post(title: str, body: str):
    db_session = SessionLocal()
    if db_session.query(BlogPost).filter_by(title=title).first():
        return {"error": "A post with this title already exists."}

    slug = generate_unique_slug(title, db_session)

    blog_post = BlogPost(title=title.title(), slug=slug, body=body)

    db_session.add(blog_post)
    db_session.commit()
    db_session.refresh(blog_post)
    db_session.close()

    return {
        "id": blog_post.id,
        "title": blog_post.title,
        "slug": blog_post.slug,
        "body": blog_post.body,
        "date_created": blog_post.date_created,
        "date_updated": blog_post.date_updated
    }


@app.delete("/api/post/{post_id}/")
async def delete_post(post_id: int):
    db_session = SessionLocal()
    blog_post = db_session.query(BlogPost).filter(BlogPost.id == post_id).first()

    if not blog_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_session.delete(blog_post)
    db_session.commit()
    db_session.close()

    return {'message': f"Post with id {post_id} has been deleted"}


@app.put("/api/post/{post_id}/")
async def update_post(post_id: int, title: Optional[str] = None, body: Optional[str] = None):
    db_session = SessionLocal()
    blog_post = db_session.query(BlogPost).filter(BlogPost.id == post_id).first()

    if not blog_post:
        raise HTTPException(status_code=404, detail="Post not found")

    if title:
        blog_post.title = title
        blog_post.slug = generate_unique_slug(title, db_session)
    if body:
        blog_post.body = body

    db_session.commit()
    db_session.refresh(blog_post)
    db_session.close()

    return {
        "id": blog_post.id,
        "title": blog_post.title,
        "slug": blog_post.slug,
        "body": blog_post.body,
        "date_created": blog_post.date_created,
        "date_updated": blog_post.date_updated
    }


@app.get("/api/post/{post_id}/")
async def read_post(post_id: int):
    with SessionLocal() as session:
        post = session.query(BlogPost).get(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return {"id": post.id, "title": post.title, "body": post.body}
