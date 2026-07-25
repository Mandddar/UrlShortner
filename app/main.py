from fastapi import FastAPI
from app.core.database import Base, engine
from app.models.url import Url
from app.routers.url import router as url_router
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Url Shortner API",
    description="A simple URL shortener API built with FastAPI",
    version="1.0.0"
)
app.include_router(url_router)
@app.get("/")
def root():
    return {"message": "Welcome to the URL Shortener API!"}
