from sqlalchemy.orm import sessionmaker
from model import BlogPost, engine  # adjust the import to your project structure

# Set up the session
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()


def seed_db():
    # Create two blog posts
    post1 = BlogPost(title='My First Blog Post', body='This is the content of my first blog post.')
    post2 = BlogPost(title='My Second Blog Post', body='This is the content of my second blog post.')

    # Add the posts to the session
    db.add(post1)
    db.add(post2)

    # Commit the session to save the objects to the database
    db.commit()
    print("Database seeded successfully.")


if __name__ == '__main__':
    seed_db()
    db.close()  # Close the session
