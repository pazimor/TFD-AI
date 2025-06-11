# AGENT.MD - Global Project Context

## Project Name
TFD-AI (Theory Crafter / Descendants Theory Builder)

## Stack
- **Frontend:** Angular 19 (signals, strict types, Material UI)
- **Backend API:** Python 3.13, Flask, Gunicorn, Flask-CORS
- **DB:** MariaDB (with Alembic for migrations)
- **Container:** Docker (NGINX for web, python:slim for API)

## Dev Conventions
- All PR titles/comments/branch name/commits **must be in English**
- Use signals for state management (Angular front)
- Prioritize separation of concerns
- Each layer (front/API/DB) must be maintainable independently

## Commit conventions
| short |          full          |
|:-----:|:----------------------:|
|  SP   |    stored procedure    |
|  DB   |        dataBase        |
|  DK   |     dockerization      |
|  RE   |        refactor        |
|  SD   |       scheduling       |
|  AI   | artificial Inteligence |
|  PI   |       API reste        |
|  FT   |        features        |
|  NA   |          NAS           |
|  CP   |  front-end Component   |
|  FX   |          Fix           |

commits should be prototyped as follow: `short: {message related}`

## Build/Run
- Front: `ng build --configuration production`
- API: `gunicorn --bind 0.0.0.0:4201 api:app`
- Docker Compose handles multi-container orchestration

## Environment
- API_URL injected in Angular via environment file
- NGINX serves Angular static, proxies `/api` to backend

## Coding Best Practices
- Favor explicit types and interfaces (TypeScript, Python)
- Use modern Angular patterns (signals over observables)
- API routes RESTful, return JSON
- SQL via SQLAlchemy ORM (strict models), migrations with Alembic

## File/Folder Structure
See the sub-AGENT.MD files for detailed breakdowns for each layer. and keep in mind the previous ones