from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_services import (
    create_url,
    get_all_urls,
    get_url_by_id,
    update_url,
    delete_url,
)

router = APIRouter(
    prefix="/url",
    tags=["URL"]
)

# CREATE
@router.post("/", response_model=URLResponse)
def create_short_url(
    url: URLCreate,
    db: Session = Depends(get_db)
):
    return create_url(db, url)


# READ ALL
@router.get("/", response_model=list[URLResponse])
def read_urls(
    db: Session = Depends(get_db)
):
    return get_all_urls(db)


# READ ONE
@router.get("/{url_id}", response_model=URLResponse)
def read_url(
    url_id: int,
    db: Session = Depends(get_db)
):
    return get_url_by_id(db, url_id)


# UPDATE
@router.put("/{url_id}", response_model=URLResponse)
def edit_url(
    url_id: int,
    url: URLCreate,
    db: Session = Depends(get_db)
):
    return update_url(db, url_id, url)


# DELETE
@router.delete("/{url_id}")
def remove_url(
    url_id: int,
    db: Session = Depends(get_db)
):
    return delete_url(db, url_id)