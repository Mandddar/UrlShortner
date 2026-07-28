from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import Base, engine
from app.dependencies.database import get_db
from app.models.url import Url  # Ensure the model is registered before create_all.
from app.routers.url import router as url_router
from app.services.url_services import get_original_url


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="Create, manage, and resolve short links.",
    version="1.0.0",
)
app.include_router(url_router)


@app.get("/", tags=["Health"])
def root():
    return {"message": "URL Shortener API is running"}


@app.get("/{short_code}", include_in_schema=False)
def redirect_to_original_url(short_code: str, db: Session = Depends(get_db)):
    original_url = get_original_url(db, short_code)
    return RedirectResponse(url=original_url, status_code=307)
