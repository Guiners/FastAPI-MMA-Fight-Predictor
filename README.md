#  FastAPI MMA Fight Predictor

## Overview
A modular **FastAPI-based REST API and HTML interface** for managing MMA fighter data and fight results.  
This project serves as a foundation for data collection, visualization, and future fight outcome prediction.

---

##  Features
- **FastAPI REST API** with modular routers:
  - `auth_router.py` — authentication and token management  
  - `base_fighter_router.py` — core fighter data  
  - `extended_fighter_router.py` — extended fighter stats  
  - `database_manager_router.py` — database admin operations  
- **Jinja2 templating** with custom filters (`short_date`, `clean_str`)
- **Database layer** with SQLAlchemy models and Alembic migrations
- **Seed scripts** for loading sample fighter data
- **Dockerized environment** with PostgreSQL and optional Redis
- **Separation of concerns**: routers, services, schemas, and middleware

---

##  Project Structure
```
app/
 ├── main.py                 # Application entry point
 ├── templates.py            # Jinja2 config and custom filters
 ├── routers/                # API route definitions
 ├── services/               # Business logic layer
 ├── schemas/                # Pydantic schemas for validation
 └── middleware/             # Common middleware and exception handling

db/
 ├── models/                 # SQLAlchemy models
 ├── scripts/seed.py         # Test data seeding
 └── example_data/           # JSON fixtures

alembic/                     # Database migrations
templates/                   # Jinja2 HTML templates
static/css/                  # Stylesheets
Dockerfile
docker-compose.yaml
```

---

##  Requirements
- Python 3.11+
- PostgreSQL
- (Optional) Redis
- `pipenv` or `venv` + `pip`
- `alembic` for migrations
- `docker` and `docker-compose` (optional)

---

##  Quick Start (Local)
```bash
# 1. Clone the repository
git clone https://github.com/Guiners/FastAPI-MMA-Fight-Predictor.git
cd FastAPI-MMA-Fight-Predictor

# 2. Install dependencies
pipenv install
# or
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Run migrations
alembic upgrade head

# 4. (Optional) Seed the database
python db/scripts/seed.py

# 5. Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

##  Run with Docker
```bash
docker-compose up --build
```
Services:
- FastAPI application  
- PostgreSQL (initialized from `postgres/init.sql`)  
- Redis (optional)  

---

##  Database & Migrations
Typical commands:
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

##  API & Documentation
- API routers in `app/routers/`
- OpenAPI docs:
  - Swagger UI → `/docs`
  - ReDoc → `/redoc`
- Example:
  ```http
  GET /fighters  # List of fighters (base or extended)
  ```

Authentication and token logic are defined in:
- `app/services/auth.py`
- `app/routers/auth_router.py`

---

##  Templates & Frontend
- Templates rendered via **Jinja2** (`app/templates.py`)
- Static assets: `static/css/`
- Example templates: `fighter.html`, `fighter_list.html`, `stats.html`

---

##  Data Seeding
Example data:
```
db/example_data/
 ├── fighters.json
 ├── base_stats.json
 ├── extended_stats.json
 └── fights_results.json
```
Seed script:
```bash
python db/scripts/seed.py
```

---

##  Authentication & Security
- JWT-based authentication (`auth.py`, `auth_router.py`)
- Secrets and DB credentials provided via environment variables
- Recommended: enable HTTPS, CORS, rate limiting for production

---

##  Development Notes
- Add tests (`pytest`) for routers, services, and migrations
- Extend API with pagination, filtering, and sorting
- Document endpoints with OpenAPI examples
- Consider adding ML-based prediction modules under `app/services/analysis/`
- Use CI/CD pipelines for linting, tests, and Docker builds

---

##  Contributing
1. Fork the repo and create a feature branch  
2. Submit a Pull Request with a clear description  
3. Follow code style: `black`, `isort`

---

##  License
This project currently lacks a license file.  
Before public release, add a proper license (e.g., **MIT**).

---

##  Summary
A clean, extensible FastAPI architecture for collecting, managing, and visualizing MMA data.  
Designed with modularity in mind — ideal as a base for analytical or predictive extensions.
