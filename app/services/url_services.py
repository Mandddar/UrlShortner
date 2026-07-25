from sqlalchemy.orm import Session
from app.models.url import Url
from app.schemas.url import URLCreate
import random
import string
from app.schemas.url import URLCreate
from fastapi import HTTPException
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
def get_url_by_id(db: Session, url_id: int):
    return db.query(Url).filter(Url.id == url_id).first()

def update_url(db: Session, url_id: int, url_data: URLCreate):
    url = db.query(Url).filter(Url.id == url_id).first()

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="URL not found"
        )

    url.original_url = str(url_data.original_url)

    db.commit()
    db.refresh(url)

    return url

def delete_url(db: Session, url_id: int):
    url = db.query(Url).filter(Url.id == url_id).first()

    if url is None:
        raise HTTPException(
            status_code=404,
            detail="URL not found"
        )

    db.delete(url)
    db.commit()

    return {
        "message": "URL deleted successfully"
    }