# URL Shortener API

A FastAPI service for creating short links, redirecting visitors to the original URL, and tracking visits.

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set `DATABASE_URL` to a PostgreSQL connection string.
4. Start the API: `uvicorn app.main:app --reload`

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/url/` | Create a short link |
| GET | `/url/` | List links |
| GET | `/url/{url_id}` | Get one link |
| PUT | `/url/{url_id}` | Change its destination |
| DELETE | `/url/{url_id}` | Delete a link |
| GET | `/{short_code}` | Redirect and increment `clicks` |

Create a link with:

```json
{"original_url": "https://example.com/a/very/long/link"}
```

The create response includes the generated `short_code`. Visit `http://127.0.0.1:8000/{short_code}` to use the link.
