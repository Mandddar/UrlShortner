from sqlalchemy.orm import Session
from app.models.url import Url
from app.schemas.url import URLCreate
import random
import string
def generate_short_code(length=6):
    return "".join(
        random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )
def create_url(db: Session, url_create: URLCreate):
    db_url = Url(
        original_url=str(url_create.original_url),
        short_code=generate_short_code()
    )

    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url
def get_all_urls(db: Session):
    return db.query(Url).all()