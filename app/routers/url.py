from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_services import (
    create_url,
    delete_url,
    get_all_urls,
    get_url_by_id,
    update_url,
)


router = APIRouter(prefix="/url", tags=["URLs"])


@router.post("/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(url: URLCreate, db: Session = Depends(get_db)):
    return create_url(db, url)


@router.get("/", response_model=list[URLResponse])
def read_urls(db: Session = Depends(get_db)):
    return get_all_urls(db)


@router.get("/{url_id}", response_model=URLResponse)
def read_url(url_id: int, db: Session = Depends(get_db)):
    return get_url_by_id(db, url_id)


@router.put("/{url_id}", response_model=URLResponse)
def edit_url(url_id: int, url: URLCreate, db: Session = Depends(get_db)):
    return update_url(db, url_id, url)


@router.delete("/{url_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_url(url_id: int, db: Session = Depends(get_db)):
    delete_url(db, url_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
