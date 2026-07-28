import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.schemas.url import URLCreate
from app.services.url_services import (
    create_url,
    get_original_url,
    get_url_by_id,
)


@pytest.fixture()
def db():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine)()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_create_resolve_and_track_clicks(db):
    url = create_url(db, URLCreate(original_url="https://example.com/docs"))

    assert len(url.short_code) == 6
    assert url.clicks == 0
    assert get_original_url(db, url.short_code) == "https://example.com/docs"
    assert get_url_by_id(db, url.id).clicks == 1


def test_unknown_urls_return_not_found(db):
    with pytest.raises(HTTPException, match="URL not found"):
        get_url_by_id(db, 99999)

    with pytest.raises(HTTPException, match="Short URL not found"):
        get_original_url(db, "does-not-exist")
