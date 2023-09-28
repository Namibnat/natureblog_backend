
import datetime
from sqlalchemy.orm import sessionmaker
from model import BlogPost, engine  # adjust the import to your project structure

# Set up the session
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()


def seed_db():
    for index, post in enumerate(['First', 'Second', 'Third', 'Forth']):
        text = f"My {post} Blog Post"
        post = BlogPost(id=index, title=text, slug=text.lower().replace(' ', '_'),
                        body=f"{text} blog content", date_created=datetime.datetime.now(),
                        date_updated=datetime.datetime.now())
        db.add(post)

    # Commit the session to save the objects to the database
    db.commit()
    print("Database seeded successfully.")


if __name__ == '__main__':
    seed_db()
    db.close()  # Close the session
