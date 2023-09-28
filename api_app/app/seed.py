from sqlalchemy.orm import sessionmaker
from slugify import slugify

from model import BlogPost, engine

SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()


def seed_db():
    # Don't seed the database if there are existing value in the BlogPost database table.
    if db.query(BlogPost).first():
        print("Database already has records. Seeding skipped.")
        return

    for index, post in enumerate(['First', 'Second', 'Third', 'Forth']):
        text = f"My {post} Blog Post"
        post = BlogPost(title=text, slug=slugify(text), body=f"{text} blog content")
        db.add(post)
    db.commit()
    print("Database seeded successfully.")


if __name__ == '__main__':
    seed_db()
    db.close()
