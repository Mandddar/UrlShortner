from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
 
from app.dependencies.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_services import create_url, get_all_urls as get_all_urls_service
router =APIRouter(
    prefix="/url",
    tags=["url"]
)
@router.post("/", response_model=URLResponse)
def create_short_url(
    url: URLCreate,
    db: Session = Depends(get_db)
):
    return create_url(db, url)

@router.get("/", response_model=list[URLResponse])
def list_urls(db: Session = Depends(get_db)):
    urls = get_all_urls_service(db)

    for u in urls:
        print("ID:", u.id)
        print("URL:", u.original_url)
        print("SHORT:", u.short_code)
        print("----------------")

    return urls