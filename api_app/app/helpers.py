from slugify import slugify


def generate_unique_slug(title: str, session, model) -> str:
    base_slug = slugify(title)
    slug = base_slug
    counter = 1

    while session.query(model).filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug
