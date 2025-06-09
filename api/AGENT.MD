# AGENT.MD - Backend API

## Technology
- Python 3.13
- Flask (REST API)
- Gunicorn (WSGI)
- Flask-CORS
- SQLAlchemy ORM
- Alembic for DB migrations
- Requests for HTTP data fetching

## API Design
- All endpoints under `/api/*`
- Returns JSON only, never HTML
- CORS enabled for Angular front (`http://localhost:4200`)
- Auth: Google OAuth (via frontend, not handled by backend)

## File Structure
```
api/
├── api.py                 # main Flask app, all routes
├── fillroutes/            # Data importers for various domains
├── sql/                   # Database models and CRUD
├── parsing.py             # Helpers for parsing text/effects
├── request_service.py     # External API fetches
├── requirements.txt       # All dependencies
└── Dockerfile             # Multistage build (builder/runtime)
```

## Coding Standards
- One route per data type (`/api/modules`, `/api/weapons`, etc.)
- Use threading for long-running imports (async data fill)
- Prefer explicit exception handling
- All migrations via Alembic (versions tracked in `sql/alembic/versions/`)
- ORM models are strictly typed (see `sql/model.py`)

## Development
- Use `gunicorn` for prod, `flask run` for debug only
- Dedicated user (`appuser`) for Docker container, never run as root

## PR/Commit Guidelines
- All commit/PR messages in English
- PRs must document API changes and routes