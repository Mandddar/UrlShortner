import secrets
import string

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.url import Url
from app.schemas.url import URLCreate


SHORT_CODE_LENGTH = 6
MAX_CODE_GENERATION_ATTEMPTS = 10
CODE_ALPHABET = string.ascii_letters + string.digits


def generate_short_code(length: int = SHORT_CODE_LENGTH) -> str:
    """Generate a URL-safe, case-sensitive short code."""
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(length))


def _url_or_404(db: Session, url_id: int) -> Url:
    url = db.get(Url, url_id)
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    return url


def create_url(db: Session, url_create: URLCreate) -> Url:
    """Persist a URL, retrying if an extremely unlikely code collision occurs."""
    for _ in range(MAX_CODE_GENERATION_ATTEMPTS):
        url = Url(
            original_url=str(url_create.original_url),
            short_code=generate_short_code(),
        )
        db.add(url)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            continue

        db.refresh(url)
        return url

    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Could not generate a unique short code. Please try again.",
    )


def get_all_urls(db: Session) -> list[Url]:
    return list(db.scalars(select(Url).order_by(Url.created_at.desc())))


def get_url_by_id(db: Session, url_id: int) -> Url:
    return _url_or_404(db, url_id)


def update_url(db: Session, url_id: int, url_data: URLCreate) -> Url:
    url = _url_or_404(db, url_id)
    url.original_url = str(url_data.original_url)
    db.commit()
    db.refresh(url)
    return url


def delete_url(db: Session, url_id: int) -> None:
    url = _url_or_404(db, url_id)
    db.delete(url)
    db.commit()


def get_original_url(db: Session, short_code: str) -> str:
    """Resolve a short code and record the visit before redirecting."""
    url = db.scalar(select(Url).where(Url.short_code == short_code))
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found",
        )

    url.clicks += 1
    db.commit()
    return url.original_url
