# AGENT.MD - SQL/Database

## Technology
- MariaDB
- SQLAlchemy ORM (Python)
- Alembic for schema migrations

## Structure

sql/
├── connectionString.py      # Connection string (do not expose secrets!)
├── database.py              # Engine/Session management
├── model.py                 # Declarative SQLAlchemy models
├── CRUD/                    # All entity CRUD operations
├── alembic/                 # Migrations and version scripts
│   └── versions/            # One .py per migration

## DB Conventions
- All tables/columns named in snake_case
- IDs are always integer PKs, named `<entity>_id`
- Foreign keys use `<referenced>_id`
- Use Alembic for all schema migrations (no manual ALTER TABLE)
- Keep migration files atomic and descriptive
- All string data that is user-facing should be normalized via `translation_strings` table for i18n

## Migration Workflow
1. Update model in `model.py`
2. Generate Alembic migration (`alembic revision --autogenerate -m "desc message"`)
3. Apply migration (`alembic upgrade head`)
4. PR should mention any DB schema change

## Data Import
- Data fetched from remote JSON APIs is normalized before DB insert
- All importers should handle upserts to avoid duplicates

## PR/Commit Guidelines
- PRs must document schema changes
- All comments/messages in English
