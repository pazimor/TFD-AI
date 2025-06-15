# TFD-AI

TFD-AI is a personal project that explores theory crafting for **The First Descendant** game. It is split into an Angular front-end and a Flask API backend. Docker images are provided for both parts to simplify local and production setups.

## Project structure

```
TFD-AI/
├── TFD-front/     # Angular 19 application
├── api/           # Flask 3.13 REST API
├── docker-compose.yml
└── docker-compose.dev.yml
```

## Prerequisites

- **Node.js 22** and `npm` for the front-end
- **Python 3.13** for the API (installed automatically in Docker images)
- **Docker** and **Docker Compose** for containerized runs
- A running **MariaDB** instance

## Setup

### Front-end

1. Install dependencies:
   ```bash
   cd TFD-front
   npm install
   ```
2. Set the API base URL in `src/env/environment.ts`:
   ```ts
   export const environment = {
     production: false,
     apiBaseUrl: 'http://localhost:4201/api',
   };
   ```
   For production builds update `environment.prod.ts` accordingly.
3. Add your Google OAuth credentials:
   - Copy `src/env/_client_secret.json` to `src/env/client_secret.json`.
   - Fill in the `client_id` and other fields provided by Google.
4. Start the dev server:
   ```bash
   npm start
   ```
   The application will be available at `http://localhost:4200`.

### Back-end

1. Create a virtual environment and install requirements (optional when not using Docker):
   ```bash
   cd api
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure the database connection string in `sql/connectionString.py` or export a `DATABASE_URL` environment variable with the same value.
3. Run the API for development:
   ```bash
   flask --app api run --debug -h 0.0.0.0 -p 4201
   ```
   In production the Docker image uses Gunicorn automatically.

## Environment variables

- `API_URL` – injected into the Angular app through the environment files.
- `DATABASE_URL` – connection string for MariaDB (e.g. `mysql+pymysql://user:pass@host:3306/dbname`). If not set, the value from `sql/connectionString.py` is used.
- `GOOGLE_OAUTH_CLIENT_SECRET` – path to the OAuth secret JSON used by the front-end. By default `src/env/client_secret.json`.

## Development workflow

1. Run both services locally with Docker Compose:
   ```bash
   docker-compose -f docker-compose.dev.yml up --build
   ```
   This mounts source code for hot reloading.
2. For production builds run:
   ```bash
   docker-compose up --build -d
   ```
   The front-end is served via NGINX on port **4202** and the API on port **4201**.
3. Database migrations are managed with Alembic. Typical workflow:
   ```bash
   alembic revision --autogenerate -m "describe change"
   alembic upgrade head
   ```

## License

This project is provided as-is for personal experimentation.
