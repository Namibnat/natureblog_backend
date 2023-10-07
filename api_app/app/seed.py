import json

from sqlalchemy.orm import sessionmaker
from slugify import slugify

from model import BlogPost, engine

SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()


def seed_db():
    if db.query(BlogPost).first():
        print("Database already has records. Seeding skipped.")
        return

    with open('seed_data.json', 'r') as fs:
        posts = json.load(fs)

    for post in posts:
        post = BlogPost(title=post['title'], slug=slugify(post['title']), body=post['body'])
        db.add(post)
    db.commit()
    print("Database seeded successfully.")


if __name__ == '__main__':
    seed_db()
    db.close()
