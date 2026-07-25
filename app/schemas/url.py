from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    clicks: int

    model_config = {
        "from_attributes": True
    }